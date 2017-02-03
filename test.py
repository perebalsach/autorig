from PySide import QtCore, QtGui


class TabDialog(QtGui.QDialog):
    def __init__(self, fileName, parent=None):
        super(TabDialog, self).__init__(parent)

        fileInfo = QtCore.QFileInfo(fileName)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(ProxyTab(fileInfo), "Bipded Proxy Skeleton")
        tabWidget.addTab(LinksTab(fileInfo), "Proxy Links")
        tabWidget.addTab(RigTab(fileInfo), "Rig Me")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)

        self.setLayout(mainLayout)

        self.setWindowTitle("HERO Autorig")


class ProxyTab(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(ProxyTab, self).__init__(parent)

        armGroup = QtGui.QGroupBox("Arms: ")
        legsGroup = QtGui.QGroupBox("Legs: ")
        spineGroup = QtGui.QGroupBox("Spine: ")

        groupLabel = QtGui.QLabel("Group")
        groupValueLabel = QtGui.QLabel(fileInfo.group())
        groupValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)

        # Arms Section
        arm_lbl_system = QtGui.QLabel('Select System:')
        arm_rad_ik = QtGui.QRadioButton('IK')
        arm_rad_fk = QtGui.QRadioButton('FK')
        arm_rad_fk_ik = QtGui.QRadioButton('FK / IK')
        arm_btn_proxy_arm = QtGui.QPushButton('Create Proxy Arm')
        arm_icon = QtGui.QPixmap('images/arm.png')
        arm_btn_proxy_arm.setIcon(QtGui.QIcon(arm_icon))

        arm_rad_fk_ik.setChecked(1)

        # Legs Section
        leg_lbl_system = QtGui.QLabel('Select System:')
        leg_rad_ik = QtGui.QRadioButton('IK')
        leg_rad_fk = QtGui.QRadioButton('FK')
        leg_rad_fk_ik = QtGui.QRadioButton('FK / IK')
        leg_btn_proxy_arm = QtGui.QPushButton('Create Proxy Leg')
        leg_rad_fk_ik.setChecked(1)

        # Spine Section
        spine_lbl_system = QtGui.QLabel('Select System:')
        spine_lbl_num_joints = QtGui.QLabel('Number of sections:')
        spine_rad_ik = QtGui.QRadioButton('IK')
        spine_rad_fk = QtGui.QRadioButton('FK')
        spine_rad_fk_ik = QtGui.QRadioButton('FK / IK')
        spine_btn_proxy_arm = QtGui.QPushButton('Create Proxy Spine')
        spine_spin_box = QtGui.QSpinBox()
        spine_rad_fk_ik.setChecked(1)

        # Layouts
        armGroupLayout = QtGui.QHBoxLayout()
        armGroupLayout.addWidget(arm_lbl_system)
        armGroupLayout.addWidget(arm_rad_fk)
        armGroupLayout.addWidget(arm_rad_ik)
        armGroupLayout.addWidget(arm_rad_fk_ik)
        armGroupLayout.addWidget(arm_btn_proxy_arm)
        armGroup.setLayout(armGroupLayout)

        legsGroupLayout = QtGui.QHBoxLayout()
        legsGroupLayout .addWidget(leg_lbl_system)
        legsGroupLayout .addWidget(leg_rad_fk)
        legsGroupLayout .addWidget(leg_rad_ik)
        legsGroupLayout .addWidget(leg_rad_fk_ik)
        legsGroupLayout .addWidget(leg_btn_proxy_arm)
        legsGroup.setLayout(legsGroupLayout)

        spineGroupLayout = QtGui.QHBoxLayout()
        spineGroupLayout.addWidget(spine_lbl_system)
        spineGroupLayout.addWidget(spine_rad_fk)
        spineGroupLayout.addWidget(spine_rad_ik)
        spineGroupLayout.addWidget(spine_rad_fk_ik)
        spineGroupLayout.addWidget(spine_lbl_num_joints)
        spineGroupLayout.addWidget(spine_spin_box)
        spineGroupLayout.addWidget(spine_btn_proxy_arm)

        spineGroup.setLayout(spineGroupLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(armGroup)
        mainLayout.addWidget(legsGroup)
        mainLayout.addWidget(spineGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


class LinksTab(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(LinksTab, self).__init__(parent)

        permissionsGroup = QtGui.QGroupBox("Permissions")

        readable = QtGui.QCheckBox("Readable")
        if fileInfo.isReadable():
            readable.setChecked(True)

        writable = QtGui.QCheckBox("Writable")
        if fileInfo.isWritable():
            writable.setChecked(True)

        executable = QtGui.QCheckBox("Executable")
        if fileInfo.isExecutable():
            executable.setChecked(True)

        ownerGroup = QtGui.QGroupBox("Ownership")

        ownerLabel = QtGui.QLabel("Owner")
        ownerValueLabel = QtGui.QLabel(fileInfo.owner())
        ownerValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)

        groupLabel = QtGui.QLabel("Group")
        groupValueLabel = QtGui.QLabel(fileInfo.group())
        groupValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)

        permissionsLayout = QtGui.QVBoxLayout()
        permissionsLayout.addWidget(readable)
        permissionsLayout.addWidget(writable)
        permissionsLayout.addWidget(executable)
        permissionsGroup.setLayout(permissionsLayout)

        ownerLayout = QtGui.QVBoxLayout()
        ownerLayout.addWidget(ownerLabel)
        ownerLayout.addWidget(ownerValueLabel)
        ownerLayout.addWidget(groupLabel)
        ownerLayout.addWidget(groupValueLabel)
        ownerGroup.setLayout(ownerLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(permissionsGroup)
        mainLayout.addWidget(ownerGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

        self.listViewEnemies = QtGui.QListWidget()
        self.listViewEnemies.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

class RigTab(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(RigTab, self).__init__(parent)

        topLabel = QtGui.QLabel("Open with:")

        applicationsListBox = QtGui.QListWidget()
        applications = []

        for i in range(1, 31):
            applications.append("Application %d" % i)

        applicationsListBox.insertItems(0, applications)

        alwaysCheckBox = QtGui.QCheckBox()

        if fileInfo.suffix():
            alwaysCheckBox = QtGui.QCheckBox("Always use this application to "
                    "open files with the extension '%s'" % fileInfo.suffix())
        else:
            alwaysCheckBox = QtGui.QCheckBox("Always use this application to "
                    "open this type of file")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(applicationsListBox)
        layout.addWidget(alwaysCheckBox)
        self.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."

    tabdialog = TabDialog(fileName)
    sys.exit(tabdialog.exec_())
