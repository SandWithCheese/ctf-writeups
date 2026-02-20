import turtle as trtl
import math
import random

def ellipse_x(width, angle_rad):
    return width * math.cos(angle_rad)

def ellipse_y(height, angle_rad):
    return height * math.sin(angle_rad)

screen = trtl.Screen()
screen.bgcolor("#d3dae8")
screen.setup(900, 800)
screen.title("Happy Birthday Furina")
screen.tracer(2)  # Enable animation, but make it faster

pen = trtl.Turtle()
pen.pensize(3)
pen.speed("fastest")
pen.hideturtle()

color_palette = {
    "light_green": "#c5e8c8",
    "medium_green": "#a3d2a7",
    "light_yellow": "#f7e8aa",
    "cream": "#fffceb",
    "off_white": "#fffdf4",
    "brown": "#8b5a2b",
    "dark_brown": "#5e4425",
    "orange": "#ffa500",
    "golden_yellow": "#ffb732",
    "teal": "#66cccc",
    "flame_orange": "#ff6600",
    "sky_blue": "#87ceeb",
    "light_steel": "#b0c4de",
    "confetti_colors": ["#4CAF50", "#FFC107", "#2196F3", "#FF5722", "#9C27B0", "#3F51B5", "#00BCD4", "#009688"]
}

def draw_ellipse(t, width, height, color, fill_color, y_offset=0):
    t.penup()
    t.goto(width, y_offset)
    t.pendown()
    t.pencolor(color)
    t.fillcolor(fill_color)
    t.begin_fill()
    for deg in range(0, 360, 6):
        rad = math.radians(deg)
        x = ellipse_x(width, rad)
        y = ellipse_y(height, rad) + y_offset
        t.goto(x, y)
    t.end_fill()

def draw_cake_layer(t, width, height, outline_color, fill_color, y_offset):
    draw_ellipse(t, width, height, outline_color, fill_color, y_offset)

def draw_candle(t, x_pos, y_base, height):
    t.penup()
    t.goto(x_pos + 4, y_base)
    t.pendown()
    t.pencolor(color_palette["teal"])
    t.fillcolor(color_palette["teal"])
    t.begin_fill()
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        x = ellipse_x(4, rad) + x_pos
        y = ellipse_y(1, rad) + y_base
        t.goto(x, y)
    t.goto(x_pos + 4, y_base + height)
    for deg in range(0, 540, 10):
        rad = math.radians(deg)
        x = ellipse_x(4, rad) + x_pos
        y = ellipse_y(1, rad) + y_base + height
        t.goto(x, y)
    t.goto(x_pos - 4, y_base)
    t.end_fill()

    t.pencolor("white")
    t.pensize(2)
    for i in range(1, 6):
        t.penup()
        t.goto(x_pos + 4, y_base + 10 * i)
        t.pendown()
        t.goto(x_pos - 4, y_base + 10 * i)

    t.penup()
    t.goto(x_pos, y_base + height)
    t.pendown()
    t.goto(x_pos, y_base + height + 10)

    t.penup()
    t.goto(x_pos + 4, y_base + height + 20)
    t.pendown()
    t.pencolor(color_palette["flame_orange"])
    t.fillcolor(color_palette["flame_orange"])
    t.begin_fill()
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        x = ellipse_x(4, rad) + x_pos
        y = ellipse_y(10, rad) + y_base + height + 20
        t.goto(x, y)
    t.end_fill()

def add_dots(t, count, x_min, x_max, y_min, y_max, size_min, size_max):
    colors = color_palette["confetti_colors"]
    for _ in range(count):
        t.penup()
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        t.goto(x, y)
        t.pendown()
        t.dot(random.randint(size_min, size_max), random.choice(colors))

# Draw cake layers (minimal code change for clarity)
draw_cake_layer(pen, 150, 60, "white", color_palette["light_green"], 0)
draw_cake_layer(pen, 120, 48, "white", color_palette["light_yellow"], 70)
draw_cake_layer(pen, 110, 44, color_palette["cream"], color_palette["cream"], 70)
draw_cake_layer(pen, 80, 32, color_palette["dark_brown"], color_palette["dark_brown"], 120)
draw_cake_layer(pen, 70, 28, color_palette["orange"], color_palette["orange"], 120)

# Draw candles
candle_positions = [(60, 120, 50), (-60, 120, 50), (0, 130, 50), (30, 110, 50), (-30, 110, 50)]
for pos in candle_positions:
    draw_candle(pen, *pos)

# Add confetti
add_dots(pen, 80, -120, 120, -25, 30, 2, 5)
add_dots(pen, 40, -90, 90, -35, 10, 2, 5)
add_dots(pen, 40, -80, 80, 60, 90, 2, 5)
add_dots(pen, 30, -50, 50, 45, 70, 2, 5)
add_dots(pen, 50, -500, 500, 120, 300, 3, 5)

# Text
pen.seth(90)
pen.penup()
pen.goto(0, 210)
pen.left(90)
pen.forward(170)
pen.pendown()
pen.write("Happy Birthday", font=("Curlz MT", 50 , 'bold'))

trtl.done()
