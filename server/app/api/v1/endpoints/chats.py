from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload  # Import joinedload for eager loading

from app import models, crud, schemas
from app.api import deps
from app.services.llm_service import LLMService  # Import your LLMService

router = APIRouter()


@router.post("/", response_model=schemas.Chat)
def create_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_in: schemas.ChatCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new chat for a specific project.
    """
    # Ensure the project exists and belongs to the current user
    project = crud.project.get(db, id=chat_in.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create a chat in this project.",
        )

    chat = crud.chat.create(db=db, obj_in=chat_in)
    return chat


@router.get("/", response_model=List[schemas.Chat])
def read_chats(
    db: Session = Depends(deps.get_db),
    project_id: int | None = None,  # Optional filter by project_id
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve chats, optionally filtered by project ID.
    Only retrieves chats for projects owned by the current user.
    """
    if project_id is not None:
        project = crud.project.get(db, id=project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access chats in this project.",
            )
        chats = crud.chat.get_multi_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit
        )
    else:
        # If no project_id is provided, retrieve all chats for projects owned by the user
        user_projects = crud.project.get_multi_by_owner(db=db, owner_id=current_user.id)
        project_ids = [p.id for p in user_projects]
        if not project_ids:
            return []  # No projects, no chats

        chats = crud.chat.get_multi_by_project_ids(
            db=db, project_ids=project_ids, skip=skip, limit=limit
        )

    return chats


@router.get("/{chat_id}", response_model=schemas.Chat)
def read_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a chat by ID.
    """
    chat = crud.chat.get(db, id=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    # Check if the chat's project belongs to the current user
    project = crud.project.get(db, id=chat.project_id)
    if not project or (project.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this chat.",
        )
    return chat


@router.put("/{chat_id}", response_model=schemas.Chat)
def update_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: int,
    chat_in: schemas.ChatUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a chat.
    """
    chat = crud.chat.get(db, id=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    # Check if the chat's project belongs to the current user
    project = crud.project.get(db, id=chat.project_id)
    if not project or (project.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this chat.",
        )
    chat = crud.chat.update(db, db_obj=chat, obj_in=chat_in)
    return chat


@router.delete("/{chat_id}", response_model=schemas.Chat)
def delete_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a chat.
    """
    chat = crud.chat.get(db, id=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    # Check if the chat's project belongs to the current user
    project = crud.project.get(db, id=chat.project_id)
    if not project or (project.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this chat.",
        )
    chat = crud.chat.remove(db, id=chat_id)
    return chat


@router.post(
    "/{chat_id}/message", response_model=Dict[str, str], status_code=status.HTTP_200_OK
)
async def post_chat_message(
    chat_id: int,
    user_message_request: schemas.UserMessageRequest,
    db: Session = Depends(deps.get_db),
    llm_service: LLMService = Depends(deps.get_llm_service),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, str]:
    """
    Receives a new user message for a specific chat, processes it with the LLM,
    persists both user and LLM messages, and returns the LLM's response.
    """
    user_message_content = user_message_request.message_content

    # 1. Fetch Chat & Project with messages loaded, ordered by created_at
    chat = (
        db.query(models.Chat)
        .options(
            joinedload(models.Chat.messages).load_only(
                models.Message.content, models.Message.role, models.Message.created_at
            ),
            joinedload(models.Chat.project).load_only(models.Project.base_instructions),
        )
        .filter(models.Chat.id == chat_id)
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with ID {chat_id} not found.",
        )

    # Authorization check:
    if not chat.project or chat.project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chat.",
        )

    # 2. Persist User Message
    user_message = crud.chat.create_message(
        db=db, chat_id=chat.id, role="user", content=user_message_content
    )

    # 3. Invoke LLM Service
    try:
        llm_response_content = await llm_service.get_llm_response(
            new_user_message_content=user_message_content,
            chat=chat,  # The chat object now has pre-sorted messages
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating LLM response: {e}",
        )

    # 4. Persist LLM Response
    llm_message = crud.chat.create_message(
        db=db, chat_id=chat.id, role="assistant", content=llm_response_content
    )

    # 5. Return LLM Response
    return {"response": llm_response_content}
