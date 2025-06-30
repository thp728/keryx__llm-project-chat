import os
import logging
from typing import List, Optional

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)

from app.models import (
    Chat,
    Message,
    Project,
)  # SQLAlchemy models

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class LLMService:
    def __init__(self):
        """
        Initializes the LLMService with a Google Gemini LLM instance.
        The Google API key is loaded from GEMINI_API_KEY environment variable.
        """
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        # Initialize the ChatGoogleGenerativeAI model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=GEMINI_API_KEY,
        )
        logger.info("LLMService initialized with Google Gemini model: gemini-2.5-flash")

    def _build_messages(
        self,
        base_instructions: Optional[str],
        history_messages: List[Message],
        new_user_message_content: str,
    ) -> List[BaseMessage]:
        """
        Constructs a list of LangChain ChatMessage objects from base instructions
        and historical messages, including the new user message.

        Args:
            base_instructions: The base instructions from the Project, forming a SystemMessage.
            history_messages: A list of historical SQLAlchemy Message objects.
            new_user_message_content: The content of the user's current message.

        Returns:
            A list of LangChain BaseMessage objects ready for the LLM.
        """
        messages: List[BaseMessage] = []

        # 1. Add SystemMessage from base_instructions if present
        if base_instructions:
            messages.append(SystemMessage(content=base_instructions))
            logger.debug(f"Added SystemMessage: {base_instructions[:50]}...")

        # 2. Add historical messages from the database
        for msg in history_messages:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
            else:
                logger.warning(
                    f"Unknown message role: {msg.role} for message ID {msg.id}. Skipping."
                )
        logger.debug(f"Added {len(history_messages)} historical messages.")

        # 3. Add the new user message
        messages.append(HumanMessage(content=new_user_message_content))
        logger.debug(f"Added new HumanMessage: {new_user_message_content[:50]}...")

        return messages

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=(
            retry_if_exception_type(Exception)
        ),  # Consider refining to specific LLM API exceptions
    )
    async def get_llm_response(
        self,
        new_user_message_content: str,
        chat: Chat,  # The Chat object with pre-loaded project and messages
    ) -> str:
        """
        Orchestrates the LLM call, preparing messages and handling the response.

        Args:
            new_user_message_content: The current message from the user.
            chat: The Chat object, which includes its associated Project and historical Messages.

        Returns:
            The content of the LLM's response.

        Raises:
            ValueError: If the Chat object or its associated Project is missing base instructions.
            Exception: If the LLM call fails after retries.
        """
        if not chat.project or not chat.project.base_instructions:
            logger.error(
                f"Chat {chat.id} or its associated Project is missing base_instructions."
            )
            raise ValueError("Chat project is missing base instructions.")

        base_instructions = chat.project.base_instructions

        # chat.messages should be pre-loaded via SQLAlchemy's joinedload
        history_messages = chat.messages if chat.messages is not None else []

        langchain_messages = self._build_messages(
            base_instructions=base_instructions,
            history_messages=history_messages,
            new_user_message_content=new_user_message_content,
        )
        logger.info(
            f"Initiating LLM call for chat {chat.id} with {len(langchain_messages)} messages."
        )

        try:
            # Asynchronously invoke the LLM with the prepared messages
            response = await self.llm.ainvoke(langchain_messages)
            llm_response_content = response.content
            logger.info(f"LLM response received for chat {chat.id}.")
            return llm_response_content
        except Exception as e:
            logger.error(
                f"Failed to get LLM response for chat {chat.id}: {e}", exc_info=True
            )
            raise  # Re-raise to be caught by the retry decorator or calling function
