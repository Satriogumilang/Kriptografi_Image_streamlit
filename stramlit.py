import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_drawable_canvas import st_canvas
import zipfile
from zipfile import ZipFile
import io
import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import os
import PIL
import cv2
import imageio
from PIL import Image, ImageFilter
import shutil
import random

# Fungsi untuk membangun model CNN
# navbar
with st.sidebar:
    selected = option_menu(
        "Membangun Model CNN",
        ["Preprocessing", "Pengujian Model", "Klasifikasi Tulisan Tangan"],
        default_index=0,
    )

if selected == "Preprocessing":
    # Judul dan deskripsi aplikasi Streamlit
    st.title("Image Preprocessing")
    st.write("Gray Scale, Gaussian Blur, and Binarization")

    def preprocess_image(image):
        # Konversi ke skala abu-abu
        gray = Image.fromarray(image).convert("L")

        # Blur Gaussian
        blurred = gray.filter(ImageFilter.GaussianBlur)

        # Binerisasi
        blurred_image_array = np.array(blurred)
        threshold = 200
        img_bin_array = (blurred_image_array > threshold) * 255
        binary = Image.fromarray(img_bin_array.astype("uint8"))

        return gray, blurred, binary

    # Mengunggah folder
    uploaded_folder = st.file_uploader("Upload Folder", type=["zip"])

    # Jika folder diunggah, lakukan preprocessing dan tampilkan hasilnya
    if uploaded_folder is not None:
        # Ekstraksi folder zip
        folder_path = "./uploaded_folder"
        os.makedirs(folder_path, exist_ok=True)
        with open(os.path.join(folder_path, "temp.zip"), "wb") as f:
            f.write(uploaded_folder.read())
        with ZipFile(os.path.join(folder_path, "temp.zip"), "r") as zip_ref:
            zip_ref.extractall(folder_path)

        # List folder dalam folder utama sebagai label
        labels = [
            folder
            for folder in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, folder))
        ]

        # Mengambil satu contoh gambar per label
        images = []
        for label in labels:
            image_files = os.listdir(os.path.join(folder_path, label))
            if len(image_files) > 0:
                image_path = os.path.join(folder_path, label, image_files[0])
                image = imageio.imread(image_path)
                images.append((image, label))

        # Preprocessing dan menampilkan hasilnya
        for image, label in images:
            # Preprocessing gambar
            gray, blurred, binary = preprocess_image(image)

            # Menampilkan judul label
            st.subheader(f"Label: {label}")

            # Mengatur tampilan gambar dalam satu baris
            col1, col2, col3, col4 = st.columns(4)

            # Menampilkan gambar asli
            with col1:
                st.write("Original Image")
                st.image(image, use_column_width=True)

            # Menampilkan gambar dalam skala abu-abu
            with col2:
                st.write("Grayscale Image")
                st.image(gray, use_column_width=True)

            # Menampilkan gambar setelah blur Gaussian
            with col3:
                st.write("Blurred Image")
                st.image(blurred, use_column_width=True)

            # Menampilkan gambar hasil binerisasi
            with col4:
                st.write("Binarized Image")
                st.image(binary, use_column_width=True)

    # Judul dan deskripsi aplikasi Streamlit
    st.title("Dataset Splitter")
    st.write("Splitting Dataset into Train and Test")

    # Mengunggah folder dataset dalam format ZIP
    uploaded_file = st.file_uploader("Upload Dataset (ZIP)", type="zip")

    # Persentase pembagian data latih dan data testing (default: 80% train, 20% test)
    train_ratio = st.slider("Train Data Percentage", 0, 100, 90)

    # Jika dataset diunggah, lakukan pembagian data latih dan data testing
    if uploaded_file is not None:
        # Ekstraksi folder dataset dari file ZIP
        dataset_path = "./dataset"
        os.makedirs(dataset_path, exist_ok=True)
        with open(os.path.join(dataset_path, "temp.zip"), "wb") as f:
            f.write(uploaded_file.read())
        with ZipFile(os.path.join(dataset_path, "temp.zip"), "r") as zip_ref:
            zip_ref.extractall(dataset_path)

        # List folder dalam dataset sebagai label
        labels = [
            folder
            for folder in os.listdir(dataset_path)
            if os.path.isdir(os.path.join(dataset_path, folder))
        ]

        # Membuat folder data latih dan data testing
        train_path = "./train"
        test_path = "./test"
        os.makedirs(train_path, exist_ok=True)
        os.makedirs(test_path, exist_ok=True)

        # Melakukan pembagian data latih dan data testing
        for label in labels:
            label_path = os.path.join(dataset_path, label)
            train_label_path = os.path.join(train_path, label)
            test_label_path = os.path.join(test_path, label)
            os.makedirs(train_label_path, exist_ok=True)
            os.makedirs(test_label_path, exist_ok=True)

            # Mengambil semua file gambar dalam label
            image_files = os.listdir(label_path)

            # Mengacak urutan file gambar
            random.shuffle(image_files)

            # Menghitung jumlah data latih berdasarkan persentase
            num_train = int(train_ratio / 100 * len(image_files))

            # Memindahkan file gambar ke folder data latih dan data testing
            train_files = image_files[:num_train]
            test_files = image_files[num_train:]

            for file in train_files:
                shutil.move(
                    os.path.join(label_path, file), os.path.join(train_label_path, file)
                )

            for file in test_files:
                shutil.move(
                    os.path.join(label_path, file), os.path.join(test_label_path, file)
                )

        # Menampilkan pesan berhasil
        st.success("Dataset has been split into train and test folders.")

