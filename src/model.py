from sqlmodel import (
    TEXT,
    String,
    SQLModel,
    Field,
    Relationship,
    BIGINT,
    Column,
    TIMESTAMP,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.event import listens_for
from sqlalchemy.engine import Connection
from datetime import datetime, timedelta
from snowflake import SnowflakeGenerator

snowflake_gen = SnowflakeGenerator(1)


def generate_snowflake_id() -> int:
    return next(snowflake_gen)


class Users(SQLModel, table=True):  # type: ignore
    __tablename__ = "users"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    username: str = Field(sa_column=Column(String(256), index=True, unique=True))
    display_name: str = Field(sa_column=Column(String(256)))
    email: str = Field(sa_column=Column(TEXT,index=True,unique=True))
    avatar_url: str = Field(sa_column=Column(TEXT))
    hashed_password: str = Field(sa_column=Column(String(60)))

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    rooms: list["Rooms"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"secondary": "room_members", "viewonly": True},
    )
    refresh_tokens: list["RefreshToken"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Rooms(SQLModel, table=True):  # type: ignore
    __tablename__ = "rooms"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    name: str = Field(sa_column=Column(String(256)))
    avatar_url: str = Field(sa_column=Column(TEXT))

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    members: list["RoomMembers"] = Relationship(
        back_populates="room", sa_relationship_kwargs={"viewonly": True}
    )  # for custom misc

    users: list["Users"] = Relationship(
        back_populates="rooms",
        sa_relationship_kwargs={"secondary": "room_members", "viewonly": True},
    )  # for user profile


class RoomMembers(SQLModel, table=True):  # type: ignore
    __tablename__ = "room_members"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    room_id: int = Field(foreign_key="rooms.id", index=True, sa_type=BIGINT)
    user_id: int = Field(foreign_key="users.id", index=True, sa_type=BIGINT)
    room_name: str | None = Field(
        default=None, sa_column=Column(String(256))
    )  # user customize room name (show only user)
    room_avatar_url: str | None = Field(
        default=None, sa_column=Column(TEXT)
    )  # user customize room avater (show only user)
    user_name: str | None = Field(
        default=None, sa_column=Column(String(256))
    )  # custom user name in room (show all room user)
    user_avatar_url: str | None = Field(
        default=None, sa_column=Column(TEXT)
    )  # custom user avater in room (show all room user)

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    room: Rooms = Relationship(
        back_populates="members", sa_relationship_kwargs={"viewonly": True}
    )
    user: Users = Relationship(sa_relationship_kwargs={"viewonly": True})

    __table_args__ = (UniqueConstraint("room_id", "user_id", name="uix_room_member"),)


class Messages(SQLModel, table=True):  # type: ignore
    __tablename__ = "messages"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    room_member_id: int = Field(
        foreign_key="room_members.id", index=True, sa_type=BIGINT
    )
    room_id: int = Field(foreign_key="rooms.id", index=True, sa_type=BIGINT)
    message: str = Field(sa_column=Column(TEXT))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )
    room_member: RoomMembers = Relationship()
    user: Users = Relationship(
        sa_relationship_kwargs={"secondary": "room_members", "viewonly": True}
    )


class RefreshToken(SQLModel, table=True):  # type: ignore
    __tablename__ = "refresh_token"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, sa_type=BIGINT)
    refresh_token: str = Field(
        sa_column=Column(String(128), nullable=False, unique=True)
    )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=30)
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now())


@listens_for(RoomMembers, "before_insert")
def before_insert_room_member(
    mapper: object, connection: Connection, target: RoomMembers
) -> None:
    if target.room_name is None:
        result = connection.execute(
            select(Rooms.name).where(Rooms.id == target.room_id)
        )
        room_name = result.scalar()
        target.room_name = room_name

    if target.room_avatar_url is None:
        result = connection.execute(
            select(Rooms.avatar_url).where(Rooms.id == target.room_id)
        )
        room_avater_url = result.scalar()
        target.room_avatar_url = room_avater_url

    if target.user_name is None:
        result = connection.execute(
            select(Users.display_name).where(Users.id == target.user_id)
        )
        user_display_name = result.scalar()
        target.user_name = user_display_name

    if target.user_avatar_url is None:
        result = connection.execute(
            select(Users.avatar_url).where(Users.id == target.user_id)
        )
        user_avatar_url = result.scalar()
        target.user_avatar_url = user_avatar_url
