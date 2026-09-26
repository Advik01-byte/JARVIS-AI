import os
import subprocess
import ollama
import threading
from jarvis_system.config import AI_SYSTEM_PROMPT

class JarvisCoreEngine:
    def __init__(self, log_callback, status_callback, confirmation_callback):
        self.log = log_callback
        self.set_status = status_callback
        self.request_auth = confirmation_callback

    def process_query(self, user_text):
        try:
            # Query Llama 3.2 in normal plain text mode (no JSON structural restrictions)
            response = ollama.generate(
                model='llama3.2',  
                system=AI_SYSTEM_PROMPT,
                prompt=user_text
            )
            raw_response = response['response'].strip()

            # Safeguard check: If the AI output is completely blank, trigger a fallback alert
            if not raw_response:
                self.log("Mainframe warning: Received an empty payload sequence from the local model. Please re-submit.")
                self.set_status("ready")
                return

            # Parse the delimiter tokens
            if "||" in raw_response:
                parts = [p.strip() for p in raw_response.split("||")]
                msg_type = parts[0]
                
                if msg_type == "CHAT":
                    chat_payload = parts[1] if len(parts) > 1 else "Standing by, Sir."
                    self.log(chat_payload)
                    self.set_status("ready")
                
                elif msg_type == "SYSTEM":
                    action_type = parts[1] if len(parts) > 1 else ""
                    target_payload = parts[2] if len(parts) > 2 else ""
                    
                    if action_type == "CREATE_FOLDER":
                        display_cmd = f"Create custom folder structure at -> '{target_payload}'"
                        self.log(f"[Action Intercepted]\nOperation -> {display_cmd}")
                        
                        authorized = self.request_auth(display_cmd)
                        if authorized:
                            self.log("Authorization verified. Processing worker task...")
                            threading.Thread(target=self._execute_folder_creation, args=(target_payload,), daemon=True).start()
                        else:
                            self.log("System Action Cancelled by User.")
                            self.set_status("ready")
                            
                    elif action_type == "OPEN_APP":
                        display_cmd = f"Launch {target_payload}"
                        self.log(f"[Action Intercepted]\nOperation -> {display_cmd}")
                        
                        authorized = self.request_auth(display_cmd)
                        if authorized:
                            self.log("Authorization verified. Deploying application...")
                            subprocess.Popen(target_payload, shell=True)
                            self.log(f"Successfully deployed process thread for {target_payload}.")
                        else:
                            self.log("System Action Cancelled by User.")
                        self.set_status("ready")
                else:
                    # Fallback plain display if formatting drops
                    self.log(raw_response)
                    self.set_status("ready")
            else:
                # If the model forgot the delimiter, treat it as direct chat communication
                self.log(raw_response)
                self.set_status("ready")
                
        except Exception as err:
            self.log(f"System logic mapping error: {str(err)}")
            self.set_status("ready")

    def _execute_folder_creation(self, full_path):
        """Builds directories using native Python file management lines."""
        try:
            # Clean up unintended quotes attached by the model
            clean_path = full_path.replace('"', '').replace("'", "").strip()
            
            # Normalize the path markers so Windows understands it perfectly
            normalized_path = os.path.normpath(clean_path)
            
            # Execute direct OS level creation without opening cmd shell environments
            os.makedirs(normalized_path, exist_ok=True)
            self.log(f"Success! Folder built successfully at:\n{normalized_path}")
        except Exception as e:
            self.log(f"Mainframe path execution failure: {str(e)}")
        
        self.set_status("ready")
