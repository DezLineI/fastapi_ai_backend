from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///chat.db")

session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = "chat_request"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

def get_user_request(ip_address: str):
    with session() as new_session:
        query = select(Chat).filter_by(ip_address=ip_address)
        result = new_session.execute(query)
        return result.scalars().all()

def add_request(ip_address: str, prompt: str, response: str) -> None:
    with session() as new_session:
        new_request = Chat(
            ip_address=ip_address,
            prompt=prompt,
            response=response,
        )
        new_session.add(new_request)
        new_session.commit()