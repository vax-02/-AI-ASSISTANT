from Assistant import Assistant
from SystemHandler import SystemHandler

def process_command(handler: SystemHandler, command: str):
    """Procesa el comando de voz del usuario."""
    
    if "salir" in command or "terminar" in command:
        handler.assistant.speak("Adiós. ¡Que tengas un buen día!")
        return False

    elif "abrir git bash" in command or "abrir consola git" in command:
        handler.open_git_bash()

    elif "listar contenido" in command or "muestra la carpeta" in command:
        handler.list_content()
        
    elif "abrir unidad" in command:
        # Busca la letra de la unidad, ej. 'abrir unidad c'
        parts = command.split()
        if len(parts) > 2:
            drive_letter = parts[-1].upper().replace(":", "") # Obtiene 'C', 'D', etc.
            handler.navigate_to_drive(drive_letter)
        else:
            handler.assistant.speak("¿Qué unidad quieres abrir? Por favor, dime la letra.")

    elif "dónde estoy" in command or "directorio actual" in command:
        handler.assistant.speak(f"Actualmente estás en el directorio: {handler.current_path}")

    # --- Comandos futuros (a implementar) ---
    # elif "buscar" in command:
    #     handler.assistant.speak("¿Qué archivo deseas buscar?")
    #     # Lógica para escuchar la palabra clave y llamar a handler.search_files(keyword)
    
    # elif "abrir" in command:
    #     handler.assistant.speak("¿Qué quieres abrir?")
    #     # Lógica para escuchar el nombre y llamar a handler.open_file_or_folder(name)
        
    else:
        handler.assistant.speak("No reconozco ese comando. Intenta con 'abrir git bash' o 'listar contenido'.")

    return True
# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    
    print("Iniciando asistente...")
    IA = Assistant()
    system_manager = SystemHandler(IA)
    print("--------------------------------------------------")
    print("Asistente listo para recibir comandos.")
    print("--------------------------------------------------")

    running = True
    while running:
        #command = IA.listen()
        command = IA.listen_controlled() 
  
        if command not in ["ERROR_VOZ", "ERROR_API", "TIMEOUT"]:
            running = process_command(system_manager, command)
        elif command == "TIMEOUT":
            IA.speak("No escuché nada después de que presionaste el botón. Repito, ¿en qué puedo ayudarte?")