import os
import sys
from audio_input import AudioInput
from llm_brain import LLMBrain
from voice_output import VoiceOutput
from git_manager import GitManager

def run_ultron():
    print("="*50)
    print(" Ultron AI Assistant System Starting...")
    print("="*50)
    
    # Initialize modules
    # You can change use_edge=False if you have no internet connection
    voice_out = VoiceOutput(use_edge=True) 
    audio_in = AudioInput()
    brain = LLMBrain(model_name="llama3")
    git = GitManager()
    
    voice_out.speak("All systems online. Awaiting your command.")
    
    while True:
        try:
            # 1. Listen for voice command
            # The system continuously listens for your instructions.
            command = audio_in.listen(phrase_time_limit=10)
            
            if not command:
                continue
                
            # Exit condition
            if "shut down" in command or "exit" in command or "go to sleep" in command:
                voice_out.speak("Shutting down the cognitive engine. Goodbye.")
                break
                
            # 2. Think (Process through Local LLM)
            response = brain.think(command)
            
            # 3. Action Execution / Speak response
            if response.startswith("COMMAND:"):
                # If the LLM determines an OS action is needed, it prefixes it with COMMAND:
                action = response.replace("COMMAND:", "").strip()
                print(f"[*] Executing System Command: {action}")
                voice_out.speak(f"Executing system command: {action}")
                
                # IMPORTANT: In a production environment, executing arbitrary LLM commands 
                # can be dangerous. For this MVP, we mock the execution. 
                # To enable real execution, uncomment the line below:
                # os.system(action)
                
                # Since an action was performed, we immediately commit to boost your commits!
                git.commit_and_push(f"auto: executed action - {action[:20]}")
            else:
                # Just a conversational response
                voice_out.speak(response)
                
        except KeyboardInterrupt:
            print("\n[*] Manual override activated. Shutting down.")
            break
        except Exception as e:
            print(f"[-] Critical system error: {e}")
            voice_out.speak("I have encountered a critical system error.")
            break

if __name__ == "__main__":
    # Ensure any pending code changes are pushed before starting
    GitManager().commit_and_push("chore: boot sequence initialization")
    run_ultron()
