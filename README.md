# Spark

## Overview

Spark is an interactive visual stimulation application. It features high-contrast patterns, gradients, and gentle animations to support visual cortex development, eye tracking, and focus. The app uses GPU shaders for smooth, appealing visuals and includes touch/mouse interactivity for engagement.

Key features:
- **Patterns**: Cycles through checkerboard, stripes, spiral, and color gradients on tap/click.
- **Interactivity**: Hand movements create fading colorful trails.
- **Safety**: Soft, pastel-safe colors; auto-closes after 5 minutes to prevent overstimulation.
- **Tech**: Built with Pyglet and OpenGL shaders for efficient rendering.

Recommended: Supervise use, limit sessions to <5 minutes.

## Installation

1. **Prerequisites**:
   - Python 3.6+ (tested on 3.12).
   - Install Pyglet: Run `pip install pyglet` in your terminal.

2. **Download**:
   - Save the provided script as `spark.py`.

## Usage

1. Run the app: `python spark.py`.
2. It launches in full-screen mode.
3. **Interactions**:
   - Tap/click: Cycle through patterns.
   - Move mouse/touch: Create trailing effects.
4. Exit: Press ESC or wait 5 minutes for auto-close.

## Code Structure

- **Shaders**: Vertex and fragment shaders for procedural patterns.
- **Modes**: 0=Checkerboard, 1=Stripes, 2=Spiral, 3=Gradient (with soft color shifts via HSV).
- **Trails**: CPU-drawn circles for movement feedback.
- **Timer**: Uses `pyglet.clock` to close after 300 seconds.

## Customization

- Adjust trail size/alpha in `on_mouse_motion`.
- Modify shader uniforms for different effects (e.g., speed via `time` multipliers).
- For non-fullscreen: Change `fullscreen=True` to `False` in `pyglet.window.Window`.

If you encounter issues, ensure your system supports OpenGL 3.3+ for shaders.