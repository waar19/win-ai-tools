"""
Estilos CSS-like para PyQt6
Tema oscuro moderno para la aplicación
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a2e;
}

QWidget {
    background-color: #1a1a2e;
    color: #eaeaea;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

QLabel {
    color: #eaeaea;
}

QLabel#title {
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
    padding: 10px;
}

QLabel#subtitle {
    font-size: 14px;
    color: #888888;
    padding: 5px 10px;
}

QPushButton {
    background-color: #16213e;
    color: #eaeaea;
    border: 2px solid #0f3460;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    min-width: 120px;
}

QPushButton:hover {
    background-color: #0f3460;
    border-color: #00d4ff;
}

QPushButton:pressed {
    background-color: #00d4ff;
    color: #1a1a2e;
}

QPushButton:disabled {
    background-color: #2a2a3e;
    color: #555555;
    border-color: #333333;
}

QPushButton#danger {
    background-color: #3d1a1a;
    border-color: #e94560;
}

QPushButton#danger:hover {
    background-color: #e94560;
    color: #ffffff;
}

QPushButton#success {
    background-color: #1a3d1a;
    border-color: #4ade80;
}

QPushButton#success:hover {
    background-color: #4ade80;
    color: #1a1a2e;
}

QFrame#serviceCard {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 15px;
    margin: 5px;
}

QFrame#serviceCard:hover {
    border-color: #00d4ff;
}

QLabel#serviceName {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#serviceDescription {
    font-size: 12px;
    color: #888888;
}

QLabel#statusEnabled {
    color: #4ade80;
    font-weight: bold;
}

QLabel#statusDisabled {
    color: #888888;
    font-weight: bold;
}

QLabel#statusNotInstalled {
    color: #666666;
    font-style: italic;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #16213e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #0f3460;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00d4ff;
}

QProgressBar {
    border: 2px solid #0f3460;
    border-radius: 8px;
    background-color: #16213e;
    text-align: center;
    color: #eaeaea;
}

QProgressBar::chunk {
    background-color: #00d4ff;
    border-radius: 6px;
}

QMessageBox {
    background-color: #1a1a2e;
}

QMessageBox QLabel {
    color: #eaeaea;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""
