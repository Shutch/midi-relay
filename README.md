# MIDI Relay
MIDI Relay used to make a remote MIDI device appear as a local device.

It uses a websocket connection for duplex communication between the client
and server.

## Server
The server is run on the local machine. It will create a virtual MIDI device
that can be interacted with by other programs. It will relay any MIDI messages
to any connected clients and forward any received MIDI messages through the 
virtual MIDI device.

## Client
The client is run on the remote machine. It connects to the MIDI device connected
to it and forward any messages from it to the relay server. It will also relay 
MIDI messages from the server to the device.

