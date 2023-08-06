from PyQt5.QtWidgets import (QWidget, QCheckBox, QPushButton, QVBoxLayout, 
                             QLineEdit, QSpinBox, QGridLayout, QLabel, 
                             QComboBox, QDoubleSpinBox, QColorDialog, 
                             QRadioButton, QScrollBar)
from PyQt5 import QtCore, QtGui
import qtawesome as qta
from pyrateshield import labels, Observable, GLOBAL_LOG_LEVEL
from pyrateshield.gui import io
from pyrateshield.constants import CONSTANTS

MAX_VALUE = float('inf')
MAX_INT_VALUE = 99999999



LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10

def safe_to_int(value):
    if value == '':
        value = 0
    else:
        value = int(round(float(value)))
    return value

def safe_to_float(value):
    if value == '':
        value = 0
    else:
        value = float(value)
    return value

def safe_set_value_to_widget(widget, value):
    # Set widget to a specified value
    # do not set when value equals current value
    # will not generate events when changed
    
    if isinstance(widget, QSpinBox):
        if widget.value() != safe_to_int(value):
            widget.setValue(safe_to_int(value))
    elif isinstance(widget, QDoubleSpinBox):
        if widget.value() != safe_to_float(value):
            widget.setValue(safe_to_float(value))
    elif isinstance(widget, (QLineEdit, QLabel)):
        if widget.text() != str(value):
            widget.setText(str(value))
    elif isinstance(widget, QCheckBox):
        if widget.isChecked() != value:
            widget.setChecked(value)
    elif isinstance(widget, QScrollBar):
        if widget.value() != safe_to_int(value):
            widget.setValue(safe_to_int(value))
    elif isinstance(widget, QComboBox):
        if isinstance(value, str):
            value = widget.findText(str(value))
        if widget.currentIndex != safe_to_int(value):
            widget.setCurrentIndex(safe_to_int(value))
    else:
        raise TypeError(f'Unsupported widget type {type(widget)}')

class QDoubleSpinBoxInfinite(QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super(QDoubleSpinBox, self).__init__(*args, **kwargs)

        self.setMinimum(float('-inf'))
        self.setMaximum(float('inf'))

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if e.key() == QtCore.Qt.Key_End:
            self.setValue(self.maximum())
        elif e.key() == QtCore.Qt.Key_Home:
            self.setValue(self.minimum())
        else:
            super(QDoubleSpinBox, self).keyPressEvent(e)
            
            
            
            
            
    
        
class EditViewBase(QWidget, Observable):
    EVENT_VIEW_UPDATE = 'event_view_update'
    _layout = None
    #LABEL = 'label'
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Observable.__init__(self, log_level=LOG_LEVEL)
        self.create_widgets()
        self.create_layout()
        self.set_callbacks()
        self.set_stretch()
        
    def set_callbacks(self):
        pass
    
    def create_widgets(self):
        pass
    
    def create_layout(self, label):
        pass
    
    def emit_change(self, event_data=None):
        self.logger.debug(f'View changed with event data: {str(event_data)}')
        self.emit(self.EVENT_VIEW_UPDATE, event_data)
        
    
    def set_stretch(self):
        self.stretch_layout = QVBoxLayout()
        
            
        self.stretch_layout.addLayout(self.layout)
        if hasattr(self, 'explanation'):
            self.help_button = QPushButton('Help')
            callback = lambda : io.show_help(title=self.LABEL,
                                             text = self.explanation)
            self.help_button.clicked.connect(callback)        
            self.stretch_layout.addWidget(self.help_button)
            
        self.stretch_layout.addStretch(1)
        self.setLayout(self.stretch_layout)
        
    @property
    def layout(self):
        if self._layout is None:
            self._layout = QGridLayout()
        return self._layout
        
    def set_enabled(self, enabled):
        index = self.layout.count()
        for i in range(index):
            widget = self.layout.itemAt(i).widget()
            widget.setEnabled(enabled)
            
        
class EditListViewBase(EditViewBase):
    _name_text = "Name:"
    EVENT_LIST_SELECTION = 'event_list_selection'
    
    def __init__(self, parent=None):
    
        super().__init__(parent)
        
        
    def create_widgets(self):
        self.list = QComboBox(self)
        
        # self.save_button = QPushButton('Save', self)
        # self.undo_button = QPushButton('Undo', self)
        #self.new_button = QPushButton('Add', self)
        #self.delete_button = QPushButton('Delete', self)
    
        self.name_label = QLabel(self._name_text)
        self.name_input = QLineEdit()
        
        self.enabled_checkbox = QCheckBox('Enabled')
        
    def set_enabled(self, enabled):
        super().set_enabled(enabled)   
        
        self.list.setEnabled(True)

    def set_callbacks(self):
        label = labels.NAME
        callback = lambda label=label: self.emit_change(label)
        self.name_input.returnPressed.connect(callback)
        
        label = labels.ENABLED
        callback = lambda event_data, labels=label: self.emit_change(label)        
        
        self.enabled_checkbox.stateChanged.connect(callback)    
        self.list.currentIndexChanged.connect(self.list_selection)

        
    def list_selection(self, _=None):
        self.logger.debug('List Selection')
        self.emit(self.EVENT_LIST_SELECTION, event_data=self.list.currentIndex())

        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.list, row , 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.name_label, row, 0)
        self.layout.addWidget(self.name_input, row, 1)
      
        self.create_layout_body()
        
        row  = self.layout.rowCount() + 1

        self.layout.addWidget(self.enabled_checkbox, row, 0)

        
    def create_layout_body(self):
        pass
        
    def clear(self):
        self.name_input.clear()      
    
    def emit_change(self, label):
        self.logger.debug(f'Item {label} in view changed')
        value = self.to_dict()[label]
        super().emit_change(event_data = {label: value})
        
    def to_dict(self):
        return {labels.NAME: self.name_input.text(),
                labels.ENABLED: self.enabled_checkbox.isChecked()}
    
    def from_dict(self, dct):
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        for label, value in dct.items():
            if label == labels.NAME:
                safe_set_value_to_widget(self.name_input, value)   
                self.logger.debug(f'Setting list to {value}')
                safe_set_value_to_widget(self.list, value)
            elif label == labels.ENABLED:
                safe_set_value_to_widget(self.enabled_checkbox, value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
class EditListViewPositionBase(EditListViewBase):
    _position_x_text = "X [cm]:"
    _position_y_text = "Y [cm]:"
    
    
    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.POSITION
        callback = lambda _, label=label: self.emit_change(label)
        
        self.x.valueChanged.connect(callback)
        self.y.valueChanged.connect(callback)
        

    def to_dict(self):
        dct = super().to_dict()
        dct[labels.POSITION] = self.get_position()
        return dct

    def from_dict(self, dct):
       super().from_dict(dct)       
       #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
       for label, value in dct.items():
            if label == labels.POSITION:
                self.set_position(value)
       #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
  
    def create_widgets(self):
        super().create_widgets()

        x = QDoubleSpinBox(decimals=1)
        x.setRange(-MAX_VALUE, MAX_VALUE)
    
        y = QDoubleSpinBox(decimals=1)
        y.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.x = x
        self.y = y
        self.position_label = QLabel(labels.POSITION)
        self.position_label.setStyleSheet('font-weight: bold')
        self.position_x_label = QLabel(self._position_x_text)
        self.position_y_label = QLabel(self._position_y_text)
        
        #self.position_button = QPushButton("Set Position By Mouse")
        
    def create_layout_body(self):
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.position_label, row, 0, 1, 2)
        row += 1
        self.layout.addWidget(self.position_x_label, row, 0)
        self.layout.addWidget(self.x, row, 1)
        row += 1
        self.layout.addWidget(self.position_y_label, row, 0)
        self.layout.addWidget(self.y, row, 1)
        # row += 1
        # self.layout.addWidget(self.position_button, row, 0, 1, 2)
        
    def clear(self):
        super().clear()
        self.x.clear()
        self.y.clear()
        
    def set_position(self, coords):
        safe_set_value_to_widget(self.x, coords[0])
        safe_set_value_to_widget(self.y, coords[1])
        
    def get_position(self):
        return [self.x.value(), self.y.value()]
        

