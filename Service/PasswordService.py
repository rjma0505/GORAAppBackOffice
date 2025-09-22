# service/password_service.py

import bcrypt

class PasswordService:
    @staticmethod
    def hash_password(plain_password):
        """Gera o hash de uma password em texto simples."""
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verifica se a password em texto simples corresponde ao hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))