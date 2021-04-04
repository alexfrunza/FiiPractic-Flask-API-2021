from src.utils.validators import validate_email


class TestUserValidation:

    def test_user_email_validation_success(self):
        email = 'test@test.com'
        valid = True
        try:
            validate_email(email)
        except Exception:
            valid = False

        assert valid

    def test_user_email_validation_failed(self):
        email = 'test@test.comasfda+'
        valid = True
        try:
            validate_email(email)
        except Exception:
            valid = False

        assert not valid
