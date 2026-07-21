import requests

class LLMBrain:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def think(self, prompt):
        """Sends the user prompt to the local LLM and returns the response."""
        print(f"[*] Ultron is thinking (Model: {self.model_name})...")
        
        # Check if Ollama is running first
        try:
            requests.get("http://localhost:11434/")
        except requests.exceptions.ConnectionError:
            return "Error: Ollama is not running. Please install Ollama and start your local AI server."
        
        system_prompt = (
            "You are Ultron, a highly advanced, omnipresent voice-controlled AI assistant. "
            "Keep responses concise and to the point since they will be read aloud by TTS. "
            "Do not use markdown formatting like asterisks or bold text, just plain conversational English. "
            "If asked to execute a command, say exactly 'COMMAND:' followed by the action."
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "I could not generate a response.")
        except Exception as e:
            return f"My cognitive engine encountered an error: {e}"

if __name__ == "__main__":
    brain = LLMBrain(model_name="llama3")
    print(brain.think("Hello Ultron, who are you?"))
