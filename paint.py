import tkinter as tk
from PIL import ImageTk, Image, ImageGrab

from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.colorchooser import askcolor

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'
old_x = None
old_y = None
line_width = DEFAULT_PEN_SIZE
color = DEFAULT_COLOR
eraser_on = False
active_button = False


def setup(canvas, size_button):
    global old_x, old_y, line_width, color, eraser_on, active_button
    old_x = None
    old_y = None
    line_width = size_button.get()
    color = DEFAULT_COLOR
    eraser_on = False
    active_button = False
    active_button = pen_button
    canvas.bind('<B1-Motion>', paint)
    canvas.bind('<ButtonRelease-1>', reset)


def use_pen():
    activate_button(pen_button)


def use_brush():
    activate_button(brush_button)


def choose_color():
    global color, eraser_on
    eraser_on = False
    color = askcolor(color=color)[1]


def use_eraser():
    activate_button(eraser_button, eraser_mode=True)


def activate_button(some_button, eraser_mode=False):
    global active_button, eraser_on
    active_button.config(relief=tk.RAISED)
    some_button.config(relief=tk.SUNKEN)
    active_button, eraser_on = some_button, eraser_mode


def paint(event):
    global old_x, old_y, line_width, color, eraser_on
    line_width = choose_size_button.get()
    paint_color = 'white' if eraser_on else color
    if old_x and old_y:
        canvas.create_line(old_x, old_y, event.x, event.y, width=line_width, fill=paint_color,
                           capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
    old_x, old_y = event.x, event.y


def reset(event):
    global old_x, old_y
    old_x, old_y = None, None


def save_canvas():
    filename = asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('All files', '*.*')])
    if filename:
        # Grab the canvas area and save it as an image
        x = window.winfo_windowx() + canvas.winfo_x()
        y = window.winfo_windowy() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(filename)


def open_image():
    filename = askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg'), ('All files', '*.*')])
    if filename:
        img = Image.open(filename)
        img = img.resize((canvas.winfo_width(), canvas.winfo_height()))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk  # Keep a reference to avoid garbage collection


def exit_app():
    window.quit()


window = tk.Tk()
window.title('Paint')
window.geometry('500x300')
window.maxsize(500, 300)
window.minsize(500, 300)

menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Save", command=save_canvas)
file_menu.add_command(label="Open", command=open_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
window.config(menu=menu_bar)

paint_tools = tk.Frame(window, width=100, height=300, relief=tk.RIDGE, borderwidth=2)
paint_tools.place(x=0, y=0)

pen_logo = ImageTk.PhotoImage(Image.open('pen.png'))
pen_button = tk.Button(paint_tools, padx=6, image=pen_logo, borderwidth=2, command=use_pen)
pen_button.place(x=60, y=10)

brush_logo = ImageTk.PhotoImage(Image.open('brush.png'))
brush_button = tk.Button(paint_tools, image=brush_logo, borderwidth=2, command=use_brush)
brush_button.place(x=60, y=40)

color_logo = ImageTk.PhotoImage(Image.open('color.png'))
color_button = tk.Button(paint_tools, image=color_logo, borderwidth=2, command=choose_color)
color_button.place(x=60, y=70)

eraser_logo = ImageTk.PhotoImage(Image.open('eraser.png'))
eraser_button = tk.Button(paint_tools, image=eraser_logo, borderwidth=2, command=use_eraser)
eraser_button.place(x=60, y=100)

pen_size_label = tk.Label(paint_tools, text="Pen Size", font=('verdana', 10, 'bold'))
pen_size_label.place(x=15, y=250)
choose_size_button = tk.Scale(paint_tools, from_=1, to=10, orient=tk.VERTICAL)
choose_size_button.place(x=20, y=150)

canvas = tk.Canvas(window, bg='white', width=600, height=600, relief=tk.RIDGE, borderwidth=0)
canvas.place(x=100, y=0)

setup(canvas, choose_size_button)
window.mainloop()
