import os.path
from pathlib import Path
from time import sleep

import mouse
import keyboard
from PyQt5.QtCore import Qt, QSize, QCoreApplication, pyqtSlot
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QSizePolicy,
    QGridLayout,
    QLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QKeySequenceEdit,
    QPushButton,
    QHBoxLayout,
    QApplication,
)

from click_process import ClickProcessInputs, ClickProcess


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
        icon_path = Path(os.path.dirname(__file__)).parent.joinpath("icon.png")
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

    def translate_ui(self):
        translate = QCoreApplication.translate
        self.setWindowTitle(translate("main_window", "Easy Auto Clicker"))
        self.smpl_clk_intvl_lbl.setText(translate("main_window", "Click Interval"))
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
        self.smpl_mb_cbox.setItemText(0, translate("main_window", "Left (M1)"))
        self.smpl_mb_cbox.setItemText(1, translate("main_window", "Right (M2)"))
        self.smpl_mb_cbox.setItemText(2, translate("main_window", "Middle (M3)"))
        self.smpl_loc_display_ledit.setPlaceholderText(translate("main_window", "None"))
        self.smpl_change_loc_btn.setText(translate("main_window", "Change"))
        self.smpl_mb_lbl.setText(translate("main_window", "Mouse Button"))
        self.smpl_clk_intvl_ledit.setPlaceholderText(translate("main_window", "100"))
        self.smpl_loc_lbl.setText(translate("main_window", "Location"))
        self.tab_wgt.setTabText(
            self.tab_wgt.indexOf(self.smpl_tab), translate("main_window", "Simple")
        )
        self.adv_loc_lbl.setText(translate("main_window", "Location"))
        self.adv_clen_ledit.setPlaceholderText(translate("main_window", "0"))
        self.adv_mb_cbox.setItemText(0, translate("main_window", "Left (M1)"))
        self.adv_mb_cbox.setItemText(1, translate("main_window", "Right (M2)"))
        self.adv_mb_cbox.setItemText(2, translate("main_window", "Middle (M3)"))
        self.adv_loc_display_ledit.setPlaceholderText(translate("main_window", "None"))
        self.adv_clk_intvl_ledit.setPlaceholderText(translate("main_window", "100"))
        self.adv_clen_lbl.setText(translate("main_window", "Click Length"))
        self.adv_clen_scale_cbox.setItemText(
            0, translate("main_window", "Milliseconds")
        )
        self.adv_clen_scale_cbox.setItemText(1, translate("main_window", "Seconds"))
        self.adv_clen_scale_cbox.setItemText(2, translate("main_window", "Minutes"))
        self.adv_clen_scale_cbox.setItemText(3, translate("main_window", "Hours"))
        self.adv_change_loc_btn.setText(translate("main_window", "Change"))
        self.adv_clk_intvl_lbl.setText(translate("main_window", "Click Interval"))
        self.adv_clk_events_lbl.setText(translate("main_window", "Click Events"))
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
        self.adv_mb_lbl.setText(translate("main_window", "Mouse Button"))
        self.adv_clicks_per_event_lbl.setText(
            translate("main_window", "Clicks per Event")
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

    def keyPressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QKeySequenceEdit):
            if event.key() == Qt.Key_Escape:
                focused_widget.clearFocus()
                focused_widget.clear()
                self.current_hotkey = None
                return
        super().keyPressEvent(event)

    @property
    def in_advanced_tab(self):
        return self.tab_wgt.currentIndex() == 1

    @property
    def inputs(self) -> ClickProcessInputs:
        inputs = ClickProcessInputs()
        inputs.is_advanced = self.in_advanced_tab
        if inputs.is_advanced:
            if self.adv_clk_intvl_ledit.text() != "":
                inputs.click_interval = self.adv_clk_intvl_ledit.text()
            inputs.click_interval_scale_index = (
                self.adv_clk_intvl_scale_cbox.currentIndex()
            )
            if self.adv_clen_ledit.text() != "":
                inputs.click_length = self.adv_clen_ledit.text()
            inputs.click_length_scale_index = self.adv_clen_scale_cbox.currentIndex()
            if self.adv_clicks_per_event_ledit.text() != "":
                inputs.clicks_per_event = self.adv_clicks_per_event_ledit.text()
            inputs.click_events = (
                self.adv_clk_events_ledit.text()
                if self.adv_clk_events_ledit.text() != ""
                else None
            )
            inputs.click_location = self.advanced_location
            inputs.mouse_button_index = self.adv_mb_cbox.currentIndex()
        else:
            if self.smpl_clk_intvl_ledit.text() != "":
                inputs.click_interval = self.smpl_clk_intvl_ledit.text()
            inputs.click_interval_scale_index = (
                self.smpl_clk_intvl_scale_cbox.currentIndex()
            )
            inputs.click_location = self.simple_location
            inputs.mouse_button_index = self.smpl_mb_cbox.currentIndex()
        return inputs

    @pyqtSlot()
    def terminate_processes(self):
        ClickProcess.terminate_all()

    @property
    def hotkey_with_location(self) -> bool:
        return (
            (
                self.advanced_location is None
                or not self.adv_hkey_keyseq.keySequence().isEmpty()
            )
            if self.in_advanced_tab
            else (
                self.simple_location is None
                or not self.smpl_hkey_keyseq.keySequence().isEmpty()
            )
        )

    @pyqtSlot()
    def start_button_clicked(self):
        if not self.hotkey_with_location:
            return
        self.active_process = True
        self.stop_btn.setDisabled(False)
        self.start_btn.setDisabled(True)
        ClickProcess.terminate_all()
        click_process = ClickProcess.get_appropriate(self.inputs)
        click_process.start()

    @pyqtSlot()
    def stop_button_clicked(self):
        self.active_process = False
        self.stop_btn.setDisabled(True)
        self.start_btn.setDisabled(False)
        self.terminate_processes()

    @pyqtSlot()
    def switched_tabs(self):
        if self.first_tab_switch:
            self.first_tab_switch = False
            return
        self.terminate_processes()

    @pyqtSlot()
    def hotkey_changed(self):
        sender = self.sender()
        if sender == self.smpl_hkey_keyseq:
            self.adv_hkey_keyseq.setKeySequence(self.smpl_hkey_keyseq.keySequence())
        elif sender == self.adv_hkey_keyseq:
            self.smpl_hkey_keyseq.setKeySequence(self.adv_hkey_keyseq.keySequence())
        key_sequence = sender.keySequence().toString()
        if key_sequence:
            key_sequence = str(key_sequence).replace(" ", "").lower()
            if self.current_hotkey:
                keyboard.unhook_all_hotkeys()
            self.current_hotkey = keyboard.add_hotkey(key_sequence, self.hotkey_toggle)

    def closeEvent(self, event):
        keyboard.unhook_all()
        mouse.unhook_all()
        event.accept()

    def hotkey_toggle(self):
        (
            self.stop_button_clicked()
            if self.active_process
            else self.start_button_clicked()
        )

    def change_location(self):
        advanced_tab = self.in_advanced_tab

        def set_location():
            x, y = mouse.get_position()
            if advanced_tab:
                self.advanced_location = (x, y)
                self.adv_change_loc_btn.setEnabled(True)
            else:
                self.simple_location = (x, y)
                self.smpl_change_loc_btn.setEnabled(True)
            self.update_location_displays()
            mouse.unhook_all()

        (
            self.adv_change_loc_btn.setEnabled(False)
            if advanced_tab
            else self.smpl_change_loc_btn.setEnabled(False)
        )
        sleep(0.1)
        mouse.on_click(set_location)

    def update_location_displays(self):
        if self.advanced_location is not None:
            self.adv_loc_display_ledit.setText(
                f"({self.advanced_location[0]}, {self.advanced_location[1]})"
            )
        if self.simple_location is not None:
            self.smpl_loc_display_ledit.setText(
                f"({self.simple_location[0]}, {self.simple_location[1]})"
            )
