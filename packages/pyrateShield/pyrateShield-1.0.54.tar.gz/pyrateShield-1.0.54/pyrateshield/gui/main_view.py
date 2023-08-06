
from pyrateshield import labels, __version__
from pyrateshield.gui.io import confirm_changes
from pyrateshield.gui.item_views import (EditPixelSizeView, 
                                         EditShieldingView, 
                                         EditCriticalPointsView,  
                                         EditSourcesNMView,
                                         EditWallsView,
                                         EditSourceCTView, 
                                         EditSourceXrayView,
                                         EditMaterialsView,
                                         EditClearanceView)
                                         
                                      
                                      


from PyQt5.QtWidgets import (QWidget, QLabel, QToolBox, QTabWidget, QMainWindow, 
                             QSplitter, QApplication, QPushButton, QTableView,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox)

from pyrateshield.gui.mpl_view import NavigationToolbar, MplCanvas



TOOLBOX_LAYOUT = {'Nuclear Medicine Sources':       [labels.SOURCES_NM, 
                                                     labels.CLEARANCE],
                  'Radiology Sources':              [labels.SOURCES_CT,
                                                     labels.SOURCES_XRAY],
                                    
                  'Walls, Shieldings && Materials':   [labels.WALLS,
                                                      labels.SHIELDINGS,
                                                      labels.MATERIALS],
                  labels.CRITICAL_POINTS:           [labels.CRITICAL_POINTS],
                  labels.PIXEL_SIZE_CM:             [labels.PIXEL_SIZE_CM]}                                                
                                              
                

RESULT_LAYOUT = [labels.CANVAS, labels.CRITICAL_POINT_REPORT_VIEW]

        
class ResultDosemapView(QWidget):
    dosemap_button_pyshield_label   = "View Dose Map PyShield"
    dosemap_button_radtracer_label   = "View Dose Map RadTracer"
    
    
    refresh_button_label    = "Refresh"
    _buttons = None
    
    @property
    def ncolumns(self):
        return len(self.buttons)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):

        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)        
        self._labels = [
            self.dosemap_button_pyshield_label,
            self.dosemap_button_radtracer_label,
            self.refresh_button_label
        ]        
        self.buttons = {label: QPushButton(label) for label in self._labels}

    def create_layout(self):
        btn_layout = QHBoxLayout()
        for label in self._labels:
            btn_layout.addWidget(self.buttons[label])        
        
        #btn_layout.addWidget(self.toolbar)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addLayout(btn_layout)

        
        
