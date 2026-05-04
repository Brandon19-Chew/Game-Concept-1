# Game-Concept-1
## Character movement by using ( A, W, S, D )

This project is a 2D MMORPG-style character movement demo built with Python.
It creates a game window where a character sprite can be controlled using the keyboard, simulating basic MMORPG character movement — similar to games like MapleStory or Ragnarok Online.

---
## Core features:

1. WASD movement — the player moves the character around an 800×600 black canvas using W (up), A (left), S (down), D (right).
2. Directional facing — pressing A switches to the left-facing sprite (C1.png), pressing D switches to the right-facing sprite (C2.png).
3. Running animation — holding A or D cycles through multiple sprite frames to simulate a running animation; releasing the key snaps back to the idle sprite.
4. Transparent sprites — PNG images with transparent backgrounds are composited onto the canvas background so the character appears clean without a visible box around it.
5. Smooth 60 FPS loop — movement and animation run on a 16ms timer loop for fluid gameplay feel.
6. Boundary detection — the character cannot walk off the edges of the screen.

---

## Demo video below

https://github.com/user-attachments/assets/f998e291-be93-420c-be68-160d75da5ae8

---
