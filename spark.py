import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.window import key, mouse
import time
import random
import math

# Shaders
vertex_source = """#version 150 core
    in vec2 position;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
    }
"""

fragment_source = """#version 150 core
    uniform vec2 resolution;
    uniform float time;
    uniform int mode;
    out vec4 fragColor;

    vec3 hsv2rgb(vec3 c) {
        vec3 rgb = clamp(abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0);
        rgb = rgb*rgb*(3.0-2.0*rgb);
        return c.z * mix(vec3(1.0), rgb, c.y);
    }

    void main() {
        vec2 uv = gl_FragCoord.xy / resolution;
        vec3 color = vec3(0.0);
        if (mode == 0) {  // Checkerboard with gentle wave
            float scale = 50.0;
            float wave = sin(time * 0.1) * 2.0;
            float check = mod(floor(gl_FragCoord.x / scale + wave) + floor(gl_FragCoord.y / scale), 2.0);
            color = check < 1.0 ? vec3(0.0) : vec3(1.0);
            // Subtle gradient overlay
            color *= (1.0 - uv.y * 0.2);
        } else if (mode == 1) {  // Moving stripes
            float scale = 50.0;
            float move = time * 0.5;
            float stripe = mod(floor(gl_FragCoord.x / scale + move), 2.0);
            color = stripe < 1.0 ? vec3(0.0) : vec3(1.0);
            // Wavy gradient
            float grad = sin(uv.x * 3.14) * 0.1 + 0.9;
            color *= grad;
        } else if (mode == 2) {  // Animated spiral
            vec2 center = resolution / 2.0;
            vec2 pos = gl_FragCoord.xy - center;
            float r = length(pos) / min(resolution.x, resolution.y) * 5.0;
            float a = atan(pos.y, pos.x);
            float val = sin(a * 5.0 + r * 20.0 - time * 0.2);
            color = vec3(smoothstep(0.0, 1.0, val));
            // Radial gradient fade
            color *= (1.0 - r * 0.5);
        } else if (mode == 3) {  // Soft gradient with color changes
            float hue = uv.y + time * 0.05;  // Vertical gradient with slow scroll
            vec3 hsv = vec3(fract(hue), 0.5, 0.9);  // Soft saturation and value for pastel colors
            color = hsv2rgb(hsv);
        }
        fragColor = vec4(color, 1.0);
    }
"""

# Compile shaders
vert_shader = Shader(vertex_source, 'vertex')
frag_shader = Shader(fragment_source, 'fragment')
program = ShaderProgram(vert_shader, frag_shader)

# Window setup
window = pyglet.window.Window(fullscreen=True)
width, height = window.width, window.height

# Full-screen quad
vlist = program.vertex_list(4, GL_TRIANGLE_STRIP,
                            position=('f', (-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0)))

# Globals
mode = 0
trails = []  # [x, y, radius, alpha]

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Bind and set uniforms
    program.use()
    program['resolution'] = (float(width), float(height))
    program['time'] = time.time()
    program['mode'] = mode
    
    # Draw background pattern
    vlist.draw(GL_TRIANGLE_STRIP)
    program.stop()
    
    # Draw trails (CPU for simplicity, with blend)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for trail in trails[:]:
        x, y, radius, alpha = trail
        color = random.choice([(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)])
        circle = pyglet.shapes.Circle(x, height - y, radius, color=(*color, int(alpha)), segments=32)
        circle.draw()
        
        # Update trail
        trail[2] -= 1  # Shrink radius
        trail[3] -= 5  # Fade alpha
        if trail[2] <= 0 or trail[3] <= 0:
            trails.remove(trail)
    glDisable(GL_BLEND)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global mode
    if button == mouse.LEFT:
        mode = (mode + 1) % 4

@window.event
def on_mouse_motion(x, y, dx, dy):
    trails.append([x, y, 50, 200])  # [x, y, radius, alpha]

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()

# Schedule auto-close after 5 minutes (300 seconds)
def close_window(dt):
    window.close()
pyglet.clock.schedule_once(close_window, 300)

# Run the app
pyglet.app.run()