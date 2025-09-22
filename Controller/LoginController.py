from PyQt5.QtWidgets import QMessageBox
from DAO.UtilizadorDAO import UtilizadorDAO
from Service.PasswordService import PasswordService
from View.DashboardView import DashboardView
from Controller.DashboardController import DashboardController

class LoginController:
    def __init__(self, login_view):
        self.login_view = login_view
        self.utilizador_dao = UtilizadorDAO()
        self.dashboard_view = None
        self.login_view.set_login_command(self.authenticate)

    def show_login(self):
        """Mostra a janela de login limpa e ativa."""
        self.login_view.limpar_campos()  # limpa campos
        self.login_view.show()
        self.login_view.raise_()
        self.login_view.activateWindow()

    def authenticate(self, username, password):
        if not username or not password:
            QMessageBox.warning(self.login_view, "Erro de Login", "Por favor, preencha todos os campos.")
            return None

        user = self.utilizador_dao.obter_por_username(username)

        if user and PasswordService.verify_password(password, user.password_hash):
            if user.role == 'admin':
                self.login_view.hide()
                self.open_dashboard()
                return user
            else:
                QMessageBox.warning(self.login_view, "Acesso Negado", "Apenas administradores podem aceder ao backoffice.")
        else:
            QMessageBox.warning(self.login_view, "Erro de Login", "Credenciais inválidas.")
        return None

    def open_dashboard(self):
        """Abre o Dashboard e inicializa o controller."""
        self.dashboard_view = DashboardView(login_controller=self)
        self.dashboard_controller = DashboardController(self.dashboard_view, self)
        self.dashboard_view.show()
        self.dashboard_view.raise_()
        self.dashboard_view.activateWindow()
