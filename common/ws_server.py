import websockets
import asyncio
from loguru import logger


class WebSocketServer:
    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 8765):
        self.host = host
        self.port = port

        self.clients = set()
        pass

    async def handle_client(self, ws):
        # add new client
        self.clients.add(websockets)

        try:
            async for message in ws:
                logger.info(f"receive message: {message}")
                await ws.send(f"server has been received: {message}")
        except websockets.ConnectionClosed as e:
            logger.error(f"client disconnected: {e}")
        finally:
            # remove disconnected client
            self.clients.remove(ws)

    async def send(self, message):
        """

        :param message:
        :return:
        """
        if not self.clients:
            logger.error("no client has been connected! can not send message.")
            return

        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.ConnectionClosed as e:
                disconnected_clients.add(client)
            finally:
                self.clients -= disconnected_clients

    async def start(self):
        logger.info(f"start websocket server: ws://{self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()
