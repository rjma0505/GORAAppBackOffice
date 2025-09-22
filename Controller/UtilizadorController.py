# -----------------------------
# File: Controller/UtilizadorController.py
# -----------------------------
import re
from Model.Utilizador import Utilizador
from DAO.UtilizadorDAO import UtilizadorDAO
from Service.PasswordService import PasswordService

class UtilizadorController:
    def __init__(self):
        self.dao = UtilizadorDAO()

    # Criação por campos individuais (já existente)
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
            self.dao.inserir(utilizador)
            return "SUCESSO"
        except Exception:
            return "ERRO"

    # Novo método: cria a partir de um objeto Utilizador diretamente
    def criar_utilizador_obj(self, utilizador: Utilizador) -> bool:
        """
        Cria um utilizador a partir de um objeto Utilizador e grava na base.
        Retorna True se gravado com sucesso, False caso contrário.
        """
        if self.dao.get_by_username(utilizador.username):
            return False  # Já existe
        try:
            return self.dao.inserir(utilizador)
        except Exception:
            return False

    # Listar usuários
    def listar_utilizadores(self):
        return self.dao.get_all()

    # Apagar usuário
    def apagar_utilizador(self, user_id: int):
        self.dao.apagar(user_id)

    # Alterar password
    def alterar_password(self, user_id, new_password):
        hashed_password = PasswordService.hash_password(new_password)
        self.dao.update_password(user_id, hashed_password)

    # Login
    def login(self, username, password):
        user = self.dao.get_by_username(username)
        if user and PasswordService.verify_password(password, user.password_hash):
            return user
        return None
