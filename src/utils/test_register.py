from core.base_scenario import BaseRegistrationScenario
from seleniumbase import BaseCase

class TestRegistration(BaseRegistrationScenario):
    def __init__(self, driver: BaseCase):
        super().__init__()
        self.driver = driver

    def _get_input_css(self, label_text):
        """
        Helper yang robust: cari input via label, dengan fallback bertingkat.
        Mendukung input MUI yang tidak punya 'id'.
        """
        print(f"[DEBUG] Menunggu render teks '{label_text}' di halaman...")
        self.driver.sleep(1.5)

        label_xpath = f"//label[contains(., '{label_text}')]"

        # Pastikan label ada dulu di DOM
        self.driver.wait_for_element(label_xpath, timeout=25, by="xpath")

        js_script = f"""
            (function() {{
                var xpath = "//label[contains(., '{label_text}')]";
                var label = document.evaluate(
                    xpath, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null
                ).singleNodeValue;

                if (!label) return null;

                // Strategi 1: pakai htmlFor / for → cari by id
                if (label.htmlFor) {{
                    var el = document.getElementById(label.htmlFor);
                    if (el) {{
                        if (el.id) return '#' + el.id;
                        // input ada tapi tidak punya id → beri id sementara
                        el.id = 'sb_dyn_{label_text.replace(" ", "_")}';
                        return '#' + el.id;
                    }}
                }}

                // Strategi 2: cari input di dalam container MUI terdekat
                var container = label.closest(
                    '.MuiFormControl-root, .MuiTextField-root, .MuiInputBase-root'
                );
                if (!container) {{
                    // Strategi 3: naik ke parent div lalu cari input di dalamnya
                    container = label.parentElement;
                    while (container && container.tagName !== 'FORM') {{
                        var input = container.querySelector('input, textarea');
                        if (input) {{
                            if (!input.id) {{
                                input.id = 'sb_dyn_{label_text.replace(" ", "_")}';
                            }}
                            return '#' + input.id;
                        }}
                        container = container.parentElement;
                    }}
                    return null;
                }}

                var input = container.querySelector('input, textarea, select');
                if (input) {{
                    if (!input.id) {{
                        input.id = 'sb_dyn_{label_text.replace(" ", "_")}';
                    }}
                    return '#' + input.id;
                }}

                return null;
            }})();
        """

        for attempt in range(5):
            dynamic_id = self.driver.execute_script(js_script)
            if dynamic_id:
                print(
                    f"[DEBUG] Selector ditemukan: '{dynamic_id}' untuk '{label_text}'")
                return dynamic_id
            print(
                f"[DEBUG] JS DOM belum stabil. Retry ke-{attempt+1} untuk '{label_text}'...")
            self.driver.sleep(2.0)

        # ── Fallback terakhir: gunakan XPath langsung via SeleniumBase ──────────
        # Ini menghindari kebutuhan CSS id sama sekali
        fallback_xpath = (
            f"//label[contains(., '{label_text}')]"
            f"/following-sibling::div//input | "
            f"//label[contains(., '{label_text}')]"
            f"/..//input"
        )
        try:
            self.driver.wait_for_element(fallback_xpath, timeout=10, by="xpath")
            print(f"[DEBUG] Fallback XPath berhasil untuk '{label_text}'")
            return fallback_xpath  # ← return XPath string, bukan CSS
        except Exception:
            pass

        raise Exception(
            f"Gagal menemukan elemen input untuk label: '{label_text}'")

    def _type_by_label(self, label_text, value):
        """Ketik nilai ke input yang ditemukan via label. Handle CSS dan XPath."""
        selector = self._get_input_css(label_text)
        if selector.startswith("//") or selector.startswith("(//"):
            self.driver.type(selector, value, by="xpath")
        else:
            self.driver.type(selector, value)


    def _click_by_label(self, label_text):
        """Klik input yang ditemukan via label."""
        selector = self._get_input_css(label_text)
        if selector.startswith("//") or selector.startswith("(//"):
            self.driver.click(selector, by="xpath")
        else:
            self.driver.click(selector)


    def testFullName(self, name_input="Test User"):
        print(f"[DEBUG] Mengisi Nama Lengkap: {name_input}")
        self._type_by_label("Nama Lengkap", name_input)


    def testEmail(self, email_input="testuser@example.com"):
        print(f"[DEBUG] Mengisi Email: {email_input}")
        self._type_by_label("Email", email_input)


    def testPhoneNumber(self, phone_input="081234567890"):
        print(f"[DEBUG] Mengisi Nomor Ponsel: {phone_input}")
        self._type_by_label("Nomor Ponsel", phone_input)


    def testPassword(self, password_input="ValidPass123!"):
        print("[DEBUG] Mengisi Password")
        self._type_by_label("Password", password_input)


    def testPasswordConfirmation(self, confirm_input="ValidPass123!"):
        print("[DEBUG] Mengisi Konfirmasi Password")
        self._type_by_label("Konfirmasi Password", confirm_input)

    def submitForm(self):
        print("[DEBUG] Menekan tombol Lanjutkan")
        # Menggunakan pencarian text murni bawaan SeleniumBase
        # yang otomatis dikonversi dengan aman di UC Mode
        self.driver.click('button:contains("Lanjutkan")')
        
    def triggerBlurValidation(self, label_text):
        print(f"[DEBUG] Memicu validasi onBlur untuk: {label_text}")
        self._click_by_label(label_text)
        self.driver.sleep(0.5)
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
