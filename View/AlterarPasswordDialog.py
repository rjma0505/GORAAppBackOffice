from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Service.PasswordService import PasswordService
from Controller.UtilizadorController import UtilizadorController

class AlterarPasswordDialog(QDialog):
    def __init__(self, parent=None, utilizador_id=None):
        """
        Inicializa o diálogo para alterar a password.

        Args:
            parent: A janela pai.
            utilizador_id: O ID do utilizador cuja password será alterada.
        """
        super().__init__(parent)
        self.setWindowTitle("Alterar Password")
        self.setFixedSize(300, 150)
        self.utilizador_id = utilizador_id
        self.controller = UtilizadorController()  # Instancia o controller para a lógica de negócio

        self.inicializarComponentes()

    def inicializarComponentes(self):
        """
        Cria e organiza os widgets do diálogo.
        """
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Campos de password
        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode(QLineEdit.Password)

        self.txtPasswordRepeat = QLineEdit()
        self.txtPasswordRepeat.setEchoMode(QLineEdit.Password)

        # Botões
        self.btnGravar = QPushButton("Gravar")
        self.btnCancelar = QPushButton("Cancelar")

        # Adicionar widgets ao layout de grade
        grid_layout.addWidget(QLabel("Nova Password:"), 0, 0)
        grid_layout.addWidget(self.txtPassword, 0, 1)
        grid_layout.addWidget(QLabel("Confirmar Password:"), 1, 0)
        grid_layout.addWidget(self.txtPasswordRepeat, 1, 1)

        # Adicionar botões ao layout vertical
        layout.addLayout(grid_layout)
        layout.addWidget(self.btnGravar)
        layout.addWidget(self.btnCancelar)

        self.setLayout(layout)

        # Conectar sinais aos slots (eventos)
        self.btnGravar.clicked.connect(self.gravar)
        self.btnCancelar.clicked.connect(self.reject)

    def gravar(self):
        """
        Valida e grava a nova password através do controller.
        """
        pass1 = self.txtPassword.text()
        pass2 = self.txtPasswordRepeat.text()

        # Verifica se os campos estão preenchidos
        if not pass1 or not pass2:
            QMessageBox.warning(self, "Erro", "Preencha ambas as passwords.")
            return

        # Verifica se as senhas coincidem
        if pass1 != pass2:
            QMessageBox.warning(self, "Erro", "As passwords não coincidem.")
            return

        # Atualiza a password usando o controller
        try:
            self.controller.alterar_password(self.utilizador_id, pass1)
            QMessageBox.information(self, "Sucesso", "Password atualizada com sucesso.")
            self.accept()  # Fecha o diálogo
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar a password: {e}")