if selected == "Pengujian Model":
    st.title("Pengujian Model")

    def build_model():
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(250, 250, 3)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(32, (3, 3), activation="relu"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation="relu"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(128, (3, 3), activation="relu"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(512, activation="relu"))
        model.add(Dense(num_classes, activation="softmax"))
        return model

    # Fungsi untuk melatih model

    def train_model(X_train, y_train, X_test, y_test, optimizer, epochs, batch_size):
        model = build_model()
        model.compile(
            optimizer=optimizer,
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        model.fit(
            X_train,
            y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
        )
        return model

    # Menambahkan judul dan deskripsi pada aplikasi Streamlit
    # st.title("CNN Training with Streamlit")
    st.write("Custom Dataset")

    # Menampilkan opsi pengaturan
    optimizer = st.selectbox("Optimizer", ["adam", "rmsprop", "sgd"])
    epochs = st.slider("Epochs", 1, 50, 10)
    batch_size = st.slider("Batch Size", 16, 128, 32)

    # Mengunggah dataset train dalam format zip
    uploaded_train_zip = st.file_uploader("Upload Train Dataset (zip)")

    # Mengunggah dataset test dalam format zip
    uploaded_test_zip = st.file_uploader("Upload Test Dataset (zip)")

    # Tombol untuk memulai pelatihan
    if (
        st.button("Start Training")
        and uploaded_train_zip is not None
        and uploaded_test_zip is not None
    ):
        st.write("Training in progress...")
        # Membaca file zip dataset train
        train_zip = zipfile.ZipFile(uploaded_train_zip, "r")
        train_image_files = train_zip.namelist()
        # Inisialisasi list untuk menyimpan gambar dan label dari dataset train
        train_images = []
        train_labels = []
        # Memproses setiap file gambar
        for image_file in train_image_files:
            with train_zip.open(image_file) as file:
                try:
                    # Memuat gambar
                    img = PIL.Image.open(io.BytesIO(file.read())).convert("RGB")
                    img = img.resize((250, 250))
                    # Mengubah gambar menjadi array
                    img_array = np.array(img)
                    # Menyimpan gambar dan label
                    train_images.append(img_array)
                    label = os.path.basename(os.path.dirname(image_file))
                    train_labels.append(label)
                except (OSError, PIL.UnidentifiedImageError) as e:
                    # Tambahkan pernyataan cetak ini
                    print("Error processing image train file:", image_file)
                    # Tambahkan pernyataan cetak ini
                    print("Error message:", str(e))

        # Membaca file zip dataset test
        test_zip = zipfile.ZipFile(uploaded_test_zip, "r")
        test_image_files = test_zip.namelist()
        # Inisialisasi list untuk menyimpan gambar dan label dari dataset test
        test_images = []
        test_labels = []
        # Memproses setiap file gambar
        for image_file in test_image_files:
            with test_zip.open(image_file) as file:
                try:
                    # Memuat gambar
                    img = PIL.Image.open(io.BytesIO(file.read())).convert("RGB")
                    img = img.resize((250, 250))
                    # Mengubah gambar menjadi array
                    img_array = np.array(img)
                    # Menyimpan gambar dan label
                    test_images.append(img_array)
                    label = os.path.basename(os.path.dirname(image_file))
                    test_labels.append(label)
                except (OSError, PIL.UnidentifiedImageError) as e:
                    # Tambahkan pernyataan cetak ini
                    print("Error processing image test file:", image_file)
                    # Tambahkan pernyataan cetak ini
                    print("Error message:", str(e))

        # Mengubah list gambar dan label menjadi array NumPy
        X_train = np.array(train_images)
        y_train = np.array(train_labels)
        X_test = np.array(test_images)
        y_test = np.array(test_labels)

        # Mendapatkan jumlah kelas (label)
        num_classes = len(np.unique(y_train))

        # Mengubah label menjadi tipe data integer
        label_mapping = {label: idx for idx, label in enumerate(np.unique(y_train))}
        y_train = np.array([label_mapping[label] for label in y_train])
        y_test = np.array([label_mapping[label] for label in y_test])

        model = train_model(
            X_train, y_train, X_test, y_test, optimizer, epochs, batch_size
        )
        st.write("Training completed!")

        # Menampilkan hasil evaluasi model
        loss, accuracy = model.evaluate(X_test, y_test)
        st.success("Test Loss:", loss)
        st.success("Test Accuracy:", accuracy)


if selected == "Klasifikasi Tulisan Tangan":
    st.title("Klasifikasi Tulisan Tangan")

    # Create a temporary directory to save the uploaded model
    TEMP_DIR = "./temp_model"
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Load the trained model
    model_path = st.file_uploader("Upload Model", type=["h5"])
    if model_path is not None:
        with open(os.path.join(TEMP_DIR, "temp_model.h5"), "wb") as f:
            f.write(model_path.read())

        model = load_model(os.path.join(TEMP_DIR, "temp_model.h5"))
        label_dict = {i: chr(65 + i) for i in range(26)}

        # Set the canvas size
        canvas_width = 640
        canvas_height = 480

        # Create a canvas using streamlit-drawable-canvas
        canvas_image_data = st_canvas(
            fill_color="#ffffff",
            stroke_width=10,
            stroke_color="#000000",
            background_color="#ffffff",
            height=canvas_height,
            width=canvas_width,
            drawing_mode="freedraw",
            key="canvas",
        )

        # Define a function to preprocess and recognize the image
        def recognize(img):
            # Preprocess the image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (250, 250))
            img = cv2.merge([img] * 3)  # Add 3 channels to grayscale image
            img = img.astype("float32") / 255
            img = np.expand_dims(img, axis=0)

            # Predict the digit using the trained model
            prediction = model.predict(img)

            return label_dict[np.argmax(prediction[0])]

        # Create a button to recognize the handwriting
        if st.button("Recognize"):
            # Get the image from the canvas
            image_data = np.array(canvas_image_data.image_data, dtype=np.uint8)
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)

            # Preprocess and recognize the image
            digit = recognize(image_data)
            st.write("Recognized Alphabet:", digit)
