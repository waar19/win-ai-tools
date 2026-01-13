"""
Windows AI Removal Tool
Aplicación para gestionar y remover servicios de AI de Windows 11
"""

import sys
import ctypes
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow


def is_admin():
    """Verifica si la aplicación se ejecuta como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Verificar permisos de administrador
    if not is_admin():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Permisos Requeridos")
        msg.setText("Esta aplicación requiere permisos de administrador para modificar configuraciones del sistema.")
        msg.setInformativeText("Por favor, ejecute la aplicación como Administrador.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        # Continuar de todos modos para mostrar la interfaz (solo lectura)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
