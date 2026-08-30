from app.core.security import hash_password, verify_password

def test_password_hash_is_not_reversible_plaintext():
    hashed = hash_password("CorrectHorseBatteryStaple123")
    assert hashed != "CorrectHorseBatteryStaple123"
    assert verify_password("CorrectHorseBatteryStaple123", hashed)
    assert not verify_password("WrongPassword123", hashed)
