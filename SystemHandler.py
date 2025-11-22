# SystemHandler.py

import os
import subprocess
from colorama import Fore, Style
import glob
import time 
import webbrowser 
import ctypes # Necesario para control de ventanas en Windows

class SystemHandler:
    """Clase para interactuar con el sistema operativo y el sistema de archivos."""
    
    def __init__(self, assistant_instance):
        self.assistant = assistant_instance
        self.current_path = os.getcwd()
        self.drives = self._get_available_drives()
        
        # Saludo Inicial
        self.assistant.speak(f"Hola! Soy tu asistente. Estoy listo y mi directorio actual es: {self.current_path}")

    def _get_available_drives(self):
        """Intenta obtener una lista simple de unidades (principalmente para Windows)."""
        drives = []
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    # --- Navegación y Archivos ---

    def navigate_to_drive(self, drive_letter):
        """Cambia a una unidad de disco (ej. C:, D:)."""
        drive_letter = drive_letter.upper().replace(":", "")
        drive = f"{drive_letter}:\\"
        
        if os.path.exists(drive):
            os.chdir(drive)
            self.current_path = os.getcwd()
            self.assistant.speak(f"Cambiado a la unidad {drive_letter}. Ahora estoy en {self.current_path}")
            return True
        else:
            self.assistant.speak(f"La unidad {drive_letter} no existe o no está accesible.")
            return False

    def list_content(self):
        """Lista y describe el contenido del directorio actual de forma mejorada."""
        try:
            content = os.listdir(self.current_path)
            
            folders = [f for f in content if os.path.isdir(os.path.join(self.current_path, f))]
            files = [f for f in content if os.path.isfile(os.path.join(self.current_path, f))]

            self.assistant.speak(f"El directorio actual: {os.path.basename(self.current_path)}, tiene {len(folders)} carpetas y {len(files)} archivos.")
            
            # Presentación en Consola (mejorada)
            print("\n" + "="*50)
            print(f"📋 CONTENIDO DE: {self.current_path}")
            print("="*50)

            for item in content:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    print(f"{Fore.BLUE}[DIR] {item}{Style.RESET_ALL}")
                elif os.path.isfile(full_path):
                    print(f"{Fore.GREEN}[FILE] {item}{Style.RESET_ALL}")
                else:
                    print(f"[???] {item}")
            
            print("="*50 + "\n")

        except Exception as e:
            self.assistant.speak(f"Ocurrió un error al listar el contenido: {e}")

    def open_item(self, item_name):
        """Abre un archivo o carpeta."""
        search_pattern = os.path.join(self.current_path, f"*{item_name}*")
        matches = glob.glob(search_pattern, recursive=False)
        
        if not matches:
            self.assistant.speak(f"No encontré ningún archivo o carpeta que contenga el nombre: {item_name}")
            return
        
        target_path = matches[0]
        item_type = "carpeta" if os.path.isdir(target_path) else "archivo"

        self.assistant.speak(f"Abriendo la {item_type}: {os.path.basename(target_path)}")

        try:
            if os.name == 'nt':
                os.startfile(target_path)
            elif os.name == 'posix':
                subprocess.call(['xdg-open', target_path]) 
        
        except Exception as e:
            self.assistant.speak(f"Error al intentar abrir el elemento: {e}")
            
    # --- Control de Aplicaciones y Ventanas ---

    def open_git_bash(self):
        """Abre Git Bash en el directorio actual."""
        self.assistant.speak(f"Abriendo Git Bash en la carpeta actual.")
        try:
            subprocess.Popen(['start', 'bash.exe'], shell=True, cwd=self.current_path)
        except Exception as e:
             self.assistant.speak(f"Error al intentar abrir Git Bash: {e}")

    def open_cmd(self):
        """Abre el Símbolo del Sistema (CMD) en el directorio actual."""
        self.assistant.speak("Abriendo el Símbolo del Sistema.")
        try:
            if os.name == 'nt':
                subprocess.Popen(['start', 'cmd'], shell=True, cwd=self.current_path)
            elif os.name == 'posix': 
                subprocess.Popen(['open', '-a', 'Terminal', self.current_path])
        except Exception as e:
            self.assistant.speak(f"Error al abrir CMD/Terminal: {e}")

    def open_task_manager(self):
        """Abre el Administrador de Tareas (Windows)."""
        self.assistant.speak("Abriendo el Administrador de Tareas.")
        try:
            if os.name == 'nt':
                subprocess.Popen(['taskmgr'])
            else:
                self.assistant.speak("Esta función es específica de Windows.")
                
        except Exception as e:
            self.assistant.speak(f"Error al abrir el Administrador de Tareas: {e}")

    def open_file_explorer(self):
        """Abre el explorador de archivos en el directorio actual."""
        self.assistant.speak("Abriendo el explorador de archivos en la carpeta actual.")
        try:
            if os.name == 'nt':
                subprocess.Popen(['explorer', self.current_path])
            elif os.name == 'posix':
                subprocess.call(['xdg-open', self.current_path]) 
            time.sleep(1)
        except Exception as e:
            self.assistant.speak(f"Error al intentar abrir el explorador: {e}")

    def minimize_all_windows(self):
        """Minimiza todas las ventanas (muestra el escritorio). Solo para Windows."""
        self.assistant.speak("Minimizando todas las ventanas.")
        try:
            if os.name == 'nt':
                # Simula la tecla Windows + D
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) 
                ctypes.windll.user32.keybd_event(0x44, 0, 0, 0) 
                ctypes.windll.user32.keybd_event(0x44, 0, 2, 0) 
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) 
            else:
                self.assistant.speak("Esta función de minimización es específica de Windows.")
        except Exception as e:
            self.assistant.speak(f"Error al intentar minimizar ventanas: {e}")

    def switch_window(self):
        """Cambia a la siguiente ventana activa (simula Alt + Tab). Solo para Windows."""
        self.assistant.speak("Cambiando de ventana.")
        try:
            if os.name == 'nt': 
                # Simula la pulsación de Alt + Tab
                ctypes.windll.user32.keybd_event(0x12, 0, 0, 0) 
                ctypes.windll.user32.keybd_event(0x09, 0, 0, 0) 
                ctypes.windll.user32.keybd_event(0x09, 0, 2, 0) 
                ctypes.windll.user32.keybd_event(0x12, 0, 2, 0) 
            else:
                self.assistant.speak("La función de cambiar ventana es específica de Windows.")
        except Exception as e:
            self.assistant.speak(f"Error al intentar cambiar de ventana: {e}")

    def open_youtube_in_brave(self):
        """Abre YouTube usando el navegador Brave o el predeterminado."""
        self.assistant.speak("Abriendo YouTube en el navegador Brave.")
        url = "https://www.youtube.com"
        try:
            # RUTA DE BRAVE - CÁMBIALA si la instalación es diferente
            brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
            webbrowser.get('brave').open_new_tab(url)
            
        except Exception:
            self.assistant.speak("No pude abrir Brave. Intentando abrir YouTube en el navegador predeterminado.")
            webbrowser.open_new_tab(url)
            
    def close_window(self):
        """Cierra el explorador de archivos (Windows) o notifica la limitación."""
        self.assistant.speak("Intentando cerrar ventanas del explorador de archivos...")
        try:
            if os.name == 'nt':
                # Cierra todas las instancias de explorer.exe (el explorador)
                subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'])
                self.assistant.speak("Se han cerrado todas las ventanas del explorador de archivos.")
            else:
                 self.assistant.speak("La función de cerrar ventanas es limitada en sistemas Unix.")
        except Exception as e:
            self.assistant.speak(f"Ocurrió un error al intentar cerrar la ventana: {e}")

    def show_commands(self):
        """Muestra y describe la lista de comandos disponibles."""
        commands = [
            ("ASISTENTE [comando]", "Activa y ejecuta el comando de forma directa."),
            ("ASISTENTE", "Activa el modo de escucha de seguimiento ('¿Qué necesitas?')."),
            ("Salir / Terminar", "Finaliza la ejecución del asistente."),
            ("Abrir unidad C/D", "Cambia el directorio de trabajo a la unidad."),
            ("Listar contenido", "Muestra archivos y carpetas del directorio actual."),
            ("Abrir [archivo/carpeta]", "Abre un archivo o carpeta en el directorio."),
            ("Abrir Explorador de archivos", "Abre el explorador de archivos en la carpeta actual."),
            ("Abrir Git Bash", "Abre Git Bash en la ubicación actual."),
            ("Abrir CMD / Símbolo del sistema", "Abre la consola de comandos en la ubicación actual."),
            ("Abrir Administrador de Tareas", "Abre la herramienta para gestionar procesos (Windows)."),
            ("Cambiar de ventana", "Simula Alt + Tab (Windows)."),
            ("Minimizar todas", "Muestra el escritorio (Simula Win + D en Windows)."),
            ("Ir a YouTube", "Abre YouTube en Brave o navegador predeterminado."),
            ("Cerrar ventana", "Cierra el explorador de archivos (Windows)."),
            ("Lista de comandos", "Muestra esta lista."),
            ("Dónde estoy", "Te dice la ruta actual.")
        ]
        
        # ... (Lógica para imprimir y hablar comandos) ...
        self.assistant.speak("Aquí tienes la lista de comandos disponibles:")
        print("\n" + "="*70)
        print(f"{Fore.CYAN}🚀 LISTA DE COMANDOS DE VOZ DISPONIBLES:{Style.RESET_ALL}")
        print("="*70)
        for cmd, desc in commands:
            print(f"{Fore.YELLOW}  - {cmd.ljust(30)}{Style.RESET_ALL} : {desc}")
        print("="*70 + "\n")