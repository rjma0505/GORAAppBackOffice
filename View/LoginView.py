from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 150)

        # Layout principal
        layout = QVBoxLayout()

        # Criação dos widgets
        self.lbl_user = QLabel("Username:")
        self.txt_user = QLineEdit()
        self.lbl_pass = QLabel("Password:")
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton("Entrar")

        # Adicionando os widgets ao layout
        layout.addWidget(self.lbl_user)
        layout.addWidget(self.txt_user)
        layout.addWidget(self.lbl_pass)
        layout.addWidget(self.txt_pass)
        layout.addWidget(self.btn_login)

        # Definindo o layout da janela
        self.setLayout(layout)

        # Comando de login externo (definido pelo controller)
        self._login_command = None

    def set_login_command(self, command):
        self._login_command = command
        try:
            self.btn_login.clicked.disconnect(self._on_login_clicked)
        except TypeError:
            pass
        self.btn_login.clicked.connect(self._on_login_clicked)

    def _on_login_clicked(self):
        username = self.txt_user.text()
        password = self.txt_pass.text()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha ambos os campos.", QMessageBox.Ok)
            return

        if self._login_command:
            user = self._login_command(username, password)
            if user:
                print("Login bem-sucedido!")
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.", QMessageBox.Ok)

    # 🔹 Método para limpar os campos ao mostrar login novamente
    def limpar_campos(self):
        self.txt_user.clear()
        self.txt_pass.clear()
