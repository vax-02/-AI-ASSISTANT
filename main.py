# main.py

from Assistant import Assistant
from SystemHandler import SystemHandler

WAKE_WORD = "asistente" # <--- Palabra clave de activación

def process_command(handler: SystemHandler, command: str):
    """Procesa el comando de voz del usuario y llama a SystemHandler."""
    
    command = command.lower().strip() # Asegurar minúsculas y sin espacios extra
    
    if "salir" in command or "terminar" in command:
        handler.assistant.speak("Adiós. ¡Que tengas un buen día!")
        return False

    elif "lista de comandos" in command or "comandos disponibles" in command:
        handler.show_commands()

    elif "abrir git bash" in command or "abrir consola git" in command:
        handler.open_git_bash()

    elif "abrir cmd" in command or "simbolo del sistema" in command:
        handler.open_cmd()

    elif "abrir administrador de tareas" in command or "abrir task manager" in command:
        handler.open_task_manager()

    elif "abrir explorador" in command or "explorar archivos" in command:
        handler.open_file_explorer()
        
    elif "cerrar ventana" in command or "cerrar explorador" in command:
        handler.close_window()

    elif "cambiar de ventana" in command or "otra ventana" in command:
        handler.switch_window()
        
    elif "minimizar todas" in command or "mostrar escritorio" in command:
        handler.minimize_all_windows()

    elif "ir a youtube" in command or "abrir youtube" in command:
        handler.open_youtube_in_brave()

    elif "listar contenido" in command or "muestra la carpeta" in command:
        handler.list_content()
        
    elif "dónde estoy" in command or "directorio actual" in command:
        handler.assistant.speak(f"Actualmente estás en el directorio: {handler.current_path}")
        
    # --- Comandos con Argumentos (Abrir Unidad, Abrir Item) ---
        
    elif command.startswith("abrir unidad") or command.startswith("explorar disco"):
        parts = command.split()
        drive_letter = ""
        for part in reversed(parts):
            if len(part) == 1 and part.isalpha():
                drive_letter = part
                break
            
        if drive_letter:
            handler.navigate_to_drive(drive_letter)
        else:
            handler.assistant.speak("¿Qué unidad quieres explorar? Dime la letra.")

    elif command.startswith("abrir"):
        item_name = command.replace("abrir", "", 1).strip()
        if item_name:
            handler.open_item(item_name)
        else:
            handler.assistant.speak("Dime el nombre de la carpeta o archivo que deseas abrir.")
        
    else:
        # Se llegó aquí con la palabra clave + un comando no reconocido
        handler.assistant.speak("No reconozco ese comando.")

    return True

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    
    print("Iniciando asistente...")
    IA = Assistant()
    system_manager = SystemHandler(IA)
    print("--------------------------------------------------")
    print(f"Asistente listo. Esperando la palabra clave '{WAKE_WORD}'.")
    print("--------------------------------------------------")

    running = True
    while running:
        command = IA.listen() 

        if command is None or command == "ERROR_API":
            continue

        # 1. Verificar la activación (Wake Word)
        if WAKE_WORD in command:
            
            # 2. Eliminar la palabra clave para obtener el comando de acción
            action_command = command.replace(WAKE_WORD, "", 1).strip()

            if not action_command:
                # Caso 1: Solo se dijo "asistente" -> Pide un comando
                IA.speak("¿Qué necesitas?")
                follow_up = IA.listen()
                
                if follow_up and follow_up not in ["ERROR_API"]:
                    running = process_command(system_manager, follow_up)
                elif follow_up is None:
                    IA.speak("No te he oído.")
                    
            else:
                # Caso 2: Se dijo "asistente [comando]" -> Ejecuta directo
                running = process_command(system_manager, action_command)