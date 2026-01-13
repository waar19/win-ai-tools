"""
Widget de selección de idioma
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal
import sys
sys.path.append('..')
from core.i18n import LANGUAGES, I18n


class LanguageSelector(QComboBox):
    """Dropdown para seleccionar idioma"""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.currentIndexChanged.connect(self._on_language_changed)
    
    def _setup_ui(self):
        """Configura el selector"""
        self.setFixedWidth(120)
        
        # Agregar idiomas
        for code, name in LANGUAGES.items():
            self.addItem(name, code)
        
        # Establecer idioma actual
        current_lang = I18n.get_language()
        for i in range(self.count()):
            if self.itemData(i) == current_lang:
                self.setCurrentIndex(i)
                break
        
        self.setStyleSheet("""
            QComboBox {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #0f3460;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #00d4ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00d4ff;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #16213e;
                color: #eaeaea;
                selection-background-color: #0f3460;
                border: 1px solid #0f3460;
            }
        """)
    
    def _on_language_changed(self, index):
        """Maneja cambio de idioma"""
        lang_code = self.itemData(index)
        if lang_code:
            I18n.set_language(lang_code)
            self.language_changed.emit(lang_code)
