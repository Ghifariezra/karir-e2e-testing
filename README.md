# E2E Automation Testing - Karir.com

## Project Overview
Proyek ini merupakan kerangka kerja otomatisasi pengujian ujung-ke-ujung (End-to-End Testing) untuk memvalidasi alur antarmuka pengguna (UI/UX) pada platform pendaftaran Karir.com berbasis framework reaktif (Material-UI).

## Tech Stack
- **Testing Framework:** Pytest dengan engine SeleniumBase
- **Parallel Execution:** `pytest-xdist`
- **Environment Manager:** `python-dotenv` & PowerShell script

## Test Scenarios Covered
Rangkaian pengujian ini mencakup Boundary Value Testing dan asersi reaktif:

- **Registration Form:**
    - **Happy Path:**
        - Pendaftaran akun dengan data valid (termasuk Strong Password).
    - **Negative:**
        - Empty Fields: Memastikan tombol submit terkunci (disabled) saat kolom kosong.
        - Invalid Email: Validasi regex format email setelah klik submit.
        - Boundary Phone: Validasi batas minimal (10 digit) dan maksimal (13 digit) nomor ponsel.
        - Password Weak: Asersi penolakan sistem terhadap kata sandi yang terlalu pendek (Too Short).
        - Password Mismatch: Validasi asersi ketidakcocokan antara kolom Password dan Konfirmasi Password.

## How to Run Locally
1. Pastikan virtual environment dan dependensi telah terinstal.
2. Setel variabel `HEADLESS=false` di dalam berkas `.env` (jika ingin melihat jendela browser).
3. Jalankan perintah terminal berikut dari root directory:

```bash
python -m pytest src/tests/test_registration.py -n 5 -v
```

## Test Report Visualization
Untuk melihat rincian laporan hasil eksekusi pengujian secara interaktif, Anda dapat membuka berkas `report.html` yang telah tergenerate di root directory menggunakan browser web (klik dua kali pada berkas tersebut).