import streamlit as st
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io
import numpy as np


# Fungsi untuk mengenkripsi gambar menggunakan AES dengan pengacakan piksel
def encrypt_image(image, key):
    # Konversi gambar ke array numpy
    img_array = np.array(image)

    # Mengacak urutan piksel
    np.random.shuffle(img_array.reshape(-1))

    # Konversi array kembali menjadi gambar
    encrypted_image = Image.fromarray(img_array)

    # Mengubah gambar menjadi byte stream
    img_byte_arr = io.BytesIO()
    encrypted_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(img_byte_arr, AES.block_size))
    return base64.b64encode(encrypted_data).decode()


# Fungsi untuk mendekripsi gambar menggunakan AES dengan pengacakan piksel
def decrypt_image(encrypted_text, key):
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # Konversi data terdekripsi menjadi array piksel
        img_array = np.frombuffer(decrypted_data, dtype=np.uint8)

        # Mengembalikan urutan piksel yang teracak menjadi urutan semula
        np.random.shuffle(img_array.reshape(-1))

        # Konversi array menjadi gambar
        decrypted_image = Image.fromarray(img_array.reshape(image.size))

        return decrypted_image
    except ValueError:
        return None


# Judul dan deskripsi aplikasi Streamlit
st.title("Enkripsi dan Dekripsi Gambar dengan Pengacakan Piksel menggunakan AES")

# Pilihan menu
menu = st.sidebar.selectbox("Menu", ["Enkripsi", "Dekripsi"])

# Menu Enkripsi
if menu == "Enkripsi":
    st.subheader("Enkripsi")
    uploaded_image = st.file_uploader("Unggah gambar:", type=["jpg", "jpeg", "png"])
    key_str = st.text_input("Masukkan kunci AES:")
    encrypt_button = st.button("Enkripsi")

    if encrypt_button and uploaded_image is not None:
        try:
            # Konversi kunci menjadi bentuk yang sesuai
            key = base64.b64encode(key_str.encode())[:16]

            # Baca dan muat gambar
            image = Image.open(uploaded_image)

            # Konversi gambar ke mode RGB
            image = image.convert("RGB")

            # Enkripsi gambar menggunakan kunci AES dengan pengacakan piksel
            encrypted_text = encrypt_image(image, key)

            # Simpan hasil enkripsi ke database atau tempat penyimpanan lainnya
            # ...

            st.image(image, caption="Gambar Asli", use_column_width=True)
            st.write("Status Enkripsi:")
            st.success("Gambar terenkripsi berhasil disimpan.")
        except ValueError:
            st.write("Status Enkripsi:")
            st.error("Kunci AES tidak valid.")

    elif encrypt_button:
        st.write("Status Enkripsi:")
        st.error("Silakan unggah sebuah gambar.")


# Menu Dekripsi
elif menu == "Dekripsi":
    st.subheader("Dekripsi")
    encrypted_file = st.file_uploader("Unggah file teks terenkripsi:", type=["txt"])
    key_str = st.text_input("Masukkan kunci AES:")
    decrypt_button = st.button("Dekripsi")

    if decrypt_button and encrypted_file is not None:
        # Baca file teks terenkripsi
        encrypted_text = encrypted_file.read().decode()

        # Konversi kunci menjadi bentuk yang sesuai
        key = base64.b64encode(key_str.encode())[:16]

        # Mendekripsi gambar menggunakan kunci AES dengan pengacakan piksel
        decrypted_image = decrypt_image(encrypted_text, key)

        if decrypted_image is not None:
            # Simpan hasil dekripsi ke file atau tampilkan di Streamlit
            # ...

            st.image(
                decrypted_image, caption="Gambar Terdekripsi", use_column_width=True
            )
            st.write("Status Enkripsi:")
            st.success("Gambar terdekripsi berhasil ditampilkan.")
        else:
            st.write("Status Enkripsi:")
            st.error("Kunci AES atau teks terenkripsi tidak valid.")

    elif decrypt_button:
        st.write("Status Enkripsi:")
        st.error("Silakan unggah sebuah file teks terenkripsi.")
