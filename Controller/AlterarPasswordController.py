import re
from Model.Utilizador import Utilizador
from DAO.UtilizadorDAO import UtilizadorDAO
from Service.PasswordService import PasswordService

class UtilizadorController:
    """
    Controlador para gerir a lógica de negócio dos utilizadores.
    """
    def __init__(self):
        self.dao = UtilizadorDAO()

    def listar_utilizadores(self):
        return self.dao.get_all()

    def apagar_utilizador(self, user_id: int):
        self.dao.delete(user_id)
        
    def login(self, username, password):
        user = self.dao.get_by_username(username)
        if user and PasswordService.check_password(user.password_hash, password):
            return user
        return None

    # --- Lógica de Criação de Utilizador ---
    def criar_utilizador(self, nome: str, username: str, password: str, role: str) -> str:
        if not all([nome, username, password, role]):
            return "CAMPOS_INCOMPLETOS"

        email_regex = r"^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(email_regex, username):
            return "USERNAME_INVALIDO"

        if self.dao.get_by_username(username):
            return "USERNAME_EXISTENTE"
            
        hashed_password = PasswordService.hash_password(password)

        utilizador = Utilizador(id=None, nome=nome, username=username, password_hash=hashed_password, role=role)
        
        try:
            self.dao.add(utilizador)
            return "SUCESSO"
        except Exception:
            return "ERRO"
            
    # --- NOVO MÉTODO: Lógica de Alteração de Password ---
    def alterar_password(self, id: int, pass1: str, pass2: str) -> str:
        """
        Valida e atualiza a password do utilizador.
        
        Args:
            id: ID do utilizador.
            pass1: Nova password.
            pass2: Confirmação da nova password.

        Returns:
            Uma string com o resultado da operação.
        """
        if not pass1 or not pass2:
            return "CAMPOS_INCOMPLETOS"

        if pass1 != pass2:
            return "PASSWORDS_DIFERENTES"

        try:
            hashed_password = PasswordService.hash_password(pass1)
            self.dao.update_password(id, hashed_password)
            return "SUCESSO"
        except Exception:
            return "ERRO"