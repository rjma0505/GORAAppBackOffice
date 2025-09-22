import mysql.connector
from config import DB_CONFIG
from Model.Utilizador import Utilizador
from Service.PasswordService import PasswordService
import logging

class UtilizadorDAO:
    """Classe DAO para manipulação de utilizadores no banco de dados."""

    def _get_connection(self):
        """Cria e retorna uma conexão com o banco de dados."""
        return mysql.connector.connect(**DB_CONFIG)

    def obter_por_username(self, username: str):
        """Obtém um utilizador pelo username."""
        try:
            with self._get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = "SELECT * FROM utilizadores WHERE username = %s"
                    cursor.execute(sql, (username,))
                    data = cursor.fetchone()
                    if data:
                        return Utilizador(
                            id=data['id'],
                            nome=data['nome'],
                            username=data['username'],
                            password_hash=data['password_hash'],
                            role=data['role']
                        )
            return None
        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter utilizador por username: {e}")
            return None

    def get_all(self):
        """Lista todos os utilizadores."""
        utilizadores = []
        try:
            with self._get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = "SELECT id, nome, username, role FROM utilizadores ORDER BY nome"
                    cursor.execute(sql)
                    for data in cursor.fetchall():
                        utilizadores.append(Utilizador(
                            id=data['id'],
                            nome=data['nome'],
                            username=data['username'],
                            password_hash=None,  # Não necessário para listagem
                            role=data['role']
                        ))
            return utilizadores
        except mysql.connector.Error as e:
            logging.error(f"Erro ao listar utilizadores: {e}")
            return []

    def inserir(self, utilizador: Utilizador) -> bool:
        """Insere um novo utilizador no banco de dados."""
        try:
            if not utilizador.password_hash:
                logging.error("A senha deve estar hashada antes da inserção.")
                return False

            con = self._get_connection()
            cursor = con.cursor()
            sql = "INSERT INTO utilizadores (nome, username, password_hash, role) VALUES (%s, %s, %s, %s)"
            params = (utilizador.nome, utilizador.username, utilizador.password_hash, utilizador.role)
            cursor.execute(sql, params)
            con.commit()
            cursor.close()
            con.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Erro ao inserir utilizador: {err}")
            return False

    def apagar(self, user_id: int) -> bool:
        """Apaga um utilizador pelo ID."""
        try:
            con = self._get_connection()
            cursor = con.cursor()
            sql = "DELETE FROM utilizadores WHERE id = %s"
            cursor.execute(sql, (user_id,))
            con.commit()
            cursor.close()
            con.close()
            return True
        except mysql.connector.Error as e:
            logging.error(f"Erro ao apagar utilizador: {e}")
            return False

    def obter_por_id(self, user_id: int):
        """Obtém um utilizador pelo ID."""
        try:
            with self._get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = "SELECT * FROM utilizadores WHERE id = %s"
                    cursor.execute(sql, (user_id,))
                    data = cursor.fetchone()
                    if data:
                        return Utilizador(
                            id=data['id'],
                            nome=data['nome'],
                            username=data['username'],
                            password_hash=data['password_hash'],
                            role=data['role']
                        )
            return None
        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter utilizador por ID: {e}")
            return None

    def update_password(self, user_id: int, password_hash: str) -> bool:
        """Atualiza a password de um utilizador."""
        try:
            con = self._get_connection()
            cursor = con.cursor()
            sql = "UPDATE utilizadores SET password_hash = %s WHERE id = %s"
            cursor.execute(sql, (password_hash, user_id))
            con.commit()
            cursor.close()
            con.close()
            return True
        except mysql.connector.Error as e:
            logging.error(f"Erro ao atualizar password: {e}")
            return False

    def contar_admins(self) -> int:
        """Conta o número de utilizadores com role 'admin'."""
        try:
            with self._get_connection() as con:
                with con.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM utilizadores WHERE role = 'admin'"
                    cursor.execute(sql)
                    count = cursor.fetchone()[0]
                    return count
        except mysql.connector.Error as e:
            logging.error(f"Erro ao contar administradores: {e}")
            return 0

    def get_by_username(self, username: str):
        """Verifica se um utilizador existe pelo username (retorna Utilizador ou None)."""
        return self.obter_por_username(username)

    def existe_email(self, username: str) -> bool:
        """Verifica se o username/email já existe no banco."""
        try:
            with self._get_connection() as con:
                with con.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM utilizadores WHERE username = %s"
                    cursor.execute(sql, (username,))
                    count = cursor.fetchone()[0]
                    return count > 0
        except mysql.connector.Error as e:
            logging.error(f"Erro ao verificar email: {e}")
            return False
