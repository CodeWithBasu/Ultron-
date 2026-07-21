import pyttsx3
import asyncio
import edge_tts
import pygame
import os

class VoiceOutput:
    def __init__(self, use_edge=True):
        self.use_edge = use_edge
        # Fallback offline engine setup
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        
        # Initialize pygame mixer for playing edge-tts audio
        # Suppress pygame hello message
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        pygame.mixer.init()

    def speak(self, text):
        """Speaks the text using the preferred TTS engine."""
        print(f"Ultron: {text}")
        if self.use_edge:
            try:
                # Run the async edge-tts generation in a synchronous wrapper
                asyncio.run(self._speak_edge(text))
            except Exception as e:
                print(f"[!] edge-tts failed ({e}), falling back to offline TTS.")
                self._speak_offline(text)
        else:
            self._speak_offline(text)

    async def _speak_edge(self, text):
        voice = "en-US-ChristopherNeural" # High quality male voice
        output_file = "temp_voice.mp3"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Play the generated audio file
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Wait for audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        pygame.mixer.music.unload()
        if os.path.exists(output_file):
            os.remove(output_file)

    def _speak_offline(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    tts = VoiceOutput(use_edge=False) # Testing offline first to avoid API lag during dev
    tts.speak("Audio module initialized successfully.")
