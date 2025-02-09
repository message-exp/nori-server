from datetime import datetime
from sqlmodel import Session ,select 
from model import Messages ,Rooms ,RoomMembers

class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
    def get_message_by_roomId(self ,room_id : int , return_quantity : int , from_when : datetime , lim :int) -> list:
        return self.db.exec(select(Messages).where(Messages.room_id == room_id).where(Messages.created_at<from_when).limit(lim)).all()
    def add_message_to_db(self , message : Messages) -> int:
        self.db.add(message)
        self.db.commit()
        return message.id
    def update_message_to_db(self , room_id :int , id : int) -> None:
        #Update
        return None
        