class EditMaterialsView(EditListViewBase):
    LABEL = labels.MATERIALS
    explanation =\
        ('Materials can be changed or added to a limited extend. '
         'Radtracer implements a limited set of materials. Pyshield uses '
         'attenuation and buildup tables for a limited set of '
         'materials. For some materials, like "Concrete-Barite", there is no '
         'buildup table available. For example the buildup table for "Concrete" is '
         'used for "Concrete-Barite" in pyshield. '
         '\n\n'
         'Defining or changing a material is mostly usefull to define a '
         'material that has a (slightly) different density. '
         'Both pyshield and radtracer can handle variations in density accurately.')
        
    
    def create_widgets(self):
        super().create_widgets()
        
        self.density_label = QLabel('Density [g/cm^3]')
        self.density_input = QDoubleSpinBox(decimals=3)
        self.attenuation_label = QLabel(labels.ATTENUATION_TABLE)
        self.attenuation_combo = QComboBox()
        self.attenuation_combo.addItems(CONSTANTS.base_materials)
        self.buildup_combo = QComboBox()
        self.buildup_combo.addItems(CONSTANTS.buildup_materials)
        self.buildup_label = QLabel(labels.BUILDUP_TABLE)
        self.radtracer_label = QLabel('Radtracer')
        self.pyshield_label = QLabel('Pyshield')
        self.radtracer_material_label = QLabel(labels.MATERIAL)
        self.radtracer_material_combo = QComboBox()
        self.radtracer_material_combo.addItems(CONSTANTS.base_materials)
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
    def from_dict(self, dct):
        super().from_dict(dct)
        
        for label, value in dct.items():
            if label == labels.DENSITY:
                safe_set_value_to_widget(self.density_input, value)
            
    
            elif label == labels.RADTRACER_MATERIAL:
                safe_set_value_to_widget(self.radtracer_material_combo, value)
                
            elif label == labels.ATTENUATION_TABLE:
                safe_set_value_to_widget(self.attenuation_combo, value)
            elif label == labels.BUILDUP_TABLE:
                safe_set_value_to_widget(self.buildup_combo, value)
    
    def to_dict(self):
        dct = super().to_dict()
        dct.pop(labels.ENABLED, None)
        
        dct[labels.DENSITY] = self.density_input.value()
        dct[labels.RADTRACER_MATERIAL] = self.radtracer_material_combo.currentText()
        
        dct[labels.ATTENUATION_TABLE] = self.attenuation_combo.currentText()
        dct[labels.BUILDUP_TABLE] = self.buildup_combo.currentText()
        return dct
        
    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.DENSITY
        callback = lambda _, label=label: self.emit_change(label)
        self.density_input.valueChanged.connect(callback)
        
        label = labels.RADTRACER_MATERIAL
        callback = lambda _, label=label: self.emit_change(label)
        self.radtracer_material_combo.currentTextChanged.connect(callback)
        
        label = labels.ATTENUATION_TABLE
        callback = lambda _, label=label: self.emit_change(label)
        self.attenuation_combo.currentTextChanged.connect(callback)
        
        label = labels.BUILDUP_TABLE
        callback = lambda _, label=label: self.emit_change(label)
        self.buildup_combo.currentTextChanged.connect(callback)
        
        
    def clear(self):
        safe_set_value_to_widget(self.density_input, 0)
        
        safe_set_value_to_widget(self.radtracer_material_combo, 
                                 CONSTANTS.base_materials[0])
        
        safe_set_value_to_widget(self.attenuation_table_combo, 
                                 CONSTANTS.base_materials[0])
        
        safe_set_value_to_widget(self.buildup_table_combo, 
                                 CONSTANTS.buildup_materials[0])
        
    
    def create_layout(self):
        super().create_layout()
        
        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.density_label, row, 0)
        self.layout.addWidget(self.density_input, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.radtracer_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.radtracer_material_label, row, 0)
        self.layout.addWidget(self.radtracer_material_combo, row, 1)
        
        
        row += 1
        self.layout.addWidget(self.pyshield_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.attenuation_label, row, 0)
        self.layout.addWidget(self.attenuation_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.buildup_label, row, 0)
        self.layout.addWidget(self.buildup_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        self.enabled_checkbox.setVisible(False)
        
    
    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self.new_button.setEnabled(True)
        
        
    
        
class EditShieldingView(EditListViewBase):
    LABEL = labels.SHIELDINGS
    _color = 'r'
    _DEFAULT_THICKNESS = 1
    _DEFAULT_LINEWIDTH = 1
    
   
    def from_dict(self, dct):
        super().from_dict(dct)
       # self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
       # self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
        for label, value in dct.items():
            if label == labels.MATERIALS:
                self.set_materials(value)
    
            elif label == labels.COLOR:
                if self.color != value:
                    self.color = value
                
            elif label == labels.LINEWIDTH:
                safe_set_value_to_widget(self.line_width, value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)

    
    @property
    def color(self):       
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color        
        icon = qta.icon('fa5s.circle', color=color)
        
        self.color_button.setIcon(icon)
        
        self.emit_change(labels.COLOR)
    
    
    def select_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.color = color.name()
            
    def to_dict(self):
        dct = super().to_dict()
        dct.pop(labels.ENABLED, None)
        
        dct[labels.LINEWIDTH]   = self.line_width.value()
        dct[labels.COLOR]       = self.color
        dct[labels.MATERIALS]   = self.get_materials()
    
        
        return dct
    
    def get_materials(self):
        material1 = self.material1_list.currentText()
        thickness1 = self.thickness1_input.value()
        
        material2 = self.material2_list.currentText()
        thickness2 =  self.thickness2_input.value()
        
        materials = [[material1, thickness1], [material2, thickness2]]
        return materials
    
    
    def set_materials(self, materials):
        if len(materials) > 0:
             material1, thickness1 = materials[0]
        else:
            material1, thickness1 = [labels.EMPTY_MATERIAL, 0]
            
        if len(materials) > 1:
            material2, thickness2 = materials[1]
        else:
            material2, thickness2 = [labels.EMPTY_MATERIAL, 0]

        safe_set_value_to_widget(self.material1_list, material1)
        safe_set_value_to_widget(self.material2_list, material2)
        safe_set_value_to_widget(self.thickness1_input, thickness1)
        safe_set_value_to_widget(self.thickness2_input, thickness2)

    
    def create_widgets(self):
        super().create_widgets()
        
        #icon = qta.icon('fa5s.circle', color='red')
        self.color_button = QPushButton("Select Color", self)
        #self.color_button.setIcon(icon)

        self.material1_label = QLabel(labels.MATERIAL + ' 1')
        self.material1_list = QComboBox()

    
        self.thickness1_label = QLabel(labels.THICKNESS)
        self.thickness1_input = QDoubleSpinBox(decimals=3)
    
        self.material2_label = QLabel(labels.MATERIAL + ' 2')
        self.material2_list = QComboBox()

        # materials = [material.name for material in CONSTANTS.materials]
        
        # self.material1_list.addItems(materials)
        # self.material2_list.addItems(materials)

        self.thickness2_label = QLabel(labels.THICKNESS)
        self.thickness2_input = QDoubleSpinBox(decimals=3)
        
        self.line_width_label = QLabel(labels.LINEWIDTH)
        self.line_width = QDoubleSpinBox()
        
        self.enabled_checkbox.setVisible(False)
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
        
    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self.new_button.setEnabled(True)
        

    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.MATERIALS
        callback = lambda _, label=label: self.emit_change(label)
        
        self.material1_list.currentTextChanged.connect(callback)
        self.material2_list.currentTextChanged.connect(callback)
        self.thickness1_input.valueChanged.connect(callback)
        self.thickness2_input.valueChanged.connect(callback)
        
        label = labels.LINEWIDTH
        callback = lambda _, label=label: self.emit_change(label)
        self.line_width.valueChanged.connect(callback)
        
        self.color_button.clicked.connect(self.select_color)
        
        
    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.material1_label, row, 0)
        self.layout.addWidget(self.material1_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness1_label, row, 0)
        self.layout.addWidget(self.thickness1_input, row, 1)
        row += 1
        self.layout.addWidget(self.material2_label, row, 0)
        self.layout.addWidget(self.material2_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness2_label, row, 0)
        self.layout.addWidget(self.thickness2_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.color_button, row, 0, 1, 2)
        
        row += 1
        self.layout.addWidget(self.line_width_label, row, 0)
        self.layout.addWidget(self.line_width, row, 1)
        super().create_layout_body()
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        
        
    def clear(self):
        super().clear()

        self.thickness1_input.setValue(self._DEFAULT_THICKNESS)
        self.thickness2_input.setValue(self._DEFAULT_THICKNESS)
        self.line_width.setValue(self._DEFAULT_LINEWIDTH)
        
