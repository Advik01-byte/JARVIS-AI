import threading
import time
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from jarvis_system import config, graphics, backend

ctk.set_appearance_mode("dark")

class JarvisMainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JARVIS System Mainframe")
        self.after(0, lambda: self.state("zoomed"))

        # Main Layout Column Configuration split
        self.grid_columnconfigure(0, weight=3)  
        self.grid_columnconfigure(1, weight=7)  
        self.grid_rowconfigure(0, weight=1)

        # LEFT PANEL: Graphics Framework
        self.left_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL_LEFT, border_width=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        self.left_center = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.left_center.pack(expand=True)

        self.status_title = ctk.CTkLabel(
            self.left_center, 
            text="JARVIS SYSTEM OPERATIONAL", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#e9edef"
        )
        self.status_title.pack(pady=20)

        self.hud_engine = graphics.HighResRadarHUD(self.left_center)

        self.pin_btn = ctk.CTkCheckBox(
            self.left_center, 
            text="ALWAYS ON TOP", 
            font=("Segoe UI", 12, "bold"),
            text_color="#8696a0",
            hover_color=config.COLOR_BACKGROUND,
            fg_color="#202c33",
            checkmark_color=config.COLOR_BORDER,
            command=self.toggle_pin_state
        )
        self.pin_btn.pack(pady=30)

        # RIGHT PANEL: WhatsApp Conversation Feed
        self.right_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL_RIGHT, border_width=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.right_panel.grid_rowconfigure(0, weight=1)  
        self.right_panel.grid_rowconfigure(1, weight=0)  
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Message stream box container
        self.chat_feed = ctk.CTkScrollableFrame(self.right_panel, fg_color=config.COLOR_PANEL_RIGHT, corner_radius=0)
        self.chat_feed.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Bottom Input Capsule Panel Box
        self.input_deck = ctk.CTkFrame(self.right_panel, fg_color="#111b21", height=60, corner_radius=0, border_width=0)
        self.input_deck.grid(row=1, column=0, sticky="ew")
        
        self.input_deck.grid_columnconfigure(0, weight=1)
        self.input_deck.grid_columnconfigure(1, weight=0)
        self.input_deck.grid_rowconfigure(0, weight=1)

        self.entry_bar = ctk.CTkEntry(
            self.input_deck, 
            placeholder_text="Type a message", 
            height=40,
            font=("Segoe UI", 15),
            border_width=0,
            corner_radius=20,  
            fg_color="#2a3942",
            text_color="#e9edef",
            placeholder_text_color="#8696a0"
        )
        self.entry_bar.grid(row=0, column=0, sticky="ew", padx=(20, 10), pady=10)
        self.entry_bar.bind("<Return>", self.trigger_processing_sequence)

        self.send_btn = ctk.CTkButton(
            self.input_deck,
            text="➔",
            font=("Segoe UI", 18, "bold"),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#202c33",
            text_color=config.COLOR_BORDER,
            command=lambda: self.trigger_processing_sequence(None)
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 20), pady=10)

        self.engine = backend.JarvisCoreEngine(
            log_callback=self.safe_append_jarvis,
            status_callback=self.update_status_header,
            confirmation_callback=self.prompt_safety_window
        )

        self.computing_mode = False
        self.append_jarvis_bubble("Core architecture synchronized smoothly. Welcome back, Boss. Command interfaces stand by.")
        self.run_animation_loop()

    def safe_append_jarvis(self, text_content):
        self.after(0, lambda: self.append_jarvis_bubble(text_content))

    def append_user_bubble(self, query_text):
        """Builds a robust right-aligned capsule bubble that maintains its design."""
        timestamp = time.strftime("%H:%M")
        
        bubble_frame = ctk.CTkFrame(self.chat_feed, fg_color="transparent")
        bubble_frame.pack(fill="x", anchor="e", pady=4, padx=(100, 20))

        # Enforced layout structural parameters using full pill labels natively
        msg_label = ctk.CTkLabel(
            bubble_frame, 
            text=f"{query_text}\n\n{timestamp}  ✔✔", 
            font=("Segoe UI", 14),
            text_color=config.COLOR_TEXT_USER, 
            fg_color=config.COLOR_BUBBLE_USER,
            corner_radius=14,
            padx=18,
            pady=10,
            justify="left",
            wraplength=500
        )
        msg_label.pack(anchor="e")
        self._scroll_to_bottom()

    def append_jarvis_bubble(self, response_text):
        """Builds a robust left-aligned capsule bubble that maintains its design."""
        timestamp = time.strftime("%H:%M")
        
        bubble_frame = ctk.CTkFrame(self.chat_feed, fg_color="transparent")
        bubble_frame.pack(fill="x", anchor="w", pady=4, padx=(20, 100))

        msg_label = ctk.CTkLabel(
            bubble_frame, 
            text=f"{response_text}\n\n{timestamp}", 
            font=("Segoe UI", 14),
            text_color=config.COLOR_TEXT_JARVIS, 
            fg_color=config.COLOR_BUBBLE_JARVIS,
            corner_radius=14,
            padx=18,
            pady=10,
            justify="left",
            wraplength=500
        )
        msg_label.pack(anchor="w")
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        self.update_idletasks()
        self.chat_feed._parent_canvas.yview_moveto(1.0)

    def toggle_pin_state(self):
        is_checked = self.pin_btn.get()
        self.attributes("-topmost", bool(is_checked))

    def update_status_header(self, state):
        def _update():
            if state == "computing":
                self.computing_mode = True
                self.status_title.configure(text="JARVIS: TYPING...", text_color=config.COLOR_BORDER)
            else:
                self.computing_mode = False
                self.status_title.configure(text="JARVIS SYSTEM OPERATIONAL", text_color="#e9edef")
        self.after(0, _update)

    def prompt_safety_window(self, command_string):
        return messagebox.askyesno(
            title="🛡️ System Command Intercepted",
            message=f"Jarvis wants to execute a computer task:\n\n👉 {command_string}\n\nAuthorize this operation, Boss?"
        )

    def run_animation_loop(self):
        self.hud_engine.render_frame(computing_mode=self.computing_mode)
        self.after(25, self.run_animation_loop)

    def trigger_processing_sequence(self, event):
        query = self.entry_bar.get().strip()
        if not query:
            return
            
        self.entry_bar.delete(0, tk.END)
        self.append_user_bubble(query)
        self.update_status_header("computing")
        
        threading.Thread(target=self.engine.process_query, args=(query,), daemon=True).start()
