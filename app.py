import streamlit as st
import numpy as np
import cv2
from PIL import Image
from scipy import stats
from skimage import measure

# --- Fungsi Bantuan (Helper Functions) ---

def load_image_from_uploader(uploaded_file):
    """Membuka file gambar yang diunggah dan mengubahnya menjadi array numpy."""
    image = Image.open(uploaded_file)
    return np.array(image)

def get_grayscale_image(image_array):
    """Mengkonversi gambar menjadi grayscale jika gambar tersebut berwarna."""
    if image_array.ndim == 3:
        # Konversi dari RGB (Pillow) ke BGR (OpenCV) lalu ke Grayscale
        # Atau langsung dari RGB ke Grayscale
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image_array
    return gray_image

def calculate_statistical_features(image):
    """
    Menghitung fitur statistik dari satu gambar (Tugas 1).
    Fitur: Skewness, Kurtosis, Entropy, Chi-Square (Goodness of Fit).
    """
    # 1. Dapatkan gambar grayscale dan data flat-nya
    gray_image = get_grayscale_image(image)
    gray_flat = gray_image.flatten()
    
    # 2. Hitung Skewness dan Kurtosis
    skewness = stats.skew(gray_flat)
    kurtosis = stats.kurtosis(gray_flat)
    
    # 3. Hitung Entropy
    # Menggunakan Shannon Entropy dari scikit-image
    entropy = measure.shannon_entropy(gray_image)
    
    # 4. Hitung Chi-Square (Goodness of Fit)
    hist, _ = np.histogram(gray_flat, bins=256, range=[0, 256])
    
    # --- PERBAIKAN DI SINI ---
    # Kita tidak perlu menghitung f_exp secara manual.
    # Jika f_exp tidak diberikan, stats.chisquare akan otomatis
    # mengasumsikan distribusi uniform (seragam) berdasarkan total f_obs.
    # Ini adalah cara yang benar dan menghindari error floating-point.
    
    # KODE BARU (Perbaikan):
    chi_stat, p_val = stats.chisquare(f_obs=hist)
    
    return skewness, kurtosis, entropy, chi_stat

def compare_image_histograms(image1, image2):
    """
    Membandingkan dua gambar menggunakan histogram (Tugas 2).
    Metode: Pearson Correlation & Chi-Square Distance.
    """
    # 1. Dapatkan gambar grayscale untuk kedua gambar
    gray1 = get_grayscale_image(image1)
    gray2 = get_grayscale_image(image2)
    
    # 2. Hitung histogram untuk kedua gambar
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    
    # 3. Normalisasi histogram (opsional tapi disarankan untuk perbandingan)
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    
    # 4. Bandingkan histogram
    
    # Metode 1: Pearson Correlation (HISTCMP_CORREL)
    # Semakin dekat ke 1, semakin mirip
    pearson_corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # Metode 2: Chi-Square (HISTCMP_CHISQR)
    # Semakin dekat ke 0, semakin mirip
    chi_square_dist = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
    
    return pearson_corr, chi_square_dist

# --- Tampilan Utama Aplikasi Streamlit ---

st.set_page_config(page_title="Analisis Citra", layout="wide")
st.title("Aplikasi Analisis dan Pencocokan Citra 📸")
st.write("Dibuat untuk memenuhi tugas mata kuliah Pengolahan Citra.")

# Membuat dua tab untuk memisahkan tugas
tab1, tab2 = st.tabs(["Analisis Fitur (Tugas 1)", "Pencocokan Citra (Tugas 2)"])

# --- Logika untuk TAB 1 ---
with tab1:
    st.header("1. Analisis Fitur Statistik Citra")
    st.write("Unggah satu citra untuk menghitung nilai Skewness, Kurtosis, Entropy, dan Chi-Square (Goodness of Fit).")
    
    uploaded_file_1 = st.file_uploader("Unggah Citra Anda", type=["jpg", "jpeg", "png"], key="uploader1")
    
    if uploaded_file_1 is not None:
        image1 = load_image_from_uploader(uploaded_file_1)
        
        st.image(image1, caption="Citra yang Diunggah", width=400)
        
        # Hitung fitur
        try:
            skew, kurt, entropy, chi_gof = calculate_statistical_features(image1)
            
            st.subheader("Hasil Ekstraksi Fitur:")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Skewness", value=f"{skew:.4f}")
                st.info("Mengukur 'kemiringan' histogram. 0 = simetris.")
                
                st.metric(label="Kurtosis", value=f"{kurt:.4f}")
                st.info("Mengukur 'keruncingan' puncak histogram. 0 = normal.")

            with col2:
                st.metric(label="Entropy (Shannon)", value=f"{entropy:.4f}")
                st.info("Mengukur 'keacakan' atau jumlah informasi dalam gambar.")
                
                st.metric(label="Chi-Square (Goodness of Fit)", value=f"{chi_gof:.4f}")
                st.info("Mengukur seberapa jauh distribusi piksel gambar dari distribusi seragam (uniform). Semakin besar, semakin tidak seragam.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses gambar: {e}")

# --- Logika untuk TAB 2 ---
with tab2:
    st.header("2. Pencocokan Citra")
    st.write("Unggah dua citra (citra pertama dan citra kedua) untuk menghitung nilai kemiripannya berdasarkan perbandingan histogram.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        uploaded_file_a = st.file_uploader("Unggah Citra A", type=["jpg", "jpeg", "png"], key="uploaderA")
        if uploaded_file_a is not None:
            image_a = load_image_from_uploader(uploaded_file_a)
            st.image(image_a, caption="Citra A", use_container_width=True)
            
    with col_b:
        uploaded_file_b = st.file_uploader("Unggah Citra B", type=["jpg", "jpeg", "png"], key="uploaderB")
        if uploaded_file_b is not None:
            image_b = load_image_from_uploader(uploaded_file_b)
            st.image(image_b, caption="Citra B", use_container_width=True)
            
    if uploaded_file_a is not None and uploaded_file_b is not None:
        st.markdown("---")
        st.subheader("Hasil Perbandingan Kemiripan:")
        
        # Hitung perbandingan
        try:
            pearson, chi_dist = compare_image_histograms(image_a, image_b)
            
            st.metric(label="Pearson Correlation (Kemiripan)", value=f"{pearson:.4f}")
            st.success("**Interpretasi:** Semakin nilai mendekati **1**, histogram kedua citra **semakin mirip**.")
            
            st.metric(label="Chi-Square (Perbedaan)", value=f"{chi_dist:.4f}")
            st.success("**Interpretasi:** Semakin nilai mendekati **0**, histogram kedua citra **semakin mirip**.")
            
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membandingkan gambar: {e}")

