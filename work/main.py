from mainwindow import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox
from PyQt5.QtGui import *
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from loginForm import Ui_Form
from google_predict import google
from lib.share import qtWindows
from sql.BuildDatabase import buildDatabase,loginCheck,give_advice,getTable,advice_by_id#引入数据库操作
from history import Ui_HisWindow
import sqlite3

class HistoryShow(QMainWindow, Ui_HisWindow):
    def __init__(self, parent=None):
        self.patient_id = 0
        self.fname = ""
        super(HistoryShow, self).__init__(parent)
        self.setupUi(self)
        self.back.mouseReleaseEvent = self.look_back
        self.search.mouseReleaseEvent = self.searchContent

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('menu')
        action = QAction('logout', self)
        file_menu.addAction(action)

        action.triggered.connect(self.exit_triggered)


        self.head.setCursor(QCursor(Qt.PointingHandCursor))#悬浮小手
        self.back.setCursor(QCursor(Qt.PointingHandCursor))#悬浮小手
        self.give_advice.setCursor(QCursor(Qt.PointingHandCursor))
        self.search.setCursor(QCursor(Qt.PointingHandCursor))

        self.showTable()
        self.table1.itemSelectionChanged.connect(
            self.handleSelectionChange
        )

        self.table1.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.table1.customContextMenuRequested.connect(self.table_menu)  # 右键菜单
        self.give_advice.clicked.connect(self.updateAdvice)

    def searchContent(self,event):
        content = self.search_content.text()
        if content == "":#如果没东西
            self.showTable()
            return
        connect = sqlite3.connect('project.db')
        cur = connect.cursor()
        cur.execute('''
            SELECT * from advice_table WHERE patient_name LIKE ? ORDER BY patient_id DESC;
            ''', ('%' + content + '%',))

        allItems = cur.fetchall()

        connect.commit()  # 提交
        connect.close()

        if len(allItems) == 0:
            QMessageBox.warning(
                self,
                "Error", "Not found"
            )
        else:#找到了
            table = self.table1
            table.clearContents()
            table.setRowCount(0)
            i = 0
            print(allItems)
            for item in allItems:
                table.insertRow(i)  # 尾部插入一行
                table.setItem(i, 0, QTableWidgetItem(str(item[0])))  # 设置该行元素
                table.setItem(i, 1, QTableWidgetItem(item[1]))
                table.setItem(i, 2, QTableWidgetItem(item[2]))
                table.setItem(i, 3, QTableWidgetItem(item[5]))
                table.item(i, 0).setFlags(Qt.ItemIsEnabled)
                i += 1
            table.update()
        self.search_content.setText("")


    def updateAdvice(self):
        advice = self.advice.toPlainText()
        connect = sqlite3.connect('project.db')
        cur = connect.cursor()
        cur.execute('''
            UPDATE advice_table SET advice=? where patient_id=?
              ''', (advice,self.patient_id))

        connect.commit()  # 提交
        connect.close()

    def table_menu(self, pos):
        menu = QMenu()  # 实例化菜单
        item = menu.addAction(u"Delete")
        action = menu.exec_(self.table1.mapToGlobal(pos))
        if action == item:#点击了
            choice = QMessageBox.question(
                self,
                '确认',
                '确定要删除该记录吗？')

            if choice == QMessageBox.Yes:
                row = self.table1.selectedItems()[0].row()  # 获取右键选中的行
                self.table1.removeRow(row)
            if choice == QMessageBox.No:
                return




    def showTable(self):
        table = self.table1
        items = getTable()
        table.clearContents()

        table.setRowCount(0)
        i = 0
        for item in items:
            table.insertRow(i)  # 尾部插入一行
            table.setItem(i, 0, QTableWidgetItem(str(item[0])))  # 设置该行元素
            table.setItem(i, 1, QTableWidgetItem(item[1]))
            table.setItem(i, 2, QTableWidgetItem(item[2]))
            table.setItem(i, 3, QTableWidgetItem(item[5]))
            table.item(i,0).setFlags(Qt.ItemIsEnabled)
            i += 1
        table.update()

    def handleSelectionChange(self):
        currentrow = self.table1.currentRow()
        id = self.table1.item(currentrow,0).text()#获得id
        advice,self.fname = advice_by_id(int(id))
        self.patient_id = int(id)#选中时更改
        self.advice.setText(advice)
        self.image()

    def image(self):

        jpg = QtGui.QPixmap(self.fname).scaled(self.Imglabel.width(), self.Imglabel.height())
        self.Imglabel.setPixmap(jpg)
        result = google(self.fname)
        self.Infolabel.setText(result)

    def exit_triggered(self):
        qtWindows.loginWindow.show()  # 登录界面
        qtWindows.mainWindow.close()  # 关闭主界面

    def trigger_AlexNet(self):
        qtWindows.loginWindow.show()  # 登录界面
        qtWindows.mainWindow.close()  # 关闭主界面

    def trigger_GoogleNet(self):
        qtWindows.loginWindow.show()  # 登录界面
        qtWindows.mainWindow.close()  # 关闭主界面

    def look_back(self,event):
        qtWindows.historyWindow.hide()
        qtWindows.mainWindow.show()


class mainShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainShow, self).__init__(parent)
        self.setupUi(self)
        self.fileBtn.clicked.connect(self.loadImage)
        self.btn_advice.clicked.connect(self.giveAdvice)
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('menu')
        self.fileBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_advice.setCursor(QCursor(Qt.PointingHandCursor))

        # 添加一个动作到菜单
        action = QAction('logout', self)
        file_menu.addAction(action)

        # 连接菜单项的点击事件到槽函数
        action.triggered.connect(self.exit_triggered)

        self.listWidget.itemSelectionChanged.connect(
            self.handleSelectionChange
        )
        self.head.setCursor(QCursor(Qt.PointingHandCursor))#悬浮小手
        self.history.setCursor(QCursor(Qt.PointingHandCursor))#悬浮小手

        self.history.mouseReleaseEvent = self.look_history

    def exit_triggered(self):
        qtWindows.loginWindow.show()  # 登录界面
        qtWindows.mainWindow.close()  # 关闭主界面


    # 选择的选项
    def handleSelectionChange(self):
        # 当前选择项目
        currentItem = self.listWidget.currentItem()
        self.fname = currentItem.text()
        result = google(self.fname)
        self.Infolabel.setText(result)

        jpg = QtGui.QPixmap(self.fname).scaled(self.Imglabel.width(), self.Imglabel.height())

        self.Imglabel.setPixmap(jpg)
    def look_history(self,event):

        qtWindows.historyWindow = HistoryShow()  # 实例化主历史
        qtWindows.historyWindow.show()  # 展示历史页面
        qtWindows.mainWindow.hide()
        qtWindows.historyWindow.doctor_name.setText("Dear doctor: " + qtWindows.doctor_name)

    def giveAdvice(self):
        patient_name = self.patient_name.text()
        patient_age = self.patient_age.text()
        advice = self.advice.toPlainText()
        if patient_name == "":
            QMessageBox.warning(
            self,
            "Error","请重新输入患者姓名"
            )
        elif patient_age == "":
            QMessageBox.warning(
                self,
                "Error", "请重新输入患者年龄"
            )
        elif advice == "":
            QMessageBox.warning(
                self,
                "Error", "请给出建议"
            )
        elif self.fname == "":
            QMessageBox.warning(
                self,
                "Error", "请输入肝脏超声图片"
            )
        else:
            give_advice(patient_name,patient_age,advice,self.fname)
            QMessageBox.information(
                self,
                'success',
                '操作成功')
            self.patient_age.setText("")
            self.patient_name.setText("")
            self.advice.setText("")

    # 打开文件功能
    def loadImage(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, '请选择图片','.','图像文件(*.jpg *.jpeg *.png)')
        if self.fname:
            self.Infolabel.setText("文件打开成功\n"+self.fname)
            # self.Imglabel.set
            jpg = QtGui.QPixmap(self.fname).scaled(self.Imglabel.width(), self.Imglabel.height())

            self.Imglabel.setPixmap(jpg)

            result = google(self.fname)

            self.Infolabel.setText(result)

            for i in range(self.listWidget.count()):
                # 取出列表项
                itemText = self.listWidget.item(i).text()
                if itemText == self.fname:
                    self.listWidget.takeItem(i)
                    break

            listItem = self.listWidget.addItem(self.fname)#添加到列表中啊

        else:
            self.Infolabel.setText("请打开文件")

class Login(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.btn_login.clicked.connect(self.onLogin)
        self.edit_password.returnPressed.connect(self.onLogin)
        self.edit_username.setText('zhoulei')
    def onLogin(self):
        username = self.edit_username.text()#获取账号
        pwd = self.edit_password.text()
        loginResult = loginCheck(username,pwd)
        if loginResult == False:
            QMessageBox.warning(
            self,
            "Error","用户名或密码错误，请重新输入"
            )
        else:
            buildDatabase()#登录成功

            qtWindows.mainWindow = mainShow()#实例化主窗口
            qtWindows.mainWindow.show()#展示主窗口
            qtWindows.doctor_name = username
            self.edit_username.setText(username)
            self.edit_password.setText('')
            qtWindows.loginWindow.hide()
            qtWindows.mainWindow.doctor_name.setText("Dear doctor: " + qtWindows.doctor_name)

            # self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtWindows.loginWindow = Login()
    qtWindows.loginWindow.show()
    sys.exit(app.exec_())
