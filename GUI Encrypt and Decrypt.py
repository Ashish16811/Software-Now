import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# --- Logic Functions ---
def encrypt_text(text, n, m):
    encrypted_text = ""
    metadata = ""
    for char in text:
        if 'a' <= char <= 'm':
            shift = (n * m) % 26
            encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            metadata += "1"
        elif 'n' <= char <= 'z':
            shift = (n + m) % 26
            encrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            metadata += "2"
        elif 'A' <= char <= 'M':
            shift = n % 26
            encrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            metadata += "3"
        elif 'N' <= char <= 'Z':
            shift = (m ** 2) % 26
            encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            metadata += "4"
        else:
            encrypted_text += char
            metadata += "0"
    return encrypted_text, metadata

def decrypt_text(encrypted_text, metadata, n, m):
    decrypted_text = ""
    for i, char in enumerate(encrypted_text):
        category = metadata[i]
        if category == "1":
            shift = (n * m) % 26
            decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        elif category == "2":
            shift = (n + m) % 26
            decrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif category == "3":
            shift = n % 26
            decrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif category == "4":
            shift = (m ** 2) % 26
            decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text

def check_decryption(original, decrypted):
    return original == decrypted

def save_file(name, content, folder):
    counter = 0
    while True:
        filename = f"{name}.txt" if counter == 0 else f"{name}{counter}.txt"
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return path
        counter += 1

def open_file(filepath):
    os.startfile(filepath)

# --- GUI Functions ---
def browse_file(entry_widget, title):
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Text Files", "*.txt")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def update_ui(event=None):
    clear_frames()
    view_frame.pack_forget()
    start_frame.pack_forget()

    selected_action = action_var.get()
    if selected_action == "Encrypt 🔒":
        frame_encrypt.pack(pady=20)
    elif selected_action == "Decrypt 🔓":
        frame_decrypt.pack(pady=20)
    elif selected_action == "Verify ✅":
        frame_verify.pack(pady=20)
    
    view_frame.pack(pady=15)
    start_frame.pack(pady=20)

def clear_frames():
    frame_encrypt.pack_forget()
    frame_decrypt.pack_forget()
    frame_verify.pack_forget()

def process_action():
    action = action_var.get()
    if action == "Select Action":
        messagebox.showerror("Error ❌", "Please select a valid action first.")
        return

    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
    except ValueError:
        messagebox.showerror("Error ❌", "Please enter valid integers for n and m.")
        return

    if action == "Encrypt 🔒":
        file_path = entry_encrypt_file.get().strip()
        if not os.path.isfile(file_path):
            messagebox.showerror("Error ❌", "Please select a valid text file!")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        encrypted_text, metadata = encrypt_text(text, n, m)
        folder = os.path.dirname(file_path)
        encrypted_path = save_file("encrypted_text", encrypted_text, folder)
        metadata_path = save_file("encryption_metadata", metadata, folder)
        messagebox.showinfo("Done ✅", "Encryption Completed!")
        show_view_buttons([encrypted_path, metadata_path])

    elif action == "Decrypt 🔓":
        encrypted_path = entry_decrypt_text.get().strip()
        metadata_path = entry_decrypt_metadata.get().strip()
        if not os.path.isfile(encrypted_path) or not os.path.isfile(metadata_path):
            messagebox.showerror("Error ❌", "Please select valid files!")
            return
        with open(encrypted_path, "r", encoding="utf-8") as f:
            encrypted_text = f.read()
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = f.read()
        decrypted_text = decrypt_text(encrypted_text, metadata, n, m)
        folder = os.path.dirname(encrypted_path)
        decrypted_path = save_file("decrypted_text", decrypted_text, folder)
        messagebox.showinfo("Done ✅", "Decryption Completed!")
        show_view_buttons([decrypted_path])

    elif action == "Verify ✅":
        original_path = entry_verify_original.get().strip()
        decrypted_path = entry_verify_decrypted.get().strip()
        if not os.path.isfile(original_path) or not os.path.isfile(decrypted_path):
            messagebox.showerror("Error ❌", "Please select valid files!")
            return
        with open(original_path, "r", encoding="utf-8") as f:
            original_text = f.read()
        with open(decrypted_path, "r", encoding="utf-8") as f:
            decrypted_text = f.read()
        if check_decryption(original_text, decrypted_text):
            messagebox.showinfo("Verification ✅", "Texts Match Successfully!")
        else:
            messagebox.showerror("Verification ❌", "Texts Do NOT Match!")

