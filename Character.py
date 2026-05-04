import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class MMORPGCharacter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MMORPG Character Movement - WASD Controls")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Game variables
        self.canvas_width = 800
        self.canvas_height = 600
        self.character_x = 380
        self.character_y = 270
        self.character_size = 80
        self.character_height = 100
        self.speed = 5
        self.facing_right = True

        # Canvas background — pure black
        self.canvas_bg_hex = '#000000'
        self.canvas_bg_rgb = (0, 0, 0)

        # ── Animation state ────────────────────────────────────────────
        self.is_running = False
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_speed = 6          # Ticks per frame (lower = faster)
        self.prev_running = False    # Track previous running state to detect changes
        # ──────────────────────────────────────────────────────────────

        # Load character images
        if not self.load_character_images():
            messagebox.showerror("Error", "Character images not found!\nPlease check the file paths.")
            self.window.destroy()
            return

        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.canvas_bg_hex
        )
        self.canvas.pack()

        # Draw initial scene
        self.draw_character()
        self.draw_ui()

        # Input
        self.keys_pressed = set()
        self.window.bind('<KeyPress>', self.key_press)
        self.window.bind('<KeyRelease>', self.key_release)
        self.window.bind('<KeyPress-Escape>', lambda e: self.exit_game())

        # Start game loop
        self.continuous_movement()

        self.window.protocol("WM_DELETE_WINDOW", self.exit_game)

    # ------------------------------------------------------------------
    # IMAGE LOADING
    # ------------------------------------------------------------------

    def make_transparent_image(self, pil_img):
        """Composite RGBA image onto canvas bg colour for pseudo-transparency."""
        img = pil_img.convert("RGBA")
        r, g, b, a = img.split()
        bg = Image.new("RGBA", img.size, (*self.canvas_bg_rgb, 255))
        bg.paste(img, mask=a)
        return ImageTk.PhotoImage(bg.convert("RGB"))

    def load_frames(self, paths):
        """Load a list of image paths as resized, transparent PhotoImages."""
        frames = []
        for path in paths:
            if not os.path.exists(path):
                print(f"Warning: frame not found → {path}")
                continue
            img = Image.open(path).convert("RGBA")
            img = img.resize(
                (self.character_size, self.character_height),
                Image.Resampling.LANCZOS
            )
            frames.append(self.make_transparent_image(img))
        return frames

    def load_character_images(self):
        """Load idle sprites and running animation frames."""
        base = r"C:\Users\BrandonChewZiChern\Downloads"

        # ── Idle sprites ──────────────────────────────────────────────
        idle_left_path  = os.path.join(base, "C1.png")
        idle_right_path = os.path.join(base, "C2.png")

        # ── Running frames ─────────────────────────────────────────────
        left_run_paths = [
            os.path.join(base, "C1.png"),
            os.path.join(base, "C1L.png"),
        ]
        right_run_paths = [
            os.path.join(base, "C2.png"),
            os.path.join(base, "C2R.png"),
        ]
        # ──────────────────────────────────────────────────────────────

        for p in (idle_left_path, idle_right_path):
            if not os.path.exists(p):
                messagebox.showerror("File Not Found", f"Cannot find:\n{p}")
                return False

        try:
            self.character_images = {}

            self.character_images['idle_left']  = self.load_frames([idle_left_path])[0]
            self.character_images['idle_right'] = self.load_frames([idle_right_path])[0]

            self.character_images['run_left']  = self.load_frames(left_run_paths)
            self.character_images['run_right'] = self.load_frames(right_run_paths)

            if not self.character_images['run_left']:
                self.character_images['run_left'] = [self.character_images['idle_left']]
            if not self.character_images['run_right']:
                self.character_images['run_right'] = [self.character_images['idle_right']]

            print("Character images loaded successfully!")
            return True

        except Exception as e:
            print(f"Error loading images: {e}")
            messagebox.showerror("Error", f"Failed to load images:\n{str(e)}")
            return False

    # ------------------------------------------------------------------
    # DRAWING
    # ------------------------------------------------------------------

    def get_current_sprite(self):
        """Return the correct sprite for the current animation state."""
        if not self.is_running:
            # Always show idle when not running horizontally
            return self.character_images['idle_right' if self.facing_right else 'idle_left']

        # Cycle through run frames
        frames = self.character_images['run_right' if self.facing_right else 'run_left']

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % len(frames)

        return frames[self.anim_frame]

    def draw_character(self):
        """Redraw the character sprite and name tag."""
        self.canvas.delete('character')

        x, y = self.character_x, self.character_y
        cx = x + self.character_size // 2
        cy = y + self.character_height // 2

        sprite = self.get_current_sprite()
        self.canvas.create_image(cx, cy, image=sprite, tags='character')

        self.canvas.create_text(
            cx, y - 12,
            text="Player",
            fill='white',
            font=('Arial', 10, 'bold'),
            tags='character'
        )

        self.canvas.delete('position')
        self.canvas.create_text(
            700, 580,
            text=f"Position: ({x}, {y})",
            fill='white',
            font=('Arial', 10),
            tags='position'
        )

    def draw_ui(self):
        """Draw the controls hint bar."""
        self.canvas.create_rectangle(
            5, 5, 350, 35,
            fill='#1A1A1A',
            outline='#4A90E2',
            tags='ui'
        )
        self.canvas.create_text(
            175, 20,
            text="WASD - Move Character | ESC - Exit",
            fill='white',
            font=('Arial', 12, 'bold'),
            tags='ui'
        )

    # ------------------------------------------------------------------
    # INPUT & MOVEMENT
    # ------------------------------------------------------------------

    def key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())

    def key_release(self, event):
        self.keys_pressed.discard(event.keysym.lower())

    def continuous_movement(self):
        """Game loop called every ~16 ms (~60 FPS)."""
        moved = False

        # ── Check EACH key independently ──────────────────────────────

        if 'w' in self.keys_pressed:
            self.character_y = max(0, self.character_y - self.speed)
            moved = True

        if 's' in self.keys_pressed:
            self.character_y = min(
                self.canvas_height - self.character_height,
                self.character_y + self.speed
            )
            moved = True

        # A and D determine running state — checked separately from W/S
        pressing_a = 'a' in self.keys_pressed
        pressing_d = 'd' in self.keys_pressed

        if pressing_a:
            self.character_x = max(0, self.character_x - self.speed)
            self.facing_right = False
            moved = True

        if pressing_d:
            self.character_x = min(
                self.canvas_width - self.character_size,
                self.character_x + self.speed
            )
            self.facing_right = True
            moved = True

        # ── Running state: ONLY true when A or D is physically held ───
        # This is the fix: running is tied strictly to A/D keys,
        # NOT to whether the character moved at all.
        currently_running = pressing_a or pressing_d

        if not currently_running:
            # No horizontal key held → always reset to idle
            # This fires correctly even if W or S is still held
            self.is_running = False
            self.anim_frame = 0
            self.anim_timer = 0
        else:
            self.is_running = True

        # ── Redraw when: moved OR running state changed OR animating ──
        state_changed = currently_running != self.prev_running
        self.prev_running = currently_running

        if moved or state_changed or self.is_running:
            self.draw_character()

        self.window.after(16, self.continuous_movement)

    # ------------------------------------------------------------------
    # EXIT
    # ------------------------------------------------------------------

    def exit_game(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the game?"):
            self.window.quit()
            self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = MMORPGCharacter()
    game.run()
