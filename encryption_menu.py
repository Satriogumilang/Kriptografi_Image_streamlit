import streamlit as st
import mysql.connector
from mysql.connector import Error
from PIL import Image


def encrypt_image(image_id, key):
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
            # Mengambil data gambar dari tabel images
            query = "SELECT image_path, pixels FROM images WHERE id = %s"
            cursor.execute(query, (image_id,))
            result = cursor.fetchone()
            image_path = result[0]
            pixel_str = result[1]

            # Mendecode string pixel menjadi list pixel
            pixels = [
                tuple(map(int, pixel.split(","))) for pixel in pixel_str.split(",")
            ]

            # Melakukan enkripsi Vigenere pada setiap pixel
            encrypted_pixels = []
            for pixel in pixels:
                encrypted_pixel = tuple(
                    (pixel[i] + ord(key[i % len(key)])) % 256 for i in range(3)
                )
                encrypted_pixels.append(encrypted_pixel)

            # Mengubah gambar ke bentuk PIL
            encrypted_image = Image.new(image.mode, image.size)
            encrypted_image.putdata(encrypted_pixels)

            # Menyimpan gambar hasil enkripsi ke database
            encrypted_image_path = (
                image_path.replace(".jpg", ".txt")
                .replace(".jpeg", ".txt")
                .replace(".png", ".txt")
            )
            encrypted_image.save(encrypted_image_path)

            # Menyimpan path file terenkripsi ke tabel encrypted_files
            insert_query = "INSERT INTO encrypted_files (image_id, encrypted_file_path) VALUES (%s, %s)"
            cursor.execute(insert_query, (image_id, encrypted_image_path))
            connection.commit()

            # Menampilkan gambar hasil enkripsi
            st.image(encrypted_image, caption="Gambar Hasil Enkripsi")

            connection.close()

    except Error as e:
        print("Error:", e)


def main():
    st.title("Enkripsi Gambar")
    image_id = st.number_input("Masukkan ID Gambar", step=1, min_value=1)
    key = st.text_input("Masukkan Key")
    if st.button("Enkripsi"):
        encrypt_image(image_id, key)


if __name__ == "__main__":
    main()
