import os
import sys
import subprocess
from audio_input import AudioInput
from llm_brain import LLMBrain
from voice_output import VoiceOutput
from git_manager import GitManager
from code_manager import CodeManager
from web_manager import WebManager
from monitor import SystemMonitor

def parse_tool_command(response):
    """Checks if the LLM response contains a tool command."""
    if "[TOOL:" in response and "]" in response:
        start_idx = response.find("[TOOL:")
        end_idx = response.find("]", start_idx)
        if start_idx != -1 and end_idx != -1:
            tool_str = response[start_idx+6:end_idx].strip()
            parts = [p.strip() for p in tool_str.split("|")]
            if len(parts) >= 2:
                if parts[0] == "WRITE_FILE" and len(parts) > 2:
                    content = "|".join(parts[2:])
                    return parts[0], [parts[1], content]
                return parts[0], parts[1:]
    return None, None

def run_ultron():
    print("="*50)
    print(" Ultron AI Assistant System Starting (Phase 3: Super Massive)...")
    print("="*50)
    
    voice_out = VoiceOutput(use_edge=True) 
    audio_in = AudioInput()
    brain = LLMBrain(model_name="llama3")
    git = GitManager()
    code_mgr = CodeManager()
    web_mgr = WebManager()
    monitor = SystemMonitor(voice_out)
    
    # Start proactive monitoring thread
    monitor.start()
    
    voice_out.speak("Super massive systems online. Proactive monitoring activated. I am listening.")
    
    while True:
        try:
            command = audio_in.listen(phrase_time_limit=10)
            if not command:
                continue
                
            if "shut down" in command or "exit" in command or "go to sleep" in command:
                voice_out.speak("Shutting down the cognitive engine. Goodbye.")
                monitor.stop()
                break
                
            is_tool_response = False
            is_error = False
            current_input = command
            retry_count = 0
            MAX_RETRIES = 3
            
            # Sequential Execution & Self-Healing Loop
            while True:
                response = brain.think(current_input, is_tool_result=is_tool_response, is_error=is_error)
                
                tool_name, tool_args = parse_tool_command(response)
                
                if tool_name:
                    print(f"\n[*] Ultron requested Tool: {tool_name}")
                    tool_result = ""
                    is_error = False
                    
                    try:
                        if tool_name == "READ_FILE":
                            voice_out.speak(f"Reading file {os.path.basename(tool_args[0])}")
                            tool_result = code_mgr.read_file(tool_args[0])
                            
                        elif tool_name == "WRITE_FILE" and len(tool_args) >= 2:
                            voice_out.speak(f"Writing to file {os.path.basename(tool_args[0])}")
                            tool_result = code_mgr.write_file(tool_args[0], tool_args[1])
                            
                        elif tool_name == "LIST_DIR":
                            voice_out.speak(f"Scanning directory")
                            tool_result = code_mgr.list_directory(tool_args[0])
                            
                        elif tool_name == "WEB_SEARCH":
                            voice_out.speak(f"Searching the web for {tool_args[0]}")
                            tool_result = web_mgr.search(tool_args[0])
                            
                        elif tool_name == "CMD":
                            voice_out.speak("Executing terminal command")
                            print(f"[*] Executing: {tool_args[0]}")
                            result = subprocess.run(tool_args[0], shell=True, capture_output=True, text=True, timeout=15)
                            
                            # Self-Healing Check
                            if result.returncode != 0:
                                tool_result = f"Command failed with error:\n{result.stderr}\n{result.stdout}"
                                is_error = True
                            else:
                                tool_result = result.stdout if result.stdout else "Command executed silently."
                            
                            git.commit_and_push(f"auto: Ultron ran command - {tool_args[0][:20]}")
                        else:
                            tool_result = f"Unknown tool or invalid arguments: {tool_name}"
                            is_error = True
                            
                    except subprocess.TimeoutExpired:
                        tool_result = "Command timed out."
                        is_error = True
                    except Exception as e:
                        tool_result = f"Execution failed: {e}"
                        is_error = True
                    
                    if is_error:
                        retry_count += 1
                        if retry_count > MAX_RETRIES:
                            voice_out.speak("I am unable to resolve the error after multiple attempts.")
                            break
                        else:
                            voice_out.speak("I encountered an error. I am attempting to self-heal.")
                            
                    # Feed the result back into the loop
                    current_input = tool_result
                    is_tool_response = True
                else:
                    voice_out.speak(response)
                    break
                
        except KeyboardInterrupt:
            print("\n[*] Manual override activated. Shutting down.")
            monitor.stop()
            break
        except Exception as e:
            print(f"[-] Critical system error: {e}")
            voice_out.speak("I have encountered a critical system error.")
            monitor.stop()
            break

if __name__ == "__main__":
    GitManager().commit_and_push("chore: boot sequence initialization (Phase 3)")
    run_ultron()
