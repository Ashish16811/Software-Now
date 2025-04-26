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
            new_code = (ord(char) - ord('a') + shift) % 26 + ord('a')
            encrypted_text += chr(new_code)
            metadata += "1"
        elif 'n' <= char <= 'z':
            shift = (n + m) % 26
            new_code = (ord(char) - ord('a') - shift) % 26 + ord('a')
            encrypted_text += chr(new_code)
            metadata += "2"
        elif 'A' <= char <= 'M':
            shift = n % 26
            new_code = (ord(char) - ord('A') - shift) % 26 + ord('A')
            encrypted_text += chr(new_code)
            metadata += "3"
        elif 'N' <= char <= 'Z':
            shift = (m ** 2) % 26
            new_code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            encrypted_text += chr(new_code)
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
            original_code = (ord(char) - ord('a') - shift) % 26 + ord('a')
            decrypted_text += chr(original_code)
        elif category == "2":
            shift = (n + m) % 26
            original_code = (ord(char) - ord('a') + shift) % 26 + ord('a')
            decrypted_text += chr(original_code)
        elif category == "3":
            shift = n % 26
            original_code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            decrypted_text += chr(original_code)
        elif category == "4":
            shift = (m ** 2) % 26
            original_code = (ord(char) - ord('A') - shift) % 26 + ord('A')
            decrypted_text += chr(original_code)
        else:
            decrypted_text += char
    return decrypted_text

def check_decryption(original_text, decrypted_text):
    return original_text == decrypted_text

def save_file(base_name, content, folder_path):
    counter = 0
    while True:
        filename = f"{base_name}.txt" if counter == 0 else f"{base_name}{counter}.txt"
        full_path = os.path.join(folder_path, filename)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return full_path
        counter += 1

# --- UI Functions ---
def ask_file(entry_widget, title):
    filepath = filedialog.askopenfilename(title=title, filetypes=[("Text Files", "*.txt")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filepath)

def update_ui(event=None):
    file_frame.pack_forget()
    metadata_frame.pack_forget()
    verify_frame.pack_forget()
    entry_file.delete(0, tk.END)
    entry_metadata.delete(0, tk.END)
    entry_original.delete(0, tk.END)

    if action_var.get() == "Encrypt":
        file_frame.pack(pady=10)
    elif action_var.get() == "Decrypt":
        file_frame.pack(pady=10)
        metadata_frame.pack(pady=10)
    elif action_var.get() == "Verify Decryption":
        file_frame.pack(pady=10)
        verify_frame.pack(pady=10)

def process_action():
    action = action_var.get()
    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for n and m.")
        return

    filepath = entry_file.get().strip()
    if not os.path.isfile(filepath):
        messagebox.showerror("Error", "Please select a valid file!")
        return

    folder_path = os.path.dirname(filepath)

    if action == "Encrypt":
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
        encrypted_text, metadata = encrypt_text(text, n, m)
        save_file("encrypted_text", encrypted_text, folder_path)
        save_file("encryption_metadata", metadata, folder_path)
        messagebox.showinfo("Success", "✅ Encryption completed!")

    elif action == "Decrypt":
        metadata_path = entry_metadata.get().strip()
        if not os.path.isfile(metadata_path):
            messagebox.showerror("Error", "Please select a valid metadata file!")
            return
        with open(filepath, "r", encoding="utf-8") as file:
            encrypted_text = file.read()
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = file.read()
        decrypted_text = decrypt_text(encrypted_text, metadata, n, m)
        save_file("decrypted_text", decrypted_text, folder_path)
        messagebox.showinfo("Success", "✅ Decryption completed!")

    elif action == "Verify Decryption":
        original_path = entry_original.get().strip()
        if not os.path.isfile(original_path):
            messagebox.showerror("Error", "Please select a valid original file!")
            return
        with open(filepath, "r", encoding="utf-8") as file:
            decrypted_text = file.read()
        with open(original_path, "r", encoding="utf-8") as file:
            original_text = file.read()
        if check_decryption(original_text, decrypted_text):
            messagebox.showinfo("Verification", "✅ Verification successful: Texts match!")
        else:
            messagebox.showerror("Verification", "❌ Verification failed: Texts do not match.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Encryptor and Decryptor 🔐")
root.geometry("650x600")
root.configure(bg="#dbeafe")

label_title = tk.Label(root, text="Encryptor and Decryptor 🔒", font=("Helvetica", 26, "bold"), bg="#dbeafe")
label_title.pack(pady=20)

action_var = tk.StringVar(value="Select Action")
action_menu = ttk.Combobox(root, textvariable=action_var, values=["Encrypt", "Decrypt", "Verify Decryption"], font=("Helvetica", 14), state="readonly")
action_menu.pack(pady=10)
action_menu.bind("<<ComboboxSelected>>", update_ui)

frame_nm = tk.Frame(root, bg="#dbeafe")
frame_nm.pack(pady=10)
entry_n = tk.Entry(frame_nm, width=15, font=("Helvetica", 14))
entry_n.grid(row=0, column=0, padx=10)
entry_n.insert(0, "n")
entry_m = tk.Entry(frame_nm, width=15, font=("Helvetica", 14))
entry_m.grid(row=0, column=1, padx=10)
entry_m.insert(0, "m")

file_frame = tk.Frame(root, bg="#dbeafe")
entry_file = tk.Entry(file_frame, width=40, font=("Helvetica", 12))
entry_file.pack(side="left", padx=5)
tk.Button(file_frame, text="Browse File", command=lambda: ask_file(entry_file, "Select File"), font=("Helvetica", 11)).pack(side="left", padx=5)

metadata_frame = tk.Frame(root, bg="#dbeafe")
entry_metadata = tk.Entry(metadata_frame, width=35, font=("Helvetica", 12))
entry_metadata.pack(side="left", padx=5)
tk.Button(metadata_frame, text="Browse Metadata", command=lambda: ask_file(entry_metadata, "Select Metadata File"), font=("Helvetica", 11)).pack(side="left", padx=5)

verify_frame = tk.Frame(root, bg="#dbeafe")
entry_original = tk.Entry(verify_frame, width=35, font=("Helvetica", 12))
entry_original.pack(side="left", padx=5)
tk.Button(verify_frame, text="Browse Original", command=lambda: ask_file(entry_original, "Select Original File"), font=("Helvetica", 11)).pack(side="left", padx=5)

btn_start = tk.Button(root, text="🚀 Start", command=process_action, font=("Helvetica", 16, "bold"), bg="#2563eb", fg="white", padx=25, pady=10)
btn_start.pack(side="bottom", pady=30)

root.mainloop()
