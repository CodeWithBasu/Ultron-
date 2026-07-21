# Ultron Virtual Assistant

Welcome to the Ultron project repository. Ultron is a next-generation, omnipresent, voice-controlled virtual AI assistant designed to automate and execute all user tasks sequentially through natural language voice commands.

## Features
- **Total Voice Control:** Uses `SpeechRecognition` and `edge-tts` for high-quality human-like voice interaction.
- **100% Local AI:** Powered by local Large Language Models. No API keys required. Total privacy.
- **Auto-Committer:** Automatically pushes code and action logs to GitHub to boost your commit history.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3 installed. Run the following command:
```bash
pip install -r requirements.txt
```

### 2. Setup the Local "Brain" (Ollama)
Because Ultron runs 100% locally to protect your data (and allows you to drop in your own trained models), you need to have a local LLM runner active:
1. Download and install [Ollama](https://ollama.com/).
2. Open a terminal and download the default model by running:
   ```bash
   ollama run llama3
   ```
   *(You can change `llama3` to any other model you have trained inside `llm_brain.py`)*

### 3. Run Ultron
Make sure your microphone is plugged in, and run:
```bash
python main.py
```

Ultron will calibrate the microphone, say "All systems online", and then listen for your commands! Every time Ultron makes a change to the system, it will automatically push to this repository to boost your commits.