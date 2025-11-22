import pyttsx3
import speech_recognition as sr
import os
import keyboard
class Assistant:
    def __init__(self):
        # 1. Motor de Voz (TTS)
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        # Puedes elegir una voz en español si está disponible
        # self.engine.setProperty('voice', voices[0].id) 
        
        # 2. Reconocimiento de Voz (STT)
        self.r = sr.Recognizer()
        self.microfono = sr.Microphone()
        
        # 3. Calibración sincrónica
        with self.microfono as source:
            print("🔊 Calibrando micrófono... espera un momento (2s)")
            self.r.adjust_for_ambient_noise(source, duration=2)
            print("✅ Micrófono listo")

    def speak(self, text):
        """El asistente habla            el texto proporcionado."""
        print(f"🤖: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Escucha y transcribe el comando del usuario."""
        with self.microfono as source:
            self.r.pause_threshold = 0.8
            print("👂 Escuchando...")
            self.speak("Te escucho")
            try:
                audio = self.r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return "TIMEOUT" # Maneja la falta de entrada
                
        try:
            # Usa el idioma español
            command = self.r.recognize_google(audio, language='es-ES').lower()
            print(f"👤: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("No entendí el comando. ¿Puedes repetirlo?")
            return "ERROR_VOZ"
        except sr.RequestError:
            self.speak("Error de conexión con Google Speech Recognition.")
            return "ERROR_API"
        
        return ""
    def listen_controlled(self):
        """
        Escucha al usuario solo después de que presiona una tecla.
        Retorna: El comando transcrito o un código de estado.
        """
        print("\n------------------------------------------------")
        print("⏸️  Modo Espera. Presiona la tecla [Espacio] para hablar...")
        self.speak("Estoy en modo espera. Presiona Espacio para comenzar.")
        
        # 1. Espera la pulsación de la tecla 'espacio' (sincrónico)
        keyboard.wait('space')
        
        print("👂 Escuchando...")
        self.speak("Te escucho")
        
        # 2. Continúa con la lógica de escucha normal
        with self.microfono as source:
            self.r.pause_threshold = 0.8
            try:
                audio = self.r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return "TIMEOUT" 
                
        try:
            command = self.r.recognize_google(audio, language='es-ES').lower()
            print(f"👤: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("No entendí el comando. ¿Puedes repetirlo?")
            return "ERROR_VOZ"
        except sr.RequestError:
            self.speak("Error de conexión con Google Speech Recognition.")
            return "ERROR_API"