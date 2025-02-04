from sqlmodel import Session ,select
from model import Messages

class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
    def get_message_by_roomId(self ,room_id : int) -> Messages:
        # cur.execute(f"""SELECT * FROM test WHERE rid = {room_id}""")
        # find_result = cur.fetchone()
        # print(find_result)
        # return {
            # 'room_member_id' :find_result[1],
            # 'room_id' : find_result[2],
            # 'message' : find_result[3],
            # 'created_at' : find_result[4],
            # 'update_at' : find_result[5],
        # }
        return self.db.exec(select(Messages).where(Messages.id == room_id)).first()

   


