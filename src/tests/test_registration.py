import pytest
from core.karir import Karir


@pytest.mark.run(order=1)
def test_regis_happy_path():
    app = Karir()
    app.formRegistration()


@pytest.mark.run(order=2)
def test_regis_neg_empty_fields():
    app = Karir()
    app.formRegistration_Negative_EmptyFields()


@pytest.mark.run(order=3)
def test_regis_neg_invalid_email():
    app = Karir()
    app.formRegistration_Negative_InvalidEmail()


@pytest.mark.run(order=4)
def test_regis_neg_phone_max():
    app = Karir()
    app.formRegistration_Negative_Phone_ExceedsMax()


@pytest.mark.run(order=5)
def test_regis_neg_phone_min():
    app = Karir()
    app.formRegistration_Negative_Phone_BelowMin()


@pytest.mark.run(order=6)
def test_regis_neg_password_weak():
    app = Karir()
    app.formRegistration_Negative_Password_Weak()


@pytest.mark.run(order=7)
def test_regis_neg_password_mismatch():
    app = Karir()
    app.formRegistration_Negative_Password_Mismatch()
