import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import io
import os
import zipfile
import streamlit as st
from PIL import Image


# Fungsi untuk mengenkripsi teks menggunakan AES
def encrypt_text(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(encrypted_data).decode()


# Fungsi untuk mendekripsi teks menggunakan AES
def decrypt_text(encrypted_text, key):
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode()
    except ValueError:
        return None


# Judul dan deskripsi aplikasi Streamlit
st.title("AES Text Encryption and Decryption")

# Pilihan menu
menu = st.sidebar.selectbox("Menu", ["Encryption", "Decryption"])

# Menu Enkripsi
if menu == "Encryption":
    st.subheader("Encryption")
    input_file = st.file_uploader("Upload a zip file:", type="zip")
    key_str = st.text_input("Enter an AES key:")

    if st.button("Encrypt") and input_file is not None:
        # Ekstrak isi file zip
        with zipfile.ZipFile(input_file, "r") as zip_ref:
            zip_ref.extractall("input_files")

        # Konversi kunci menjadi bentuk yang sesuai
        key = base64.b64encode(key_str.encode())[:16]

        # Enkripsi setiap file dalam zip
        encrypted_texts = []
        for file_name in os.listdir("input_files"):
            file_path = os.path.join("input_files", file_name)
            with open(file_path, "r") as f:
                file_content = f.read()

            # Enkripsi teks menggunakan kunci AES
            encrypted_text = encrypt_text(file_content, key)
            encrypted_texts.append(encrypted_text)

        # Simpan setiap teks terenkripsi sebagai file txt
        os.makedirs("encrypted_texts", exist_ok=True)
        for i, encrypted_text in enumerate(encrypted_texts):
            file_name = f"encrypted_{i}.txt"
            file_path = os.path.join("encrypted_texts", file_name)
            with open(file_path, "w") as f:
                f.write(encrypted_text)

        st.write("Encryption completed. Encrypted texts saved as individual files.")

# Menu Dekripsi
elif menu == "Decryption":
    st.subheader("Decryption")
    input_file = st.file_uploader("Upload an encrypted text file:", type=["txt"])
    key_str = st.text_input("Enter an AES key:")

    if st.button("Decrypt") and input_file is not None:
        # Baca file teks terenkripsi
        encrypted_text = input_file.read().decode()

        # Konversi kunci menjadi bentuk yang sesuai
        key = base64.b64encode(key_str.encode())[:16]

        # Mendekripsi teks menggunakan kunci AES
        decrypted_texts = []
        decrypted_text = decrypt_text(encrypted_text, key)
        if decrypted_text is not None:
            decrypted_texts.append(decrypted_text)

        # Buat folder zip untuk menyimpan hasil dekripsi
        os.makedirs("decrypted_texts", exist_ok=True)
        output_zip = zipfile.ZipFile("decrypted_texts.zip", "w")

        # Simpan setiap teks terdekripsi dalam folder zip
        for i, decrypted_text in enumerate(decrypted_texts):
            file_name = f"decrypted_{i}.txt"
            file_path = os.path.join("decrypted_texts", file_name)
            with open(file_path, "w") as f:
                f.write(decrypted_text)
            output_zip.write(file_path, arcname=file_name)

        output_zip.close()

        st.write("Decryption completed. Decrypted texts saved as a zip file.")
