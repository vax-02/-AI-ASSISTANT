import os
import subprocess
from colorama import Fore, Style
import glob # ¡NUEVA LIBRERÍA!
class SystemHandler:
    def __init__(self, assistant_instance):
        self.assistant = assistant_instance
        self.current_path = os.getcwd()
        self.drives = self._get_available_drives()
        self.assistant.speak(f"Estoy en la carpeta: {self.current_path}")

    def _get_available_drives(self):
        """Intenta obtener una lista simple de unidades (principalmente para Windows)."""
        drives = []
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    def navigate_to_drive(self, drive_letter):
        """Cambia a una unidad de disco (ej. C:, D:)."""
        drive = f"{drive_letter}:\\"
        if os.path.exists(drive):
            os.chdir(drive)
            self.current_path = os.getcwd()
            self.assistant.speak(f"Cambiado a la unidad {drive_letter}.")
            return True
        else:
            self.assistant.speak(f"La unidad {drive_letter} no existe.")
            return False

    def list_content(self):
        """Lista y describe el contenido del directorio actual de forma mejorada."""
        try:
            content = os.listdir(self.current_path)
            
            # 1. Descripción por Voz
            folders = [f for f in content if os.path.isdir(os.path.join(self.current_path, f))]
            files = [f for f in content if os.path.isfile(os.path.join(self.current_path, f))]

            self.assistant.speak(f"El directorio actual: {os.path.basename(self.current_path)}, tiene {len(folders)} carpetas y {len(files)} archivos.")
            
            # 2. Presentación en Consola (mejorada)
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
        """Abre un archivo o carpeta utilizando el comando del sistema operativo (start o xdg-open)."""
        
        # 1. Encuentra la ruta exacta: busca el archivo o carpeta que contenga el nombre
        # Usamos glob para encontrar una coincidencia que no sea sensible a mayúsculas/minúsculas
        search_pattern = os.path.join(self.current_path, f"*{item_name}*")
        matches = glob.glob(search_pattern, recursive=False)
        
        if not matches:
            self.assistant.speak(f"No encontré ningún archivo o carpeta que contenga el nombre: {item_name}")
            return
        
        # 2. Selecciona la mejor coincidencia (la primera)
        target_path = matches[0]
        
        if os.path.isdir(target_path):
            item_type = "carpeta"
        else:
            item_type = "archivo"

        self.assistant.speak(f"Abriendo la {item_type}: {os.path.basename(target_path)}")

        try:
            # Comando genérico para abrir en el sistema operativo predeterminado
            if os.name == 'nt':  # Windows
                os.startfile(target_path)
            elif os.name == 'posix':  # Linux, macOS
                subprocess.call(['xdg-open', target_path]) # o 'open' en Mac
        
        except Exception as e:
            self.assistant.speak(f"Error al intentar abrir el elemento: {e}")
            
    def open_git_bash(self):
        """Abre Git Bash en el directorio actual."""
        self.assistant.speak(f"Abriendo Git Bash en la carpeta actual.")
        try:
            # Comando estándar para Windows. Asegúrate de que Git esté en el PATH.
            # Alternativamente, puedes usar la ruta completa: "C:\\Program Files\\Git\\bin\\bash.exe"
            subprocess.Popen(['start', 'bash.exe'], shell=True, cwd=self.current_path)
        except FileNotFoundError:
            self.assistant.speak("No encontré la aplicación Git Bash. Asegúrate de tenerla instalada y en el PATH.")
        except Exception as e:
             self.assistant.speak(f"Error al intentar abrir Git Bash: {e}")

    # --- Implementaciones futuras ---
    # def open_file_or_folder(self, name):
    #     """Abre un archivo o carpeta. Depende de 'os.startfile' o 'subprocess.call'."""
    #     pass

    # def search_files(self, keyword):
    #     """Busca archivos con una palabra clave en el directorio actual y subdirectorios."""
    #     pass