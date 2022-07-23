FROM python:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libasound2 \
    libasound2-dev \
    alsa-utils

RUN pip install \
    mido \
    python-rtmidi \
    starlite \
    uvicorn \
    asyncio \
    websockets \
    watchdog[watchmedo]==2.1.5  # auto-restart bug in 2.1.6

COPY src /src

CMD ["watchmedo", "auto-restart", \
     "--directory", "/src/", \
     "--pattern", "*.py", \
     "--recursive", \
     "--signal", "SIGTERM", \
     "python", "/src/server.py"]
