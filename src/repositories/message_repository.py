from sqlmodel import Session
import psycopg2

conn = psycopg2.connect(host = "localhost" , dbname = "postgres" ,user = "postgres" , password="524162027" , port = 5432)
cur = conn.cursor()




class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
    def get_message_by_roomId(self ,room_id) -> dict:
        cur.execute(f"""SELECT * FROM test WHERE rid = {room_id}""")
        find_result = cur.fetchone()
        print(find_result)
        return {
            'room_member_id' :find_result[1],
            'room_id' : find_result[2],
            'message' : find_result[3],
            'created_at' : find_result[4],
            'update_at' : find_result[5],
        }

   


