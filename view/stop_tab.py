# Componente para la pestaña "Paso por Parada"
from PyQt6 import QtCore, QtGui, QtWidgets


class StopTab:
    """Componente que crea y configura la pestaña de consulta por parada"""
    
    def __init__(self, parent_widget):
        self.tab = QtWidgets.QWidget(parent=parent_widget)
        self.tab.setObjectName("tab_3")
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la pestaña"""
        # Estilo general de la pestaña - Tema oscuro
        self.tab.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
        """)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setContentsMargins(15, 15, 15, 15)
        
        # Layout izquierdo con fondo decorado - Tema oscuro
        left_container = QtWidgets.QWidget(parent=self.tab)
        left_container.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.leftLayout = QtWidgets.QVBoxLayout(left_container)
        self.leftLayout.setObjectName("leftLayout")
        self.leftLayout.setSpacing(15)
        
        # Título con estilo mejorado
        self.titleLabel = QtWidgets.QLabel(parent=left_container)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("""
            QLabel {
                color: #ffffff;
                padding: 10px;
                background-color: #3a3a3a;
                border-radius: 8px;
            }
        """)
        self.leftLayout.addWidget(self.titleLabel)
        
        # Campo de entrada de parada con estilo mejorado
        self.stopLineEdit = QtWidgets.QLineEdit(parent=left_container)
        self.stopLineEdit.setObjectName("stopLineEdit")
        self.stopLineEdit.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #555555;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #2a2a2a;
            }
        """)
        self.leftLayout.addWidget(self.stopLineEdit)
        
        # Botón de consulta con estilo mejorado
        self.checkButton = QtWidgets.QPushButton(parent=left_container)
        self.checkButton.setObjectName("checkButton")
        self.checkButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        self.leftLayout.addWidget(self.checkButton)
        
        # Label de historial con estilo mejorado
        self.historyLabel = QtWidgets.QLabel(parent=left_container)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.historyLabel.setFont(font)
        self.historyLabel.setObjectName("historyLabel")
        self.historyLabel.setStyleSheet("""
            QLabel {
                color: #ffffff;
                padding: 5px;
            }
        """)
        self.leftLayout.addWidget(self.historyLabel)
        
        # Layout de paradas recientes
        self.recentStopsLayout = QtWidgets.QGridLayout()
        self.recentStopsLayout.setObjectName("recentStopsLayout")
        self.recentStopsLayout.setSpacing(8)
        self.leftLayout.addLayout(self.recentStopsLayout)
        
        # Espaciador
        spacerItem = QtWidgets.QSpacerItem(
            48, 371, 
            QtWidgets.QSizePolicy.Policy.Minimum, 
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.leftLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(left_container)
        
        # Layout derecho con fondo decorado - Tema oscuro
        right_container = QtWidgets.QWidget(parent=self.tab)
        right_container.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.rightLayout = QtWidgets.QVBoxLayout(right_container)
        self.rightLayout.setObjectName("rightLayout")
        self.rightLayout.setSpacing(10)
        
        # Label de tiempo con estilo mejorado
        self.timeLabel = QtWidgets.QLabel(parent=right_container)
        self.timeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 11px;
                padding: 8px;
                background-color: #3a3a3a;
                border-radius: 6px;
            }
        """)
        self.rightLayout.addWidget(self.timeLabel)
        
        # Área de scroll para resultados con estilo mejorado
        self.scrollArea = QtWidgets.QScrollArea(parent=right_container)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
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
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 360, 463))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.rightLayout.addWidget(self.scrollArea)
        
        self.horizontalLayout_2.addWidget(right_container)
    
    def retranslate_ui(self):
        """Traduce los textos de la interfaz"""
        _translate = QtCore.QCoreApplication.translate
        self.titleLabel.setText(_translate("MainWindow", "EMT PALMA"))
        self.stopLineEdit.setPlaceholderText(
            _translate("MainWindow", "Introduce el número de parada")
        )
        self.checkButton.setText(_translate("MainWindow", "Consultar parada"))
        self.historyLabel.setText(_translate("MainWindow", "Historial:"))
        self.timeLabel.setText(_translate("MainWindow", "Última actualización: -"))

