from core.base_scenario import BaseLoginScenario
from seleniumbase import BaseCase


class TestLogin(BaseLoginScenario):
    def __init__(self, driver: BaseCase):
        super().__init__()
        self.driver = driver

    def _get_input_css(self, label_text):
        """Helper robust untuk mencari input via label di Material-UI."""
        print(
            f"[DEBUG] Menunggu render teks '{label_text}' di halaman login...")
        self.driver.sleep(1.5)

        label_xpath = f"//label[contains(., '{label_text}')]"
        self.driver.wait_for_element(label_xpath, timeout=15, by="xpath")

        js_script = f"""
            (function() {{
                var xpath = "//label[contains(., '{label_text}')]";
                var label = document.evaluate(
                    xpath, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null
                ).singleNodeValue;

                if (!label) return null;

                if (label.htmlFor) {{
                    var el = document.getElementById(label.htmlFor);
                    if (el) {{
                        if (el.id) return '#' + el.id;
                        el.id = 'sb_dyn_{label_text.replace(" ", "_")}';
                        return '#' + el.id;
                    }}
                }}

                var container = label.closest('.MuiFormControl-root, .MuiTextField-root, div');
                if (container) {{
                    var input = container.querySelector('input');
                    if (input) {{
                        if (!input.id) input.id = 'sb_dyn_{label_text.replace(" ", "_")}';
                        return '#' + input.id;
                    }}
                }}
                return null;
            }})();
        """

        for attempt in range(3):
            dynamic_id = self.driver.execute_script(js_script)
            if dynamic_id:
                return dynamic_id
            self.driver.sleep(1)

        fallback_xpath = f"//label[contains(., '{label_text}')]/following-sibling::div//input | //label[contains(., '{label_text}')]/..//input"
        try:
            self.driver.wait_for_element(fallback_xpath, timeout=5, by="xpath")
            return fallback_xpath
        except Exception:
            raise Exception(
                f"Gagal menemukan elemen input login untuk: '{label_text}'")

    def _type_by_label(self, label_text, value):
        selector = self._get_input_css(label_text)
        if selector.startswith("//"):
            self.driver.type(selector, value, by="xpath")
        else:
            self.driver.type(selector, value)

    def testEmail(self, email_input="testuser@email.com"):
        print(f"[DEBUG] Mengisi Email Login: {email_input}")
        self._type_by_label("Masukan alamat Email", email_input)

    def testPassword(self, password_input="ValidPass123!"):
        print("[DEBUG] Mengisi Password Login")
        self._type_by_label("Masukan Password", password_input)

    # DIPERBARUI: Dibuat dinamis agar bisa menerima teks tombol yang berbeda
    def clickSubmitButton(self, button_text="Lanjutkan"):
        print(f"[DEBUG] Menekan tombol aksi form: '{button_text}'")
        self.driver.click(f'button:contains("{button_text}")')

    def assertSubmitButtonDisabled(self):
        print("[DEBUG] Memvalidasi tombol Lanjutkan terkunci (Disabled)")
        self.driver.assert_element('button[disabled]:contains("Lanjutkan")')

    def saveScreenshot(self, filename="screenshot_login.png"):
        print(f"[DEBUG] Menyimpan screenshot login: {filename}")
        self.driver.sleep(0.5)
        self.driver.save_screenshot(f"public/screenshots/login/{filename}.png")
