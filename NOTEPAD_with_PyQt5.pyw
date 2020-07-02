import PyQt5.QtWidgets as qwt
from PyQt5.QtGui import QKeySequence
from PyQt5.Qt import QTextCursor
# 主界面


class MainWindow(qwt.QMainWindow):
    def closeEvent(self, e) -> None:
        if not text.document().isModified():
            return
        answer = qwt.QMessageBox.question(window, '关闭之前查看', '关闭之前是否保存文件',
                                          qwt.QMessageBox.Save | qwt.QMessageBox.Discard | qwt.QMessageBox.Cancel
                                          )
        if answer & qwt.QMessageBox.Save:
            if file_path is None:
                save_as()
            else:
                save()
        elif answer & qwt.QMessageBox.Cancel:
            e.ignore()


app = qwt.QApplication([])
app.setApplicationName('QS的文本编辑器')
text = qwt.QPlainTextEdit()
window = MainWindow()
window.setMinimumSize(800, 600)
window.setCentralWidget(text)


# 文件路径的变量
file_path = None


# 添加菜单项

# 打开
menu = window.menuBar().addMenu('文件')
open_action = qwt.QAction('打开')


def open_file():
    global file_path
    path = qwt.QFileDialog.getOpenFileName(window, "open")[0]
    if path:
        text.setPlainText(open(path).read())
        file_path = path


open_action.setShortcut(QKeySequence.Open)
open_action.triggered.connect(open_file)
menu.addAction(open_action)

# 保存
save_action = qwt.QAction('保存')


def save():
    if file_path is None:
        pass
    else:
        with open(file_path, 'w') as f:
            f.write(text.toPlainText())
        text.document().setModified(False)


save_action.setShortcut(QKeySequence.Save)
save_action.triggered.connect(save)
menu.addAction(save_action)

# 另存为
save_as_action = qwt.QAction('另存为')


def save_as():
    global file_path
    path = qwt.QFileDialog.getSaveFileName(window, '另存为')[0]
    if path:
        file_path = path
        save()


save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)

menu.addSeparator()  # 分隔线


# 退出
exit_action = qwt.QAction('退出')
exit_action.setShortcut(QKeySequence.Close)
exit_action.triggered.connect(window.close)
menu.addAction(exit_action)


# 帮助
help_menu = window.menuBar().addMenu('帮助')
about_action = qwt.QAction('关于')


def show_about_dialog():
    about_text = "<center>这里是QS的文本编辑器</center><p>使用PyQt5制作</p><p>版本v1.0</p>"
    qwt.QMessageBox.about(window, '说明', about_text)


about_action.triggered.connect(show_about_dialog)
help_menu.addAction(about_action)


# 工具
tool_menu = window.menuBar().addMenu('工具')
find_action = qwt.QAction('查找')


def getStrPositions(shortString, longString):
    posList = []
    for i in range(0, len(longString)-len(shortString)+1):
        if longString[i:i+len(shortString)] == shortString:
            posList.append(i)
    return posList


def find_String():
    txt, choice = qwt.QInputDialog.getText(window, '查找', '请输入要查找的字符串：')
    TextContent = text.toPlainText()
    StrPosList = getStrPositions(shortString=txt, longString=TextContent)
    # txtbegin = TextContent.find(txt)
    # txtend = txtbegin+len(txt)
    if len(StrPosList) == 0:
        about_text = '<center>未找到"{}"</center>'.format(txt)
        qwt.QMessageBox.about(window, 'Error', about_text)
    else:
        textCsr = text.textCursor()
        for p in StrPosList:
            textCsr.setPosition(p, QTextCursor.MoveAnchor)
            textCsr.setPosition(p+len(txt), QTextCursor.KeepAnchor)
            text.setTextCursor(textCsr)  # 修改完光标之后 还得反向设置回文本编辑器
            about_text = '<center>坐标{}，已选中</center>'.format(p)
            qwt.QMessageBox.about(window, 'Tip', about_text)


find_action.triggered.connect(find_String)
tool_menu.addAction(find_action)

window.show()
app.exec_()
