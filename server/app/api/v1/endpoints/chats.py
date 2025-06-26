from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

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
        # This requires an update to crud.chat to get chats by user (via projects)
        user_projects = crud.project.get_multi_by_owner(db=db, owner_id=current_user.id)
        project_ids = [p.id for p in user_projects]
        if not project_ids:
            return []  # No projects, no chats

        # This assumes crud.chat has a method to get chats for a list of project_ids
        # We'll need to add a `get_multi_by_project_ids` method to crud_chat.py
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
