import bcrypt
from typing import Optional

class Utilizador:
    """
    Representa um utilizador do sistema.
    """
    def __init__(self, id: Optional[int] = None, nome: Optional[str] = None, 
                 username: Optional[str] = None, password_hash: Optional[str] = None, 
                 role: Optional[str] = None, criado_em: Optional[str] = None):
        """
        Inicializa um novo objeto Utilizador.
        """
        self.id = id
        self.nome = nome
        self.username = username
        self.password_hash = password_hash
        
        # Validação do 'role'
        if role not in ["admin", "funcionario"]:
            raise ValueError("O 'role' deve ser 'admin' ou 'funcionario'.")
        self.role = role

        # Atributo para armazenar a data de criação
        self.criado_em = criado_em

    def __str__(self) -> str:
        """
        Retorna uma representação em string do utilizador.
        """
        return f"Utilizador(id={self.id}, nome='{self.nome}', username='{self.username}', role='{self.role}', criado_em='{self.criado_em}')"
    
    def verificar_password(self, password: str) -> bool:
        """
        Verifica se a senha fornecida corresponde à senha armazenada (usando bcrypt).
        """
        if self.password_hash:
            # A bcrypt retorna o hash como 'bytes', então converte para 'str' antes de comparar
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        return False

    def to_dict(self) -> dict:
        """
        Retorna o utilizador como um dicionário (útil para APIs ou exportação de dados).
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "username": self.username,
            "role": self.role,
            "criado_em": self.criado_em  # Adicionando o campo 'criado_em' ao dicionário
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Utilizador':
        """
        Constrói um objeto Utilizador a partir de um dicionário de dados.
        """
        return cls(
            id=data.get('id'),
            nome=data.get('nome'),
            username=data.get('username'),
            password_hash=data.get('password_hash'),
            role=data.get('role'),
            criado_em=data.get('criado_em')  # Atribuindo o campo 'criado_em'
        )