class EditWallsView(EditViewBase):
    LABEL = labels.WALLS
    
    explanation = ("To add a Wall select Wall from the toolbar. "
                   "Click and hold the left mouse button to draw a wall")
    EVENT_SCROLL = 'event_scroll'
    start_x1, start_y1, start_x2, start_y2 = ['X1 [cm]', 'Y1 [cm]', 
                                              'X2 [cm]', 'Y2 [cm]']
    
    def create_widgets(self):
        super().create_widgets()
        self.shielding_label = QLabel("Shielding")
        self.shielding_list = QComboBox()
        
        self.position_input = {}
        self.position_label = {}
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            self.position_input[text] = QDoubleSpinBox()
            self.position_input[text].setRange(-MAX_VALUE, MAX_VALUE)
            self.position_label[text] = QLabel(text)
            
            
        self.scroll_widget = QScrollBar(QtCore.Qt.Horizontal)
        self.scroll_widget.setPageStep(1)
        
        self.index_label = QLabel()
        
    
    def emit_change(self, label):
        self.logger.debug(f'Item {label} in view changed')
        value = self.to_dict()[label]
        super().emit_change(event_data = {label: value})
        
        
    def set_callbacks(self):
        label = labels.SHIELDING
        callback = lambda _, label=label: self.emit_change(label)
        self.shielding_list.currentTextChanged.connect(callback)
        
        
        label = labels.VERTICES
        callback = lambda _, label=label: self.emit_change(label)
        
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            self.position_input[text].valueChanged.connect(callback)
        
        self.scroll_widget.valueChanged.connect(lambda _: self.scroll())
            
    def scroll(self):
        self.emit(self.EVENT_SCROLL, self.scroll_widget.value())
        
            
    def to_dict(self):
        dct = {}
        dct[labels.VERTICES] = self.get_vertices()
        dct[labels.SHIELDING] = self.shielding_list.currentText()

        return dct
        
    def set_index(self, index=None):
        if index is None:
            return
        
        self.scroll_widget.setValue(index)
        self.index_label.setText(f'Wall index {index}')
        
    def create_layout(self): 
        row = 0
        
        self.layout.addWidget(self.scroll_widget, row , 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.index_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.shielding_label, row, 0)
        self.layout.addWidget(self.shielding_list, row, 1)
        
        row += 1
        
        text = self.start_x1
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        row += 1
        
        text = self.start_y1
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        
        row += 1
        
        text = self.start_x2
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        row += 1
        
        text = self.start_y2
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
            
    def from_dict(self, dct):
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        for label, value in dct.items():
            if label == labels.SHIELDING:
                safe_set_value_to_widget(self.shielding_list, 
                                         dct[labels.SHIELDING])      
            elif label == labels.VERTICES:
                self.set_vertices(value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
    
        
    def get_vertices(self):
        return [[self.position_input[self.start_x1].value(),
                 self.position_input[self.start_y1].value()],
                [self.position_input[self.start_x2].value(),
                 self.position_input[self.start_y2].value()]]
        
    def set_vertices(self, vertices):
        v1, v2 = vertices
        x1, y1 = v1
        x2, y2 = v2
        
        safe_set_value_to_widget(self.position_input[self.start_x1], x1)
        safe_set_value_to_widget(self.position_input[self.start_y1], y1)
        safe_set_value_to_widget(self.position_input[self.start_x2], x2)
        safe_set_value_to_widget(self.position_input[self.start_y2], y2)
        
        
    def clear(self):
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            
            self.position_input[text].setValue(0)
        self.shielding_list.setCurrentIndex(0)
        
class EditClearanceView(EditListViewBase):
    LABEL = labels.CLEARANCE
    explanation = ("\nUp to two biological fraction can be defined with a"
                   " corresponding biological halflife. For each fraction "
                   "pyrateshield will calculate an effective halflife by "
                   "combining the physical halflife and biological halflife. "
                   "If (physical) decay is not checked in the Sources NM tab "
                   "physical decay will be ignored and only biological "
                   "decay will be applied.\n\n"
                   "If the fractions add up to less than 1, no biological"
                   "decay correction will be applied to the remaining fraction"
                   "\n\n"
                   "Optionally fractions can be split in time. The first "
                   "fraction will be integrated until the split time. The "
                   "second fraction and if applicable the remaining fraction "
                   "will be integrated from the split time. Integration will "
                   "always stop after source duration.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggle_fraction1()
        self.toggle_fraction2()
        self.toggle_split_time()
     
    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self.new_button.setEnabled(True)
        self.toggle_fraction1()
        self.toggle_fraction2()
        self.toggle_split_time()
        
    def from_dict(self, dct):
        super().from_dict(dct)
        
        if labels.ENABLE_SPLIT_FRACTIONS in dct.keys():
            value = dct[labels.ENABLE_SPLIT_FRACTIONS]
            safe_set_value_to_widget(self.split_time_checkbox, value)   
        
        
        for label, value in dct.items():
            if label == labels.APPLY_FRACTION1:
                safe_set_value_to_widget(self.decay_fraction1_checkbox, value)
                self.enable_fraction1()
            elif label == labels.APPLY_FRACTION2:
                safe_set_value_to_widget(self.decay_fraction2_checkbox, value)
                self.enable_fraction2()
            elif label == labels.DECAY_FRACTION1:
                safe_set_value_to_widget(self.decay_fraction1, value)
            elif label == labels.DECAY_FRACTION2:
                safe_set_value_to_widget(self.decay_fraction2, value)
            elif label == labels.HALFLIFE1:
                safe_set_value_to_widget(self.half_life_value1, value)
            elif label == labels.HALFLIFE2:
                safe_set_value_to_widget(self.half_life_value2, value)
            
            elif label == labels.SPLIT_FRACTION_TIME:
                safe_set_value_to_widget(self.split_time_input, value)
                         
            
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.APPLY_FRACTION1] = self.decay_fraction1_checkbox.isChecked()
        dct[labels.APPLY_FRACTION2] = self.decay_fraction2_checkbox.isChecked()  
        dct[labels.DECAY_FRACTION1] = self.decay_fraction1.value()
        dct[labels.DECAY_FRACTION2] = self.decay_fraction2.value()
        dct[labels.ENABLE_SPLIT_FRACTIONS] = self.split_time_checkbox.isChecked()
        dct[labels.SPLIT_FRACTION_TIME] = self.split_time_input.value()
        dct[labels.HALFLIFE1] = self.half_life_value1.value()
        dct[labels.HALFLIFE2] = self.half_life_value2.value()    
        return dct
    
    
    def create_widgets(self):
        super().create_widgets()
        
        self.decay_fraction1_checkbox = QCheckBox(labels.DECAY_FRACTION1)
        self.decay_fraction1 = QDoubleSpinBox(decimals=2)
        self.decay_fraction1.setRange(0, 1)
        self.decay_fraction1.setSingleStep(0.05)
        

        self.decay_fraction2_checkbox = QCheckBox(labels.DECAY_FRACTION2)
        self.decay_fraction2 = QDoubleSpinBox(decimals=2)
        self.decay_fraction2.setRange(0, 1)
        self.decay_fraction2.setSingleStep(0.05)
        
        # Prevent halflives to become zero
        self.half_life_label1 = QLabel(labels.HALF_LIFE)
        self.half_life_value1 = QDoubleSpinBoxInfinite(decimals=2)
        self.half_life_value1.setRange(0.01, MAX_VALUE)
        
        self.half_life_label2 = QLabel(labels.HALF_LIFE)
        self.half_life_value2 = QDoubleSpinBoxInfinite(decimals=2)
        self.half_life_value2.setRange(0.01, MAX_VALUE)
        
        self.split_time_checkbox = QCheckBox(labels.ENABLE_SPLIT_FRACTIONS)
        self.split_time_label = QLabel(labels.SPLIT_FRACTION_TIME)
        self.split_time_input = QDoubleSpinBox(decimals=1)
        self.split_time_input.setRange(0, MAX_VALUE)
        
        
        self.enabled_checkbox.setVisible(False)
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
    def set_callbacks(self):
        super().set_callbacks()
        label = labels.HALFLIFE1
        callback = lambda _, label=label: self.emit_change(label)        
        self.half_life_value1.valueChanged.connect(callback)
        
        label = labels.HALFLIFE2
        callback = lambda _, label=label: self.emit_change(label)        
        self.half_life_value2.valueChanged.connect(callback)

        label = labels.SPLIT_FRACTION_TIME
        callback = lambda _, label=label: self.emit_change(label)        
        self.split_time_input.valueChanged.connect(callback)
        
        label = labels.DECAY_FRACTION1
        callback = lambda _, label=label: self.emit_change(label)        
        self.decay_fraction1.valueChanged.connect(callback)
        
        label = labels.DECAY_FRACTION2
        callback = lambda _, label=label: self.emit_change(label)        
        self.decay_fraction1.valueChanged.connect(callback)
        
        
        self.decay_fraction1_checkbox.toggled.connect(self.toggle_fraction1)
        self.decay_fraction2_checkbox.toggled.connect(self.toggle_fraction2)
        self.split_time_checkbox.toggled.connect(self.toggle_split_time)
        
        
        
    def create_layout_body(self):
        row = self.layout.rowCount() + 1
     
        self.layout.addWidget(self.decay_fraction1_checkbox, row, 0)
        self.layout.addWidget(self.decay_fraction1, row, 1)
        row += 1
        self.layout.addWidget(self.half_life_label1, row, 0)
        self.layout.addWidget(self.half_life_value1, row, 1)    
                
        row += 1
        
        self.layout.addWidget(self.decay_fraction2_checkbox, row, 0)
        self.layout.addWidget(self.decay_fraction2, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.half_life_label2, row, 0)
        self.layout.addWidget(self.half_life_value2, row, 1)  
        
       
        row += 1
        
        self.layout.addWidget(self.split_time_checkbox, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.split_time_label, row, 0)
        self.layout.addWidget(self.split_time_input, row, 1)
   
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.delete_button, row, 0, 1, 2)
      
        
                    
    def enable_fraction1(self):
        state = self.decay_fraction1_checkbox.isChecked()
        self.decay_fraction1.setEnabled(state)
        self.half_life_label1.setEnabled(state)
        self.half_life_value1.setEnabled(state)
        # if state:
        #     self.validate_fraction1()
        
    
    def enable_fraction2(self):
        state = self.decay_fraction2_checkbox.isChecked()
        self.decay_fraction2.setEnabled(state)
        self.half_life_label2.setEnabled(state)
        self.half_life_value2.setEnabled(state)
        # if state:
        #     self.validate_fraction2()
    
    def enable_split_time(self):
        state = self.split_time_checkbox.isChecked()
        self.split_time_label.setEnabled(state)
        self.split_time_input.setEnabled(state)
        
        if state:
            self.decay_fraction1_checkbox.setChecked(state)
            self.decay_fraction2_checkbox.setChecked(state)
            self.decay_fraction1.setValue(1)
            self.decay_fraction2.setValue(1)

        self.decay_fraction1_checkbox.setEnabled(not state)
        self.decay_fraction2_checkbox.setEnabled(not state)
        
        self.decay_fraction1.setEnabled(not state)
        self.decay_fraction2.setEnabled(not state)
        
                
    def toggle_split_time(self, _=None):
        label = labels.ENABLE_SPLIT_FRACTIONS
        #self.validate_fraction1()
        self.emit_change(label)
        self.enable_split_time()
            
    def toggle_fraction1(self, _=None):
        label = labels.APPLY_FRACTION1
        #self.validate_fraction1()
        self.emit_change(label)
        self.enable_fraction1()
        
    def toggle_fraction2(self, _=None):        
        label = labels.APPLY_FRACTION2
        #self.validate_fraction2()
        self.emit_change(label)
        self.enable_fraction2()
 
        
