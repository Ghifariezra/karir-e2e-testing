import os
import atexit
from dotenv import load_dotenv
from core.singleton import Singleton
from seleniumbase import SB

load_dotenv()

class Driver(metaclass=Singleton):
    """Singleton class untuk mengelola instance SeleniumBase secara dinamis."""

    _os: os = os

    def __init__(self):
        is_headless = self._os.getenv("HEADLESS", "false").lower() == "true"

        self._sb_manager = SB(
            # uc=True,
            uc=False,
            chromium_arg="--ignore-certificate-errors",
            incognito=True,
            locale="id-ID",
            maximize=not is_headless,
            headless=is_headless,
            page_load_strategy="eager",
            disable_csp=True
        )

        # Mengekstrak instance native SeleniumBase
        self.driver = self._sb_manager.__enter__()

        # Mendaftarkan fungsi teardown agar jalan otomatis di akhir program
        atexit.register(self.quit)

    def get_driver(self):
        """Mengembalikan instance native SeleniumBase."""
        return self.driver

    def quit(self):
        """Menutup proses Context Manager SeleniumBase dengan aman."""
        try:
            if hasattr(self, '_sb_manager') and self._sb_manager:
                self._sb_manager.__exit__(None, None, None)
                self._sb_manager = None
                self.driver = None
                print("\n[DEBUG] Browser ditutup dengan aman.")
        except Exception as e:
            print(f"\n[DEBUG] Kesalahan saat menutup browser: {e}")
