import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, Menu, Button
import sys
import io
from PIL import ImageGrab

size = 0

def take_screenshot():
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    x1 = x + root.winfo_width()
    y1 = y + root.winfo_height()

    img = ImageGrab.grab(bbox=(x, y, x1, y1))
    img.save("screenshot.png")
    print("Screenshot saved as screenshot.png")

def on_keypress(event):
    text = code_editor.get("1.0", tk.END)
    
    if event.char == '(':
        code_editor.insert(tk.INSERT, ')')
        code_editor.mark_set("insert", f"{code_editor.index(tk.INSERT)}-1c")

    elif event.char == '"':
        code_editor.insert(tk.INSERT, '"')
        code_editor.mark_set("insert", f"{code_editor.index(tk.INSERT)}-1c")
    
    elif event.char == "'":
        code_editor.insert(tk.INSERT, "'")
        code_editor.mark_set("insert", f"{code_editor.index(tk.INSERT)}-1c")

def run_code():
    code = code_editor.get("1.0", tk.END)
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    try:
        exec(code)
        output = redirected_output.getvalue()
    except Exception as e:
        output = str(e)
    finally:
        sys.stdout = old_stdout

    output_console.config(state="normal")
    output_console.delete("1.0", tk.END)
    output_console.insert(tk.END, output)
    output_console.config(state="disabled")

def save_code():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    
    if file_path:
        code = code_editor.get("1.0", tk.END)
        with open(file_path, "w") as file:
            file.write(code)

def open_code():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            code_editor.delete("1.0", tk.END)
            code_editor.insert(tk.END, code)

def new_file():
    if messagebox.askyesno("New File", "Do you want to save the current file?"):
        save_code()
    code_editor.delete("1.0", tk.END)

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def chatbot_response():
    messagebox.showinfo("Chatbot", "This is where chatbot will be added.")

def zoom():
    global size
    size += 1
    code_editor.config(font=("Consolas", 12 + size))

def unzoom():
    global size
    if size > -10:
        size -= 1
        code_editor.config(font=("Consolas", 12 + size))

root = tk.Tk()
root.title("Python Code Editor")
root.state("zoomed")
root.minsize(800, 600)

menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_code)
file_menu.add_command(label="Save", command=save_code)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

chat_menu = Menu(menu_bar, tearoff=0)
chat_menu.add_command(label="Talk", command=chatbot_response)
menu_bar.add_cascade(label="Chatbot", menu=chat_menu)

root.config(menu=menu_bar)

code_editor = scrolledtext.ScrolledText(root, height=20, font=("Consolas", 12+size))
code_editor.pack(fill="both", expand=True, padx=10, pady=(10, 5))
code_editor.bind("<Key>", on_keypress)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

run_button = tk.Button(button_frame, text="Run", command=run_code, bg="#5cb85c", fg="white", font=("Arial", 11, "bold"))
run_button.pack()

zoom_button = tk.Button(button_frame, text="Zoom", command=zoom, bg="gray", fg="white", font=("Arial", 11, "bold"))
zoom_button.pack()

unzoom_button = tk.Button(button_frame, text="Unzoom", command=unzoom, bg="gray", fg="white", font=("Arial", 11, "bold"))
unzoom_button.pack()

screenshot_button = tk.Button(button_frame, text="Screenshot", command=take_screenshot, bg="#0275d8", fg="white")
screenshot_button.pack()

output_console = scrolledtext.ScrolledText(root, height=10, bg="black", fg="light green", font=("Consolas", 13), state="disabled")
output_console.pack(fill="both", expand=True, padx=10, pady=(5, 10))

root.mainloop()