from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    resume_text: Mapped[str] = mapped_column(Text, nullable=True)