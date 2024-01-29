from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)
password = "alallddm1722"
encrypted_password = cipher_suite.encrypt(password.encode()).decode()
print(encrypted_password)


decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

print(decrypted_password)