class EditSourcesNMView(EditListViewPositionBase):
    LABEL = labels.SOURCES_NM
    explanation = ("To add a new source select Source NM from the toolbar and "
                   "click on the floorplan to add a source at that position."
                   "\n\n"
                   "When setting self shielding to 'Body', pyshield will "
                   "assume 10 cm of water as additional shielding (buildup "
                   "and attenuation). Radtracer will use a pre-simulated "
                   "spectrum after additional 10 cm of "
                   "shielding with water. Note that large differences in results "
                   "may occur between pyshield and radtracer when setting self "
                   "shielding to 'Body.'\n\n"
                   "Note that setting the self shielding to 'Body' may increase "
                   "the dose rates for pyshield for some isotopes. This is due "
                   "to the buildup in 10 cm of water. Using a user defined fixed "
                   "factor could provide a better results for pyshield.")
                   
    
    def from_dict(self, dct):
        super().from_dict(dct)
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        for label, value in dct.items():
            if label == labels.DURATION:
                safe_set_value_to_widget(self.duration, value)
            elif label == labels.ACTIVITY:
                safe_set_value_to_widget(self.activity, value)
            elif label == labels.ISOTOPE:
                safe_set_value_to_widget(self.isotope_input, value)
                halflife = CONSTANTS.get_isotope_by_name(value).half_life
                safe_set_value_to_widget(self.isotope_half_life_value, halflife)
            elif label == labels.SELF_SHIELDING:
                if isinstance(value, str):
                    safe_set_value_to_widget(self.self_shielding_list, value)
                else:
                    safe_set_value_to_widget(self.self_shielding_list, labels.SELF_SHIELDING_FACTOR)
                    safe_set_value_to_widget(self.self_shielding_factor_input, value)                
            elif label == labels.NUMBER_OF_EXAMS:
                safe_set_value_to_widget(self.number_of_exams_input, value)
            elif label == labels.APPLY_DECAY_CORRECTION:
                safe_set_value_to_widget(self.decay_correction, value)
                self.toggle_halflife_visible()
            elif label == labels.CLEARANCE:
                safe_set_value_to_widget(self.clearance_list, value)
                
    def toggle_halflife_visible(self):
        visible = self.decay_correction.isChecked()
        self.isotope_half_life_label.setEnabled(visible)
        self.isotope_half_life_value.setEnabled(visible)
        
    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        
        
        if self.self_shielding_list.currentText() != labels.SELF_SHIELDING_FACTOR:
            enabled = False
        
        if enabled:
            self.toggle_halflife_visible()
       
        
        self.logger.debug(f'Setting Visble to {enabled}')
        
        
        self.set_enabled_self_shielding(enabled)
        
         
        
    def set_enabled_self_shielding(self, enabled):
        self.self_shielding_factor_input.setEnabled(enabled)
        self.self_shielding_factor_input.setVisible(enabled)
        self.self_shielding_factor_label.setEnabled(enabled)
        self.self_shielding_factor_label.setVisible(enabled)
       
                
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.DURATION] = self.duration.value()
        dct[labels.ACTIVITY] =  self.activity.value()
        dct[labels.ISOTOPE] = self.isotope_input.currentText()
        
        value = self.self_shielding_list.currentText()
        if value == labels.SELF_SHIELDING_FACTOR:
            dct[labels.SELF_SHIELDING] = self.self_shielding_factor_input.value()
        else:
            dct[labels.SELF_SHIELDING] = value
            
        dct[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input.value()
        dct[labels.APPLY_DECAY_CORRECTION] = self.decay_correction.isChecked()
        dct[labels.CLEARANCE] = self.clearance_list.currentText()
    
        return dct

    
    def create_widgets(self):
        super().create_widgets()
    
        self.duration = QDoubleSpinBoxInfinite()
        self.duration.setRange(0, MAX_VALUE)
        self.duration_label = QLabel(labels.DURATION)
        
        
       
        self.activity = QDoubleSpinBox(decimals=2)
        self.activity.setRange(0, MAX_VALUE)
        self.activity_label = QLabel(labels.ACTIVITY)
        
        self.isotope_input = QComboBox()
        self.isotope_input.addItems(CONSTANTS.get_isotope_name_list())
        
        self.isotope_label = QLabel(labels.ISOTOPE)
        
        self.self_shielding_list = QComboBox()
        self.self_shielding_list.addItems(CONSTANTS.self_shielding_options)
        self.self_shielding_label = QLabel(labels.SELF_SHIELDING)
        self.self_shielding_factor_label = QLabel(labels.SELF_SHIELDING_FACTOR)
        self.self_shielding_factor_input = QDoubleSpinBox()
        self.self_shielding_factor_input.setSingleStep(0.01)
        self.self_shielding_factor_input.setRange(0, MAX_VALUE)
        self.self_shielding_factor_input.setDecimals(2)
        self.self_shielding_factor_input.setValue(1.0)
        
        
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        

        self.decay_correction = QCheckBox(labels.APPLY_DECAY_CORRECTION)
        
        self.isotope_half_life_label = QLabel(labels.HALF_LIFE)
        self.isotope_half_life_value = QLabel("0")
        
        self.clearance_label = QLabel('Clearance Model')
        self.clearance_list = QComboBox()
        

     
    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.DURATION
        callback = lambda _, label=label: self.emit_change(label)
        self.duration.valueChanged.connect(callback)
        
        label = labels.ACTIVITY
        callback = lambda _, label=label: self.emit_change(label)
        self.activity.valueChanged.connect(callback)
        
        label = labels.ISOTOPE
        callback = lambda _, label=label: self.emit_change(label)
        self.isotope_input.currentTextChanged.connect(callback)
        
        label = labels.SELF_SHIELDING
        callback = lambda _, label=label: self.change_self_shielding(label)
        self.self_shielding_list.currentTextChanged.connect(callback)
        callback = lambda _, label=label: self.emit_change(label)
        self.self_shielding_factor_input.valueChanged.connect(callback)
        
        
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.emit_change(label)
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.APPLY_DECAY_CORRECTION
        callback = lambda _, label=label: self.emit_change(label)        
        self.decay_correction.stateChanged.connect(callback)
        
        label = labels.CLEARANCE
        callback = lambda _, label=label: self.emit_change(label)        
        self.clearance_list.currentIndexChanged.connect(callback)
    
    def change_self_shielding(self, label):
        if self.self_shielding_list.currentText() == labels.SELF_SHIELDING_FACTOR:
            enabled = True
        else:
            enabled = False
            
        self.set_enabled_self_shielding(enabled)
        
        super().emit_change(label)
              
    def clear(self):
        super().clear()
        self.activity.clear()
        self.number_of_exams_input.clear()
        self.decay_correction.setChecked(False)
        self.isotope_half_life_value.clear()
        self.duration.clear()
        
        

    def create_layout_body(self):
        

        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.activity_label, row, 0)
        self.layout.addWidget(self.activity, row, 1)
        row += 1
        self.layout.addWidget(self.isotope_label, row, 0)
        self.layout.addWidget(self.isotope_input, row, 1)
        row += 1
        self.layout.addWidget(self.self_shielding_label, row, 0)
        self.layout.addWidget(self.self_shielding_list, row, 1)
        row += 1
        self.layout.addWidget(self.self_shielding_factor_label, row, 0)
        self.layout.addWidget(self.self_shielding_factor_input, row, 1)
        row += 1
        self.layout.addWidget(self.duration_label, row, 0)
        self.layout.addWidget(self.duration, row, 1)
        row += 1
        self.layout.addWidget(self.decay_correction, row, 0, 1, 2)
        row += 1
        self.layout.addWidget(self.isotope_half_life_label, row, 0)
        self.layout.addWidget(self.isotope_half_life_value, row, 1)
        row += 1
        self.layout.addWidget(self.clearance_label, row, 0, 1, 2)
        row += 1
        self.layout.addWidget(self.clearance_list, row, 0, 1, 2)
       
        
       
        super().create_layout_body()


