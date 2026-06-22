# E2E Automation Testing - Karir.com

## Project Overview
Proyek ini merupakan kerangka kerja otomatisasi pengujian ujung-ke-ujung (End-to-End Testing) untuk memvalidasi alur antarmuka pengguna (UI/UX) pada platform [Karir.com](https://karir.com/) berbasis framework reaktif (Material-UI).

## Tech Stack
- **Testing Framework:** Pytest dengan engine SeleniumBase
- **Parallel Execution:** `pytest-xdist`
- **Environment Manager:** `python-dotenv` & PowerShell script

## Assumed Business Rules & Test Scenarios
Karena pengujian ini bersifat *Black-Box Testing* yang dieksekusi tanpa dokumen *Product Requirements Document* (PRD) internal, skenario di bawah ini dirancang berdasarkan *reverse-engineering* terhadap *behavior* aktual antarmuka pengguna Karir.com. Rangkaian pengujian mencakup *Boundary Value Testing*, asersi reaktif, manipulasi DOM (Vanilla JS Injection), serta *Security Testing*.

### Test Scenario Matrix

| Modul / Halaman | Skenario | Tipe Uji | Ekspektasi Hasil (Assertion) |
| :--- | :--- | :--- | :--- |
| **Registration Form** | Pendaftaran dengan data valid & Strong Password | Happy Path | Form berhasil dikirim, lanjut ke tahap verifikasi Email. |
| | Input & Submit Kode OTP Verifikasi | Happy Path | OTP tervalidasi oleh sistem. |
| | Injeksi payload berbahaya (XSS) pada input | Security | Payload dinetralisir (*sanitized*); tidak ada eksekusi *alert* DOM JS. |
| | Mengosongkan form (Empty Fields) | Negative | Tombol *Submit* tetap dalam keadaan *disabled*. |
| | Input format Email yang salah | Negative | Muncul pesan error validasi regex UI: "Format email belum sesuai". |
| | Input Nomor Ponsel di bawah 10 digit | Negative (Boundary) | Muncul pesan error: "Minimal 10 digit". |
| | Input Nomor Ponsel di atas 13 digit | Negative (Boundary) | Muncul pesan error: "Maksimal 13 digit". |
| | Input Kata Sandi lemah (< 8 karakter) | Negative | Muncul pesan error: "Too Short". |
| | Konfirmasi Kata Sandi tidak sama | Negative | Muncul pesan ketidakcocokan (*mismatch error*) yang relevan. |
| **Login Form** | Login multi-langkah dengan kredensial valid | Happy Path | Autentikasi sukses, masuk ke halaman *Dashboard* pengguna. |
| | Mengosongkan form (Empty Fields) | Negative | Tombol *Lanjutkan* tetap dalam keadaan *disabled*. |
| | Input format Email yang salah di langkah awal | Negative | Muncul pesan error: "Format email harus seperti email@karir.com." |
| **Job Search Form** | Pencarian presisi (Posisi/Perusahaan + Lokasi) | Happy Path | Daftar lowongan dirender sesuai dengan kedua parameter. |
| | Pencarian parsial (Hanya Posisi/Perusahaan) | Happy Path | Daftar lowongan dirender sesuai kata kunci posisi terkait. |
| | Pencarian parsial (Hanya Lokasi) | Happy Path | Daftar lowongan dirender sesuai kata kunci lokasi terkait. |
| | Manipulasi Modal Filter (S1 & Remote) | Advance / Happy Path | DOM berhasil dimanipulasi; pencarian mematuhi aturan filter. |
| | Eksekusi Pencarian Kosong (Edge Case) | Negative | UI tidak *crash*; URL termodifikasi natif dengan parameter `?keyword=`. |

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