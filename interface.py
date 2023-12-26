from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea

import cv2

from Manager import load_graph

class ClickableImageLabel(QtWidgets.QLabel):
    """
    Classe d'étiquette (Label) personnalisée héritant de << QLabel >> pour gérer les événements de clic et la coloration des pixels.

    Attributs:
    - clicked: QtCore.pyqtSignal(QtCore.QPoint) - Signal émis au clic de souris.
    - start_pixel: QPoint - La position du pixel de départ.
    - end_pixel: QPoint - La position du pixel d'arrivé.
    - path: List - La liste des sommets de classe << Vertex >> composant le chemin le plus court.

    Methodes:
    - __init__(self, parent = None): Constructeur de la classe.
    - mouseMoveEvent(self, event): Event handler pour le mouvement de la souris sur l'étiquette.
    - mousePressEvent(self, event): Event handler pour le clic de souris sur l'étiquette.
    - update_tooltip(self, event): Met à jour l'info-bulle avec les coordonnées en pixels.
    - mapToResizedImage(self, pos, image_size): Mappe la position de l'évènement aux coordonnées équivalentes dans l'image redimensionnées.
    - paintEvent(self, event): Peint l'étiquette et colore les pixels de début, de fin et de chemin.
    - color_pixel(self, pos, color): Colore un pixel spécifique sur l'étiquette.
    - clearImage(self): efface le pixmap (image) de l'étiquette et réinitialise les attributs (reset).
    """
    clicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent = None):
        """
        __init__(self, parent = None): Constructeur de la classe.

        Arguments:
            parent: QtWidgets.QWidget - Le widget parent. "None" par défaut.
        """
        super(ClickableImageLabel, self).__init__(parent)
        self.setMouseTracking(True)
        self.start_pixel = None
        self.end_pixel = None
        self.path = None

    def mouseMoveEvent(self, event):
        """
        mouseMoveEvent(self, event): Event handler pour le mouvement de la souris sur l'étiquette.

        Arguments:
            event: QtCore.QEvent - L'évènement de mouvement de la sourics sur l'étiquette
        """
        self.update_tooltip(event)

    def mousePressEvent(self, event):
        """
        mousePressEvent(self, event): Event handler pour le clic de souris sur l'étiquette.

        Arguments:
            event: QtCore.QEvent - L'évènement de clic de sourics sur l'étiquette
        """
        self.clicked.emit(event.pos())

    def update_tooltip(self, event):
        """
        update_tooltip(self, event): Met à jour l'info-bulle avec les coordonnées en pixels.

        Arguments:
            event: QtCore.QEvent - L'évènement de la sourics sur l'étiquette contenant des informations sur la position (coordonnées)
        """
        image_size = QtCore.QSize(21, 21)
        pos = event.pos()

        label_width = self.width()
        label_height = self.height()

        # Calculate the scaling factors
        scale_x = image_size.width() / label_width
        scale_y = image_size.height() / label_height

        x_resized = int(pos.x() * scale_x)
        y_resized = int(pos.y() * scale_y)

        tooltip_text = f'Pixel : ({y_resized}, {x_resized})'
        self.setToolTip(tooltip_text)

    def mapToResizedImage(self, pos, image_size):
        """
        mapToResizedImage(self, pos, image_size): Mappe la position de l'évènement aux coordonnées équivalentes dans l'image redimensionnées.
        
        Arguments:
            pos: QtCore.QPoint - La position à mapper
            image_size: QtCore.QSize - La taille de l'image

        Retourne:
            QPoint: La position mappée
        """
        # Map the position to the corresponding position on the resized image
        label_width = self.width()
        label_height = self.height()

        # Calculate the scaling factors
        scale_x = image_size.width() / label_width
        scale_y = image_size.height() / label_height

        # Map the position to the resized image coordinates
        x_resized = int(pos.x() * scale_x)
        y_resized = int(pos.y() * scale_y)

        return QtCore.QPoint(x_resized, y_resized)
    
    def paintEvent(self, event):
        """
        paintEvent(self, event): Peint l'étiquette et colore les pixels de début, de fin et de chemin.

        Arguments:
            event: QtCore.QEvent - L'évènement de peint
        """
        super().paintEvent(event)

        if self.start_pixel:
            self.color_pixel(self.start_pixel, QtGui.QColor(1, 212, 73))

        if self.end_pixel:
            self.color_pixel(self.end_pixel, QtGui.QColor(131, 76, 171))

        if self.path:
            for vertex in self.path:
                self.color_pixel(QtCore.QPoint(vertex.column, vertex.line), QtGui.QColor(255, 0, 0))

    def color_pixel(self, pos, color):
        """
        color_pixel(self, pos, color): Colore un pixel spécifique sur l'étiquette.

        Arguments:
            pos: QPoint - La position du pixel à colorer
            color: QColor - La nouvelle couleur du pixel
        """
        image_size = QtCore.QSize(21, 21)
        label_width = self.width()
        label_height = self.height()

        scale_x = label_width / image_size.width()
        scale_y = label_height / image_size.height()

        x_resized = int(pos.x() * scale_x)
        y_resized = int(pos.y() * scale_y)

        pixmap = self.pixmap()
        if pixmap:
            painter = QtGui.QPainter(pixmap)
            rect = QtCore.QRect(x_resized, y_resized, int(scale_x) + 1, int(scale_y) + 1)
            painter.fillRect(rect, color)
            self.setPixmap(pixmap)

    def clearImage(self):
        """
        clearImage(self): efface le pixmap (image) de l'étiquette et réinitialise les attributs (reset).
        """
        self.setPixmap(QtGui.QPixmap())
        self.start_pixel = None
        self.end_pixel = None
        self.path = None

