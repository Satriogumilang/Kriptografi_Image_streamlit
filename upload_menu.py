import streamlit as st
import os
import mysql.connector
from mysql.connector import Error
from PIL import Image
from streamlit_option_menu import option_menu


# Fungsi untuk mengunggah gambar ke database MySQL
def upload_image_to_mysql(image):
    try:
        # Menghubungkan ke database MySQL
        connection = mysql.connector.connect(
            host="localhost",
            database="db_krip",
            user="root",
            password="",
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Membaca gambar sebagai byte array
            img_byte_arr = image.read()

            # Mengirim perintah SQL untuk memasukkan gambar ke tabel
            sql_query = "INSERT INTO images (namafile, gambar) VALUES (%s, %s)"
            cursor.execute(sql_query, (image.name, img_byte_arr))
            connection.commit()

            st.success("Gambar berhasil diunggah ke database.")

    except Error as e:
        st.error(f"Terjadi kesalahan: {e}")

    finally:
        # Menutup koneksi database
        if connection.is_connected():
            cursor.close()
            connection.close()


with st.sidebar:
    selected = option_menu(
        "Sistem Keamanan Data",
        ["Import Data", "Enkripsi", "Dekripsi"],
        default_index=0,
    )

if selected == "Enkripsi":
    import encryption_menu

    encryption_menu.main()

if selected == "Dekripsi":
    import decryption_menu

    decryption_menu.main()

if selected == "Import Data":
    st.title("Unggah Gambar ke Database MySQL")

    # Membuat komponen input untuk memilih dan mengunggah gambar
    uploaded_file = st.file_uploader("Pilih gambar...", type=["png", "jpg", "jpeg"])

    # Menampilkan gambar yang diunggah jika ada
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)

    # Tombol untuk mengunggah gambar ke database
    if st.button("Unggah"):
        if uploaded_file is not None:
            upload_image_to_mysql(uploaded_file)
        else:
            st.warning("Silakan pilih gambar terlebih dahulu.")
