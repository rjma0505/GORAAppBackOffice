from PyQt5.QtWidgets import QMessageBox, QDialog
from DAO.UtilizadorDAO import UtilizadorDAO
from View.CreateUserDialog import CreateUserDialog
from View.AlterarPasswordDialog import AlterarPasswordDialog
from PyQt5.QtCore import QObject

class DashboardController(QObject):
    def __init__(self, dashboard_view, login_controller):
        super().__init__()
        self.dashboard_view = dashboard_view
        self.utilizador_dao = UtilizadorDAO()
        self.login_controller = login_controller

        # Conecta botões da view
        self.dashboard_view.btn_criar.clicked.connect(self.criar_utilizador)
        self.dashboard_view.btn_eliminar.clicked.connect(self.eliminar_utilizador)
        self.dashboard_view.btn_alterar_password.clicked.connect(self.abrir_alterar_password)
        self.dashboard_view.btn_logout.clicked.connect(self.fazer_logout)

        # Carrega lista inicial
        self.carregar_utilizadores()

    def carregar_utilizadores(self):
        self.dashboard_view.carregar_utilizadores()

    def criar_utilizador(self):
        dialog = CreateUserDialog(self.dashboard_view)
        if dialog.exec_() == QDialog.Accepted and dialog.user_data:
            try:
                sucesso = self.utilizador_dao.inserir(dialog.user_data)
                if sucesso:
                    QMessageBox.information(self.dashboard_view, "Sucesso", "Utilizador criado com sucesso.")
                    self.carregar_utilizadores()
                else:
                    QMessageBox.critical(self.dashboard_view, "Erro", "Erro ao criar utilizador.")
            except Exception as e:
                QMessageBox.critical(self.dashboard_view, "Erro", f"Erro ao criar utilizador: {str(e)}")

    def eliminar_utilizador(self):
        user_id = self.dashboard_view.get_selected_user_id()
        if user_id is None:
            QMessageBox.warning(self.dashboard_view, "Aviso", "Selecione um utilizador para eliminar.")
            return

        utilizador_a_eliminar = self.utilizador_dao.obter_por_id(user_id)
        if not utilizador_a_eliminar:
            QMessageBox.critical(self.dashboard_view, "Erro", "Utilizador não encontrado.")
            return

        if utilizador_a_eliminar.role == 'admin':
            n_admins = self.utilizador_dao.contar_admins()
            if n_admins <= 1:
                QMessageBox.warning(self.dashboard_view, "Acesso Negado", "Não é possível eliminar o único administrador do sistema.")
                return

        confirm = QMessageBox.question(self.dashboard_view, "Confirmação",
                                       f"Tem certeza que deseja eliminar o utilizador '{utilizador_a_eliminar.username}'?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            sucesso = self.utilizador_dao.apagar(user_id)
            if sucesso:
                QMessageBox.information(self.dashboard_view, "Sucesso", "Utilizador eliminado com sucesso.")
                self.carregar_utilizadores()
            else:
                QMessageBox.critical(self.dashboard_view, "Erro", "Erro ao eliminar utilizador.")

    def abrir_alterar_password(self):
        user_id = self.dashboard_view.get_selected_user_id()
        if not user_id:
            QMessageBox.warning(self.dashboard_view, "Aviso", "Selecione um utilizador para alterar a password.")
            return

        dialog = AlterarPasswordDialog(self.dashboard_view, utilizador_id=user_id)
        if dialog.exec_() == QDialog.Accepted:
            self.dashboard_view.mostrar_status("Password alterada com sucesso.")

    def fazer_logout(self):
        self.dashboard_view.close()
        self.login_controller.show_login()
