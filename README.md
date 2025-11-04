# Sistem-Analisis-Statistik-Citra

Aplikasi Analisis dan Pencocokan Citra

Ini adalah aplikasi web sederhana yang dibuat dengan Streamlit untuk menganalisis fitur statistik dari sebuah gambar dan membandingkan kemiripan antara dua gambar. Aplikasi ini dibuat untuk memenuhi tugas mata kuliah Pengolahan Citra.

# Fitur

Aplikasi ini memiliki dua fungsi utama yang dibagi menjadi dua tab:

1. Analisis Fitur 
- Mengunggah satu gambar.
- Menghitung dan menampilkan fitur statistik dari gambar tersebut (dalam grayscale):
- Skewness: Mengukur kemiringan distribusi piksel.
- Kurtosis: Mengukur keruncingan distribusi piksel.
- Entropy: Mengukur tingkat keacakan atau informasi dalam gambar.
- Chi-Square (Goodness of Fit): Mengukur seberapa beda distribusi piksel gambar dari distribusi seragam (uniform).

2. Pencocokan Citra (Tugas 2)
- Mengunggah dua gambar (Gambar A dan Gambar B).
- Membandingkan histogram dari kedua gambar tersebut menggunakan dua metode:
- Pearson Correlation: Menghasilkan nilai antara -1 dan 1. Semakin dekat ke 1, semakin mirip.
- Chi-Square Distance: Menghasilkan nilai. Semakin dekat ke 0, semakin mirip.

# Cara Menjalankan Secara Lokal
- Pastikan Anda memiliki Python 3.8+ terinstal.

- Buka terminal dan arahkan ke folder proyek.
- Instal semua library yang dibutuhkan:
- pip install -r requirements.txt

# Jalankan aplikasi Streamlit:
streamlit run app.py
Kebutuhan Library
streamlit
numpy
opencv-python-headless
Pillow
scipy
scikit-image
