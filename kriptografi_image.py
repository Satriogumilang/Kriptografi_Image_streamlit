import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import io
import streamlit as st
from PIL import Image
import os


# Fungsi untuk mengenkripsi gambar menggunakan AES
def encrypt_image(image, key):
    # Mengubah gambar menjadi byte stream
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(img_byte_arr, AES.block_size))
    return base64.b64encode(encrypted_data).decode()


# Fungsi untuk mendekripsi gambar menggunakan AES
def decrypt_image(encrypted_text, key):
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        img_byte_arr = io.BytesIO(decrypted_data)
        return Image.open(img_byte_arr)
    except ValueError:
        return None


# Judul dan deskripsi aplikasi Streamlit
st.title("Enkripsi dan Dekripsi Gambar menggunakan AES")

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

            # Enkripsi gambar menggunakan kunci AES
            encrypted_text = encrypt_image(image, key)

            st.image(image, caption="Gambar Asli", use_column_width=True)

            # Simpan hasil enkripsi ke file dengan nama unik
            output_folder = "enkripsi"
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, f"encrypted_{key_str}.txt")
            with open(file_path, "w") as f:
                f.write(encrypted_text)

            st.write("Status Enkripsi:")
            st.success("Teks terenkripsi berhasil disimpan, di Folder enkripsi")
        except ValueError:
            st.write("Status Enkripsi:")
            st.error("Kunci AES Tidak Valid")

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

        # Mendekripsi gambar menggunakan kunci AES
        decrypted_image = decrypt_image(encrypted_text, key)

        if decrypted_image is not None:
            # Simpan hasil dekripsi ke file dengan nama unik
            output_folder = "dekripsi"
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, f"decrypted_{key_str}.jpg")

            # Konversi gambar ke mode RGB sebelum menyimpannya
            decrypted_image = decrypted_image.convert("RGB")
            decrypted_image.save(file_path, "JPEG")

            st.image(
                decrypted_image, caption="Gambar Terdekripsi", use_column_width=True
            )
            st.write("Status Enkripsi:")
            st.success("Gambar terdekripsi berhasil disimpan!")
        else:
            st.write("Status Enkripsi:")
            st.error("Kunci AES atau teks terenkripsi tidak valid.")

    elif decrypt_button:
        st.write("Status Enkripsi:")
        st.error("Silakan unggah sebuah file teks terenkripsi.")
