import asyncio
import websockets
import mido

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG,
)


def get_devices():
    ports = mido.get_ioport_names()
    return ports

def get_piano_port_name(device_string="Digital Piano"):
    ports = get_devices()

    for p in ports:
        if device_string in p:
            return p

    raise ValueError(f"No piano port found. Port names: {ports}") 

def get_piano_port():
    port_name = get_piano_port_name()
    port = mido.open_input(port_name)
    return port

def make_stream():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    def callback(message):
        loop.call_soon_threadsafe(queue.put_nowait, message)
    async def stream():
        while True:
            yield await queue.get()
    return callback, stream()


async def consumer_handler(websocket):
    # Connect to piano
    while True:
        try:
            port_name = get_piano_port_name()
            port = mido.open_output(port_name)
            logging.info('Connected to output piano port.')
            break
        except ValueError:
            wait_time = 1.0
            logging.info(f"No output piano port found, waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            continue
        except KeyboardInterrupt:
            return

    async for bytes in websocket:
        logging.debug(f"Consumer: {bytes}")
        message = mido.Message.from_bytes(bytes)
        port.send(message)

async def producer_handler(websocket):
    # create a callback/stream pair and pass callback to mido
    cb, stream = make_stream()

    # Connect to piano
    while True:
        try:
            port_name = get_piano_port_name()
            port = mido.open_input(port_name, callback=cb)
            logging.info('Connected to input piano port.')
            break
        except ValueError:
            wait_time = 1.0
            logging.info(f"No input piano port found, waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            continue
        except KeyboardInterrupt:
            return

    # print messages as they come just by reading from stream
    async for message in stream:
        await websocket.send(message.bin())


async def main():
    # connect to server
    address = "192.168.231.220"
    port = 9999
    while True:
        try:
            async with websockets.connect(f"ws://{address}:{port}") as websocket:
                logging.info(f"Connected to ws server at {address}:{port}")
                while True:
                    await asyncio.gather(
                        consumer_handler(websocket),
                        producer_handler(websocket),
                    )
        except ConnectionError:
            wait_time = 1.0
            logging.info(f"Server connection to {address}:{port} failed, waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            continue
        except KeyboardInterrupt:
            exit(0)

asyncio.run(main())
