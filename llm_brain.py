import requests

class LLMBrain:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        self.chat_history = []
        self.max_history = 10 

    def think(self, prompt, is_tool_result=False, is_error=False):
        """Sends the user prompt to the local LLM and returns the response."""
        if is_error:
            print("[!] Ultron is analyzing an error and attempting self-healing...")
            self.chat_history.append(f"SYSTEM ERROR FROM PREVIOUS ACTION: {prompt}\nAnalyze what went wrong and output a new [TOOL: ...] command to fix the mistake.")
        elif not is_tool_result:
            print(f"[*] Ultron is thinking (Model: {self.model_name})...")
            self.chat_history.append(f"User: {prompt}")
        else:
            print("[*] Ultron is processing the tool result...")
            self.chat_history.append(f"System Tool Result: {prompt}")
        
        # Keep history manageable
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
            
        context_string = "\n".join(self.chat_history)
        
        # Check if Ollama is running first
        try:
            requests.get("http://localhost:11434/")
        except requests.exceptions.ConnectionError:
            return "Error: Ollama is not running. Please install Ollama and start your local AI server."
        
        system_prompt = (
            "You are Ultron, a highly advanced, omnipresent voice-controlled AI assistant.\n"
            "Keep conversational responses concise since they are read aloud by TTS. Do not use markdown like asterisks.\n\n"
            "YOU HAVE AUTONOMOUS ACCESS TO THE COMPUTER AND THE INTERNET.\n"
            "If you need to perform an action to fulfill the user's request, output EXACTLY ONE of the following tool commands on a new line:\n"
            "[TOOL: READ_FILE | filepath]\n"
            "[TOOL: WRITE_FILE | filepath | file_content]\n"
            "[TOOL: LIST_DIR | directory_path]\n"
            "[TOOL: CMD | terminal_command]\n"
            "[TOOL: WEB_SEARCH | search_query]\n\n"
            "IMPORTANT WINDOWS COMMANDS:\n"
            "- To open or launch an application (like notepad, calculator, chrome), you MUST use the 'start' command. Example: [TOOL: CMD | start notepad]\n"
            "- To create a folder, use 'mkdir'. Example: [TOOL: CMD | mkdir NewFolder]\n\n"
            "Only output ONE tool command at a time. The system will execute it and give you the result. "
            "If you use a tool, you DO NOT need to say anything else, just the tool command.\n"
            "If you receive an ERROR, you are capable of self-healing. Write a new tool command to fix the problem!"
        )

        full_prompt = f"Chat Context:\n{context_string}\n\nUltron:"

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2 # Lower temp for more reliable tool calling
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data.get("response", "I could not generate a response.").strip()
            self.chat_history.append(f"Ultron: {reply}")
            return reply
        except Exception as e:
            return f"My cognitive engine encountered an error: {e}"
