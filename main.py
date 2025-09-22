import sys
from PyQt5.QtWidgets import QApplication
from View.LoginView import LoginView
from Controller.LoginController import LoginController
from Controller.DashboardController import DashboardController

if __name__ == "__main__":
    app = QApplication(sys.argv)  # ✅ Isto tem de vir antes de qualquer QWidget

    login_view = LoginView()
    LoginController(login_view)

    login_view.show()
    sys.exit(app.exec_())  # ✅ Mantém a aplicação viva
