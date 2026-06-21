from core.base_scenario import BaseRegistrationScenario
from seleniumbase import BaseCase

class TestRegistration(BaseRegistrationScenario):
    def __init__(self, driver: BaseCase):
        super().__init__()
        self.driver = driver

    def _get_input_css(self, label_text):
        """
        Helper Absolut: Menggunakan mesin XPath native bawaan browser via JS.
        Ini menembus animasi, bayangan DOM, dan mengunci target langsung di tag <label>.
        """
        print(f"[DEBUG] Menunggu render teks '{label_text}' di halaman...")
        self.driver.wait_for_text(label_text, "body", timeout=25)

        # Logika JS: Cari label, lalu ambil elemen input terdekat yang valid (input, textarea)
        js_script = f"""
            (function() {{
                var xpath = "//label[contains(., '{label_text}')]";
                var label = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                
                if (label) {{
                    var container = label.closest('.MuiFormControl-root, .MuiTextField-root, div');
                    if (container) {{
                        var input = container.querySelector('input, textarea, select');
                        if (input && input.id) {{
                            return '#' + input.id;
                        }}
                    }}
                }}
                return null;
            }})();
        """

        dynamic_id = None
        # Perluas percobaan pengambilan ID dari 3 menjadi 5 kali
        for attempt in range(5):
            dynamic_id = self.driver.execute_script(js_script)
            if dynamic_id:
                return dynamic_id
            print(
                f"[DEBUG] JS DOM belum stabil. Retry ke-{attempt+1} untuk '{label_text}'...")
            self.driver.sleep(1.5)

        raise Exception(
            f"Gagal menemukan elemen input untuk label: '{label_text}'")

    def testFullName(self, name_input="Test User"):
        print(f"[DEBUG] Mengisi Nama Lengkap: {name_input}")
        css_name = self._get_input_css("Nama Lengkap")
        self.driver.type(css_name, name_input)

    def testEmail(self, email_input="testuser@example.com"):
        print(f"[DEBUG] Mengisi Email: {email_input}")
        css_email = self._get_input_css("Email")
        self.driver.type(css_email, email_input)

    def testPhoneNumber(self, phone_input="081234567890"):
        print(f"[DEBUG] Mengisi Nomor Ponsel: {phone_input}")
        css_phone = self._get_input_css("Nomor Ponsel")
        self.driver.type(css_phone, phone_input)

    def testPassword(self, password_input="ValidPass123!"):
        print("[DEBUG] Mengisi Password")
        # Catatan: Akan cocok dengan "Password" pertama yang ditemukan (bukan Konfirmasi)
        css_password = self._get_input_css("Password")
        self.driver.type(css_password, password_input)

    def testPasswordConfirmation(self, confirm_input="ValidPass123!"):
        print("[DEBUG] Mengisi Konfirmasi Password")
        css_confirm = self._get_input_css("Konfirmasi Password")
        self.driver.type(css_confirm, confirm_input)

    def submitForm(self):
        print("[DEBUG] Menekan tombol Lanjutkan")
        # Menggunakan pencarian text murni bawaan SeleniumBase
        # yang otomatis dikonversi dengan aman di UC Mode
        self.driver.click('button:contains("Lanjutkan")')
        
    def triggerBlurValidation(self, label_text):
        """
        Meniru perilaku manusia: Mengeklik kolom input, lalu mengeklik area kosong 
        untuk memicu validasi real-time (onBlur) tanpa menekan submit.
        """
        print(f"[DEBUG] Memicu validasi onBlur untuk: {label_text}")
        css_selector = self._get_input_css(label_text)

        # 1. Klik ke dalam kolom input
        self.driver.click(css_selector)
        self.driver.sleep(0.5)  # Jeda animasi UI

        # 2. Klik elemen netral (seperti judul "Buat Akun") untuk menghilangkan fokus
        self.driver.click('p:contains("Buat Akun")')
        self.driver.sleep(0.5)

    def assertSubmitButtonDisabled(self):
        """Memastikan tombol Lanjutkan mati (disabled) saat form tidak valid"""
        print("[DEBUG] Memvalidasi bahwa tombol Lanjutkan tidak dapat diklik (Disabled)")
        # Cek apakah elemen button memiliki atribut 'disabled'
        self.driver.assert_element('button[disabled]:contains("Lanjutkan")')

    def assertErrorMessage(self, expected_text):
        """
        Helper untuk Negative Test: 
        Memastikan pesan error validasi muncul di layar.
        """
        print(f"[DEBUG] Memvalidasi kemunculan error: '{expected_text}'")
        # Di Material-UI, pesan error biasanya menggunakan class Mui-error
        # atau dirender sebagai helper text standar.
        self.driver.assert_text(expected_text)

    def saveScreenshot(self, filename="screenshot.png"):
        """
        Menyimpan screenshot elemen form utama untuk bukti visual.
        Otomatis menggunakan fallback (full screen) jika elemen spesifik tidak ditemukan.
        """
        print(f"[DEBUG] Menyimpan screenshot ke: {filename}")

        # Target selector utama pembungkus form registrasi
        target_selector = 'div.MuiBox-root.css-1trv35u'

        try:
            # Beri sedikit waktu untuk animasi transisi UI selesai sebelum dijepret
            self.driver.sleep(0.5)

            element = self.driver.find_element(target_selector)
            # Menyimpan gambar dengan nama dinamis yang dikirimkan dari parameter
            element.save_screenshot(
                f"public/screenshots/registration/{filename}_element.png")
            print(
                f"[INFO] Screenshot elemen {filename}_element.png berhasil diambil.")

        except Exception as e:
            print(f"[WARNING] Gagal menangkap screenshot elemen: {e}")
            # Fallback: Jepret seluruh layar
            self.driver.save_screenshot(
                f"public/screenshots/registration/{filename}_fallback.png")
