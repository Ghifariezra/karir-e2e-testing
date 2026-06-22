import pytest
from core.karir import Karir


@pytest.mark.run(order=1)
def test_regis_happy_path():
    app = Karir()
    app.formLogin()

@pytest.mark.run(order=2)
def test_login_negative_empty_fields():
    app = Karir()
    app.formLogin_Negative_EmptyFields()
    
@pytest.mark.run(order=3)
def test_login_negative_invalid_email():
    app = Karir()
    app.formLogin_Negative_InvalidEmail()
