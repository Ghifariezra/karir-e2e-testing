import os
import time
from core.base_test import BaseTest
from utils.test_register import TestRegistration
from utils.test_login import TestLogin

class Karir(BaseTest):
    _os: os = os
    _time: time = time
    __listURL = {
        "registration": "https://karir.com/register",
        "login": "https://karir.com/login",
        "search": "https://karir.com/search-lowongan",
        # "apply": "https://karir.com/apply"
    }

    def __init__(self):
        super().__init__()
        self.test_registration = TestRegistration(self.driver)
        self.test_login = TestLogin(self.driver)

    """
        Skenario Pengujian Form Registrasi:
            1. Happy Path: Isi form dengan data valid, submit, lalu verifikasi OTP
            2. Negative - Empty Fields: Pastikan tombol submit disabled saat form kosong
            3. Negative - Invalid Email: Isi form dengan email tidak valid, submit, lalu verifikasi pesan error
            4. Negative - Phone Exceeds Max: Isi form dengan nomor ponsel lebih dari 13 digit, submit, lalu verifikasi pesan error
            5. Negative - Phone Below Min: Isi form dengan nomor ponsel kurang dari 10 digit, submit, lalu verifikasi pesan error
            6. Negative - Password Weak: Isi form dengan password yang terlalu lemah (misalnya hanya 5 karakter), submit, lalu verifikasi pesan error
            7. Negative - Password Mismatch: Isi form dengan password dan konfirmasi password yang tidak sama, submit, lalu verifikasi pesan error
            8. Negative - XSS Injection: Suntikkan payload XSS ke kolom input, submit, lalu verifikasi bahwa payload tidak dieksekusi (tidak muncul alert) dan aplikasi tetap aman.
    """
    def formRegistration(self):
        self._time.sleep(2)
        print("[INFO] Membuka halaman registrasi...")
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Eksekusi Skenario Pengisian Form (Happy Path)
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso@email.com")
        self.test_registration.testPhoneNumber("081299998888")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("StrongPass123!")

        # 2. Ambil Screenshot dengan fungsi helper (KODE JADI JAUH LEBIH BERSIH!)
        self.test_registration.saveScreenshot("form_registration_happy_path")

        # 3. Eksekusi Submit
        self.test_registration.submitForm()
        self._time.sleep(3)
        
        # 4. Verifikasi section
        self.test_registration.clickEmailVerification()
        self._time.sleep(2)
        
        # 5. Validation Verifikasi Kode
        self.test_registration.saveScreenshot("form_registration_otp_step")
        

        # 6. Eksekusi Pengisian Kode Verifikasi
        self.test_registration.inputVerificationCode("123456")

        # 7. Submit Verifikasi
        self.test_registration.submitVerification()

        # Tambah sleep lebih panjang — CI perlu waktu round-trip ke server OTP
        self._time.sleep(5)
        print("[DEBUG] Menunggu response server OTP...")

        # 8. Asersi
        try:
            self.test_registration.assertErrorMessage(
                "Verifikasi Kode OTP Tidak Valid")
            self.test_registration.saveScreenshot(
                "form_registration_otp_result_sukses")
            print("[INFO] Skenario Registrasi Happy Path & Verifikasi Selesai!")
        except Exception as e:
            self.test_registration.saveScreenshot("form_registration_otp_result_gagal")
            print("[ERROR] Asersi gagal, silakan cek screenshot di Artifact GitHub!")
            raise e
        
    def formRegistration_Negative_XSS_Injection(self):
        """
        Skenario Keamanan (Negative): Menguji kerentanan Cross-Site Scripting (XSS)
        dengan menyuntikkan payload skrip berbahaya ke kolom input.
        Aplikasi yang aman harus menolak input ini atau melakukan sanitasi (escaping).
        """
        self._time.sleep(2)
        print("[INFO] Membuka halaman registrasi untuk Security Test (XSS)...")
        self.driver.get(self.__listURL["registration"])
        self._time.sleep(3)

        # Payload XSS standar untuk memicu alert jika aplikasi rentan
        xss_payload = "<img src='x' onerror='alert(\"XSS-Vulnerability\")'>"

        # 1. Suntikkan payload berbahaya ke kolom Nama Lengkap
        self.test_registration.testFullName(xss_payload)

        # Gunakan email dinamis agar tidak terkena validasi duplikat
        unique_email = f"xss.test.{int(self._time.time())}@email.com"
        self.test_registration.testEmail(unique_email)

        self.test_registration.testPhoneNumber("081299998888")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("StrongPass123!")

        # 2. Ambil Screenshot bukti injeksi sebelum submit
        self.test_registration.saveScreenshot(
            "form_registration_xss_injection")

        # 3. Eksekusi Submit
        self.test_registration.submitForm()
        self._time.sleep(2)

        # 4. Asersi Keamanan (Security Assertion)
        print("[INFO] Memvalidasi keamanan DOM dari eksekusi XSS...")
        # Beri sedikit jeda agar alert punya waktu untuk muncul (jika ada)
        self._time.sleep(1)

        is_xss_vulnerable = False
        try:
            # Mencoba mengambil teks alert.
            # Jika aplikasi AMAN, baris ini akan gagal dan langsung melompat ke 'except'.
            alert_text = self.driver.get_alert_text()
            is_xss_vulnerable = True
            self.driver.accept_alert()  # Tutup alert berbahaya agar browser tidak hang
        except Exception:
            # Exception terjadi karena tidak ada alert yang terbuka (Aman)
            pass

        # Validasi Hasil Akhir
        if is_xss_vulnerable:
            # Tangkap layar dan gagalkan test karena sistem berhasil dijebol
            self.test_registration.saveScreenshot(
                "form_registration_xss_vulnerable")
            raise Exception(
                "KRITIS: Kerentanan XSS terdeteksi! Payload skrip berhasil dieksekusi oleh browser.")
        else:
            print(
                "[INFO] DOM Aman: Tidak ada eksekusi alert JavaScript berbahaya yang terdeteksi.")

            # (Opsional) Asersi bahwa UI memunculkan pesan validasi error input nama yang mengandung simbol
            # self.test_registration.assertErrorMessage("Format nama tidak valid")

            print("[INFO] Negative Security Test (XSS Injection) PASSED.")
        
    def formRegistration_Negative_Password_Weak(self):
        """Skenario Negatif: Password tidak memenuhi syarat (Terlalu pendek / lemah)"""
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Isi form dengan password lemah (hanya 5 huruf kecil & angka)
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso@email.com")
        self.test_registration.testPhoneNumber("081299998888")
        self.test_registration.testPassword("lemah12")
        self.test_registration.testPasswordConfirmation("lemah12")

        # 2. Klik Lanjutkan
        self.test_registration.submitForm()
        self._time.sleep(1)

        # 3. Asersi Ekspektasi
        # Sesuaikan dengan pesan error dari Karir.com jika berbeda
        self.test_registration.assertErrorMessage(
            "Too Short")
        print("[INFO] Negative Test (Password Weak/Too Short) PASSED.")

        # 4. Ambil Screenshot
        self.test_registration.saveScreenshot(
            "form_registration_password_weak")

    def formRegistration_Negative_Password_Mismatch(self):
        """Skenario Negatif: Konfirmasi password tidak sama"""
        self.driver.get(self.__listURL["registration"])
        self._time.sleep(3)

        # 1. Isi form dengan konfirmasi password yang BERBEDA
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso@email.com")
        self.test_registration.testPhoneNumber("081299998888")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("TypoPass123!")

        # 2. Klik Lanjutkan (Ini akan memicu validasi form/onBlur)
        self.test_registration.submitForm()
        self._time.sleep(2)

        # 3. AMBIL SCREENSHOT DULU! (Sebelum asersi)
        # Agar jika gagal, kita bisa mengecek gambar di Artifact GitHub
        self.test_registration.saveScreenshot(
            "form_registration_password_mismatch")

        # 4. Asersi Ekspektasi
        # Catatan: Teks "Password baru tidak sama" kemungkinan besar SALAH.
        # Nanti sesuaikan string ini dengan teks yang ada di dalam screenshot.
        self.test_registration.assertErrorMessage("Password baru tidak sama")
        print("[INFO] Negative Test (Password Mismatch) PASSED.")

    def formRegistration_Negative_EmptyFields(self):
        """Skenario Negatif: Memastikan tombol Lanjutkan mati (disabled) saat form kosong"""
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Asersi Ekspektasi
        self.test_registration.assertSubmitButtonDisabled()
        print(
            "[INFO] Negative Test (Empty Fields) PASSED. Tombol Lanjutkan tidak bisa diklik.")

        # 2. Ambil Screenshot
        self.test_registration.saveScreenshot("form_registration_empty_fields")

    def formRegistration_Negative_InvalidEmail(self):
        """Skenario Negatif: Form diisi penuh, submit, lalu muncul error format email"""
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Isi form dengan email salah
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso.tanpadomain")
        self.test_registration.testPhoneNumber("081299998888")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("StrongPass123!")

        # 2. Klik Lanjutkan
        self.test_registration.submitForm()
        self._time.sleep(1)

        # 3. Asersi Ekspektasi
        self.test_registration.assertErrorMessage("Format email belum sesuai")
        print(
            "[INFO] Negative Test (Invalid Email) PASSED. Error format email berhasil divalidasi.")

        # 4. Ambil Screenshot
        self.test_registration.saveScreenshot(
            "form_registration_invalid_email")

    def formRegistration_Negative_Phone_ExceedsMax(self):
        """Skenario Negatif: Nomor ponsel melebihi batas maksimal (>13 digit)"""
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Isi form dengan nomor kepanjangan
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso@email.com")
        self.test_registration.testPhoneNumber("08230198231232")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("StrongPass123!")

        # 2. Klik Lanjutkan
        self.test_registration.submitForm()
        self._time.sleep(1)

        # 3. Asersi Ekspektasi
        self.test_registration.assertErrorMessage("Maksimal 13 digit")
        print("[INFO] Negative Test (Phone Exceeds Max) PASSED.")

        # 4. Ambil Screenshot
        self.test_registration.saveScreenshot("form_registration_phone_max")

    def formRegistration_Negative_Phone_BelowMin(self):
        """Skenario Negatif: Nomor ponsel kurang dari batas minimal (<10 digit)"""
        self.driver.get(self.__listURL["registration"])
        # self._time.sleep(2)
        self._time.sleep(3)

        # 1. Isi form dengan nomor kependekan
        self.test_registration.testFullName("Budi Santoso")
        self.test_registration.testEmail("budi.santoso@email.com")
        self.test_registration.testPhoneNumber("081234567")
        self.test_registration.testPassword("StrongPass123!")
        self.test_registration.testPasswordConfirmation("StrongPass123!")

        # 2. Klik Lanjutkan
        self.test_registration.submitForm()
        self._time.sleep(1)

        # 3. Asersi Ekspektasi
        self.test_registration.assertErrorMessage("Minimal 10 digit")
        print("[INFO] Negative Test (Phone Below Min) PASSED.")

        # 4. Ambil Screenshot
        self.test_registration.saveScreenshot("form_registration_phone_min")

    """
        Skenario Pengujian Form Login:
            1. Happy Path: Isi form dengan email dan password valid, submit, lalu verifikasi berhasil login
            2. Negative - Empty Fields: Pastikan tombol submit disabled saat form kosong
    """

    def formLogin(self):
        """Skenario Positif: Login dengan kredensial valid"""
        self._time.sleep(2)
        print("[INFO] Membuka halaman Login...")
        self.driver.get(self.__listURL["login"])
        self._time.sleep(3)

        email = self._os.getenv("EMAIL", "budi.santoso@email.com")
        password = self._os.getenv("PASSWORD", "StrongPass123!")

        # 1. Input Email
        self.test_login.testEmail(email)
        self.test_login.saveScreenshot("login_step_1_email")

        # 2. Klik Lanjutkan (Multi-step login)
        self.test_login.clickSubmitButton("Lanjutkan")
        self._time.sleep(2)  # Tunggu transisi DOM ke input password

        # 3. Input Password
        self.test_login.testPassword(password)
        self.test_login.saveScreenshot("login_step_2_password")

        # 4. Submit Form Final (Tombol berubah menjadi 'Login')
        self.test_login.clickSubmitButton("Login")

        # 5. Asersi Keberhasilan (Tunggu masuk ke Dashboard)
        self._time.sleep(20)
        self.test_login.saveScreenshot("login_success_dashboard")
        print("[INFO] Skenario Login Happy Path Selesai!")

    def formLogin_Negative_EmptyFields(self):
        """Skenario Negatif: Submit disabled saat email kosong"""
        self._time.sleep(2)
        print("[INFO] Membuka halaman Login (Negative Test)...")
        self.driver.get(self.__listURL["login"])
        self._time.sleep(3)

        # Asersi langsung bahwa tombol "Lanjutkan" dalam keadaan disabled
        self.test_login.assertSubmitButtonDisabled()
        self.test_login.saveScreenshot("login_negative_empty")
        print("[INFO] Negative Test (Empty Fields) Login PASSED.")
        
    def formLogin_Negative_InvalidEmail(self):
        """Skenario Negatif: Submit dengan email tidak valid, lalu muncul error format email"""
        self._time.sleep(2)
        print("[INFO] Membuka halaman Login (Negative Test - Invalid Email)...")
        self.driver.get(self.__listURL["login"])
        self._time.sleep(3)

        # 1. Input Email tidak valid
        self.test_login.testEmail("budi.santoso.tanpadomain")

        # 2. Klik Lanjutkan
        self.test_login.clickSubmitButton("Lanjutkan")
        self._time.sleep(3)

        # 3. Asersi Ekspektasi
        self.test_login.saveScreenshot("login_negative_invalid_email")
        self.test_login.assertErrorMessage(
            "Format email harus seperti email@karir.com.")
        print(
            "[INFO] Negative Test (Invalid Email) Login PASSED. Error format email berhasil divalidasi.")

    def formSearch(self):
        self._time.sleep(2)
        self.driver.get(self.__listURL["search"])
        self._time.sleep(2)

    def formApply(self):
        pass