class EditCriticalPointsView(EditListViewPositionBase):
    LABEL = labels.CRITICAL_POINTS
    explanation = ("To add a new critcal point select Critical Point from "
                   "the toolbar and click on the floorplan to add a "
                   "critical point at that position.")
              
    
    def from_dict(self, dct):
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        super().from_dict(dct)
        for label, value in dct.items():
            if label == labels.OCCUPANCY_FACTOR:
                safe_set_value_to_widget(self.occupancy_factor_input, value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.OCCUPANCY_FACTOR] = self.occupancy_factor_input.value()
        return dct

    def create_widgets(self):
        super().create_widgets()
    
        self.occupancy_factor_label = QLabel("Occupancy Factor:")
        self.occupancy_factor_input = QDoubleSpinBox()
        self.occupancy_factor_input.setSingleStep(0.05)
        self.occupancy_factor_input.setRange(0, 1)
        self.occupancy_factor_input.setValue(1)
        self.clear()

    def set_callbacks(self):
        super().set_callbacks()
        label = labels.OCCUPANCY_FACTOR
        callback = lambda _, label=label: self.emit_change(label)
    
        self.occupancy_factor_input.valueChanged.connect(callback)
        
        
        
    def clear(self):
        super().clear()
        self.name_input.clear()
        self.occupancy_factor_input.clear()
        
    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1

        self.layout.addWidget(self.occupancy_factor_label, row, 0)
        self.layout.addWidget(self.occupancy_factor_input, row, 1)
        super().create_layout_body() 

        
