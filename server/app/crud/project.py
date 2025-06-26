from typing import List, TypeVar, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

# Define a TypeVar for the model to help with type hinting in the generic CRUDBase
ModelType = TypeVar("ModelType", bound=Project)


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """
    CRUD operations for Project model.
    Inherits from CRUDBase for generic CRUD functionalities.
    """

    def create_with_owner(
        self, db: Session, *, obj_in: ProjectCreate, owner_id: int
    ) -> Project:
        """
        Creates a new project and associates it with a specific owner.

        Args:
            db: The database session.
            obj_in: Pydantic schema for creating a project.
            owner_id: The ID of the user who owns this project.

        Returns:
            The newly created Project ORM object.
        """
        # Convert the Pydantic model to a dictionary, then add the owner_id
        obj_in_data = obj_in.model_dump()  # Use .model_dump() for Pydantic v2
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Retrieves multiple projects filtered by a specific owner ID.

        Args:
            db: The database session.
            owner_id: The ID of the owner whose projects are to be retrieved.
            skip: The number of records to skip (for pagination).
            limit: The maximum number of records to return (for pagination).

        Returns:
            A list of Project ORM objects.
        """
        return (
            db.query(self.model)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


# Create an instance of CRUDProject for direct use in API endpoints
project = CRUDProject(Project)
