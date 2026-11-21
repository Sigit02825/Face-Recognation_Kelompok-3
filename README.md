# Sistem Pengenalan Wajah (Face Recognition AI) - FaceNet512 & RetinaFace

Aplikasi web interaktif khusus untuk **deteksi dan pengenalan wajah (Face Recognition 1:N)** berbasis eksperimen Google Colab dan dataset foto mahasiswa dari penelitian:
> **"IMPLEMENTASI PENGENALAN WAJAH MENGGUNAKAN ARSITEKTUR FACENET512 BERBASIS DETEKTOR RETINAFACE"**  
> *Dataset: 33 Mahasiswa, 234 Citra Wajah (Universitas Dian Nuswantoro)*

---

## 🎯 Fokus Aplikasi
1. **Khusus Arsitektur FaceNet512 (Inception-ResNet-v1):**  
   Mengekstrak 512 representasi fitur laten biometrik ternormalisasi ($L_2\text{-norm}$). Menghasilkan akurasi pengenalan **91.04% ± 1.55%** pada validasi 5-Fold Colab.
2. **Deteksi & Penyelarasan Wajah RetinaFace:**  
   Melokalisasi wajah dan 5 titik tengara kanonik (*canonical landmarks*): mata kiri, mata kanan, hidung, sudut mulut kiri, dan sudut mulut kanan.
3. **Mengenali & Menolak Wajah Berdasarkan Ambang Batas (Threshold):**  
   - **Wajah Sesuai / Terdaftar:** Skor kemiripan kosinus $\ge \text{Threshold}$ (default $0.65$) $\rightarrow$ **DIKENALI (Terverifikasi)**.
   - **Gaya Rambut Berubah / Foto Tidak Sesuai / Orang Luar:** Skor kemiripan anjlok di bawah ambang batas $\rightarrow$ **TIDAK DIKENALI (Ditolak)**.

---

## 📌 Mengapa Seseorang yang Merubah Gaya Rambut Tidak Terdeteksi? (Penjelasan Ilmiah)

1. **Pengaruh Gaya Rambut Terhadap Fitur Konvolusi:**  
   Lapisan konvolusi awal Inception-ResNet-v1 sangat sensitif terhadap kontur tepi atas wajah, garis dahi (*hairline*), dan pelipis. Jika seseorang merubah potongan rambut secara ekstrem (misal memanjangkan poni hingga menutupi dahi/alis, rambut samping menutupi pipi, atau volume rambut berubah drastis), distribusi piksel spasial mengalami deviasi signifikan.
2. **Pergeseran Jarak Kosinus:**  
   $$\text{Cosine Similarity} = \sum_{i=1}^{512} u_i \cdot v_i, \quad \text{Jarak Kosinus} = 1 - \text{Cosine Similarity}$$
   Ketika gaya rambut berubah drastis atau wajah tertutup bayangan helai rambut, kemiripan kosinus terhadap foto master galeri turun tajam (sering kali $< 0.40$).
3. **Penyaringan Ambang Batas:**  
   Karena skor kemiripan berada di bawah batas ambang ($0.65$), sistem secara tegas mengklasifikasikan foto tersebut sebagai **"TIDAK DIKENALI"**, mencegah kesalahan identifikasi (*false positive match*).

---

## 🚀 Cara Menjalankan Aplikasi

Aplikasi dibangun mandiri (*zero-dependency* dari segi server Node.js), ringan, dan langsung siap dijalankan:

### Cara 1: Menggunakan File Batch (Klik Ganda di Windows)
Klik ganda (*double-click*) file:
```
start_app.bat
```
Peramban (*browser*) akan langsung terbuka ke alamat: **`http://localhost:3000`**

### Cara 2: Melalui Terminal / Command Prompt
```bash
node server.js
```
Lalu buka peramban dan akses: **`http://localhost:3000`**

---

## 🌟 Fitur Antarmuka Aplikasi

1. **Uji Pengenalan Wajah (Live & Dataset):**
   - **Pilih dari Dataset Mahasiswa:** Memilih foto langsung dari 234 foto 33 mahasiswa terdaftar.
   - **Unggah Foto Mandiri:** Mendukung format `.jpg`, `.png`, dan `.webp`.
   - **Kamera Langsung (Webcam):** Ambil foto langsung melalui peramban.
   - **Kanvas RetinaFace:** Menampilkan visualisasi kotak pembatas wajah dan 5 titik tengara (mata, hidung, bibir).
   - **Barcode Vektor 512-D:** Visualisasi barcode dari fitur laten FaceNet512.
   - **Peringkat 5 Kandidat Terdekat:** Menampilkan 5 kemiripan wajah terdekat secara transparan.
2. **Slider Ambang Batas (Threshold Sensitivity):**
   - Pengaturan sensitivitas (0.40 s.d. 0.90) dengan tombol preset:
     * **Toleran (0.50):** Menerima variasi rambut dan sudut yang lebih longgar.
     * **Standar Riset (0.65):** Rekomendasi optimal hasil pengujian 5-Fold Colab.
     * **Ketat (0.75):** Menolak segala bentuk perubahan gaya rambut/penampilan.
3. **Lab Eksperimen Gaya Rambut & Penolakan Wajah:**
   - Menyediakan sampel pengujian nyata:
     * *Kasus 1:* Mahasiswa normal (frontal) $\rightarrow$ Dikenali ($> 0.85$).
     * *Kasus 2:* Mahasiswa merubah gaya rambut/poni (misal Cherishta Foto 04, Radithya Foto 06) $\rightarrow$ Ditolak (skor anjlok di bawah threshold).
4. **Galeri Wajah 33 Mahasiswa Terdaftar:**
   - Katalog visual 33 mahasiswa dengan fitur pencarian nama/NIM dan modal koleksi foto.
5. **Dashboard Metrik Hasil Pengujian Colab:**
   - Visualisasi kurva ROC FaceNet512 (AUC = 0.968) dan distribusi kemiripan pasangan asli vs pasangan berbeda.

---

## 📁 Struktur Berkas Proyek

```
d:\Aplikasi face\
├── app_data\
│   ├── dataset_entries.json      # Metadata 234 foto & vektor FaceNet512
│   ├── students_gallery.json     # Profil master galeri 33 mahasiswa
│   ├── test_samples.json         # Kasus uji (gaya rambut & normal)
│   └── colab_metrics.json        # Data hasil evaluasi Colab
├── extracted_project\
│   └── Face Recognition\
│       ├── Dataset_Kelas\        # 33 folder mahasiswa (234 foto)
│       ├── Eksperimen_*.ipynb    # Notebook Google Colab
│       └── embeddings_cache_*.npz# Cache embedding FaceNet512
├── public\
│   ├── index.html                # Tampilan UI pengenalan wajah
│   ├── app.js                    # Logika pengenalan & kanvas
│   ├── style.css                 # Desain tema gelap modern
│   └── avatar-placeholder.png   # Placeholder aset
├── server.js                     # Server backend HTTP & REST API (Node.js)
├── start_app.bat                 # Peluncur 1-klik di Windows
├── colab_inference.py            # Skrip inferensi Python / Colab
└── README.md                     # Dokumentasi panduan
```
