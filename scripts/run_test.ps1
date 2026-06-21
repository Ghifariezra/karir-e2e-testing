# ====================================================================
# Script Execution Automation untuk Karir.com E2E Testing
# ====================================================================

param (
    [Parameter(Mandatory = $false)]
    [string]$Target
)

# Jika argumen tidak diberikan saat menjalankan skrip, tanyakan ke pengguna
if ([string]::IsNullOrWhiteSpace($Target)) {
    Write-Host "======================================" -ForegroundColor Yellow
    Write-Host "   Pilih Test Suite Karir.com         " -ForegroundColor Yellow
    Write-Host "======================================" -ForegroundColor Yellow
    Write-Host "[1] register"
    Write-Host "[2] login"
    Write-Host "[3] all (Jalankan Keduanya)"
    Write-Host "======================================" -ForegroundColor Yellow
    $Target = Read-Host "Masukkan pilihan Anda (register/login/all)"
}

# Blok perkondisian
switch ($Target.ToLower()) {
    "register" {
        Write-Host "`n[INFO] Memulai Eksekusi Test Registrasi (Parallel: 5 Workers)..." -ForegroundColor Cyan
        python -m pytest .\src\tests\test_registration.py -n 5 -v --html=report.html
    }
    "login" {
        Write-Host "`n[INFO] Memulai Eksekusi Test Login (Parallel: 2 Workers)..." -ForegroundColor Cyan
        python -m pytest .\src\tests\test_login.py -n 2 -v --html=report.html
    }
    "all" {
        Write-Host "`n[INFO] Memulai Eksekusi Semua Test Suite..." -ForegroundColor Cyan
        # Menjalankan spesifik kedua file test agar terpusat di satu laporan
        python -m pytest .\src\tests\test_registration.py .\src\tests\test_login.py -n 5 -v --html=report.html
    }
    default {
        Write-Host "`n[ERROR] Input tidak valid! Silakan masukkan 'register' atau 'login'." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n[DONE] Eksekusi selesai. Silakan cek report.html untuk melihat hasil." -ForegroundColor Green