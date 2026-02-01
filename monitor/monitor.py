
import pystray
from PIL import Image, ImageDraw
import time
import threading
import requests
import psutil
import subprocess
import os
import sys
import json
from functools import partial



# Config
GATEWAY_PORT = 18789
GATEWAY_CMD = ["openclaw", "gateway"]
CHECK_INTERVAL = 5
CONFIG_PATH = os.path.expanduser(r"~\.openclaw\openclaw.json")
LOG_PATH = os.path.expanduser(r"~\Desktop\skarner\monitor\monitor.log")

# ... (logging and create_image are fine) ...

class SkarnerMonitor:
    # ... (init and helpers fine) ...

    # ... (check_gateway fine) ...

    def update_loop(self):
        while self.running:
            try:
                new_status = self.check_gateway()
                if new_status != self.status or True: 
                    self.status = new_status
                    if self.icon:
                        self.icon.icon = create_image(self.status)
                        state_text = "Online" if new_status == "green" else "Offline"
                        pid_text = f"(PID: {self.gateway_pid})" if self.gateway_pid else ""
                        self.icon.title = f"Skarner: {state_text} {pid_text}"
            except Exception as e:
                log(f"Loop error: {e}")
            time.sleep(CHECK_INTERVAL)

    def start_gateway(self, icon=None, item=None):
        if self.status == "green":
            self.icon.notify("Gateway is already running!", "Skarner")
            return
        
        try:
            subprocess.Popen(
                ["powershell", "-NoExit", "-Command", "openclaw gateway"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.icon.notify("Gateway starting...", "Skarner")
        except Exception as e:
            self.icon.notify(f"Start failed: {e}", "Error")

    def kill_gateway(self, icon=None, item=None):
        try:
            killed = False
            for conn in psutil.net_connections():
                if conn.laddr.port == GATEWAY_PORT:
                     psutil.Process(conn.pid).terminate()
                     killed = True
            
            if killed:
                self.icon.notify("Gateway killed.", "Skarner")
            else:
                self.icon.notify("No Gateway found.", "Skarner")
        except Exception as e:
            self.icon.notify(f"Kill failed: {e}", "Error")

    def stop_app(self, icon=None, item=None):
        self.running = False
        self.icon.stop()

    def set_model(self, model_alias, icon=None, item=None):
        full_name = "google-antigravity/gemini-3-pro-low"
        if model_alias == "Flash":
            full_name = "google/gemini-3-flash-preview"
        elif model_alias == "Pro":
             full_name = "google/gemini-3-pro-preview"
        
        self.update_config("agents.defaults.model.primary", full_name)

    def toggle_tts(self, state, icon=None, item=None):
        val = "auto" if state else "off"
        self.update_config("messages.tts.auto", val)



    def start_gateway(self):
        if self.status == "green":
            self.icon.notify("Gateway is already running!", "Skarner")
            return

        try:
            # Spawn new visible console window for the gateway
            subprocess.Popen(
                ["powershell", "-NoExit", "-Command", "openclaw gateway"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.icon.notify("Gateway starting in new window...", "Skarner")
        except Exception as e:
            self.icon.notify(f"Failed to start: {e}", "Error")

    def kill_gateway(self):
        # Kill any node/openclaw process on the port or by name
        # Windows specific: Taskkill is safer/easier specifically for the node process
        try:
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                 if 'node' in proc.info['name'].lower():
                     # Check if it looks like our gateway? Hard to tell without parsing cmdline
                     # For now, let's just warn it kills node processes
                     pass
            
            # Brute force port:
            # Finding PID listening on port 18789
            for conn in psutil.net_connections():
                if conn.laddr.port == GATEWAY_PORT:
                     psutil.Process(conn.pid).terminate()
                     killed = True
            
            if killed:
                self.icon.notify("Gateway process terminated.", "Skarner")
            else:
                self.icon.notify("No Gateway process found on port 18789.", "Skarner")

        except Exception as e:
            self.icon.notify(f"Error stopping: {e}", "Error")

    def stop_app(self):
        self.running = False
        self.icon.stop()

    def set_model(self, model_alias):
        # Quick switch between common models
        full_name = "google-antigravity/gemini-3-pro-low"
        if model_alias == "Flash":
            full_name = "google/gemini-3-flash-preview"
        elif model_alias == "Pro":
             full_name = "google/gemini-3-pro-preview"
        
        self.update_config("agents.defaults.model.primary", full_name)

    def toggle_tts(self, state):
        val = "auto" if state else "off"
        self.update_config("messages.tts.auto", val)

    def build_menu(self):
        return pystray.Menu(
            pystray.MenuItem("🚀 Start Gateway", self.start_gateway),
            pystray.MenuItem("🛑 Kill Gateway", self.kill_gateway),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🧠 Model", pystray.Menu(
                pystray.MenuItem("Gemini Pro Low (Default)", partial(self.set_model, "Low")),
                pystray.MenuItem("Gemini Flash (Fast)", partial(self.set_model, "Flash")),
            )),
            pystray.MenuItem("🗣️ TTS (Voz)", pystray.Menu(
                pystray.MenuItem("On (Auto)", partial(self.toggle_tts, True)),
                pystray.MenuItem("Off", partial(self.toggle_tts, False)),
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit Monitor", self.stop_app)
        )

    def run(self):
        self.icon = pystray.Icon("Skarner")
        self.icon.icon = create_image("red") 
        self.icon.title = "Skarner Monitor"
        self.icon.menu = self.build_menu()
        
        # Start checking thread
        t = threading.Thread(target=self.update_loop)
        t.daemon = True
        t.start()

        self.icon.run()

if __name__ == "__main__":
    app = SkarnerMonitor()
    app.run()
