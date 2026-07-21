# Ultron Virtual Assistant

Welcome to the Ultron project repository. Ultron is a next-generation, omnipresent, voice-controlled virtual AI assistant designed to automate and execute all user tasks sequentially through natural language voice commands.

## Features
- **Premium Web UI (Phase 4):** A gorgeous, animated, dark-mode dashboard that visualizes Ultron's cognitive state (Listening, Thinking, Speaking) using WebSockets.
- **Total Voice Control:** Uses `SpeechRecognition` and `edge-tts` for high-quality human-like voice interaction.
- **100% Local AI:** Powered by local Large Language Models. No API keys required. Total privacy.
- **Auto-Committer:** Automatically pushes code and action logs to GitHub to boost your commit history.
- **Advanced Execution:** Ultron can autonomously read files, write code, list directories, and execute terminal commands (with strict Windows compatibility).
- **Self-Healing Code Execution:** If Ultron runs a command or script that crashes, it catches the error and autonomously rewrites the code to fix the issue!
- **Proactive System Monitoring:** Ultron runs a background thread tracking your CPU/RAM and will proactively speak up to warn you of spikes.
- **Web Browsing:** Ultron can search the internet for current events without relying on paid APIs.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3 installed. Run the following command:
```bash
pip install -r requirements.txt
```

### 2. Setup the Local "Brain" (Ollama)
Because Ultron runs 100% locally to protect your data, you need to have a local LLM runner active:
1. Download and install [Ollama](https://ollama.com/).
2. Open a terminal and download the default model by running:
   ```bash
   ollama run llama3
   ```

### 3. Run Ultron's Web Dashboard
Make sure your microphone is plugged in, and run:
```bash
python web_ui.py
```
This will start Ultron in the background and launch a stunning Web UI on `http://127.0.0.1:5000`. Open that link in your browser to watch the magic happen!