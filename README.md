# Audio Splitter with Docker and FFmpeg

This project provides a Dockerized solution for splitting an audio file (`sample.mp3`) into smaller chunks using `ffmpeg`. The setup ensures that all dependencies are handled within a Docker container, making it easy to run the script in any environment.

## Features

- Uses **FFmpeg** to split audio files into chunks.
- Runs inside a **Docker container** with all dependencies pre-installed.
- Mounts the current working directory to persist output files.
- Splits `sample.mp3` into **5MB** chunks.

## Prerequisites

- **Docker** installed on your system.
- **Python 3.x** (if you want to run the script without Docker).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/shubham-pyc/audio-splitter.git
cd audio-splitter
```

### 2. Build docker image
```bash
docker build -t audio-splitter .
```

### 3. Build docker image
```bash
docker run --rm -v $(pwd):/app audio-splitter
```

### 4. Output Files
After running the script, the audio chunks will be stored in an output_chunks/ directory in your current folder.




