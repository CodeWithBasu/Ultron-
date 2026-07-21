import speech_recognition as sr

class AudioInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # We try to initialize and calibrate the mic
        try:
            with sr.Microphone() as source:
                print("[*] Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("[+] Calibration complete.")
        except Exception as e:
            print(f"[-] Could not access microphone: {e}")

    def listen(self, timeout=None, phrase_time_limit=None):
        """Listens to the microphone and returns the transcribed text."""
        try:
            with sr.Microphone() as source:
                print("\n[*] Listening...")
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    print("[*] Processing speech...")
                    # Using Google's free STT API as a fallback. 
                    # To remain 100% offline, you can install Vosk and replace this line with recognize_vosk(audio)
                    text = self.recognizer.recognize_google(audio)
                    print(f"You: {text}")
                    return text.lower()
                except sr.WaitTimeoutError:
                    return None
                except sr.UnknownValueError:
                    print("[-] Could not understand the audio.")
                    return None
                except sr.RequestError as e:
                    print(f"[-] Could not request results; {e}")
                    return None
        except Exception as e:
            print(f"[-] Microphone error: {e}")
            return None

if __name__ == "__main__":
    audio_module = AudioInput()
    text = audio_module.listen(timeout=5)
    if text:
        print(f"Test Transcribed: {text}")
