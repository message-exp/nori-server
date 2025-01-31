from sqlmodel import (
    TEXT,
    String,
    SQLModel,
    Field,
    Relationship,
    BIGINT,
    Column,
    TIMESTAMP,
    func,
)
from datetime import datetime
from snowflake import SnowflakeGenerator

snowflake_gen = SnowflakeGenerator(1)


def generate_snowflake_id() -> int:
    return next(snowflake_gen)


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    username: str = Field(sa_column=Column(String(256), index=True, unique=True))
    display_name: str = Field(sa_column=Column(String(256)))
    email: str = Field(sa_column=Column(TEXT))
    token: str = Field(sa_column=Column(String(512), index=True))
    hashed_password: str = Field(sa_column=Column(String(60)))

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    rooms: list["Rooms"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"secondary": "room_members"}
    )


class Rooms(SQLModel, table=True):
    __tablename__ = "rooms"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    name: str = Field(sa_column=Column(String(256)))
    avater_url: str = Field(sa_column=Column(TEXT))

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    members: list["RoomMembers"] = Relationship(
        back_populates="room"
    )  # for custom misc

    users: list["Users"] = Relationship(
        back_populates="rooms", sa_relationship_kwargs={"secondary": "room_members"}
    )  # for user profile


class RoomMembers(SQLModel, table=True):
    __tablename__ = "room_members"
    id: int | None = Field(
        sa_column=Column(BIGINT, primary_key=True, default=generate_snowflake_id)
    )
    room_id: int = Field(foreign_key="rooms.id", index=True, sa_type=BIGINT)
    user_id: int = Field(foreign_key="users.id", index=True, sa_type=BIGINT)
    room_name: str = Field(
        sa_column=Column(String(256))
    )  # user customize room name (show only user)
    room_avater_url: str = Field(
        sa_column=Column(TEXT)
    )  # user customize room avater (show only user)
    user_name: str = Field(
        sa_column=Column(String(256))
    )  # custom user name in room (show all room user)
    user_avater_url: str = Field(
        sa_column=Column(TEXT)
    )  # custom user avater in room (show all room user)

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
        )
    )

    room: Rooms = Relationship(back_populates="members")
    user: Users = Relationship()


class Messages(SQLModel, table=True):
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
    user: Users = Relationship(sa_relationship_kwargs={"secondary": "room_members"})
