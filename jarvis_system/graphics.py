import math
import tkinter as tk
from jarvis_system import config

class HighResRadarHUD:
    def __init__(self, parent_frame):
        """
        Manages the high-resolution calm sci-fi radar visual layout.
        """
        self.canvas_width = 280
        self.canvas_height = 280
        self.cx = self.canvas_width // 2
        self.cy = self.canvas_height // 2
        
        self.canvas = tk.Canvas(
            parent_frame, 
            width=self.canvas_width, 
            height=self.canvas_height, 
            bg=config.COLOR_BACKGROUND, 
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Vector Engine state parameters
        self.angle = 0.0
        self.pulse = 0.0

    def render_frame(self, computing_mode=False):
        """Renders one frame of clean vector shapes using steady mathematical curves."""
        self.canvas.delete("all")
        
        # Smooth baseline parameters (No randomized glitches or shakes)
        pulse_speed = 0.10 if computing_mode else 0.03
        spin_speed = 1.0 if computing_mode else 0.5
        
        self.angle += spin_speed
        self.pulse += pulse_speed

        # 1. Generate Calm Central Core Structure
        self.canvas.create_oval(self.cx - 45, self.cy - 45, self.cx + 45, self.cy + 45, fill="", outline=config.COLOR_CORE_AURA, width=1)
        self.canvas.create_oval(self.cx - 38, self.cy - 38, self.cx + 38, self.cy + 38, fill=config.COLOR_CORE_AURA, outline=config.COLOR_BORDER, width=2)
        self.canvas.create_oval(self.cx - 28, self.cy - 28, self.cx + 28, self.cy + 28, fill=config.COLOR_CORE_SOLID, outline="#ffffff", width=1)

        # 2. Compute Interleaved Nested Mechanical Rings
        num_dashes = 12                  
        dash_len = 16         
        gap_len = 14          
        total_step = dash_len + gap_len 
        
        # Smoothly swelling sine waves
        inner_radius = 75 + 10 * math.sin(self.pulse)
        outer_radius = 110 + 12 * math.sin(self.pulse * 0.8)

        for i in range(num_dashes):
            # RING 1: Inner Set (Smooth continuous clockwise travel)
            deg1 = i * total_step + self.angle
            x1_r1 = self.cx + inner_radius * math.cos(math.radians(deg1))
            y1_r1 = self.cy + inner_radius * math.sin(math.radians(deg1))
            x2_r1 = self.cx + inner_radius * math.cos(math.radians(deg1 + dash_len))
            y2_r1 = self.cy + inner_radius * math.sin(math.radians(deg1 + dash_len))
            self.canvas.create_line(x1_r1, y1_r1, x2_r1, y2_r1, fill=config.COLOR_RING_INNER, width=3, capstyle="round")

            # RING 2: Outer Set (Smooth continuous counter-clockwise nested positioning filling gaps)
            deg2 = i * total_step - self.angle + (total_step / 2)
            x1_r2 = self.cx + outer_radius * math.cos(math.radians(deg2))
            y1_r2 = self.cy + outer_radius * math.sin(math.radians(deg2))
            x2_r2 = self.cx + outer_radius * math.cos(math.radians(deg2 + dash_len))
            y2_r2 = self.cy + outer_radius * math.sin(math.radians(deg2 + dash_len))
            self.canvas.create_line(x1_r2, y1_r2, x2_r2, y2_r2, fill=config.COLOR_RING_OUTER, width=3, capstyle="round")
