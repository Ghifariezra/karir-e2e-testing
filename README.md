# E2E Automation Testing - Karir.com

## Project Overview
Proyek ini merupakan kerangka kerja otomatisasi pengujian ujung-ke-ujung (End-to-End Testing) untuk memvalidasi alur antarmuka pengguna (UI/UX) pada platform [Karir.com](https://karir.com/) berbasis framework reaktif (Material-UI).

## Tech Stack
- **Testing Framework:** Pytest dengan engine SeleniumBase
- **Parallel Execution:** `pytest-xdist`
- **Environment Manager:** `python-dotenv` & PowerShell script

## Test Scenarios Covered
Rangkaian pengujian ini mencakup Boundary Value Testing, asersi reaktif, manipulasi DOM (Vanilla JS Injection), serta pengujian keamanan dasar (Security Testing):

### 1. Registration Form
- **Happy Path:**
    - Pendaftaran akun dengan data valid (termasuk Strong Password).
    - Pemilihan metode verifikasi (melalui Email).
    - Eksekusi pengisian dinamis 6-digit kode OTP dan penyelesaian verifikasi.
- **Negative & Security:**
    - **XSS Injection (Security):** Menguji kerentanan form terhadap injeksi payload skrip berbahaya (Cross-Site Scripting) dan memastikan tidak ada DOM alert yang tereksekusi.
    - **Empty Fields:** Memastikan tombol submit terkunci (disabled) saat kolom kosong.
    - **Invalid Email:** Validasi regex format email setelah klik submit.
    - **Boundary Phone:** Validasi batas minimal (10 digit) dan maksimal (13 digit) nomor ponsel.
    - **Password Weak:** Asersi penolakan sistem terhadap kata sandi yang terlalu pendek (Too Short).
    - **Password Mismatch:** Validasi asersi ketidakcocokan antara kolom Password dan Konfirmasi Password.

### 2. Login Form
- **Happy Path:**
    - Pengujian alur login multi-langkah (Email -> Password) dengan kredensial valid.
- **Negative:**
    - **Empty Fields:** Memastikan tombol lanjutkan terkunci (disabled) saat input kosong.
    - **Invalid Email:** Validasi format regex email yang salah pada langkah pertama login.

### 3. Job Search Form
- **Happy Path:**
    - Pencarian presisi menggunakan parameter lengkap (Posisi/Perusahaan dan Lokasi).
    - Pencarian parsial hanya menggunakan parameter Posisi.
    - Pencarian parsial hanya menggunakan parameter Lokasi.
- **Advance Filters:**
    - Otomatisasi pembukaan modal Material-UI dan interaksi pada hidden checkbox untuk menyaring lowongan berdasarkan Tingkat Pendidikan (Sarjana S1) dan Tipe Pekerjaan (Remote).
- **Negative:**
    - **Empty Fields:** Eksekusi pencarian kosong tanpa menahan UI error (karena form search diizinkan kosong), melainkan memvalidasi perubahan *behavior* parameter `?keyword=` pada URL secara native.

## How to Run Locally

### Persiapan Lingkungan
1. Pastikan virtual environment aktif dan semua dependensi telah terinstal.
2. Buat berkas `.env` di root directory (berdasarkan `.env.example`) dan atur kredensial Anda:
   ```env
   HEADLESS=false
   EMAIL=email.testing.anda@gmail.com
   PASSWORD=KataSandiAnda123!
   ```

### Eksekusi Pengujian (Menggunakan Runner Script)
Proyek ini dilengkapi dengan skrip PowerShell dinamis untuk mempermudah eksekusi. Jalankan perintah berikut dari root directory:
```bash
# Membuka menu interaktif untuk memilih Test Suite (Register / Login / All)
.\scripts\run_test.ps1

# ATAU jalankan secara langsung dengan parameter
.\scripts\run_test.ps1 -Target search
```

## Test Report Visualization
Untuk melihat rincian laporan hasil eksekusi pengujian secara interaktif, Anda dapat membuka berkas `report.html` (ter-generate di root directory setelah proses selesai) menggunakan browser web (klik dua kali pada berkas tersebut). Laporan ini mencakup rincian kegagalan dan bukti screenshot visual.