def show_view_buttons(filepaths):
    for widget in view_frame.winfo_children():
        widget.destroy()
    view_frame.pack(pady=15)
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        tk.Button(view_frame, text=f"📂 View {filename}", font=("Helvetica", 14, "bold"), bg="#34d399",
                  command=lambda path=filepath: open_file(path)).pack(pady=5)
    start_frame.pack(pady=20)

# --- GUI Setup ---
root = tk.Tk()
root.title("Encryptor & Decryptor App 🔐")
root.geometry("650x750")  # 🔥 made window smaller
root.configure(bg="#e0f2fe")

# Title
tk.Label(root, text="Encryptor & Decryptor 🔒", font=("Helvetica", 28, "bold"), bg="#e0f2fe").pack(pady=20)

# Action Dropdown
action_var = tk.StringVar(value="Select Action")  # 🔥 default text
action_menu = ttk.Combobox(root, textvariable=action_var, font=("Helvetica", 22), state="readonly",
                           values=["Encrypt 🔒", "Decrypt 🔓", "Verify ✅"], width=20, justify="center")
action_menu.pack(pady=20)
action_menu.bind("<<ComboboxSelected>>", update_ui)

# N and M Inputs
frame_nm = tk.Frame(root, bg="#e0f2fe")
frame_nm.pack(pady=15)
entry_n = tk.Entry(frame_nm, font=("Helvetica", 18), width=10, justify="center")
entry_n.grid(row=0, column=0, padx=10)
entry_n.insert(0, "n")
entry_m = tk.Entry(frame_nm, font=("Helvetica", 18), width=10, justify="center")
entry_m.grid(row=0, column=1, padx=10)
entry_m.insert(0, "m")

# Frames for each action
frame_encrypt = tk.Frame(root, bg="#e0f2fe")
entry_encrypt_file = tk.Entry(frame_encrypt, width=40, font=("Helvetica", 16), justify="center")
entry_encrypt_file.pack(pady=5)
tk.Button(frame_encrypt, text="📄 Browse Text File", font=("Helvetica", 14),
          command=lambda: browse_file(entry_encrypt_file, "Select Text File")).pack(pady=5)

frame_decrypt = tk.Frame(root, bg="#e0f2fe")
entry_decrypt_text = tk.Entry(frame_decrypt, width=40, font=("Helvetica", 16), justify="center")
entry_decrypt_text.pack(pady=5)
tk.Button(frame_decrypt, text="📄 Browse Encrypted File", font=("Helvetica", 14),
          command=lambda: browse_file(entry_decrypt_text, "Select Encrypted File")).pack(pady=5)
entry_decrypt_metadata = tk.Entry(frame_decrypt, width=40, font=("Helvetica", 16), justify="center")
entry_decrypt_metadata.pack(pady=5)
tk.Button(frame_decrypt, text="📜 Browse Metadata File", font=("Helvetica", 14),
          command=lambda: browse_file(entry_decrypt_metadata, "Select Metadata File")).pack(pady=5)

frame_verify = tk.Frame(root, bg="#e0f2fe")
entry_verify_original = tk.Entry(frame_verify, width=40, font=("Helvetica", 16), justify="center")
entry_verify_original.pack(pady=5)
tk.Button(frame_verify, text="📄 Browse Original Text", font=("Helvetica", 14),
          command=lambda: browse_file(entry_verify_original, "Select Original File")).pack(pady=5)
entry_verify_decrypted = tk.Entry(frame_verify, width=40, font=("Helvetica", 16), justify="center")
entry_verify_decrypted.pack(pady=5)
tk.Button(frame_verify, text="📜 Browse Decrypted Text", font=("Helvetica", 14),
          command=lambda: browse_file(entry_verify_decrypted, "Select Decrypted File")).pack(pady=5)

# View Buttons Frame
view_frame = tk.Frame(root, bg="#e0f2fe")

# Start Button Frame
start_frame = tk.Frame(root, bg="#e0f2fe")
start_button = tk.Button(start_frame, text="🚀 Start", font=("Helvetica", 20, "bold"), bg="#2563eb", fg="white",
                         command=process_action)
start_button.pack(pady=10)

root.mainloop()
