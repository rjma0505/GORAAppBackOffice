from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QAbstractItemView, QHeaderView
)
from PyQt5.QtCore import QTimer
from Controller.UtilizadorController import UtilizadorController

class DashboardView(QWidget):
    def __init__(self, login_controller, parent=None):
        super().__init__(parent)
        self.login_controller = login_controller
        self.setWindowTitle("Dashboard - Gestão de Utilizadores")
        self.resize(800, 500)
        self.controller = UtilizadorController()

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Botões
        button_layout = QHBoxLayout()
        self.btn_criar = QPushButton("Criar Utilizador")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_alterar_password = QPushButton("Alterar Password")
        self.btn_logout = QPushButton("Logout")

        button_layout.addWidget(self.btn_criar)
        button_layout.addWidget(self.btn_eliminar)
        button_layout.addWidget(self.btn_alterar_password)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_logout)
        main_layout.addLayout(button_layout)

        # Tabela de utilizadores
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Username", "Perfil"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Barra de status
        self.lbl_status = QLabel(" ")
        self.lbl_status.setStyleSheet("background-color: lightgray; padding: 5px; border: 1px solid gray;")
        main_layout.addWidget(self.lbl_status)

        # Conecta botões aos métodos (serão sobrescritos pelo controller)
        self.btn_criar.clicked.connect(lambda: None)
        self.btn_eliminar.clicked.connect(lambda: None)
        self.btn_alterar_password.clicked.connect(lambda: None)
        self.btn_logout.clicked.connect(lambda: None)

    def carregar_utilizadores(self):
        """Carrega todos os utilizadores na tabela."""
        users = self.controller.listar_utilizadores()
        self.table.setRowCount(0)
        for row_idx, user in enumerate(users):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(user.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(user.nome))
            self.table.setItem(row_idx, 2, QTableWidgetItem(user.username))
            self.table.setItem(row_idx, 3, QTableWidgetItem(user.role))

    def get_selected_user_id(self):
        selected = self.table.currentRow()
        if selected >= 0:
            item = self.table.item(selected, 0)
            return int(item.text()) if item else None
        return None

    def mostrar_status(self, mensagem, sucesso=True):
        style = "background-color: green; color: black; padding: 5px;" if sucesso else "background-color: red; color: black; padding: 5px;"
        self.lbl_status.setStyleSheet(style)
        self.lbl_status.setText(mensagem)
        QTimer.singleShot(3000, lambda: self.lbl_status.setText(" "))
