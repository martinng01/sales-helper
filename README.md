# TikTok Sales Helper

Originally a project submitted for TikTok Techjam 2024, I continued the development of the project and added more features.

Original project [here](https://github.com/joseyjh/sales-helper-hackathon), which was built on top of [WhisperLive](https://github.com/collabora/WhisperLive), a nearly-live implementation of OpenAI's Whisper.

## Demo

VIDEO HERE

## Project Overview

This project is designed to assist sales teams by leveraging customer relationship management (CRM) systems to streamline their daily workflows throughout the end-to-end sales processes. By integrating artificial intelligence (AI) models, the project aims to provide smart sales helper functionalities that enable managerial insights and optimize sales strategies.

## Features

- 📹 Live Video Conferencing 
- 😊 Emotion Detection 
- 📝 Real-Time Transcription 
- 🔍 Live Automatic Information Retrieval 

## Technologies

The project was created with:

- Frontend
  - React
  - Vite
  - Tailwind CSS
  - [getstream.io](https://getstream.io)
  - [socket.io](https://socket.io)

- Application Server
  - Flask
  - WebSockets
  - LangChain
  - ChromaDB
  - OpenAI
  - OpenCV

## Getting Started

Run the following commands to run this application on your local machine.

### Clone this Respository

```bash
git clone https://github.com/martinng01/sales-helper.git
```

### Setting Up the Environment

Set up the Anaconda environment with **Python 3.11.9**

```bash
conda create -n sales-helper python==3.11.9
conda activate sales-helper
pip install -r requirements.txt
```

Install npm dependencies
```bash
cd react-video-call
npm install
```

### Running the Application

Run all 3 code blocks in **different** terminal windows from the base directory:

- Frontend
```bash
cd react-video-call
npm run dev
```

- Application Server
```bash
python middleware/middleware.py
```

- Transcription Server
```bash
python WhisperLive/run_server.py
```

Visit the localhost website in the frontend terminal window.

## Documentation

### Architecture
![architecture](docs/images/saleshelper.jpg)

### Retrieval Augmented Generation (RAG) Engine
![rag](docs/images/rag.jpg)