class EditSourceXrayView(EditListViewPositionBase):
    LABEL = labels.SOURCES_XRAY
    explanation = ("To add a new source select Source Xray from the toolbar and "
                   "click on the floorplan to add a source at that position.")
                   
    def from_dict(self, dct):
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        super().from_dict(dct)
        
        for label, value in dct.items():
            if label == labels.DAP:
                safe_set_value_to_widget(self.dap, value)
            elif label == labels.KVP:
                safe_set_value_to_widget(self.kvp, str(value))
            elif label == labels.NUMBER_OF_EXAMS:
                safe_set_value_to_widget(self.number_of_exams_input, value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.DAP] = self.dap.value()
        dct[labels.KVP] = safe_to_int(self.kvp.currentText())
        dct[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input.value()
        return dct
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.xray]
    
    def create_widgets(self):
        super().create_widgets()
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)
        
        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.dap = QDoubleSpinBox()
        self.dap.setRange(0, MAX_VALUE)
        self.dap_label = QLabel(labels.DAP)
        
    def set_callbacks(self):
        super().set_callbacks()
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.emit_change(label)        
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.KVP
        callback = lambda _, label=label: self.emit_change(label)        
        self.kvp.currentTextChanged.connect(callback)
        
        label = labels.DAP
        callback = lambda _, label=label: self.emit_change(label)        
        self.dap.valueChanged.connect(callback)

    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.dap_label, row, 0)
        self.layout.addWidget(self.dap, row, 1)
        super().create_layout_body() 

    def clear(self):
        super().clear()

        self.number_of_exams_input.clear()
        self.kvp.setCurrentIndex(0)
        self.dap.clear()

