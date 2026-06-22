import pytest
from core.karir import Karir


@pytest.mark.run(order=1)
def test_search_happy_path():
    """Test Case: Pencarian lowongan dengan keyword dan lokasi valid"""
    app = Karir()
    app.formSearch()


@pytest.mark.run(order=2)
def test_search_posisi_only():
    """Test Case: Pencarian lowongan dengan keyword posisi saja"""
    app = Karir()
    app.formSearch_PosisiOnly()


@pytest.mark.run(order=3)
def test_search_lokasi_only():
    """Test Case: Pencarian lowongan dengan keyword lokasi saja"""
    app = Karir()
    app.formSearch_LokasiOnly()


@pytest.mark.run(order=4)
def test_search_negative_empty_fields():
    """Test Case (Negative): Pencarian dikosongkan, validasi URL parameter"""
    app = Karir()
    app.formSearch_Negative_EmptyFields()


@pytest.mark.run(order=5)
def test_search_with_filter():
    """Test Case: Menggunakan modal Semua Filter untuk menyaring lowongan"""
    app = Karir()
    app.formSearch_Filter()
