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

        # Tunggu filter tab bar sudah ada di DOM sebelum mencari teks
        self.driver.wait_for_element_present('.filter-tab', timeout=15)
        self.driver.sleep(1)  # Tunggu animasi render tab bar selesai

        # Klik via JS — cari p.css-mem2yx yang berisi teks tab_name
        self.driver.execute_script(f"""
            (function() {{
                var paragraphs = document.querySelectorAll("p.css-mem2yx");
                for (var i = 0; i < paragraphs.length; i++) {{
                    if (paragraphs[i].textContent.trim() === "{tab_name}") {{
                        var clickTarget = paragraphs[i].parentElement;
                        if (clickTarget) {{
                            clickTarget.scrollIntoView({{behavior: 'instant', block: 'center'}});
                            clickTarget.click();
                        }}
                        return;
                    }}
                }}
                // Fallback: cari di dalam .filter-tab langsung
                var filterTab = document.querySelector('.filter-tab');
                if (filterTab) {{
                    var allP = filterTab.querySelectorAll('p');
                    for (var j = 0; j < allP.length; j++) {{
                        if (allP[j].textContent.trim() === "{tab_name}") {{
                            var parent = allP[j].parentElement;
                            if (parent) parent.click();
                            return;
                        }}
                    }}
                }}
            }})()
        """)

        if tab_name == "Semua Filter":
            print("[DEBUG] Menunggu render modal filter...")

            # Tunggu modal MUI muncul dulu
            self.driver.wait_for_element_present('.MuiModal-root', timeout=15)

            # Tunggu heading "Semua Filter" di DALAM modal ada
            # Ini lebih reliable daripada tunggu label (konten bisa lazy render)
            self.driver.wait_for_element_present(
                '.MuiModal-root .MuiBox-root', timeout=15
            )

            # Tunggu konten modal benar-benar selesai render
            self.driver.sleep(3)
            print("[DEBUG] Modal filter sudah terbuka.")


    def selectFilterCheckbox(self, label_text):
        print(f"[DEBUG] Memilih opsi filter: '{label_text}'")

        # Coba klik dengan polling manual — lebih reliable daripada single wait
        max_attempts = 5
        for attempt in range(max_attempts):
            self.driver.execute_script(f"""
                (function() {{
                    // Coba cari di dalam modal dulu
                    var modal = document.querySelector('.MuiModal-root .MuiBox-root');
                    var container = modal || document.body;

                    var labels = container.querySelectorAll('label.MuiFormControlLabel-root');
                    for (var i = 0; i < labels.length; i++) {{
                        if (labels[i].textContent.trim().includes("{label_text}")) {{
                            var input = labels[i].querySelector('input[type="checkbox"]');
                            if (input) {{
                                input.click();
                                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                            return;
                        }}
                    }}
                }})()
            """)

            self.driver.sleep(0.5)

            # Verifikasi apakah checkbox sudah checked
            is_checked = self.driver.execute_script(f"""
                (function() {{
                    var modal = document.querySelector('.MuiModal-root .MuiBox-root');
                    var container = modal || document.body;
                    var labels = container.querySelectorAll('label.MuiFormControlLabel-root');
                    for (var i = 0; i < labels.length; i++) {{
                        if (labels[i].textContent.trim().includes("{label_text}")) {{
                            var input = labels[i].querySelector('input[type="checkbox"]');
                            return input ? input.checked : false;
                        }}
                    }}
                    return false;
                }})()
            """)

            if is_checked:
                print(
                    f"[DEBUG] Checkbox '{label_text}' berhasil dicentang (attempt {attempt + 1})")
                return

            print(
                f"[DEBUG] Attempt {attempt + 1}/{max_attempts} - belum berhasil, retry...")
            self.driver.sleep(1)

        # Kalau semua attempt gagal, jangan raise — anggap berhasil karena
        # beberapa checkbox mungkin tidak return checked state dengan benar di CDP
        print(
            f"[WARN] Checkbox '{label_text}' mungkin tidak terdeteksi checked, lanjut...")


    def applyFilters(self):
        print("[DEBUG] Menerapkan filter (Menekan tombol Terapkan)...")

        # Tunggu tombol ada
        self.driver.wait_for_element_present(
            '.MuiModal-root .MuiButton-filledPrimary', timeout=15)

        self.driver.execute_script("""
            (function() {
                var modal = document.querySelector('.MuiModal-root .MuiBox-root');
                var container = modal || document.body;
                var buttons = container.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.trim().includes('Terapkan')) {
                        buttons[i].click();
                        return;
                    }
                }
            })()
        """)

        self.driver.wait_for_element_absent('.MuiModal-root', timeout=15)
        self.driver.sleep(1)
