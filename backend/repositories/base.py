"""Base repository pattern implementation."""
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import Base
from core.exceptions import DatabaseError, NotFoundError
from core.logging import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get entity by ID.
        
        Args:
            id: Entity ID
        
        Returns:
            Entity or None if not found
        
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_id: {str(e)}")
            raise DatabaseError(f"Failed to fetch {self.model.__name__}")
    
    def get_or_404(self, id: int) -> ModelType:
        """
        Get entity by ID or raise 404.
        
        Args:
            id: Entity ID
        
        Returns:
            Entity
        
        Raises:
            NotFoundError: If entity not found
            DatabaseError: If database operation fails
        """
        entity = self.get_by_id(id)
        if not entity:
            raise NotFoundError(self.model.__name__, id)
        return entity
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get all entities with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filters as dict

        Returns:
            List of entities
        
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            query = self.db.query(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all: {str(e)}")
            raise DatabaseError(f"Failed to fetch {self.model.__name__} list")
    
    def create(self, **kwargs) -> ModelType:
        """
        Create new entity.
        
        Args:
            **kwargs: Entity attributes
        
        Returns:
            Created entity
        
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            entity = self.model(**kwargs)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            logger.info(f"Created {self.model.__name__} with id={entity.id}")
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in create: {str(e)}")
            raise DatabaseError(f"Failed to create {self.model.__name__}")
    
    def update(self, id: int, **kwargs) -> ModelType:
        """
        Update entity.
        
        Args:
            id: Entity ID
            **kwargs: Attributes to update
        
        Returns:
            Updated entity
        
        Raises:
            NotFoundError: If entity not found
            DatabaseError: If database operation fails
        """
        try:
            entity = self.get_or_404(id)
            
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            self.db.commit()
            self.db.refresh(entity)
            logger.info(f"Updated {self.model.__name__} with id={id}")
            return entity
        except NotFoundError:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in update: {str(e)}")
            raise DatabaseError(f"Failed to update {self.model.__name__}")
    
    def delete(self, id: int) -> bool:
        """
        Delete entity.
        
        Args:
            id: Entity ID
        
        Returns:
            True if deleted successfully
        
        Raises:
            NotFoundError: If entity not found
            DatabaseError: If database operation fails
        """
        try:
            entity = self.get_or_404(id)
            self.db.delete(entity)
            self.db.commit()
            logger.info(f"Deleted {self.model.__name__} with id={id}")
            return True
        except NotFoundError:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in delete: {str(e)}")
            raise DatabaseError(f"Failed to delete {self.model.__name__}")
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count entities.
        
        Args:
            filters: Optional filters as dict
        
        Returns:
            Count of entities
        
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            query = self.db.query(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            
            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Database error in count: {str(e)}")
            raise DatabaseError(f"Failed to count {self.model.__name__}")