class ResultCriticalPointView(QWidget):
    check_button_label = 'Show contribution of each individual source'
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.critical_point_button        = QPushButton("Calculate Critical Points")
        self.save_critcial_point_button   = QPushButton("Save To Excel")
        
        self.table_view             = QTableView()
        self.table_view.verticalHeader().setVisible(False)
        self.source_checkbox = QCheckBox(self.check_button_label)

        #self.table_view.setRowCount(100)
        #self.table_view.setColumnCount(5)
        
    def create_layout(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(self.table_view)
    
        
        blayout = QGridLayout()
        blayout.addWidget(self.critical_point_button, 0, 0)
        blayout.addWidget(self.save_critcial_point_button, 0, 1)
        
        vlayout.addLayout(blayout)
        vlayout.addWidget(self.source_checkbox)
        
        self.setLayout(vlayout)
        
        # auto resize columns
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(header.ResizeToContents)
        
        
    
        
class MainView(QMainWindow):
    _views = None
    def __init__(self, mouse=None):
        super(MainView, self).__init__()
        self.views = self.create_widgets()
        self.create_layout()
        self.status_label = self.create_status_label()
        self.show()
        self.set_focus(labels.SOURCES_NM)
        
        
        
        
        self.setWindowTitle('PyrateShield (version ' + __version__ + ")")
    
    def closeEvent(self, event):
        if confirm_changes('Quit Application?'):
            super().closeEvent(event)
        else:
            event.ignore()
    
    
    def get_active_tool_panel_name(self):
        tool_index = self.toolbox.currentIndex()
        tool_name = self.toolbox.itemText(tool_index)
        if len(TOOLBOX_LAYOUT[tool_name]) > 1:
            tab_index = self.toolbox_tabs[tool_name].currentIndex()
        else:
            tab_index = 0
            
        tab_name = TOOLBOX_LAYOUT[tool_name][tab_index]
        
        return tab_name
    
    
    def set_focus(self, item_label):
        def location_in_toolbox(label):
            for name, items in TOOLBOX_LAYOUT.items():
                if label in items:
                    return name
            return None
            
        
        if item_label in RESULT_LAYOUT:
            self.result_container.setCurrentWidget(self.views[item_label])
        
        toolgroup = location_in_toolbox(item_label)
        
        if toolgroup is None:
            raise ValueError(f'No view item with label {item_label}')
            
        else:
            toolbox_tab = self.toolbox_tabs[toolgroup]
            self.toolbox.setCurrentWidget(toolbox_tab)
            if len(TOOLBOX_LAYOUT[toolgroup]) > 1:
                toolbox_tab.setCurrentWidget(self.views[item_label])
            
    def set_tab_enabled(self, label, enabled):
        for toolbox_tab_name, tabs in TOOLBOX_LAYOUT.items():
            if label in tabs:
                index = tabs.index(label)
                tab_widget = self.toolbox_tabs[toolbox_tab_name]
                tab_widget.setTabEnabled(index, enabled)
                
            
    @property
    def status_text(self):
        return self.status_label.text()
    
    def set_status_text(self, text):
        self.status_text = text
    
    @status_text.setter
    def status_text(self, text):
        self.status_label.setText(str(text))
        
        
    
    def create_widgets(self):
        if self._views is None:
            views = {labels.SOURCES_NM:             EditSourcesNMView(),
                     labels.CLEARANCE:              EditClearanceView(),
                     labels.SOURCES_CT:             EditSourceCTView(),
                     labels.SOURCES_XRAY:           EditSourceXrayView(),
                     # labels.FLOORPLAN:              EditFloorplanView(),
                     labels.PIXEL_SIZE_CM:          EditPixelSizeView(),
                   
                     labels.CRITICAL_POINTS:        EditCriticalPointsView(),
                     labels.WALLS:                  EditWallsView(),
                     labels.SHIELDINGS:             EditShieldingView(),
                     labels.MATERIALS:              EditMaterialsView(),
                     
                     labels.CANVAS:                 ResultDosemapView(),
                     labels.CRITICAL_POINT_REPORT_VIEW:  ResultCriticalPointView()}
            self._views = views
                 
        
        
        return self._views
                 
                  
                 
        
    def create_status_label(self):
        status_label = QLabel()
        
        statusbar = self.statusBar()
        statusbar.addWidget(status_label)
        statusbar.setVisible(True)
        return status_label
        

        

    def put_views_in_tabs(self, layout):
        tab_widget = QTabWidget()
        for item in layout:
            tab_widget.addTab(self.views[item], item)
        return tab_widget
        
    def put_views_in_toolbox(self, layout):
        toolbox = QToolBox()
        tabs = {}
        for group_name, items in layout.items():
            if len(items) > 1:
                tabs[group_name] = self.put_views_in_tabs(items)
            else:
                tabs[group_name] = self.views[items[0]]
            toolbox.addItem(tabs[group_name], group_name)
        
        return toolbox, tabs
       
    
    def create_layout(self):
        toolbox, toolbox_tabs = self.put_views_in_toolbox(TOOLBOX_LAYOUT)
        self.toolbox = toolbox
        self.toolbox_tabs = toolbox_tabs
        
        self.result_container = self.put_views_in_tabs(RESULT_LAYOUT)
        
        self.main_container = QSplitter()
        
        # self.toolbox.setMinimumWidth(WIDGET_WIDTH+10)
        #self.toolbox.setMaximumWidth(WIDGET_WIDTH+20)
        
        
        self.main_container.addWidget(self.toolbox)
       
        self.main_container.addWidget(self.result_container)
        
        

        self.setCentralWidget(self.main_container)
        
        self.setContentsMargins(10, 10, 10, 10)
        
        self.main_container.setSizes([100, 500])

    
        
if __name__ == "__main__":
    def main():
        app = QApplication([])
        window = MainView()
        window.show()    
        app.exec_()
        return window
    
    
    window = main()

        