class EditSourceCTView(EditListViewPositionBase):
    LABEL = labels.SOURCES_CT
    explanation = ("To add a new source select Source CT from the toolbar and "
                   "click on the floorplan to add a source at that position.")
    def from_dict(self, dct):
        super().from_dict(dct)
        #self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        for label, value in dct.items():
           if label == labels.DLP:
               safe_set_value_to_widget(self.dlp, value)
           elif label == labels.KVP:
               safe_set_value_to_widget(self.kvp, str(value))
           elif label == labels.NUMBER_OF_EXAMS:
               safe_set_value_to_widget(self.number_of_exams_input, value)
           elif label == labels.CT_BODY_PART:
               safe_set_value_to_widget(self.body_part, value)
        #self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
        return dct
        
        
    
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.NUMBER_OF_EXAMS] = safe_to_int(self.number_of_exams_input.value())
        dct[labels.KVP] = safe_to_int(self.kvp.currentText())
        dct[labels.CT_BODY_PART] = self.body_part.currentText()
        dct[labels.DLP] = safe_to_float(self.dlp.value())
        return dct        
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.ct]
    
    def create_widgets(self):
        super().create_widgets()
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)

        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.body_part = QComboBox()
        self.body_part.addItems(CONSTANTS.CT_body_part_options ) 
        self.body_part_label = QLabel(labels.CT_BODY_PART)

        self.dlp = QDoubleSpinBox()
        self.dlp.setRange(0, MAX_VALUE)
        self.dlp_label = QLabel(labels.DLP)

        
    def set_callbacks(self):
        super().set_callbacks()
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.emit_change(label)                
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.KVP
        callback = lambda _, label=label: self.emit_change(label)        
        self.kvp.currentTextChanged.connect(callback)
 
        
        label = labels.DLP
        callback = lambda _, label=label: self.emit_change(label)        
        self.dlp.valueChanged.connect(callback)
                
        label = labels.CT_BODY_PART
        callback = lambda _, label=label: self.emit_change(label)        
        self.dlp.valueChanged.connect(callback)
        self.body_part.currentTextChanged.connect(callback)
        
    def create_layout_body(self):
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.body_part_label, row, 0)
        self.layout.addWidget(self.body_part, row, 1)
        row += 1
        self.layout.addWidget(self.dlp_label, row, 0)
        self.layout.addWidget(self.dlp, row, 1)
        
        super().create_layout_body()

    def clear(self):
        super().clear()
        self.number_of_exams_input.clear()
        self.kvp.setCurrentIndex(0)
        self.body_part.setCurrentIndex(0)
        self.dlp.clear()

 
