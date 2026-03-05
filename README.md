diff --git a/README.md b/README.md
index 31c2266491046378237ba1edee9e6710bf78a1d8..1ca469082d4434dc7cad4f87c176d004135da69e 100644
--- a/README.md
+++ b/README.md
@@ -1,16 +1,120 @@
-# How to use this RAG AI Teaching assistant on your own data
-## Step 1 - Collect your videos
-Move all your video files to the videos folder
+# RAG Course Assistant
 
-## Step 2 - Convert to mp3
-Convert all the video files to mp3 by ruunning video_to_mp3
+A simple Retrieval-Augmented Generation (RAG) pipeline that answers learner questions from your course videos.
 
-## Step 3 - Convert mp3 to json 
-Convert all the mp3 files to json by ruunning mp3_to_json
+This project takes videos, extracts audio, transcribes content into timestamped chunks, creates vector embeddings, and retrieves the most relevant chunks to generate grounded answers.
 
-## Step 4 - Convert the json files to Vectors
-Use the file preprocess_json to convert the json files to a dataframe with Embeddings and save it as a joblib pickle
+---
 
-## Step 5 - Prompt generation and feeding to LLM
+## What this project does
 
-Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM
+- Converts course videos into `.mp3` audio files.
+- Transcribes audio into text chunks with timestamps.
+- Creates embeddings for each chunk and stores them in a local vector-ready dataset.
+- Accepts a learner question, retrieves top relevant chunks, and generates an answer with an LLM.
+
+---
+
+## Project structure
+
+- `videos/` – input course videos.
+- `audios/` – extracted `.mp3` files.
+- `jsons/` – transcript chunks in JSON format.
+- `process_video.py` – video → audio conversion using `ffmpeg`.
+- `speech_to_text.py` – audio → transcript chunks using Whisper.
+- `create_chunk.py` – transcript chunks → embeddings dataset (`embeddings.joblib`).
+- `process_incoming.py` – query-time retrieval + answer generation.
+- `embeddings.joblib` – saved dataframe of chunk metadata + vectors.
+
+---
+
+## Prerequisites
+
+- Python 3.9+
+- `ffmpeg` installed and available in PATH
+- Ollama running locally on `http://localhost:11434`
+- Models available in Ollama:
+  - Embedding model: `bge-m3`
+  - Generation model: `llama3.2`
+- (Optional) NVIDIA GPU/CUDA for faster Whisper transcription
+
+---
+
+## Installation
+
+```bash
+python -m venv .venv
+source .venv/bin/activate
+pip install -U pip
+pip install openai-whisper torch pandas scikit-learn numpy joblib requests
+```
+
+> Note: Depending on your platform, installing `torch` may require a specific command from the official PyTorch docs.
+
+---
+
+## End-to-end workflow
+
+### 1) Add videos
+Put all source videos in `videos/`.
+
+### 2) Convert videos to audio
+```bash
+python process_video.py
+```
+
+### 3) Transcribe audio to JSON chunks
+```bash
+python speech_to_text.py
+```
+
+### 4) Build embeddings dataset
+```bash
+python create_chunk.py
+```
+This creates/updates `embeddings.joblib`.
+
+### 5) Ask questions
+```bash
+python process_incoming.py
+```
+You will be prompted with:
+```text
+Ask a Question:
+```
+
+The script retrieves top relevant chunks and generates an answer grounded in course content.
+
+---
+
+## How retrieval works
+
+1. User query is embedded using Ollama (`/api/embed`).
+2. Query vector is compared against chunk vectors with cosine similarity.
+3. Top-k chunks are selected.
+4. A prompt is built with chunk metadata (`title`, `number`, `start`, `end`, `text`).
+5. LLM (`/api/generate`) returns the final response.
+
+---
+
+## Output artifacts
+
+- `embeddings.joblib` – dataframe storing each chunk plus embedding vector.
+- `prompt.txt` – last generated prompt sent to LLM.
+- `response.txt` – last generated LLM answer.
+- `output.json` – sample single-file transcription output.
+
+---
+
+## Notes and limitations
+
+- Current scripts assume local folders (`videos`, `audios`, `jsons`) already exist.
+- File name parsing in `process_video.py` expects a specific video naming pattern.
+- Transcription is currently configured with `language="hi"` and `task="translate"`; adjust for your content.
+- No API retry/error handling is implemented yet for Ollama endpoints.
+
+---
+
+## Quick interview-friendly summary
+
+This repository is a lightweight educational RAG assistant: it indexes your video course transcripts and answers student questions by retrieving relevant timestamped sections, then generating grounded guidance with an LLM.
