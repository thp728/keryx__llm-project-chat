from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass  # Generic CRUD methods are sufficient for now


project = CRUDProject(Project)