class EditPixelSizeView(EditViewBase):
    LABEL = labels.PIXEL_SIZE_CM
    EVENT_GEOMETRY_RADIO_BUTTON = 'event_geometry_radio_button'
    explanation =\
("The pixel size can be set by hand or by a measurement on the floor plan " 
 "image. Measurement is done by drawing a line between two points for which "
 "the real world distance in cm is known.")


    def create_widgets(self):
        #self.explanation = QLabel(self.explanation.replace('\n', ' '))
        
        
        self.choose_fixed = QRadioButton("Set Fixed")
        
        self.choose_measured = QRadioButton("Measure")

        
        self.measure_button = QPushButton('Measure On Floorplan')
        
        self.physical_distance_label = QLabel("Real world distance [cm]")
        self.physical_distance = QDoubleSpinBox(decimals=2)
        self.physical_distance.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.pixel_distance_label = QLabel("Distance [pixels]")
        self.pixel_distance = QLabel("Use Button To Measure")
        
        self.pixel_size_label = QLabel(labels.PIXEL_SIZE_CM)
        self.pixel_size = QDoubleSpinBox(decimals=2)
        self.pixel_size.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.confirm_button = QPushButton("Confirm")
        
        self.choose_fixed.toggled.connect(self.radio_button)
        self.choose_measured.toggled.connect(self.radio_button)
        
        
        self.pixel_size_measured_label = QLabel(labels.PIXEL_SIZE_CM)
        self.pixel_size_measured = QLabel()
        self.set_callbacks()
        
    def set_callbacks(self):        
        label = labels.REAL_WORLD_DISTANCE_CM
        callback = lambda _, label=label: self.emit_change(label)        
        self.physical_distance.valueChanged.connect(callback)
        
       

    def radio_button(self):
        
        if self.choose_measured.isChecked():
            self.set_choose_measured()
        elif self.choose_fixed.isChecked():
            self.set_choose_fixed()
        
        event_data = {labels.LOCKED: self.choose_fixed.isChecked()}
        self.emit(self.EVENT_GEOMETRY_RADIO_BUTTON, event_data)
        
            
            
    def set_choose_fixed(self):
        self.choose_measured.setChecked(False)
        self.choose_fixed.setChecked(True)
        self.measure_button.setEnabled(False)
        self.physical_distance.setEnabled(False)
        self.pixel_size_label.setEnabled(True)
        self.pixel_size.setEnabled(True)
        self.pixel_size_measured.setText('')
        self.pixel_size_measured.setEnabled(False)
        
        
    def set_choose_measured(self):
        self.choose_measured.setChecked(True)
        self.choose_fixed.setChecked(False)
        self.measure_button.setEnabled(True)
        self.physical_distance.setEnabled(True)
        self.pixel_size.setEnabled(False)
        self.pixel_size_measured.setEnabled(True)
        self.pixel_size.setEnabled(False)
        
    def create_layout(self):
        
        row = self.layout.rowCount() + 1
        
        #self.layout.addWidget(self.explanation, row, 0, 1, 2)
        
        #row += 1
        
        self.layout.addWidget(self.choose_fixed, row, 0, 1, 2)

        row += 1
        
        self.layout.addWidget(self.pixel_size_label, row, 0)
        self.layout.addWidget(self.pixel_size, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.choose_measured, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.physical_distance_label, row, 0)
        self.layout.addWidget(self.physical_distance, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.pixel_distance_label, row, 0)
        self.layout.addWidget(self.pixel_distance, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.pixel_size_measured_label, row, 0)
        self.layout.addWidget(self.pixel_size_measured, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.measure_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.confirm_button, row, 0, 1, 2)

        
        self.set_choose_measured()
       
        
