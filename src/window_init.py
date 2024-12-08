import os
from pathlib import Path

from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QKeySequenceEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QSizePolicy,
    QLayout,
    QApplication,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_wgt = QWidget
        self.central_wgt_layout = QVBoxLayout
        self.tab_wgt = QTabWidget
        self.smpl_tab = QWidget
        self.smpl_grid_layout = QGridLayout
        self.smpl_clk_intvl_lbl = QLabel
        self.smpl_clk_intvl_scale_cbox = QComboBox
        self.smpl_hkey_lbl = QLabel
        self.smpl_loc_display_ledit = QLineEdit
        self.smpl_mb_cbox = QComboBox
        self.smpl_hkey_keyseq = QKeySequenceEdit
        self.smpl_change_loc_btn = QPushButton
        self.smpl_mb_lbl = QLabel
        self.smpl_clk_intvl_ledit = QLineEdit
        self.smpl_loc_lbl = QLabel
        self.adv_tab = QWidget
        self.adv_grid_layout = QGridLayout
        self.adv_clicks_per_event_ledit = QLineEdit
        self.adv_clk_events_ledit = QLineEdit
        self.adv_clicks_per_event_lbl = QLabel
        self.adv_mb_lbl = QLabel
        self.adv_hkey_lbl = QLabel
        self.adv_clk_intvl_scale_cbox = QComboBox
        self.adv_clk_events_lbl = QLabel
        self.adv_clk_intvl_lbl = QLabel
        self.adv_change_loc_btn = QPushButton
        self.adv_clen_scale_cbox = QComboBox
        self.adv_hkey_keyseq = QKeySequenceEdit
        self.adv_clen_lbl = QLabel
        self.adv_clk_intvl_ledit = QLineEdit
        self.adv_mb_cbox = QComboBox
        self.adv_clen_ledit = QLineEdit
        self.adv_loc_display_ledit = QLineEdit
        self.adv_loc_lbl = QLabel
        self.btn_layout = QHBoxLayout
        self.start_btn = QPushButton
        self.stop_btn = QPushButton
        self.softlock_warning_msgb = QMessageBox

        self.current_hotkey = None

        self.advanced_location = None
        self.simple_location = None
        self.active_process = False
        self.first_tab_switch = True

        QApplication.processEvents()
        self.initialize_window()
        self.translate_ui()

    def initialize_window(self):
        self.setObjectName("main_window")
        self.resize(400, 300)
        built_icon_path = Path(os.path.dirname(__file__)).parent.joinpath("icon.png")
        source_icon_path = (
            Path(os.path.dirname(__file__))
            .parent.joinpath("assets")
            .joinpath("icon.png")
        )
        icon_path = built_icon_path if built_icon_path.exists() else source_icon_path
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.initialize_central_wgt()

    def initialize_central_wgt(self):
        central_wgt = QWidget()
        central_wgt.setObjectName("central_wgt")

        central_wgt_layout = QVBoxLayout(central_wgt)
        central_wgt_layout.setObjectName("central_wgt_layout")
        central_wgt_layout.setContentsMargins(5, 5, 5, 5)
        central_wgt_layout.setSpacing(0)
        central_wgt.setLayout(central_wgt_layout)
        self.central_wgt_layout = central_wgt_layout

        self.setCentralWidget(central_wgt)
        self.central_wgt = central_wgt

        self.initialize_tabs()
        self.initialize_btn_controls()
        self.initialize_hotkey_location_warning()

    def initialize_tabs(self):
        tab_wgt = QTabWidget(self.central_wgt)
        tab_wgt.setObjectName("tab_wgt")
        tab_wgt.currentChanged.connect(self.switched_tabs)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(tab_wgt.sizePolicy().hasHeightForWidth())
        tab_wgt.setSizePolicy(size_policy)
        tab_wgt.setMinimumSize(QSize(0, 0))
        tab_wgt.setAutoFillBackground(False)
        tab_wgt.setTabShape(QTabWidget.Rounded)

        self.central_wgt_layout.addWidget(tab_wgt)
        self.tab_wgt = tab_wgt

        self.initialize_smpl_tab()
        self.initialize_adv_tab()

    def initialize_smpl_tab(self):
        smpl_tab = QWidget()
        smpl_tab.setObjectName("smpl_tab")

        smpl_grid_layout = QGridLayout(smpl_tab)
        smpl_grid_layout.setObjectName("smpl_grid_layout")
        smpl_grid_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        smpl_clk_intvl_lbl = QLabel(smpl_tab)
        smpl_clk_intvl_lbl.setObjectName("smpl_clk_intvl_lbl")
        smpl_clk_intvl_lbl.setLayoutDirection(Qt.LeftToRight)
        smpl_grid_layout.addWidget(smpl_clk_intvl_lbl, 0, 0, 1, 1, Qt.AlignRight)
        self.smpl_clk_intvl_lbl = smpl_clk_intvl_lbl

        smpl_clk_intvl_scale_cbox = QComboBox(smpl_tab)
        smpl_clk_intvl_scale_cbox.setObjectName("smpl_clk_intvl_scale_cbox")
        smpl_clk_intvl_scale_cbox.setMinimumSize(QSize(0, 0))
        smpl_clk_intvl_scale_cbox.addItem("")
        smpl_clk_intvl_scale_cbox.addItem("")
        smpl_clk_intvl_scale_cbox.addItem("")
        smpl_clk_intvl_scale_cbox.addItem("")
        smpl_grid_layout.addWidget(smpl_clk_intvl_scale_cbox, 0, 2, 1, 1)
        self.smpl_clk_intvl_scale_cbox = smpl_clk_intvl_scale_cbox

        smpl_hkey_lbl = QLabel(smpl_tab)
        smpl_hkey_lbl.setObjectName("smpl_hkey_lbl")
        smpl_grid_layout.addWidget(smpl_hkey_lbl, 3, 0, 1, 1, Qt.AlignRight)
        self.smpl_hkey_lbl = smpl_hkey_lbl

        smpl_loc_display_ledit = QLineEdit(smpl_tab)
        smpl_loc_display_ledit.setObjectName("smpl_loc_display_ledit")
        smpl_loc_display_ledit.setReadOnly(True)
        smpl_loc_display_ledit.setPlaceholderText("")
        smpl_grid_layout.addWidget(smpl_loc_display_ledit, 2, 1, 1, 1)
        self.smpl_loc_display_ledit = smpl_loc_display_ledit

        smpl_mb_cbox = QComboBox(smpl_tab)
        smpl_mb_cbox.setObjectName("smpl_mb_cbox")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(smpl_mb_cbox.sizePolicy().hasHeightForWidth())
        smpl_mb_cbox.setSizePolicy(size_policy)
        smpl_mb_cbox.setEditable(False)
        smpl_mb_cbox.setMaxVisibleItems(3)
        smpl_mb_cbox.addItem("")
        smpl_mb_cbox.addItem("")
        smpl_mb_cbox.addItem("")
        smpl_grid_layout.addWidget(smpl_mb_cbox, 1, 1, 1, 2)
        self.smpl_mb_cbox = smpl_mb_cbox

        smpl_hkey_keyseq = QKeySequenceEdit(smpl_tab)
        smpl_hkey_keyseq.setObjectName("smpl_hkey_keyseq")
        smpl_hkey_keyseq.editingFinished.connect(self.hotkey_changed)
        smpl_hkey_keyseq.keySequenceChanged.connect(self.clear_hotkey)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(smpl_hkey_keyseq.sizePolicy().hasHeightForWidth())
        smpl_hkey_keyseq.setSizePolicy(size_policy)
        smpl_grid_layout.addWidget(smpl_hkey_keyseq, 3, 1, 1, 2)
        self.smpl_hkey_keyseq = smpl_hkey_keyseq

        smpl_change_loc_btn = QPushButton(smpl_tab)
        smpl_change_loc_btn.setObjectName("smpl_change_loc_btn")
        smpl_change_loc_btn.pressed.connect(self.change_location)
        smpl_grid_layout.addWidget(smpl_change_loc_btn, 2, 2, 1, 1)
        self.smpl_change_loc_btn = smpl_change_loc_btn

        smpl_mb_lbl = QLabel(smpl_tab)
        smpl_mb_lbl.setObjectName("smpl_mb_lbl")
        smpl_grid_layout.addWidget(smpl_mb_lbl, 1, 0, 1, 1, Qt.AlignRight)
        self.smpl_mb_lbl = smpl_mb_lbl

        smpl_clk_intvl_ledit = QLineEdit(smpl_tab)
        smpl_clk_intvl_ledit.setObjectName("smpl_clk_intvl_ledit")
        smpl_clk_intvl_ledit.setValidator(QIntValidator())
        smpl_clk_intvl_ledit.setMaxLength(7)
        smpl_grid_layout.addWidget(smpl_clk_intvl_ledit, 0, 1, 1, 1)
        self.smpl_clk_intvl_ledit = smpl_clk_intvl_ledit

        smpl_loc_lbl = QLabel(smpl_tab)
        smpl_loc_lbl.setObjectName("smpl_loc_lbl")
        smpl_grid_layout.addWidget(smpl_loc_lbl, 2, 0, 1, 1, Qt.AlignRight)
        self.smpl_loc_lbl = smpl_loc_lbl

        smpl_grid_layout.setColumnStretch(0, 0)
        smpl_grid_layout.setColumnStretch(1, 4)
        smpl_grid_layout.setColumnStretch(2, 3)
        self.smpl_grid_layout = smpl_grid_layout

        self.tab_wgt.addTab(smpl_tab, "")
        self.smpl_tab = smpl_tab

    def initialize_adv_tab(self):
        adv_tab = QWidget()
        adv_tab.setObjectName("adv_tab")

        adv_grid_layout = QGridLayout(adv_tab)
        adv_grid_layout.setObjectName("adv_grid_layout")
        adv_grid_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        adv_loc_lbl = QLabel(adv_tab)
        adv_loc_lbl.setObjectName("adv_loc_lbl")
        adv_grid_layout.addWidget(adv_loc_lbl, 5, 0, 1, 1, Qt.AlignRight)
        self.adv_loc_lbl = adv_loc_lbl

        adv_loc_display_ledit = QLineEdit(adv_tab)
        adv_loc_display_ledit.setObjectName("adv_loc_display_ledit")
        adv_loc_display_ledit.setReadOnly(True)
        adv_loc_display_ledit.setPlaceholderText("")
        adv_grid_layout.addWidget(adv_loc_display_ledit, 5, 1, 1, 1)
        self.adv_loc_display_ledit = adv_loc_display_ledit

        adv_clen_ledit = QLineEdit(adv_tab)
        adv_clen_ledit.setObjectName("adv_clen_ledit")
        adv_clen_ledit.setValidator(QIntValidator())
        adv_clen_ledit.setMaxLength(7)
        adv_grid_layout.addWidget(adv_clen_ledit, 1, 1, 1, 1)
        self.adv_clen_ledit = adv_clen_ledit

        adv_mb_cbox = QComboBox(adv_tab)
        adv_mb_cbox.setObjectName("adv_mb_cbox")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(adv_mb_cbox.sizePolicy().hasHeightForWidth())
        adv_mb_cbox.setSizePolicy(size_policy)
        adv_mb_cbox.setEditable(False)
        adv_mb_cbox.setMaxVisibleItems(3)
        adv_mb_cbox.addItem("")
        adv_mb_cbox.addItem("")
        adv_mb_cbox.addItem("")
        adv_grid_layout.addWidget(adv_mb_cbox, 4, 1, 1, 2)
        self.adv_mb_cbox = adv_mb_cbox

        adv_clk_intvl_ledit = QLineEdit(adv_tab)
        adv_clk_intvl_ledit.setObjectName("adv_clk_intvl_ledit")
        adv_clk_intvl_ledit.setValidator(QIntValidator())
        adv_clk_intvl_ledit.setMaxLength(7)
        adv_grid_layout.addWidget(adv_clk_intvl_ledit, 0, 1, 1, 1)
        self.adv_clk_intvl_ledit = adv_clk_intvl_ledit

        adv_clen_lbl = QLabel(adv_tab)
        adv_clen_lbl.setObjectName("adv_clen_lbl")
        adv_grid_layout.addWidget(adv_clen_lbl, 1, 0, 1, 1, Qt.AlignRight)
        self.adv_clen_lbl = adv_clen_lbl

        adv_hkey_keyseq = QKeySequenceEdit(adv_tab)
        adv_hkey_keyseq.setObjectName("adv_hkey_keyseq")
        adv_hkey_keyseq.editingFinished.connect(self.hotkey_changed)
        adv_hkey_keyseq.keySequenceChanged.connect(self.clear_hotkey)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(adv_hkey_keyseq.sizePolicy().hasHeightForWidth())
        adv_hkey_keyseq.setSizePolicy(size_policy)
        adv_grid_layout.addWidget(adv_hkey_keyseq, 6, 1, 1, 2)
        self.adv_hkey_keyseq = adv_hkey_keyseq

        adv_clen_scale_cbox = QComboBox(adv_tab)
        adv_clen_scale_cbox.setObjectName("adv_clen_scale_cbox")
        adv_clen_scale_cbox.addItem("")
        adv_clen_scale_cbox.addItem("")
        adv_clen_scale_cbox.addItem("")
        adv_clen_scale_cbox.addItem("")
        adv_grid_layout.addWidget(adv_clen_scale_cbox, 1, 2, 1, 1)
        self.adv_clen_scale_cbox = adv_clen_scale_cbox

        adv_change_loc_btn = QPushButton(adv_tab)
        adv_change_loc_btn.setObjectName("adv_change_loc_btn")
        adv_change_loc_btn.pressed.connect(self.change_location)
        adv_grid_layout.addWidget(adv_change_loc_btn, 5, 2, 1, 1)
        self.adv_change_loc_btn = adv_change_loc_btn

        adv_clk_intvl_lbl = QLabel(adv_tab)
        adv_clk_intvl_lbl.setObjectName("adv_clk_intvl_lbl")
        adv_clk_intvl_lbl.setLayoutDirection(Qt.LeftToRight)
        adv_grid_layout.addWidget(adv_clk_intvl_lbl, 0, 0, 1, 1, Qt.AlignRight)
        self.adv_clk_intvl_lbl = adv_clk_intvl_lbl

        adv_clk_events_lbl = QLabel(adv_tab)
        adv_clk_events_lbl.setObjectName("adv_clk_events_lbl")
        adv_grid_layout.addWidget(adv_clk_events_lbl, 2, 0, 1, 1, Qt.AlignRight)
        self.adv_clk_events_lbl = adv_clk_events_lbl

        adv_clk_intvl_scale_cbox = QComboBox(adv_tab)
        adv_clk_intvl_scale_cbox.setObjectName("adv_clk_intvl_scale_cbox")
        adv_clk_intvl_scale_cbox.setMinimumSize(QSize(0, 0))
        adv_clk_intvl_scale_cbox.addItem("")
        adv_clk_intvl_scale_cbox.addItem("")
        adv_clk_intvl_scale_cbox.addItem("")
        adv_clk_intvl_scale_cbox.addItem("")
        adv_grid_layout.addWidget(adv_clk_intvl_scale_cbox, 0, 2, 1, 1)
        self.adv_clk_intvl_scale_cbox = adv_clk_intvl_scale_cbox

        adv_hkey_lbl = QLabel(adv_tab)
        adv_hkey_lbl.setObjectName("adv_hkey_lbl")
        adv_grid_layout.addWidget(adv_hkey_lbl, 6, 0, 1, 1, Qt.AlignRight)
        self.adv_hkey_lbl = adv_hkey_lbl

        adv_mb_lbl = QLabel(adv_tab)
        adv_mb_lbl.setObjectName("adv_mb_lbl")
        adv_grid_layout.addWidget(adv_mb_lbl, 4, 0, 1, 1, Qt.AlignRight)
        self.adv_mb_lbl = adv_mb_lbl

        adv_clicks_per_event_lbl = QLabel(adv_tab)
        adv_clicks_per_event_lbl.setObjectName("adv_clicks_per_event_lbl")
        adv_grid_layout.addWidget(adv_clicks_per_event_lbl, 3, 0, 1, 1, Qt.AlignRight)
        self.adv_clicks_per_event_lbl = adv_clicks_per_event_lbl

        adv_clk_events_ledit = QLineEdit(adv_tab)
        adv_clk_events_ledit.setObjectName("adv_clk_events_ledit")
        adv_clk_events_ledit.setValidator(QIntValidator())
        adv_clk_events_ledit.setMaxLength(7)
        adv_grid_layout.addWidget(adv_clk_events_ledit, 2, 1, 1, 2)
        self.adv_clk_events_ledit = adv_clk_events_ledit

        adv_clicks_per_event_ledit = QLineEdit(adv_tab)
        adv_clicks_per_event_ledit.setObjectName("adv_clicks_per_event_ledit")
        adv_clicks_per_event_ledit.setValidator(QIntValidator())
        adv_clicks_per_event_ledit.setMaxLength(7)
        adv_grid_layout.addWidget(adv_clicks_per_event_ledit, 3, 1, 1, 2)
        self.adv_clicks_per_event_ledit = adv_clicks_per_event_ledit

        adv_grid_layout.setColumnStretch(0, 0)
        adv_grid_layout.setColumnStretch(1, 4)
        adv_grid_layout.setColumnStretch(2, 3)
        self.adv_grid_layout = adv_grid_layout

        self.tab_wgt.addTab(adv_tab, "")
        self.adv_tab = adv_tab

    def initialize_btn_controls(self):
        btn_layout = QHBoxLayout()
        btn_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        btn_layout.setContentsMargins(0, 5, 0, 0)
        btn_layout.setSpacing(5)
        btn_layout.setObjectName("btn_layout")

        start_btn = QPushButton(self.central_wgt)
        start_btn.setObjectName("start_btn")
        start_btn.clicked.connect(self.start_button_clicked)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(start_btn.sizePolicy().hasHeightForWidth())
        start_btn.setSizePolicy(size_policy)
        start_btn.setMinimumSize(QSize(0, 50))
        btn_layout.addWidget(start_btn)
        self.start_btn = start_btn

        stop_btn = QPushButton(self.central_wgt)
        stop_btn.setObjectName("stop_btn")
        stop_btn.clicked.connect(self.stop_button_clicked)
        stop_btn.setDisabled(True)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(stop_btn.sizePolicy().hasHeightForWidth())
        stop_btn.setSizePolicy(size_policy)
        stop_btn.setMinimumSize(QSize(0, 50))
        stop_btn.setBaseSize(QSize(0, 0))
        btn_layout.addWidget(stop_btn)
        self.stop_btn = stop_btn

        btn_layout.setStretch(0, 1)
        btn_layout.setStretch(1, 1)
        self.central_wgt_layout.addLayout(btn_layout)
        self.btn_layout = btn_layout

    def initialize_hotkey_location_warning(self):
        hloc_warning_msgb = QMessageBox(self)
        hloc_warning_msgb.setIcon(QMessageBox.Icon.Warning)
        hloc_warning_msgb.setText("")
        hloc_warning_msgb.setWindowTitle("")
        hloc_warning_msgb.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.softlock_warning_msgb = hloc_warning_msgb

    def translate_ui(self):
        translate = QCoreApplication.translate
        self.setWindowTitle(translate("main_window", "Easy Auto Clicker"))
        self.smpl_clk_intvl_lbl.setText(translate("main_window", "Interval"))
        self.smpl_clk_intvl_lbl.setToolTip(
            translate("main_window", "The time between each click event")
        )
        self.smpl_clk_intvl_scale_cbox.setItemText(
            0, translate("main_window", "Milliseconds")
        )
        self.smpl_clk_intvl_scale_cbox.setItemText(
            1, translate("main_window", "Seconds")
        )
        self.smpl_clk_intvl_scale_cbox.setItemText(
            2, translate("main_window", "Minutes")
        )
        self.smpl_clk_intvl_scale_cbox.setItemText(3, translate("main_window", "Hours"))
        self.smpl_hkey_lbl.setText(translate("main_window", "Hotkey"))
        self.smpl_hkey_lbl.setToolTip(
            translate("main_window", "The hotkey to toggle the click process")
        )
        self.smpl_mb_cbox.setItemText(0, translate("main_window", "Left (M1)"))
        self.smpl_mb_cbox.setItemText(1, translate("main_window", "Right (M2)"))
        self.smpl_mb_cbox.setItemText(2, translate("main_window", "Middle (M3)"))
        self.smpl_loc_display_ledit.setPlaceholderText(translate("main_window", "None"))
        self.smpl_change_loc_btn.setText(translate("main_window", "Change"))
        self.smpl_mb_lbl.setText(translate("main_window", "Mouse Button"))
        self.smpl_mb_lbl.setToolTip(
            translate("main_window", "The mouse button to use for each click")
        )
        self.smpl_clk_intvl_ledit.setPlaceholderText(translate("main_window", "100"))
        self.smpl_loc_lbl.setText(translate("main_window", "Location"))
        self.smpl_loc_lbl.setToolTip(
            translate("main_window", "The (x, y) location on the screen to click")
        )
        self.tab_wgt.setTabText(
            self.tab_wgt.indexOf(self.smpl_tab), translate("main_window", "Simple")
        )
        self.adv_loc_lbl.setText(translate("main_window", "Location"))
        self.adv_loc_lbl.setToolTip(
            translate("main_window", "The (x, y) location on the screen to click")
        )
        self.adv_clen_ledit.setPlaceholderText(translate("main_window", "0"))
        self.adv_mb_cbox.setItemText(0, translate("main_window", "Left (M1)"))
        self.adv_mb_cbox.setItemText(1, translate("main_window", "Right (M2)"))
        self.adv_mb_cbox.setItemText(2, translate("main_window", "Middle (M3)"))
        self.adv_loc_display_ledit.setPlaceholderText(translate("main_window", "None"))
        self.adv_clk_intvl_ledit.setPlaceholderText(translate("main_window", "100"))
        self.adv_clen_lbl.setText(translate("main_window", "Length"))
        self.adv_clen_lbl.setToolTip(
            translate("main_window", "The amount of time to hold each click")
        )
        self.adv_clen_scale_cbox.setItemText(
            0, translate("main_window", "Milliseconds")
        )
        self.adv_clen_scale_cbox.setItemText(1, translate("main_window", "Seconds"))
        self.adv_clen_scale_cbox.setItemText(2, translate("main_window", "Minutes"))
        self.adv_clen_scale_cbox.setItemText(3, translate("main_window", "Hours"))
        self.adv_change_loc_btn.setText(translate("main_window", "Change"))
        self.adv_clk_intvl_lbl.setText(translate("main_window", "Interval"))
        self.adv_clk_intvl_lbl.setToolTip(
            translate("main_window", "The time between each click event")
        )
        self.adv_clk_events_lbl.setText(translate("main_window", "Event Count"))
        self.adv_clk_intvl_scale_cbox.setItemText(
            0, translate("main_window", "Milliseconds")
        )
        self.adv_clk_intvl_scale_cbox.setItemText(
            1, translate("main_window", "Seconds")
        )
        self.adv_clk_intvl_scale_cbox.setItemText(
            2, translate("main_window", "Minutes")
        )
        self.adv_clk_intvl_scale_cbox.setItemText(3, translate("main_window", "Hours"))
        self.adv_hkey_lbl.setText(translate("main_window", "Hotkey"))
        self.adv_hkey_lbl.setToolTip(
            translate("main_window", "The hotkey to toggle the click process")
        )
        self.adv_mb_lbl.setText(translate("main_window", "Mouse Button"))
        self.adv_mb_lbl.setToolTip(
            translate("main_window", "The mouse button to use for each click")
        )
        self.adv_clicks_per_event_lbl.setText(
            translate("main_window", "Clicks per Event")
        )
        self.adv_clicks_per_event_lbl.setToolTip(
            translate("main_window", "The amount of clicks to run for each click event")
        )
        self.adv_clk_events_ledit.setPlaceholderText(translate("main_window", "∞"))
        self.adv_clicks_per_event_ledit.setPlaceholderText(
            translate("main_window", "1")
        )
        self.tab_wgt.setTabText(
            self.tab_wgt.indexOf(self.adv_tab),
            translate("main_window", "Advanced"),
        )
        self.start_btn.setText(translate("main_window", "Start"))
        self.stop_btn.setText(translate("main_window", "Stop"))
        self.softlock_warning_msgb.setWindowTitle("Softlock Prevention")
        self.softlock_warning_msgb.setText(
            "You must set a hotkey if you are using a location.\nThis prevents you from softlocking your mouse."
        )
