from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QSizePolicy, QGridLayout, QLayout, QLabel, QComboBox, QLineEdit, QKeySequenceEdit, QPushButton, QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget
        self.central_widget_layout = QVBoxLayout
        self.tab_widget = QTabWidget
        self.simple_tab = QWidget
        self.simple_grid_layout = QGridLayout
        self.simple_click_interval_label = QLabel
        self.simple_click_interval_timescale_combo_box = QComboBox
        self.simple_hotkey_label = QLabel
        self.simple_location_display_line_edit = QLineEdit
        self.simple_mouse_button_combo_box = QComboBox
        self.simple_hotkey_key_sequence = QKeySequenceEdit
        self.simple_change_location_button = QPushButton
        self.simple_mouse_button_label = QLabel
        self.simple_click_interval_line_edit = QLineEdit
        self.simple_location_label = QLabel
        self.advanced_tab = QWidget
        self.advanced_grid_layout = QGridLayout
        self.advanced_clicks_per_event_line_edit = QLineEdit
        self.advanced_click_events_line_edit = QLineEdit
        self.advanced_clicks_per_event_label = QLabel
        self.advanced_mouse_button_label = QLabel
        self.advanced_hotkey_label = QLabel
        self.advanced_click_interval_timescale_combo_box = QComboBox
        self.advanced_click_events_label = QLabel
        self.advanced_click_interval_label = QLabel
        self.advanced_change_location_button = QPushButton
        self.advanced_click_length_timescale_combo_box = QComboBox
        self.advanced_hotkey_key_sequence = QKeySequenceEdit
        self.advanced_click_length_label = QLabel
        self.advanced_click_interval_line_edit = QLineEdit
        self.advanced_mouse_button_combo_box = QComboBox
        self.advanced_click_length_line_edit = QLineEdit
        self.advanced_location_display_line_edit = QLineEdit
        self.advanced_location_label = QLabel
        self.button_layout = QHBoxLayout
        self.start_button = QPushButton
        self.stop_button = QPushButton

        self.initialize_window()
        self.translate_ui()

    def initialize_window(self):
        self.setObjectName("main_window")
        self.resize(425, 0)
        self.setWindowIcon(QIcon("../../assets/icon.png"))

        self.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.initialize_central_widget()


    def initialize_central_widget(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")

        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.setObjectName("central_widget_layout")
        central_widget_layout.setContentsMargins(5, 5, 5, 5)
        central_widget_layout.setSpacing(0)
        central_widget.setLayout(central_widget_layout)
        self.central_widget_layout = central_widget_layout

        self.setCentralWidget(central_widget)
        self.central_widget = central_widget

        self.initialize_tabs()
        self.initialize_button_controls()

    def initialize_tabs(self):
        tab_widget = QTabWidget(self.central_widget)
        tab_widget.setObjectName("tab_widget")
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(tab_widget.sizePolicy().hasHeightForWidth())
        tab_widget.setSizePolicy(size_policy)
        tab_widget.setMinimumSize(QSize(0, 0))
        tab_widget.setAutoFillBackground(False)
        tab_widget.setTabShape(QTabWidget.Rounded)

        self.central_widget_layout.addWidget(tab_widget)
        self.tab_widget = tab_widget

        self.initialize_simple_tab()
        self.initialize_advanced_tab()

    def initialize_simple_tab(self):
        simple_tab = QWidget()
        simple_tab.setObjectName("simple_tab")

        simple_grid_layout = QGridLayout(simple_tab)
        simple_grid_layout.setObjectName("simple_grid_layout")
        simple_grid_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        simple_click_interval_label = QLabel(simple_tab)
        simple_click_interval_label.setObjectName("simple_click_interval_label")
        simple_click_interval_label.setLayoutDirection(Qt.LeftToRight)
        simple_grid_layout.addWidget(simple_click_interval_label, 0, 0, 1, 1, Qt.AlignRight)
        self.simple_click_interval_label = simple_click_interval_label

        simple_click_interval_timescale_combo_box = QComboBox(simple_tab)
        simple_click_interval_timescale_combo_box.setObjectName("simple_click_interval_timescale_combo_box")
        simple_click_interval_timescale_combo_box.setMinimumSize(QSize(0, 0))
        simple_click_interval_timescale_combo_box.addItem("")
        simple_click_interval_timescale_combo_box.addItem("")
        simple_click_interval_timescale_combo_box.addItem("")
        simple_click_interval_timescale_combo_box.addItem("")
        simple_grid_layout.addWidget(simple_click_interval_timescale_combo_box, 0, 2, 1, 1)
        self.simple_click_interval_timescale_combo_box = simple_click_interval_timescale_combo_box

        simple_hotkey_label = QLabel(simple_tab)
        simple_hotkey_label.setObjectName("simple_hotkey_label")
        simple_grid_layout.addWidget(simple_hotkey_label, 3, 0, 1, 1, Qt.AlignRight)
        self.simple_hotkey_label = simple_hotkey_label

        simple_location_display_line_edit = QLineEdit(simple_tab)
        simple_location_display_line_edit.setObjectName("simple_location_display_line_edit")
        simple_location_display_line_edit.setReadOnly(True)
        simple_location_display_line_edit.setPlaceholderText("")
        simple_grid_layout.addWidget(simple_location_display_line_edit, 2, 1, 1, 1)
        self.simple_location_display_line_edit = simple_location_display_line_edit

        simple_mouse_button_combo_box = QComboBox(simple_tab)
        simple_mouse_button_combo_box.setObjectName("simple_mouse_button_combo_box")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(simple_mouse_button_combo_box.sizePolicy().hasHeightForWidth())
        simple_mouse_button_combo_box.setSizePolicy(size_policy)
        simple_mouse_button_combo_box.setEditable(False)
        simple_mouse_button_combo_box.setMaxVisibleItems(3)
        simple_mouse_button_combo_box.addItem("")
        simple_mouse_button_combo_box.addItem("")
        simple_mouse_button_combo_box.addItem("")
        simple_grid_layout.addWidget(simple_mouse_button_combo_box, 1, 1, 1, 2)
        self.simple_mouse_button_combo_box = simple_mouse_button_combo_box

        simple_hotkey_key_sequence = QKeySequenceEdit(simple_tab)
        simple_hotkey_key_sequence.setObjectName("simple_hotkey_key_sequence")
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(simple_hotkey_key_sequence.sizePolicy().hasHeightForWidth())
        simple_hotkey_key_sequence.setSizePolicy(size_policy)
        simple_grid_layout.addWidget(simple_hotkey_key_sequence, 3, 1, 1, 2)
        self.simple_hotkey_key_sequence = simple_hotkey_key_sequence

        simple_change_location_button = QPushButton(simple_tab)
        simple_change_location_button.setObjectName("simple_change_location_button")
        simple_grid_layout.addWidget(simple_change_location_button, 2, 2, 1, 1)
        self.simple_change_location_button = simple_change_location_button

        simple_mouse_button_label = QLabel(simple_tab)
        simple_mouse_button_label.setObjectName("simple_mouse_button_label")
        simple_grid_layout.addWidget(simple_mouse_button_label, 1, 0, 1, 1, Qt.AlignRight)
        self.simple_mouse_button_label = simple_mouse_button_label

        simple_click_interval_line_edit = QLineEdit(simple_tab)
        simple_click_interval_line_edit.setObjectName("simple_click_interval_line_edit")
        simple_click_interval_line_edit.setMaxLength(7)
        simple_grid_layout.addWidget(simple_click_interval_line_edit, 0, 1, 1, 1)
        self.simple_click_interval_line_edit = simple_click_interval_line_edit

        simple_location_label = QLabel(simple_tab)
        simple_location_label.setObjectName("simple_location_label")
        simple_grid_layout.addWidget(simple_location_label, 2, 0, 1, 1, Qt.AlignRight)
        self.simple_location_label = simple_location_label

        simple_grid_layout.setColumnStretch(0, 0)
        simple_grid_layout.setColumnStretch(1, 4)
        simple_grid_layout.setColumnStretch(2, 3)
        self.simple_grid_layout = simple_grid_layout

        self.tab_widget.addTab(simple_tab, "")
        self.simple_tab = simple_tab
    
    def initialize_advanced_tab(self):
        advanced_tab = QWidget()
        advanced_tab.setObjectName("advanced_tab")
        
        advanced_grid_layout = QGridLayout(advanced_tab)
        advanced_grid_layout.setObjectName("advanced_grid_layout")
        advanced_grid_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        
        advanced_location_label = QLabel(advanced_tab)
        advanced_location_label.setObjectName("advanced_location_label")
        advanced_grid_layout.addWidget(advanced_location_label, 5, 0, 1, 1, Qt.AlignRight)
        self.advanced_location_label = advanced_location_label
        
        advanced_location_display_line_edit = QLineEdit(advanced_tab)
        advanced_location_display_line_edit.setObjectName("advanced_location_display_line_edit")
        advanced_location_display_line_edit.setReadOnly(True)
        advanced_location_display_line_edit.setPlaceholderText("")
        advanced_grid_layout.addWidget(advanced_location_display_line_edit, 5, 1, 1, 1)
        self.advanced_location_display_line_edit = advanced_location_display_line_edit
        
        advanced_click_length_line_edit = QLineEdit(advanced_tab)
        advanced_click_length_line_edit.setObjectName("advanced_click_length_line_edit")
        advanced_grid_layout.addWidget(advanced_click_length_line_edit, 1, 1, 1, 1)
        self.advanced_click_length_line_edit = advanced_click_length_line_edit
        
        advanced_mouse_button_combo_box = QComboBox(advanced_tab)
        advanced_mouse_button_combo_box.setObjectName("advanced_mouse_button_combo_box")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(advanced_mouse_button_combo_box.sizePolicy().hasHeightForWidth())
        advanced_mouse_button_combo_box.setSizePolicy(size_policy)
        advanced_mouse_button_combo_box.setEditable(False)
        advanced_mouse_button_combo_box.setMaxVisibleItems(3)
        advanced_mouse_button_combo_box.addItem("")
        advanced_mouse_button_combo_box.addItem("")
        advanced_mouse_button_combo_box.addItem("")
        advanced_grid_layout.addWidget(advanced_mouse_button_combo_box, 4, 1, 1, 2)
        self.advanced_mouse_button_combo_box = advanced_mouse_button_combo_box
        
        advanced_click_interval_line_edit = QLineEdit(advanced_tab)
        advanced_click_interval_line_edit.setObjectName("advanced_click_interval_line_edit")
        advanced_click_interval_line_edit.setMaxLength(7)
        advanced_grid_layout.addWidget(advanced_click_interval_line_edit, 0, 1, 1, 1)
        self.advanced_click_interval_line_edit = advanced_click_interval_line_edit
        
        advanced_click_length_label = QLabel(advanced_tab)
        advanced_click_length_label.setObjectName("advanced_click_length_label")
        advanced_grid_layout.addWidget(advanced_click_length_label, 1, 0, 1, 1, Qt.AlignRight)
        self.advanced_click_length_label = advanced_click_length_label
        
        advanced_hotkey_key_sequence = QKeySequenceEdit(advanced_tab)
        advanced_hotkey_key_sequence.setObjectName("advanced_hotkey_key_sequence")
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(advanced_hotkey_key_sequence.sizePolicy().hasHeightForWidth())
        advanced_hotkey_key_sequence.setSizePolicy(size_policy)
        advanced_grid_layout.addWidget(advanced_hotkey_key_sequence, 6, 1, 1, 2)
        self.advanced_hotkey_key_sequence = advanced_hotkey_key_sequence
        
        advanced_click_length_timescale_combo_box = QComboBox(advanced_tab)
        advanced_click_length_timescale_combo_box.setObjectName("advanced_click_length_timescale_combo_box")
        advanced_click_length_timescale_combo_box.addItem("")
        advanced_click_length_timescale_combo_box.addItem("")
        advanced_click_length_timescale_combo_box.addItem("")
        advanced_click_length_timescale_combo_box.addItem("")
        advanced_grid_layout.addWidget(advanced_click_length_timescale_combo_box, 1, 2, 1, 1)
        self.advanced_click_length_timescale_combo_box = advanced_click_length_timescale_combo_box
        
        advanced_change_location_button = QPushButton(advanced_tab)
        advanced_change_location_button.setObjectName("advanced_change_location_button")
        advanced_grid_layout.addWidget(advanced_change_location_button, 5, 2, 1, 1)
        self.advanced_change_location_button = advanced_change_location_button
        
        advanced_click_interval_label = QLabel(advanced_tab)
        advanced_click_interval_label.setObjectName("advanced_click_interval_label")
        advanced_click_interval_label.setLayoutDirection(Qt.LeftToRight)
        advanced_grid_layout.addWidget(advanced_click_interval_label, 0, 0, 1, 1, Qt.AlignRight)
        self.advanced_click_interval_label = advanced_click_interval_label
        
        advanced_click_events_label = QLabel(advanced_tab)
        advanced_click_events_label.setObjectName("advanced_click_events_label")
        advanced_grid_layout.addWidget(advanced_click_events_label, 2, 0, 1, 1, Qt.AlignRight)
        self.advanced_click_events_label = advanced_click_events_label
        
        advanced_click_interval_timescale_combo_box = QComboBox(advanced_tab)
        advanced_click_interval_timescale_combo_box.setObjectName("advanced_click_interval_timescale_combo_box")
        advanced_click_interval_timescale_combo_box.setMinimumSize(QSize(0, 0))
        advanced_click_interval_timescale_combo_box.addItem("")
        advanced_click_interval_timescale_combo_box.addItem("")
        advanced_click_interval_timescale_combo_box.addItem("")
        advanced_click_interval_timescale_combo_box.addItem("")
        advanced_grid_layout.addWidget(advanced_click_interval_timescale_combo_box, 0, 2, 1, 1)
        self.advanced_click_interval_timescale_combo_box = advanced_click_interval_timescale_combo_box
        
        advanced_hotkey_label = QLabel(advanced_tab)
        advanced_hotkey_label.setObjectName("advanced_hotkey_label")
        advanced_grid_layout.addWidget(advanced_hotkey_label, 6, 0, 1, 1, Qt.AlignRight)
        self.advanced_hotkey_label = advanced_hotkey_label
        
        advanced_mouse_button_label = QLabel(advanced_tab)
        advanced_mouse_button_label.setObjectName("advanced_mouse_button_label")
        advanced_grid_layout.addWidget(advanced_mouse_button_label, 4, 0, 1, 1, Qt.AlignRight)
        self.advanced_mouse_button_label = advanced_mouse_button_label
        
        advanced_clicks_per_event_label = QLabel(advanced_tab)
        advanced_clicks_per_event_label.setObjectName("advanced_clicks_per_event_label")
        advanced_grid_layout.addWidget(advanced_clicks_per_event_label, 3, 0, 1, 1, Qt.AlignRight)
        self.advanced_clicks_per_event_label = advanced_clicks_per_event_label
        
        advanced_click_events_line_edit = QLineEdit(advanced_tab)
        advanced_click_events_line_edit.setObjectName("advanced_click_events_line_edit")
        advanced_grid_layout.addWidget(advanced_click_events_line_edit, 2, 1, 1, 2)
        self.advanced_click_events_line_edit = advanced_click_events_line_edit
        
        advanced_clicks_per_event_line_edit = QLineEdit(advanced_tab)
        advanced_clicks_per_event_line_edit.setObjectName("advanced_clicks_per_event_line_edit")
        advanced_grid_layout.addWidget(advanced_clicks_per_event_line_edit, 3, 1, 1, 2)
        self.advanced_clicks_per_event_line_edit = advanced_clicks_per_event_line_edit
        
        advanced_grid_layout.setColumnStretch(0, 0)
        advanced_grid_layout.setColumnStretch(1, 4)
        advanced_grid_layout.setColumnStretch(2, 3)
        self.advanced_grid_layout = advanced_grid_layout
        
        self.tab_widget.addTab(advanced_tab, "")
        self.advanced_tab = advanced_tab

    def initialize_button_controls(self):
        button_layout = QHBoxLayout()
        button_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        button_layout.setContentsMargins(0, 5, 0, 0)
        button_layout.setSpacing(5)
        button_layout.setObjectName("button_layout")

        start_button = QPushButton(self.central_widget)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(start_button.sizePolicy().hasHeightForWidth())
        start_button.setSizePolicy(size_policy)
        start_button.setMinimumSize(QSize(0, 50))
        start_button.setObjectName("start_button")
        button_layout.addWidget(start_button)
        self.start_button = start_button

        stop_button = QPushButton(self.central_widget)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(stop_button.sizePolicy().hasHeightForWidth())
        stop_button.setSizePolicy(size_policy)
        stop_button.setMinimumSize(QSize(0, 50))
        stop_button.setBaseSize(QSize(0, 0))
        stop_button.setObjectName("stop_button")
        button_layout.addWidget(stop_button)
        self.stop_button = stop_button

        button_layout.setStretch(0, 1)
        button_layout.setStretch(1, 1)
        self.central_widget_layout.addLayout(button_layout)
        self.button_layout = button_layout

    def translate_ui(self):
        translate = QCoreApplication.translate
        self.setWindowTitle(translate("main_window", "Easy Auto Clicker"))
        self.simple_click_interval_label.setText(translate("main_window", "Click Interval"))
        self.simple_click_interval_timescale_combo_box.setItemText(0, translate("main_window", "Milliseconds"))
        self.simple_click_interval_timescale_combo_box.setItemText(1, translate("main_window", "Seconds"))
        self.simple_click_interval_timescale_combo_box.setItemText(2, translate("main_window", "Minutes"))
        self.simple_click_interval_timescale_combo_box.setItemText(3, translate("main_window", "Hours"))
        self.simple_hotkey_label.setText(translate("main_window", "Hotkey"))
        self.simple_mouse_button_combo_box.setItemText(0, translate("main_window", "Left (M1)"))
        self.simple_mouse_button_combo_box.setItemText(1, translate("main_window", "Right (M2)"))
        self.simple_mouse_button_combo_box.setItemText(2, translate("main_window", "Middle (M3)"))
        self.simple_change_location_button.setText(translate("main_window", "Change"))
        self.simple_mouse_button_label.setText(translate("main_window", "Mouse Button"))
        self.simple_click_interval_line_edit.setPlaceholderText(translate("main_window", "e.g. 100"))
        self.simple_location_label.setText(translate("main_window", "Location"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.simple_tab), translate("main_window", "Simple"))
        self.advanced_location_label.setText(translate("main_window", "Location"))
        self.advanced_click_length_line_edit.setPlaceholderText(translate("main_window", "e.g. 50"))
        self.advanced_mouse_button_combo_box.setItemText(0, translate("main_window", "Left (M1)"))
        self.advanced_mouse_button_combo_box.setItemText(1, translate("main_window", "Right (M2)"))
        self.advanced_mouse_button_combo_box.setItemText(2, translate("main_window", "Middle (M3)"))
        self.advanced_click_interval_line_edit.setPlaceholderText(translate("main_window", "e.g. 100"))
        self.advanced_click_length_label.setText(translate("main_window", "Click Length"))
        self.advanced_click_length_timescale_combo_box.setItemText(0, translate("main_window", "Milliseconds"))
        self.advanced_click_length_timescale_combo_box.setItemText(1, translate("main_window", "Seconds"))
        self.advanced_click_length_timescale_combo_box.setItemText(2, translate("main_window", "Minutes"))
        self.advanced_click_length_timescale_combo_box.setItemText(3, translate("main_window", "Hours"))
        self.advanced_change_location_button.setText(translate("main_window", "Change"))
        self.advanced_click_interval_label.setText(translate("main_window", "Click Interval"))
        self.advanced_click_events_label.setText(translate("main_window", "Click Events"))
        self.advanced_click_interval_timescale_combo_box.setItemText(0, translate("main_window", "Milliseconds"))
        self.advanced_click_interval_timescale_combo_box.setItemText(1, translate("main_window", "Seconds"))
        self.advanced_click_interval_timescale_combo_box.setItemText(2, translate("main_window", "Minutes"))
        self.advanced_click_interval_timescale_combo_box.setItemText(3, translate("main_window", "Hours"))
        self.advanced_hotkey_label.setText(translate("main_window", "Hotkey"))
        self.advanced_mouse_button_label.setText(translate("main_window", "Mouse Button"))
        self.advanced_clicks_per_event_label.setText(translate("main_window", "Clicks per Event"))
        self.advanced_click_events_line_edit.setPlaceholderText(translate("main_window", "e.g. 0"))
        self.advanced_clicks_per_event_line_edit.setPlaceholderText(translate("main_window", "e.g. 1"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.advanced_tab), translate("main_window", "Advanced"))
        self.start_button.setText(translate("main_window", "Start"))
        self.stop_button.setText(translate("main_window", "Stop"))