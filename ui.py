import traceback

from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

import sys
import os

def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class AutorigUI(QtGui.QDialog):

    test_signal = QtCore.Signal()

    def __init__(self, parent=maya_main_window()):
        super(AutorigUI, self).__init__(parent)


    def create(self):
        '''
        Set up the UI prior to display
        '''
        self.setWindowTitle("Autorig")
        self.setWindowFlags(QtCore.Qt.Tool)

        self.create_controls()
        self.create_layout()
        self.create_connections()
        self._load_events()

    def create_controls(self):
        '''
        Create the widgets for the dialog
        '''
        self.lbl_img = QtGui.QLabel()
        pixmap = 'Z:\\_maya\\scripts\\animationEventsExport\\images\\logo.png'
        self.lbl_img.setPixmap(pixmap)

        self.lbl_output = QtGui.QLabel('Select Output Folder: ')

        self.line_edit_path = QtGui.QLineEdit('.. Hero repo ..')

        self.output_btn = QtGui.QPushButton('...')

        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(("Event Name;Start Frame;End Frame").split(";"))

        self.add_anim_btn = QtGui.QPushButton('Add Animation Event')
        self.remove_event_btn = QtGui.QPushButton('Remove Animation Event')
        self.save_events_btn = QtGui.QPushButton('Save Events')
        self.clear_events_btn = QtGui.QPushButton('Clear All Events')

        self.separator01 = QtGui.QFrame()
        self.separator01.setFrameShape(QtGui.QFrame.HLine)

        self.separator02 = QtGui.QFrame()
        self.separator02.setFrameShape(QtGui.QFrame.HLine)

        self.export_with_anmes_btn = QtGui.QPushButton('Export With Custom Names')
        self.export_all_btn = QtGui.QPushButton('Export All Events')



    def create_layout(self):
        '''
        Create the layouts and add widgets
        '''

        check_box_layout = QtGui.QHBoxLayout()
        check_box_layout.setContentsMargins(2, 2, 2, 2)
        check_box_layout.addWidget(self.lbl_output)
        check_box_layout.addWidget(self.line_edit_path)
        check_box_layout.addWidget(self.output_btn)

        grid_layout = QtGui.QGridLayout()
        grid_layout.setContentsMargins(2, 2, 2, 2)

        grid_layout.addWidget(self.add_anim_btn, 0, 0)
        grid_layout.addWidget(self.remove_event_btn, 0, 1)
        grid_layout.addWidget(self.save_events_btn, 1, 0)
        grid_layout.addWidget(self.clear_events_btn, 1, 1)


        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.addWidget(self.lbl_img)

        main_layout.addLayout(check_box_layout)
        main_layout.addWidget(self.separator02)
        main_layout.addWidget(self.table)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.separator01)
        main_layout.addWidget(self.export_with_anmes_btn)
        main_layout.addWidget(self.export_all_btn)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_connections(self):
        '''
        Create the signal/slot connections
        '''

        self.output_btn.clicked.connect(self.sel_output_folder)

        self.add_anim_btn.clicked.connect(self.add_item)
        self.remove_event_btn.clicked.connect(self.rem_row)
        self.save_events_btn.clicked.connect(self.save_events)
        self.clear_events_btn.clicked.connect(self.remove_items)
        self.export_all_btn.clicked.connect(self.export)

if __name__ == "__main__":

    # Development workaround for PySide winEvent error (in Maya 2014)
    # Make sure the UI is deleted before recreating
    try:
        autorig_ui.deleteLater()
    except:
        pass

    # Create minimal UI object
    autorig_ui = AutorigUI()

    # Delete the UI if errors occur to avoid causing winEvent
    # and event errors (in Maya 2014)
    try:
        autorig_ui.create()
        autorig_ui.show()
    except:
        autorig_ui.deleteLater()
        traceback.print_exc()