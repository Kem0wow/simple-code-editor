import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, Menu, Button, simpledialog
import sys
import io
from PIL import ImageGrab
import keyword
import re

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
    if event.char in "({[\"'":
        match = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" }
        code_editor.insert(tk.INSERT, match[event.char])
        code_editor.mark_set("insert", f"{code_editor.index(tk.INSERT)}-1c")

def custom_input(prompt=""):
    return simpledialog.askstring("Input", prompt)

def run_code():
    code = code_editor.get("1.0", tk.END)
    old_stdout = sys.stdout
    old_input = __builtins__.input
    redirected_output = sys.stdout = io.StringIO()
    try:
        __builtins__.input = custom_input
        exec(code)
        output = redirected_output.getvalue()
    except Exception as e:
        output = str(e)
    finally:
        sys.stdout = old_stdout
        __builtins__.input = old_input
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
            highlight_keywords()

def new_file():
    if messagebox.askyesno("New File", "Do you want to save the current file?"):
        save_code()
    code_editor.delete("1.0", tk.END)

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def simple_bot(message):
    responses = {
        "hello": "Hi there! How can I help you?",
        "hi": "Hey! Need some help?",
        "how are you": "I'm just code, but thanks for asking!",
        "bye": "Goodbye! Have a nice day.",
        "code": "I'm here to help with your code!",
        "help": "Sure, just tell me what you're stuck on.",
        "no": "Yes!",
        "kai": "Yep, that's my name",
        "creator": "Kem0wow",
        "your name": "KAI"
    }
    
    message = message.lower()
    for key in responses:
        if key in message:
            return responses[key]
    return "I don't understand. Try asking something else."

def chatbot_response():
    chat_window = tk.Toplevel(root)
    chat_window.title("Chatbot - KAI")
    chat_window.geometry("400x500")

    chat_display = tk.Text(chat_window, state="disabled", wrap="word", font=("Arial", 11))
    chat_display.pack(expand=True, fill="both", padx=10, pady=10)

    entry_field = tk.Entry(chat_window, font=("Arial", 11))
    entry_field.pack(fill="x", padx=10, pady=(0,10))

    def send_message(event=None):
        user_msg = entry_field.get()
        if user_msg.strip() == "":
            return
        entry_field.delete(0, tk.END)
        bot_reply = simple_bot(user_msg)

        chat_display.config(state="normal")
        chat_display.insert(tk.END, f"You: {user_msg}\n", "user")
        chat_display.insert(tk.END, f"KAI: {bot_reply}\n\n", "bot")
        chat_display.config(state="disabled")
        chat_display.see(tk.END)

    entry_field.bind("<Return>", send_message)

    # Tag renkleri
    chat_display.tag_config("user", foreground="blue")
    chat_display.tag_config("bot", foreground="green")

def zoom():
    global size
    size += 1
    code_editor.config(font=("Consolas", 12 + size))

def unzoom():
    global size
    if size > -10:
        size -= 1
        code_editor.config(font=("Consolas", 12 + size))

def highlight_keywords(event=None):
    code = code_editor.get("1.0", tk.END)
    code_editor.tag_remove("keyword", "1.0", tk.END)
    code_editor.tag_remove("builtin", "1.0", tk.END)
    code_editor.tag_remove("string", "1.0", tk.END)
    code_editor.tag_remove("comment", "1.0", tk.END)

    for kw in keyword.kwlist:
        start = "1.0"
        while True:
            start = code_editor.search(rf'\b{kw}\b', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(kw)}c"
            code_editor.tag_add("keyword", start, end)
            start = end

    for const in ['True', 'False', 'None']:
        start = "1.0"
        while True:
            start = code_editor.search(rf'\b{const}\b', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(const)}c"
            code_editor.tag_add("builtin", start, end)
            start = end

    matches = re.finditer(r'(\'[^\']*\'|"[^"]*")', code)
    for match in matches:
        start = f"1.0 + {match.start()}c"
        end = f"1.0 + {match.end()}c"
        code_editor.tag_add("string", start, end)

    start = "1.0"
    while True:
        start = code_editor.search("#", start, stopindex=tk.END)
        if not start:
            break
        end = code_editor.index(f"{start} lineend")
        code_editor.tag_add("comment", start, end)
        start = end

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
code_editor.bind("<KeyRelease>", highlight_keywords)

code_editor.tag_config("keyword", foreground="#ce42f5")
code_editor.tag_config("builtin", foreground="#091bbd")
code_editor.tag_config("string", foreground="#bf5d1b")
code_editor.tag_config("comment", foreground="#228B22")

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Run", command=run_code, bg="#5cb85c", fg="white", font=("Arial", 11, "bold")).pack()
tk.Button(button_frame, text="Zoom", command=zoom, bg="gray", fg="white", font=("Arial", 11, "bold")).pack()
tk.Button(button_frame, text="Unzoom", command=unzoom, bg="gray", fg="white", font=("Arial", 11, "bold")).pack()
tk.Button(button_frame, text="Screenshot", command=take_screenshot, bg="#0275d8", fg="white").pack()

output_console = scrolledtext.ScrolledText(root, height=10, bg="black", fg="light green", font=("Consolas", 13), state="disabled")
output_console.pack(fill="both", expand=True, padx=10, pady=(5, 10))

root.mainloop()