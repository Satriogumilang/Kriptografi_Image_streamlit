import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import io
import streamlit as st
from PIL import Image
import os
import mysql.connector

# Membuat koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="db_kriptografi"
)

# Membuat cursor
cursor = db.cursor()


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
    except (ValueError, IndexError, TypeError) as e:
        print(f"Error during decryption: {e}")
        return None


# Fungsi untuk mengunggah gambar ke database
def upload_image_to_db(file_name, image_data):
    sql = "INSERT INTO upload_images (file_name, image_data) VALUES (%s, %s)"
    values = (file_name, image_data)
    cursor.execute(sql, values)
    db.commit()
    st.success("Gambar berhasil diunggah ke database.")


# Judul dan deskripsi aplikasi Streamlit
st.title("Enkripsi dan Dekripsi Gambar menggunakan AES")

# Pilihan menu
menu = st.sidebar.selectbox("Menu", ["Upload Gambar", "Enkripsi", "Dekripsi"])

# Menu upload
if menu == "Upload Gambar":
    # Judul dan deskripsi aplikasi Streamlit
    st.subheader("Upload Gambar ke Database MySQL")

    # Upload gambar
    uploaded_image = st.file_uploader("Unggah gambar:", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Baca data gambar
        image_data = uploaded_image.read()

        # Tampilkan gambar
        st.image(uploaded_image, caption="Gambar yang diunggah", use_column_width=True)

        # Tombol untuk mengunggah gambar ke database
        upload_button = st.button("Upload Gambar")

        if upload_button:
            # Ambil nama file dari objek uploaded_image
            file_name = uploaded_image.name

            # Panggil fungsi untuk mengunggah gambar ke database
            upload_image_to_db(file_name, image_data)

# Menu Enkripsi
if menu == "Enkripsi":
    st.subheader("Enkripsi")

    # Ambil data teks terenkripsi dari database
    cursor.execute("SELECT file_name FROM upload_images")
    file_names = cursor.fetchall()

    selected_image = st.selectbox(
        "Gambar dari database:", [file[0] for file in file_names]
    )

    cursor.execute(
        "SELECT image_data FROM upload_images WHERE file_name = %s", (selected_image,)
    )
    image_data = cursor.fetchone()[0]

    image = Image.open(io.BytesIO(image_data))
    st.image(image, caption="Gambar Terpilih", use_column_width=True)

    # uploaded_image = st.file_uploader("Unggah gambar:", type=["jpg", "jpeg", "png"])
    key_str = st.text_input("Masukkan kunci AES:")
    encrypt_button = st.button("Enkripsi")

    if encrypt_button and image is not None:
        try:
            # Konversi kunci menjadi bentuk yang sesuai
            key = base64.b64encode(key_str.encode())[:16]

            # Konversi gambar ke mode RGB
            image_rgb = image.convert("RGB")

            # Enkripsi gambar menggunakan kunci AES
            encrypted_text = encrypt_image(image_rgb, key)

            # Simpan hasil enkripsi ke file dengan nama unik
            output_folder = "enkripsi"
            os.makedirs(output_folder, exist_ok=True)
            file_name = f"encrypted_{key_str}.txt"
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, "w") as f:
                f.write(encrypted_text)

            # Simpan hasil enkripsi ke database
            sql = "INSERT INTO encrypted_files (file_name, encrypted_text) VALUES (%s, %s)"
            values = (file_name, encrypted_text)
            cursor.execute(sql, values)
            db.commit()

            st.write("Status Enkripsi:")
            st.success("Teks terenkripsi berhasil disimpan di folder enkripsi.")
        except ValueError:
            st.write("Status Enkripsi:")
            st.error("Kunci AES Tidak Valid")

    elif encrypt_button:
        st.write("Status Enkripsi:")
        st.error("Silakan pilih sebuah gambar dari database.")


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
            decrypted_image = decrypted_image.convert("RGB")

            st.image(
                decrypted_image, caption="Gambar Terdekripsi", use_column_width=True
            )

            st.write("Status Dekripsi:")
            st.success("Gambar terdekripsi berhasil didekripsi")

            # Mengubah gambar menjadi byte stream
            image_bytes = io.BytesIO()
            decrypted_image.save(image_bytes, format="PNG")
            image_bytes = image_bytes.getvalue()

            # Menghasilkan tautan unduh
            b64_image = base64.b64encode(image_bytes).decode()
            href = f'<a href="data:image/png;base64,{b64_image}" download="decrypted_image.png">Unduh Gambar Terdekripsi</a>'
            st.markdown(href, unsafe_allow_html=True)

        else:
            st.write("Status Enkripsi:")
            st.error("Kunci AES atau teks terenkripsi tidak valid.")

    elif decrypt_button:
        st.write("Status Enkripsi:")
        st.error("Silakan unggah sebuah file teks terenkripsi.")


# Menutup koneksi ke database
db.close()
