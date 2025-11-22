# Assistant.py

import pyttsx3
import speech_recognition as sr
import os
import ctypes # Necesario para algunas funciones de SystemHandler

class Assistant:
    """Clase principal que maneja las interacciones de voz."""
    def __init__(self):
        # 1. Motor de Voz (TTS)
        self.engine = pyttsx3.init()
        # Puedes configurar la voz aquí si lo deseas
        
        # 2. Reconocimiento de Voz (STT)
        self.r = sr.Recognizer()
        self.microfono = sr.Microphone()
        
        # 3. Calibración sincrónica para ruido de fondo
        with self.microfono as source:
            print("🔊 Calibrando micrófono... espera 2 segundos")
            self.r.adjust_for_ambient_noise(source, duration=2) 
            print("✅ Micrófono listo")

    def speak(self, text):
        """El asistente habla el texto proporcionado."""
        print(f"🤖: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """
        Escucha y transcribe una frase corta, manejando silencios y errores.
        Devuelve el comando en minúsculas o None si no se reconoce nada/fue ruido.
        """
        with self.microfono as source:
            self.r.pause_threshold = 0.8
            print("👂 Escuchando en modo silencioso...")
            
            try:
                # Escucha hasta 5 segundos. Si hay silencio total, saltará el timeout.
                audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                return None 
                
        try:
            command = self.r.recognize_google(audio, language='es-ES').lower()
            return command
        except sr.UnknownValueError:
            return None # Ruido o voz no clara
        except sr.RequestError:
            self.speak("Error de conexión con Google Speech Recognition.")
            return "ERROR_API"