class Ui_MainWindow(object):

    def __init__(self):
        """
        Initialise les variables stockantles information sur le chemin vers l'image, le graph résultant, les pixels de début et de fin et plus court chemin
        """
        self.image_path = None
        self.graph = None
        self.start_pixel = None
        self.end_pixel = None
        self.path = None

    def setupUi(self, MainWindow):
        """
        Mets en forme l'interface graphique
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(self.centralwidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.verticalStackedWidget.setStyleSheet("")
        self.verticalStackedWidget.setObjectName("verticalStackedWidget")
        self.LandingPage = QtWidgets.QWidget()
        self.LandingPage.setObjectName("LandingPage")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.LandingPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.welcomeLabelContainer = QtWidgets.QWidget(self.LandingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.welcomeLabelContainer.sizePolicy().hasHeightForWidth())
        self.welcomeLabelContainer.setSizePolicy(sizePolicy)
        self.welcomeLabelContainer.setMinimumSize(QtCore.QSize(301, 80))
        self.welcomeLabelContainer.setObjectName("welcomeLabelContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.welcomeLabelContainer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.welcomeLabel = QtWidgets.QLabel(self.welcomeLabelContainer)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.welcomeLabel.setFont(font)
        self.welcomeLabel.setStyleSheet("color: rgb(131, 76, 171);")
        self.welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.verticalLayout_2.addWidget(self.welcomeLabel)
        self.verticalLayout_3.addWidget(self.welcomeLabelContainer)
        self.tutorialContainer = QtWidgets.QWidget(self.LandingPage)
        self.tutorialContainer.setObjectName("tutorialContainer")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tutorialContainer)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tutorialLabel = QtWidgets.QLabel(self.tutorialContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tutorialLabel.sizePolicy().hasHeightForWidth())
        self.tutorialLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tutorialLabel.setFont(font)
        self.tutorialLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tutorialLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tutorialLabel.setWordWrap(True)
        self.tutorialLabel.setObjectName("tutorialLabel")
        self.verticalLayout_4.addWidget(self.tutorialLabel)
        self.verticalLayout_3.addWidget(self.tutorialContainer)
        self.loadtButtonContainer = QtWidgets.QWidget(self.LandingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadtButtonContainer.sizePolicy().hasHeightForWidth())
        self.loadtButtonContainer.setSizePolicy(sizePolicy)
        self.loadtButtonContainer.setStyleSheet("#loadButton{\n"
"    padding: 6px 10px;\n"
"    background-color: rgb(1, 212, 73);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#loadButton:hover{\n"
"    background-color: rgba(1, 212, 73, 0.5);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"#loadButton:pressed{\n"
"    background-color: rgb(131, 76, 171);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.loadtButtonContainer.setObjectName("loadtButtonContainer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.loadtButtonContainer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadButton = QtWidgets.QPushButton(self.loadtButtonContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.loadButton.setFont(font)
        self.loadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout.addWidget(self.loadButton)
        self.verticalLayout_3.addWidget(self.loadtButtonContainer)
        self.verticalStackedWidget.addWidget(self.LandingPage)
        self.FileLoadingPage = QtWidgets.QWidget()
        self.FileLoadingPage.setObjectName("FileLoadingPage")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.FileLoadingPage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pageTitleLabelContainer = QtWidgets.QWidget(self.FileLoadingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageTitleLabelContainer.sizePolicy().hasHeightForWidth())
        self.pageTitleLabelContainer.setSizePolicy(sizePolicy)
        self.pageTitleLabelContainer.setObjectName("pageTitleLabelContainer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.pageTitleLabelContainer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pageTitleLable = QtWidgets.QLabel(self.pageTitleLabelContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageTitleLable.sizePolicy().hasHeightForWidth())
        self.pageTitleLable.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pageTitleLable.setFont(font)
        self.pageTitleLable.setStyleSheet("color: rgb(131, 76, 171);")
        self.pageTitleLable.setAlignment(QtCore.Qt.AlignCenter)
        self.pageTitleLable.setObjectName("pageTitleLable")
        self.verticalLayout_6.addWidget(self.pageTitleLable)
        self.verticalLayout_5.addWidget(self.pageTitleLabelContainer)
        self.elementsContainer = QtWidgets.QWidget(self.FileLoadingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elementsContainer.sizePolicy().hasHeightForWidth())
        self.elementsContainer.setSizePolicy(sizePolicy)
        self.elementsContainer.setObjectName("elementsContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.elementsContainer)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.resultContainer = QtWidgets.QWidget(self.elementsContainer)
        self.resultContainer.setObjectName("resultContainer")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.resultContainer)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.imageContainer = QtWidgets.QWidget(self.resultContainer)
        self.imageContainer.setObjectName("imageContainer")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.imageContainer)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.imageLabel = ClickableImageLabel(self.imageContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setObjectName("imageLabel")
        self.imageLayout = QtWidgets.QVBoxLayout()
        self.imageLayout.addWidget(self.imageLabel)
        self.imageLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_7.setAlignment(QtCore.Qt.AlignLeft)
        self.imageLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.verticalLayout_7.addWidget(self.imageLabel)
        self.horizontalLayout_4.addWidget(self.imageContainer)
        self.messagesContainer = QtWidgets.QWidget(self.resultContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messagesContainer.sizePolicy().hasHeightForWidth())
        self.messagesContainer.setSizePolicy(sizePolicy)
        self.messagesContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.messagesContainer.setObjectName("messagesContainer")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.messagesContainer)
        self.verticalLayout_8.setContentsMargins(-1, 40, -1, -1)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.taskMessageLabel = QtWidgets.QLabel(self.messagesContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskMessageLabel.sizePolicy().hasHeightForWidth())
        self.taskMessageLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.taskMessageLabel.setFont(font)
        self.taskMessageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.taskMessageLabel.setObjectName("taskMessageLabel")
        self.verticalLayout_8.addWidget(self.taskMessageLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_8.addItem(spacerItem)
        self.startLabel = QtWidgets.QLabel(self.messagesContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startLabel.sizePolicy().hasHeightForWidth())
        self.startLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.startLabel.setFont(font)
        self.startLabel.setObjectName("startLabel")
        self.verticalLayout_8.addWidget(self.startLabel)
        self.endLabel = QtWidgets.QLabel(self.messagesContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endLabel.sizePolicy().hasHeightForWidth())
        self.endLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.endLabel.setFont(font)
        self.endLabel.setObjectName("endLabel")
        self.verticalLayout_8.addWidget(self.endLabel)
        self.pathLabel = QtWidgets.QLabel(self.messagesContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathLabel.sizePolicy().hasHeightForWidth())
        self.pathLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pathLabel.setFont(font)
        self.pathLabel.setText("")
        self.pathLabel.setWordWrap(True)
        self.pathLabel.setObjectName("pathLabel")
        self.verticalLayout_8.addWidget(self.pathLabel)
        self.horizontalLayout_4.addWidget(self.messagesContainer)
        self.verticalLayout.addWidget(self.resultContainer)
        self.goBackButtonContainer = QtWidgets.QWidget(self.elementsContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goBackButtonContainer.sizePolicy().hasHeightForWidth())
        self.goBackButtonContainer.setSizePolicy(sizePolicy)
        self.goBackButtonContainer.setStyleSheet("#goBackButton{\n"
"    padding: 6px 10px;\n"
"    background-color: rgb(1, 212, 73);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#goBackButton:hover{\n"
"    background-color: rgba(1, 212, 73, 0.5);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"#goBackButton:pressed{\n"
"    background-color: rgb(131, 76, 171);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.goBackButtonContainer.setObjectName("goBackButtonContainer")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.goBackButtonContainer)
        self.horizontalLayout_3.setContentsMargins(-1, 4, -1, 4)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.goBackButton = QtWidgets.QPushButton(self.goBackButtonContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goBackButton.sizePolicy().hasHeightForWidth())
        self.goBackButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.goBackButton.setFont(font)
        self.goBackButton.setObjectName("goBackButton")
        self.horizontalLayout_3.addWidget(self.goBackButton)
        self.verticalLayout.addWidget(self.goBackButtonContainer)
        self.verticalLayout_5.addWidget(self.elementsContainer)
        self.verticalStackedWidget.addWidget(self.FileLoadingPage)
        self.MainPage = QtWidgets.QWidget()
        self.MainPage.setObjectName("MainPage")
        self.verticalStackedWidget.addWidget(self.MainPage)
        self.horizontalLayout_2.addWidget(self.verticalStackedWidget)
        MainWindow.setCentralWidget(scroll_area)

        self.retranslateUi(MainWindow)
        self.verticalStackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect UI elements to methods
        self.loadButton.clicked.connect(self.choose_image)
        self.imageLabel.clicked.connect(self.handle_image_click)
        self.goBackButton.clicked.connect(self.change_start)

    def change_start(self):
        """
        Réinitialise les attributs et change la mise en page à celle de la page d'accueil 
        """
        self.verticalStackedWidget.setCurrentIndex(0)
        self.graph = None
        self.image_path = None
        self.taskMessageLabel.setText("Séléctionner le pixel de départ")
        self.pathLabel.setText("")
        self.startLabel.setText(f"Début => ")
        self.endLabel.setText(f"Fin => ")
        self.start_pixel = None
        self.end_pixel = None
        self.path = None
        self.imageLabel.clearImage()

    def choose_image(self):
        """
        Ouvre une boîte de dialogue de fichier pour sélectionner un fichier image et le charger
        """
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.List)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                self.image_path = image_path
                self.load_image(image_path)
                self.verticalStackedWidget.setCurrentIndex(1)

    def load_image(self, image_path):
        """
        Charge l'image sélectionnée et l'affiche
        """
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (21, 21))

        self.graph = load_graph(self.image_path)

        q_image = QtGui.QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0], resized_image.strides[0], QtGui.QImage.Format_RGB888)
        
        pixmap = QtGui.QPixmap.fromImage(q_image.rgbSwapped())

        zoom_factor = 30  # Increase this value to zoom in further
        zoomed_pixmap = pixmap.scaled(pixmap.width() * zoom_factor, pixmap.height() * zoom_factor, QtCore.Qt.KeepAspectRatio)

        self.imageLabel.setPixmap(zoomed_pixmap)

    def handle_image_click(self, pos):
        """
        Gére les clics sur l'étiquette de l'image pour sélectionner les pixels de début et de fin et trouve le chemin le plus court
        """
        resized_pos = self.imageLabel.mapToResizedImage(pos, QtCore.QSize(21, 21))

        if self.start_pixel is None:
            self.start_pixel = resized_pos
            self.taskMessageLabel.setText("Sélectionnez le pixel d'arrivée")
            self.startLabel.setText(f"Début => ({resized_pos.y()}, {resized_pos.x()})")
            self.imageLabel.start_pixel = self.start_pixel
            self.imageLabel.update()
        elif self.end_pixel is None:
            self.end_pixel = resized_pos
            self.endLabel.setText(f"Fin => ({resized_pos.y()}, {resized_pos.x()})")
            self.imageLabel.end_pixel = self.end_pixel
            self.imageLabel.update() 
            start = self.graph.get_vertex(self.start_pixel.y(), self.start_pixel.x())
            end = self.graph.get_vertex(self.end_pixel.y(), self.end_pixel.x())
            self.path, cost = self.graph.dijkstra(start, end)
            self.taskMessageLabel.setText(f"Le plus courts chemin : cout = {cost}")
            path_text = ""
            for vertex in self.path:
                path_text += f"({vertex.line}, {vertex.column}) -> "
            path_text = path_text[:-4]
            self.pathLabel.setText(path_text)
            self.imageLabel.path = self.path[1:-1]
            self.imageLabel.update()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.welcomeLabel.setText(_translate("MainWindow", "Bienvenu !!"))
        self.tutorialLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:11pt;\">Cette application a été conçue dans le cadre du projet d\'Algorithmique avancée pour trouver le chemin le plus court entre deux pixels sur une image.</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">Pour l\'utiliser :</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- Cliquez sur le bouton &quot;Parcourir&quot; pour parcourir et sélectionner une image à l\'aide du sélecteur de fichiers.</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- Une fois votre image chargée, vous serez invité(e) à sélectionner deux pixels sur l\'image (Attention : l\'image sera redimensionnée en 16x16 pixels).</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- Cliquez sur deux points pour définir les pixels de départ et d\'arrivée pour l\'algorithme de recherche de chemin.</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- Une fois vos pixels sélectionnés, l\'algorithme trouvera le chemin le plus court entre eux.</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- L\'application affichera le chemin sur l\'image, mettant en évidence l\'itinéraire entre les pixels choisis.</span></p><p align=\"center\"><span style=\" font-size:11pt;\">- Vous avez terminé ! N\'hésitez pas à explorer davantage ou à recommencer le processus.</span></p></body></html>"))
        self.loadButton.setText(_translate("MainWindow", "Parcourir"))
        self.pageTitleLable.setText(_translate("MainWindow", "Visualisation du Chemin"))
        self.imageLabel.setText(_translate("MainWindow", "TextLabel"))
        self.taskMessageLabel.setText(_translate("MainWindow", "Séléctionnez le pixel de départ"))
        self.startLabel.setText(_translate("MainWindow", "Début => "))
        self.endLabel.setText(_translate("MainWindow", "Fin =>"))
        self.goBackButton.setText(_translate("MainWindow", "Précédent"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized() 
    sys.exit(app.exec_())