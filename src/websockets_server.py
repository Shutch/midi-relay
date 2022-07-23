import asyncio
import websockets
import mido
import functools

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG,
)

async def handler(websocket, mido_port):
    await asyncio.gather(
        consumer_handler(websocket, mido_port),
        producer_handler(websocket, mido_port),
    )

async def consumer_handler(websocket, mido_port):
    async for message in websocket:
        logging.debug(f"Consumer: {message}")
    # async for bytes in websocket:
    #     message = mido.Message.from_bytes(bytes) 
    #     logging.debug(f"Relaying {message}")
    #     out_port.send(message)

async def producer_handler(websocket, mido_port):
    while True:
        note = mido.Message('note_on', note=48, velocity=20)
        await websocket.send(note.bin())
        await asyncio.sleep(5.0)
    # async for message in piano_port:
        # await websocket.send(message.bin())


async def main():
    # Open virtual port
    while True:
        name = "MIDI Relay Output"
        try:
            out_port = mido.open_output(name, virtual=True, autoreset=True)
            logging.info(f'Created virtual MIDI port {name}.')
            break
        except ConnectionError:
            wait_time = 1.0
            logging.info(f"Virtual MIDI port {name} creation failed, waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            continue
        except KeyboardInterrupt:
            return

    # Start server
    address = "0.0.0.0"
    port = 9999
    bound_handler = functools.partial(handler, mido_port=out_port)
    try:
        async with websockets.serve(bound_handler, address, port):
            logging.info(f"Serving websocket server on {address}:{port}")
            await asyncio.Future()  # run forever

    except KeyboardInterrupt:
        return

asyncio.run(main())
