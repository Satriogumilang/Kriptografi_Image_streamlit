# Enkripsi dan Dekripsi Gambar menggunakan AES

Ini adalah aplikasi sederhana untuk mengenkripsi dan mendekripsi gambar menggunakan metode AES (Advanced Encryption Standard). Aplikasi ini juga memungkinkan pengguna untuk mengunggah gambar ke database MySQL, mengenkripsi gambar dari database, dan mendekripsi gambar dari file teks terenkripsi.

## Instalasi

Untuk menjalankan aplikasi ini, ikuti langkah-langkah berikut:

1. Pastikan Python telah terinstal di sistem Anda. Versi Python yang direkomendasikan adalah Python 3.7 atau yang lebih baru.
2. Clone repositori ini atau unduh dan ekstrak arsip ZIP.
3. Buka terminal atau command prompt dan masuk ke direktori proyek.
4. Instal dependensi yang diperlukan dengan menjalankan perintah berikut:

pip install -r requirements.txt


## Menjalankan Aplikasi

Setelah menginstal dependensi, Anda dapat menjalankan aplikasi dengan perintah berikut:


Ini akan menjalankan aplikasi Streamlit dan membuka aplikasi di browser Anda.

## Menggunakan Aplikasi

Aplikasi ini memiliki tiga menu utama: "Upload Gambar", "Enkripsi", dan "Dekripsi".

### 1. Upload Gambar

Menu ini memungkinkan Anda mengunggah gambar ke database MySQL.

1. Pilih menu "Upload Gambar" pada sidebar.
2. Klik tombol "Unggah gambar" dan pilih gambar yang ingin Anda unggah.
3. Gambar yang diunggah akan ditampilkan di aplikasi.
4. Klik tombol "Upload Gambar" untuk mengunggah gambar ke database.

### 2. Enkripsi

Menu ini memungkinkan Anda mengenkripsi gambar yang telah diunggah ke database.

1. Pilih menu "Enkripsi" pada sidebar.
2. Pilih gambar yang ingin Anda enkripsi dari dropdown "Gambar dari database".
3. Masukkan kunci AES yang akan digunakan untuk enkripsi.
4. Klik tombol "Enkripsi" untuk memulai proses enkripsi.
5. Gambar terenkripsi akan disimpan dalam folder "enkripsi" dengan nama file unik.
6. Status enkripsi akan ditampilkan di aplikasi.

### 3. Dekripsi

Menu ini memungkinkan Anda mendekripsi gambar dari file teks terenkripsi.

1. Pilih menu "Dekripsi" pada sidebar.
2. Unggah file teks terenkripsi dengan memilih tombol "Unggah file teks terenkripsi".
3. Masukkan kunci AES yang digunakan saat enkripsi.
4. Klik tombol "Dekripsi" untuk memulai proses dekripsi.
5. Gambar terdekripsi akan ditampilkan di aplikasi.
6. Status dekripsi akan ditampilkan di aplikasi.
7. Anda dapat mengunduh gambar terdekripsi dengan mengklik tautan "Unduh Gambar Terdekripsi".

## Catatan

- Pastikan Anda memiliki MySQL server yang berjalan dan mengubah pengaturan host, pengguna, kata sandi, dan database sesuai dengan konfigurasi Anda di kode.
- Aplikasi ini hanya mendukung format gambar JPEG (jpg), JPEG (jpeg), dan PNG (png).
- Pastikan Anda memberikan kunci AES yang valid saat melakukan enkripsi dan dekripsi.

Terima kasih telah menggunakan aplikasi ini! Jika Anda memiliki pertanyaan atau masalah, jangan ragu untuk menghubungi saya.


