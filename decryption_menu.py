import streamlit as st
import mysql.connector
from mysql.connector import Error
from PIL import Image


def decrypt_image(image_id):
    try:
        # Menghubungkan ke database MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_krip",
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Mengambil data gambar dari tabel
            query = "SELECT image_path, pixels FROM images WHERE id = %s"
            cursor.execute(query, (image_id,))
            result = cursor.fetchone()
            image_path = result[0]
            pixel_str = result[1]

            # Mendecode string pixel menjadi list pixel
            pixels = [
                tuple(map(int, pixel.split(","))) for pixel in pixel_str.split(",")
            ]

            # Melakukan dekripsi Vigenere pada setiap pixel
            decrypted_pixels = []
            for pixel in pixels:
                decrypted_pixel = tuple(
                    (pixel[i] - ord(key[i % len(key)])) % 256 for i in range(3)
                )
                decrypted_pixels.append(decrypted_pixel)

            # Mengubah gambar ke bentuk PIL
            decrypted_image = Image.new(image.mode, image.size)
            decrypted_image.putdata(decrypted_pixels)

            # Menyimpan gambar hasil dekripsi ke penyimpanan lokal
            decrypted_image_path = (
                image_path.replace(".txt", ".jpg")
                .replace(".txt", ".jpeg")
                .replace(".txt", ".png")
            )
            decrypted_image.save(decrypted_image_path)

            st.success("Gambar berhasil dideskripsi dan disimpan.")

            connection.close()

    except Error as e:
        print("Error:", e)


def main():
    st.title("Dekripsi Gambar")
    image_id = st.number_input("Masukkan ID Gambar", step=1, min_value=1)
    if st.button("Dekripsi"):
        decrypt_image(image_id)


if __name__ == "__main__":
    main()
