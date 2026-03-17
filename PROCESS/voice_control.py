import speech_recognition as sr
import threading

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command = None
        self.listening = True
        
        # adjust for background noise
        with self.microphone as source:
            print("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready!")
        
        # start listening in background thread
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                if "volume" in text:
                    self.command = "volume"
                elif "brightness" in text:
                    self.command = "brightness"
                elif "mute" in text:
                    self.command = "mute"
                elif "play" in text or "pause" in text:
                    self.command = "playpause"
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                pass

    def get_command(self):
        # returns command and resets it
        cmd = self.command
        self.command = None
        return cmd