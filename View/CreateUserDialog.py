from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from Model.Utilizador import Utilizador
from Service.PasswordService import PasswordService

class CreateUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Criar Utilizador")
        self.setFixedSize(300, 250)
        self.user_data = None

        layout = QVBoxLayout()

        # Widgets
        self.nome_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "funcionario"])

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.save)  # Conectar ao método save

        # Adicionar widgets ao layout
        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.nome_entry)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_entry)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_entry)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role_combo)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def save(self):
        # Obter valores dos campos
        nome = self.nome_entry.text().strip()
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        role = self.role_combo.currentText()

        # Validação dos campos
        if not all([nome, username, password, role]):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return

        # Hash da senha
        hashed_password = PasswordService.hash_password(password)

        # Criar o objeto Utilizador
        self.user_data = Utilizador(id=None, nome=nome, username=username, password_hash=hashed_password, role=role)

        # Fechar o diálogo com sucesso
        self.accept()  # Encerra o diálogo com a resposta 'Accepted'
