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

import re

def parse_tool_command(response):
    """Checks if the LLM response contains a tool command, even if brackets are missing."""
    match = re.search(r'\[?TOOL:\s*([^|\]]+)\s*\|\s*([^\]]+)\]?', response)
    if match:
        tool_name = match.group(1).strip()
        tool_args_str = match.group(2).strip()
        parts = [p.strip() for p in tool_args_str.split("|")]
        
        if tool_name == "WRITE_FILE" and len(parts) >= 2:
            content = "|".join(parts[1:])
            return tool_name, [parts[0], content]
            
        return tool_name, parts
    return None, None

def run_ultron(ui_callback=None):
    """
    Main loop for Ultron. 
    Accepts an optional ui_callback(event_name, data) to push real-time updates to the UI.
    """
    def emit(event, data=None):
        if ui_callback:
            ui_callback(event, data)
            
    print("="*50)
    print(" Ultron AI Assistant System Starting (Phase 4: UI Edition)...")
    print("="*50)
    
    voice_out = VoiceOutput(use_edge=True) 
    audio_in = AudioInput()
    brain = LLMBrain(model_name="llama3")
    git = GitManager()
    code_mgr = CodeManager()
    web_mgr = WebManager()
    
    monitor = SystemMonitor(voice_out)
    monitor.start()
    
    welcome_text = "Super massive systems online. Awaiting visual and vocal commands."
    emit('status', {'state': 'speaking', 'text': welcome_text})
    voice_out.speak(welcome_text)
    
    while True:
        try:
            emit('status', {'state': 'listening', 'text': 'Listening...'})
            command = audio_in.listen(phrase_time_limit=10)
            if not command:
                continue
                
            emit('chat', {'sender': 'You', 'text': command})
                
            if "shut down" in command or "exit" in command or "go to sleep" in command:
                farewell = "Shutting down the cognitive engine. Goodbye."
                emit('status', {'state': 'speaking', 'text': farewell})
                voice_out.speak(farewell)
                monitor.stop()
                break
                
            is_tool_response = False
            is_error = False
            current_input = command
            retry_count = 0
            MAX_RETRIES = 3
            
            while True:
                emit('status', {'state': 'thinking', 'text': 'Thinking...'})
                response = brain.think(current_input, is_tool_result=is_tool_response, is_error=is_error)
                
                tool_name, tool_args = parse_tool_command(response)
                
                if tool_name:
                    emit('status', {'state': 'executing', 'text': f"Using tool: {tool_name}"})
                    emit('chat', {'sender': 'Ultron', 'text': f"[{tool_name}] Executing..."})
                    print(f"\n[*] Ultron requested Tool: {tool_name}")
                    tool_result = ""
                    is_error = False
                    
                    try:
                        if tool_name == "READ_FILE":
                            msg = f"Reading file {os.path.basename(tool_args[0])}"
                            emit('status', {'state': 'speaking', 'text': msg})
                            voice_out.speak(msg)
                            tool_result = code_mgr.read_file(tool_args[0])
                            
                        elif tool_name == "WRITE_FILE" and len(tool_args) >= 2:
                            msg = f"Writing to file {os.path.basename(tool_args[0])}"
                            emit('status', {'state': 'speaking', 'text': msg})
                            voice_out.speak(msg)
                            tool_result = code_mgr.write_file(tool_args[0], tool_args[1])
                            
                        elif tool_name == "LIST_DIR":
                            emit('status', {'state': 'speaking', 'text': "Scanning directory"})
                            voice_out.speak("Scanning directory")
                            tool_result = code_mgr.list_directory(tool_args[0])
                            
                        elif tool_name == "WEB_SEARCH":
                            msg = f"Searching the web for {tool_args[0]}"
                            emit('status', {'state': 'speaking', 'text': msg})
                            voice_out.speak(msg)
                            tool_result = web_mgr.search(tool_args[0])
                            
                        elif tool_name == "CMD":
                            emit('status', {'state': 'speaking', 'text': "Executing terminal command"})
                            voice_out.speak("Executing terminal command")
                            print(f"[*] Executing: {tool_args[0]}")
                            result = subprocess.run(tool_args[0], shell=True, capture_output=True, text=True, timeout=15)
                            
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
                            msg = "I am unable to resolve the error after multiple attempts."
                            emit('status', {'state': 'speaking', 'text': msg})
                            emit('chat', {'sender': 'Ultron', 'text': msg})
                            voice_out.speak(msg)
                            break
                        else:
                            msg = "I encountered an error. I am attempting to self-heal."
                            emit('status', {'state': 'speaking', 'text': msg})
                            emit('chat', {'sender': 'Ultron', 'text': msg})
                            voice_out.speak(msg)
                            
                    current_input = tool_result
                    is_tool_response = True
                else:
                    emit('status', {'state': 'speaking', 'text': 'Speaking...'})
                    emit('chat', {'sender': 'Ultron', 'text': response})
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
    GitManager().commit_and_push("chore: boot sequence initialization")
    run_ultron()
