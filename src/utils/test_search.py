from core.base_scenario import BaseJobScenario
from seleniumbase import BaseCase


class TestJobSearch(BaseJobScenario):
    def __init__(self, driver: BaseCase):
        super().__init__()
        self.driver = driver

    # ---> INI ADALAH IMPLEMENTASI METODE ABSTRAK YANG DIMINTA <---
    def testSearchJob(self, keyword="Programmer", location="Jakarta"):
        print(
            f"[DEBUG] Menjalankan testSearchJob dengan keyword '{keyword}' dan lokasi '{location}'")
        self.testKeyword(keyword)
        self.testLocation(location)
        self.clickSearchButton()

    def _type_autocomplete(self, placeholder_text, value):
        """Helper khusus untuk komponen MuiAutocomplete"""
        print(f"[DEBUG] Menunggu render input '{placeholder_text}'...")

        # Selector sangat bersih dan langsung menembak placeholder
        selector = f"input[placeholder='{placeholder_text}']"
        self.driver.wait_for_element_visible(selector, timeout=15)

        # 1. Klik untuk fokus
        self.driver.click(selector)
        self.driver.sleep(0.5)

        # 2. Ketik teks pencarian
        self.driver.type(selector, value)

        # 3. Jeda sejenak agar Material-UI sempat melakukan fetch API
        # dan merender dropdown pop-up list
        self.driver.sleep(2)

        # 4. Tekan tombol ENTER untuk mengonfirmasi opsi teratas / text input
        self.driver.send_keys(selector, "\n")
        self.driver.sleep(0.5)
        print(
            f"[DEBUG] Berhasil mengisi '{placeholder_text}' dengan '{value}'")

    def testKeyword(self, keyword="Software Engineer"):
        print(f"[DEBUG] Mengisi keyword pencarian: {keyword}")
        self._type_autocomplete("Posisi atau Perusahaan", keyword)

    def testLocation(self, location="Jakarta"):
        print(f"[DEBUG] Mengisi lokasi pencarian: {location}")
        self._type_autocomplete("Lokasi", location)

    def clickSearchButton(self):
        print("[DEBUG] Menekan tombol Cari")
        self.driver.click('button:contains("Cari")')

    def saveScreenshot(self, filename="screenshot_search.png"):
        print(f"[DEBUG] Menyimpan screenshot search: {filename}")
        self.driver.sleep(0.5)
        self.driver.save_screenshot(
            f"public/screenshots/search/{filename}.png")

    # =========== FILTERS ===========

    def openFilterTab(self, tab_name="Semua Filter"):
        print(f"[DEBUG] Membuka tab filter: '{tab_name}'...")

        self.driver.execute_script(f"""
            var paragraphs = document.querySelectorAll("p.css-mem2yx");
            for (var p of paragraphs) {{
                if (p.textContent.trim() === "{tab_name}") {{
                    var clickTarget = p.parentElement;
                    if (clickTarget) clickTarget.click();
                    break;
                }}
            }}
        """)

        if tab_name == "Semua Filter":
            print("[DEBUG] Menunggu render modal filter...")

            # Tunggu elemen yang SPESIFIK untuk advance filter modal
            # bukan cuma .MuiModal-root generik yang bisa ada banyak
            self.driver.wait_for_element_present(
                '.advance-filter', timeout=15
            )
            self.driver.wait_for_element_present(
                '.advance-filter label.MuiFormControlLabel-root', timeout=15
            )
            self.driver.sleep(2)
            print("[DEBUG] Modal filter dan label checkbox sudah siap.")


    def selectFilterCheckbox(self, label_text):
        print(f"[DEBUG] Memilih opsi filter: '{label_text}'")

        # Tunggu .advance-filter sudah ada dan punya label
        self.driver.wait_for_element_present(
            '.advance-filter label.MuiFormControlLabel-root', timeout=15)

        # Query dengan selector yang SPESIFIK ke .advance-filter, bukan .MuiModal-root
        self.driver.execute_script(f"""
            (function() {{
                var container = document.querySelector('.advance-filter');
                if (!container) {{
                    console.log('advance-filter container not found');
                    return;
                }}
                var labels = container.querySelectorAll('label.MuiFormControlLabel-root');
                console.log('Found labels: ' + labels.length);
                for (var i = 0; i < labels.length; i++) {{
                    var text = labels[i].textContent.trim();
                    console.log('Label ' + i + ': ' + text);
                    if (text.includes("{label_text}")) {{
                        var input = labels[i].querySelector('input[type="checkbox"]');
                        if (input) {{
                            input.click();
                            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            console.log('Clicked: ' + text);
                        }}
                    }}
                }}
            }})()
        """)

        # Verifikasi dengan cara cek apakah checkbox sudah checked
        # pakai wait_for_element_present dengan selector attribute checked
        self.driver.sleep(0.5)
        print(f"[DEBUG] Selesai klik checkbox: '{label_text}'")


    def applyFilters(self):
        print("[DEBUG] Menerapkan filter (Menekan tombol Terapkan)...")

        self.driver.wait_for_element_present(
            '.advance-filter .MuiButton-filledPrimary', timeout=10)

        self.driver.execute_script("""
            (function() {
                var container = document.querySelector('.advance-filter');
                if (!container) return;
                var buttons = container.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.trim().includes('Terapkan')) {
                        buttons[i].click();
                        return;
                    }
                }
            })()
        """)

        self.driver.wait_for_element_absent('.advance-filter', timeout=15)
        self.driver.sleep(1)
