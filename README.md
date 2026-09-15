# Desktop Pet

## Introduction

Desktop Pet is a small Python and Pygame project that places an animated character along the bottom of the screen. The character moves automatically, reacts to player input, and shares the scene with randomly generated fish. The project explores simple game physics, sprite animation, desktop-sized window placement, and interactive visual effects.

## Program Files

- `desktoplize-try-2.py` is the final presentation program. Run this file to use the complete desktop-pet experience.
- `moving-try.py` is the earlier movement test program. It is included for reference and testing; it demonstrates the core character movement, jumping, and squash-and-stretch animation in a standard 800-by-600 window.

## Features of the Final Program

The final program includes:

- A borderless Pygame window sized to the current display width and positioned near the bottom of the screen on macOS and other POSIX systems.
- An automatically moving character that reverses direction at the screen edges.
- Gravity-based jumping and landing behavior.
- Squash-and-stretch animation when the character jumps and lands.
- A speed boost while the left **Shift** key is held.
- Random fish creation, random colors, variable lifetimes, and changing horizontal movement.
- A limit on the number of visible fish to keep the scene manageable.
- A draft settings button in the lower-right corner that currently reports a click in the terminal.

## Environment Requirements

- Python 3.10 to 3.13
- Pygame 2.5 or later
- A desktop environment capable of opening a Pygame window

No image or audio assets are required; all visual elements are drawn by the program.

## Installation

1. Clone or download this repository.
2. Open a terminal in the downloaded project folder.
3. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install Pygame:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Usage

Start the final application with:

```bash
python3 desktoplize-try-2.py
```

Controls:

- Press **Space** to jump.
- Hold the left **Shift** key to boost horizontal movement.
- Click the white settings button in the lower-right corner to test the draft settings interaction.
- Press **Esc** or close the window to exit.

To run the simpler movement test instead, use:

```bash
python3 moving-try.py
```

## Development Notes

The project was developed in stages:

- June 30: `moving-try.py` introduced horizontal and vertical character movement plus squash-and-stretch animation.
- June 30: `desktoplize-try-2.py` adapted the character for a desktop-sized, borderless window.
- July 3: `desktoplize-try-2.py` added Shift boosting, a draft settings button, and randomly spawning fish with variable colors and movement.
