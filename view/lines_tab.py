# Componente para la pestaña "Consulta por lineas"
from PyQt6 import QtCore, QtWidgets


class LinesTab:
    """Componente que crea y configura la pestaña de consulta por líneas"""
    
    def __init__(self, parent_widget):
        self.tab = QtWidgets.QWidget(parent=parent_widget)
        self.tab.setObjectName("tab_4")
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la pestaña"""
        # Estilo general de la pestaña - Tema oscuro
        self.tab.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)
        
        # Label de líneas con estilo mejorado
        self.label = QtWidgets.QLabel(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(8, 5, 371, 41))
        self.label.setObjectName("label")
        self.label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #2d2d2d;
                border-radius: 8px;
            }
        """)
        
        # Label de sublíneas y dirección con estilo mejorado
        self.label_2 = QtWidgets.QLabel(parent=self.tab)
        self.label_2.setGeometry(QtCore.QRect(390, 0, 361, 51))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #2d2d2d;
                border-radius: 8px;
            }
        """)
        
        # Scroll area izquierda (líneas) con estilo mejorado
        self.scrollArea_2 = QtWidgets.QScrollArea(parent=self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 50, 361, 451))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border-radius: 8px;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
        """)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 359, 449))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        
        # Scroll area derecha (sublíneas y dirección) con estilo mejorado
        self.scrollArea_3 = QtWidgets.QScrollArea(parent=self.tab)
        self.scrollArea_3.setGeometry(QtCore.QRect(380, 50, 361, 451))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollArea_3.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border-radius: 8px;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
        """)
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 359, 449))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
    
    def retranslate_ui(self):
        """Traduce los textos de la interfaz"""
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Lineas"))
        self.label_2.setText(_translate("MainWindow", "Sublineas y Direccion"))

