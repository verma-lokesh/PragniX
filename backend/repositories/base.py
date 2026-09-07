from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    model: Type[ModelT]

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: str) -> Optional[ModelT]:
        return self.db.get(self.model, id)

    def list_all(self, limit: int = 100) -> list[ModelT]:
        return self.db.query(self.model).limit(limit).all()

    def add(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.flush()
        return obj

    def add_all(self, objs: list[ModelT]) -> list[ModelT]:
        self.db.add_all(objs)
        self.db.flush()
        return objs

    def commit(self):
        self.db.commit()
