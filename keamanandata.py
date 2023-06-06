import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import streamlit as st


# Fungsi untuk mengenkripsi pesan menggunakan AES
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(encrypted_data).decode()


# Fungsi untuk mendekripsi pesan menggunakan AES
def decrypt_message(encrypted_message, key):
    encrypted_data = base64.b64decode(encrypted_message)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode()


# Judul dan deskripsi aplikasi Streamlit
st.title("AES Encryption and Decryption")
st.write("Enter a message and an AES key to encrypt and decrypt the message.")

# Mengambil inputan pesan dan kunci dari pengguna
message = st.text_input("Enter a message:")
key_str = st.text_input("Enter an AES key:")

# Mengenkripsi pesan jika tombol "Encrypt" ditekan
if st.button("Encrypt"):
    # Konversi kunci menjadi bentuk yang sesuai
    key = base64.b64encode(key_str.encode())[:16]

    # Enkripsi pesan menggunakan kunci AES
    encrypted_message = encrypt_message(message, key)
    st.write("Encrypted Message:", encrypted_message)

# Mendekripsi pesan jika tombol "Decrypt" ditekan
if st.button("Decrypt"):
    # Konversi kunci menjadi bentuk yang sesuai
    key = base64.b64encode(key_str.encode())[:16]

    # Mendekripsi pesan menggunakan kunci AES
    decrypted_message = decrypt_message(message, key)
    st.write("Decrypted Message:", decrypted_message)
