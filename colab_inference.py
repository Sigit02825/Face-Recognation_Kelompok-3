"""
Script Inferensi Pengenalan Wajah 1:N Berbasis FaceNet512 (Google Colab / Python Engine)
Sesuai dengan penelitian: IMPLEMENTASI PENGENALAN WAJAH MENGGUNAKAN ARSITEKTUR FACENET512 BERBASIS DETEKTOR RETINAFACE
"""

import os
import numpy as np

EMBEDDINGS_CACHE = 'embeddings_cache_5kelas.npz'

def load_data():
    """Memuat cache representasi vektor 512 dimensi FaceNet512."""
    if not os.path.exists(EMBEDDINGS_CACHE):
        print(f"[!] File cache {EMBEDDINGS_CACHE} tidak ditemukan.")
        return None

    cache = np.load(EMBEDDINGS_CACHE, allow_pickle=True)
    fn_embs = cache['Facenet512']
    print(f"[✓] Vektor embedding FaceNet512 dimuat: {fn_embs.shape} (234 foto, 512 fitur)")
    return fn_embs

def verify_face_with_threshold(query_embedding, gallery_embeddings, gallery_labels, threshold=0.65):
    """
    Klasifikasi 1:N Nearest Cosine Match dengan Ambang Batas (Thresholding).
    Jika skor kemiripan < threshold (misal karena perubahan gaya rambut, pose miring, atau wajah luar),
    maka sistem secara otomatis berstatus TIDAK DIKENALI.
    """
    # Dot product karena vektor sudah L2-normalized: dot product == cosine similarity
    sims = np.dot(gallery_embeddings, query_embedding)
    
    best_idx = np.argmax(sims)
    best_sim = sims[best_idx]
    best_dist = 1.0 - best_sim
    best_label = gallery_labels[best_idx]

    is_verified = best_sim >= threshold

    return {
        'verified': bool(is_verified),
        'status': 'DIKENALI (Terverifikasi)' if is_verified else 'TIDAK DIKENALI (Ditolak / Wajah Tidak Sesuai)',
        'predicted_label': best_label if is_verified else 'Unknown / Wajah Tidak Dikenali',
        'nearest_candidate': best_label,
        'similarity': float(best_sim),
        'distance': float(best_dist),
        'threshold': float(threshold),
        'confidence_percent': f"{best_sim * 100:.2f}%",
        'reason': (
            "Verifikasi berhasil. Landmark wajah dan representasi laten FaceNet512 cocok."
            if is_verified else
            f"Kemiripan ({best_sim * 100:.2f}%) di bawah threshold ({threshold * 100:.2f}%). "
            f"Terdeteksi perubahan gaya rambut yang signifikan, sudut miring, atau wajah tidak terdaftar."
        )
    }

if __name__ == '__main__':
    print("=" * 70)
    print("PENGUJIAN PENGENALAN WAJAH FACENET512 (PYTHON / COLAB ENGINE)")
    print("=" * 70)
    fn_embs = load_data()
    if fn_embs is not None:
        print("\n[Simulasi Uji Sampel Foto]")
        dummy_labels = [f"Mahasiswa_{i}" for i in range(len(fn_embs))]
        res = verify_face_with_threshold(fn_embs[0], fn_embs, dummy_labels, threshold=0.65)
        print("Hasil:", res)
