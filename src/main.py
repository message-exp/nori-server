import asyncio
import logging

from api.server import server

async def serve() -> None:
    server.add_insecure_port("[::]:3000")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(serve())
