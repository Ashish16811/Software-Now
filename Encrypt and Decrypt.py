import os

def encrypt_text(text, n, m):
    encrypted_text = ""
    metadata = ""

    for char in text:
        if 'a' <= char <= 'm':  # Lowercase first half
            shift = (n * m) % 26
            new_code = (ord(char) - ord('a') + shift) % 26 + ord('a')
            encrypted_text += chr(new_code)
            metadata += "1"
        elif 'n' <= char <= 'z':  # Lowercase second half
            shift = (n + m) % 26
            new_code = (ord(char) - ord('a') - shift) % 26 + ord('a')
            encrypted_text += chr(new_code)
            metadata += "2"
        elif 'A' <= char <= 'M':  # Uppercase first half
            shift = n % 26
            new_code = (ord(char) - ord('A') - shift) % 26 + ord('A')
            encrypted_text += chr(new_code)
            metadata += "3"
        elif 'N' <= char <= 'Z':  # Uppercase second half
            shift = (m ** 2) % 26
            new_code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            encrypted_text += chr(new_code)
            metadata += "4"
        else:  # Special characters and numbers
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
    if original_text == decrypted_text:
        return True
    else:
        for i, (orig, decr) in enumerate(zip(original_text, decrypted_text)):
            if orig != decr:
                print(f"⚠️ First mismatch at position {i}: '{orig}' vs '{decr}'")
                break
        if len(original_text) != len(decrypted_text):
            print(f"⚠️ Length mismatch: original={len(original_text)}, decrypted={len(decrypted_text)}")
        return False

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

def main():
    try:
        print("🔐 Welcome to the Encryption-Decryption Program 🔐")
        
        filepath = input("📂 Enter the full path of the text file: ").strip()
        if not os.path.isfile(filepath):
            print("❌ Error: File not found.")
            return

        action = input("✨ Do you want to Encrypt or Decrypt? (E/D): ").strip().lower()
        if action not in ('e', 'd'):
            print("❗ Invalid choice. Please enter 'E' or 'D'.")
            return

        n = int(input("🔢 Enter the value of n: "))
        m = int(input("🔢 Enter the value of m: "))
        folder_path = os.path.dirname(filepath)

        if action == 'e':
            with open(filepath, "r", encoding="utf-8") as file:
                original_text = file.read()

            encrypted_text, metadata = encrypt_text(original_text, n, m)
            encrypted_file = save_file("encrypted_text", encrypted_text, folder_path)
            metadata_file = save_file("encryption_metadata", metadata, folder_path)

            print(f"✅ Encryption complete!\n📝 Encrypted file saved as: {encrypted_file}\n🗂️ Metadata saved as: {metadata_file}")

        elif action == 'd':
            with open(filepath, "r", encoding="utf-8") as file:
                encrypted_text = file.read()

            metadata_path = input("📂 Enter the path of the corresponding metadata file: ").strip()
            if not os.path.isfile(metadata_path):
                print("❌ Error: Metadata file not found.")
                return

            with open(metadata_path, "r", encoding="utf-8") as file:
                metadata = file.read()

            decrypted_text = decrypt_text(encrypted_text, metadata, n, m)
            decrypted_file = save_file("decrypted_text", decrypted_text, folder_path)

            print(f"✅ Decryption complete!\n📝 Decrypted file saved as: {decrypted_file}")

            original_path = input("📂 Enter the path to the original file for verification (optional): ").strip()
            if os.path.isfile(original_path):
                with open(original_path, "r", encoding="utf-8") as file:
                    original_text = file.read()
                if check_decryption(original_text, decrypted_text):
                    print("🎉 Decryption successful! Original and decrypted texts match.")
                else:
                    print("❗ Decryption failed: Original and decrypted texts do not match.")
            else:
                print("ℹ️ Skipped verification (original file not provided or found).")

    except ValueError:
        print("❗ Error: Please enter valid integers for n and m.")
    except Exception as e:
        print(f"❗ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
