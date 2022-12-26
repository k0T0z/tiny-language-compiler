from argparse import ArgumentParser, RawTextHelpFormatter
import sys

from PySide6.QtCore import (QByteArray, QFile, QFileInfo, QSaveFile, QSettings,
                            QTextStream, Qt, Slot, QDir)
from PySide6.QtGui import (QAction, QIcon, QColorSpace, QGuiApplication,
                           QImageReader, QKeySequence,
                           QPalette, QPixmap)
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QWidget, QTextEdit, QHBoxLayout, QLabel,
                               QMessageBox, QPushButton, QVBoxLayout,
                               QSizePolicy)
import tinylanguagecompiler_rc
from scanner import Lexer
from parser_3 import parser


class MainWindow(QMainWindow):
    _status_bar_message_lifetime = 2000

    def __init__(self):
        super().__init__()

        self._image_label = QLabel()
        self._image_label.setBackgroundRole(QPalette.Base)
        self._image_label.setSizePolicy(QSizePolicy.Ignored,
                                        QSizePolicy.Ignored)
        self._image_label.setScaledContents(True)

        self.vals = []
        self.types = []

        self._cur_file = ''

        self.create_layout()
        self.create_actions()
        self.create_menus()
        self.create_tool_bars()
        self.create_status_bar()

        self.read_settings()

        self._text_edit.document() \
            .contentsChanged.connect(self.document_was_modified)

        self.set_current_file('')
        self.setUnifiedTitleAndToolBarOnMac(True)

    def closeEvent(self, event):
        if self.maybe_save():
            self.write_settings()
            event.accept()
        else:
            event.ignore()

    @Slot()
    def new_file(self):
        if self.maybe_save():
            self._text_edit.clear()
            self.set_current_file('')

    @Slot()
    def open(self):
        if self.maybe_save():
            fileName, filtr = QFileDialog.getOpenFileName(self)
            if fileName:
                self.load_file(fileName)

    @Slot()
    def save(self):
        if self._cur_file:
            return self.save_file(self._cur_file)

        return self.save_as()

    @Slot()
    def save_as(self):
        fileName, filtr = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.save_file(fileName)

        return False

    @Slot()
    def about(self):
        QMessageBox.about(self, "About Tiny Language Compiler",
                          "The <b>Tiny Language Compiler</b> used to scan "
                          "and parse tiny language source files.")

    @Slot()
    def scan(self):
        if self._text_edit.toPlainText() == "":
            return QMessageBox.warning(self, "Tiny Language Compiler",
                                       "Can't find any tiny language code. Try"
                                       " to open tiny language source file.")
        self._output_console.clear()
        self._output_console.append("scanning...\n")
        lex = Lexer(self._text_edit.toPlainText())
        s = ""
        self.vals = []
        self.types = []
        while lex.pos < len(lex.text):
            token = lex.get_next_token()
            if token is None:
                continue
            s += token.__str__()
            self.vals.append(token.value)
            self.types.append(token.type)
        self._output_console.append(s)
        self._output_console.append("\nScanning completed")

    @Slot()
    def parse(self):
        if self._text_edit.toPlainText() == "":
            return QMessageBox.warning(self, "Tiny Language Compiler",
                                       "Can't find any tiny language code. Try"
                                       " to open tiny language source file.")
        if self.vals == [] or self.types == []:
            return QMessageBox.warning(self, "Tiny Language Compiler",
                                       "Can't find any stored tokens. This is "
                                       "because you didn't scan your code.")
        self._output_console.clear()
        self._output_console.append("parsing...\n")
        par = parser(self.vals, self.types)
        par.drawParseTree()
        self._output_console.append("parsing completed")

    @Slot()
    def show_syntax_tree(self):
        if self._text_edit.toPlainText() == "":
            return QMessageBox.warning(self, "Tiny Language Compiler",
                                       "Can't find any tiny language code. Try"
                                       " to open tiny language source file.")
        if self.vals == [] or self.types == []:
            return QMessageBox.warning(self, "Tiny Language Compiler",
                                       "Can't find any stored tokens. This is "
                                       "because you didn't scan your code.")

        reader = QImageReader("output.png")
        reader.setAutoTransform(True)
        new_image = reader.read()
        native_filename = QDir.toNativeSeparators("output.png")
        if new_image.isNull():
            error = reader.errorString()
            QMessageBox.information(self,
                                    QGuiApplication.applicationDisplayName(),
                                    f"Cannot load {native_filename}: {error}")
            return False
        self._set_image(new_image)
        self.setWindowFilePath("output.png")

        w = self._image.width()
        h = self._image.height()
        d = self._image.depth()
        color_space = self._image.colorSpace()
        description = color_space.description() \
            if color_space.isValid() else 'unknown'
        message = \
            f'Opened "{native_filename}", {w}x{h}, Depth: {d} ({description})'
        self.statusBar().showMessage(message)
        return True

    def _set_image(self, new_image):
        self._image = new_image
        if self._image.colorSpace().isValid():
            self._image.convertToColorSpace(QColorSpace.SRgb)
        self._image_label.setPixmap(QPixmap.fromImage(self._image))
        self._scale_factor = 1.0
        self._image_label.setWindowTitle("Syntax Tree")
        self._image_label.show()

    @Slot()
    def document_was_modified(self):
        self.setWindowModified(self._text_edit.document().isModified())

    def create_layout(self):
        self._text_edit = QTextEdit()

        self._main_widget = QWidget()

        main_layout = QVBoxLayout()

        horizontal_group_box = QHBoxLayout()
        horizontal_group_box.addWidget(self._text_edit)

        vertical_group_box = QVBoxLayout()
        scan_button = QPushButton("Scan")
        scan_button.clicked.connect(self.scan)
        parse_button = QPushButton("Parse")
        parse_button.clicked.connect(self.parse)
        show_syntax_tree_button = QPushButton("Show Syntax Tree")
        show_syntax_tree_button.clicked.connect(self.show_syntax_tree)
        vertical_group_box.addWidget(scan_button)
        vertical_group_box.addWidget(parse_button)
        vertical_group_box.addWidget(show_syntax_tree_button)

        horizontal_group_box.addLayout(vertical_group_box)

        main_layout.addLayout(horizontal_group_box)

        self._output_console = QTextEdit()
        self._output_console.setReadOnly(True)

        main_layout.addWidget(self._output_console)

        self._main_widget.setLayout(main_layout)

        self.setCentralWidget(self._main_widget)

    def create_actions(self):
        icon = QIcon.fromTheme("document-new", QIcon(':/images/new.png'))
        self._new_act = QAction(icon, "&New", self, shortcut=QKeySequence.New,
                                statusTip="Create a new file",
                                triggered=self.new_file)

        icon = QIcon.fromTheme("document-open", QIcon(':/images/open.png'))
        self._open_act = QAction(icon, "&Open...", self,
                                 shortcut=QKeySequence.Open,
                                 statusTip="Open an existing file",
                                 triggered=self.open)

        icon = QIcon.fromTheme("document-save", QIcon(':/images/save.png'))
        self._save_act = QAction(icon, "&Save", self,
                                 shortcut=QKeySequence.Save,
                                 statusTip="Save the document to disk",
                                 triggered=self.save)

        self._save_as_act = QAction("Save &As...", self,
                                    shortcut=QKeySequence.SaveAs,
                                    statusTip="Save the document "
                                    "under a new name",
                                    triggered=self.save_as)

        self._exit_act = QAction("E&xit", self, shortcut="Ctrl+Q",
                                 statusTip="Exit the tiny Language compiler",
                                 triggered=self.close)

        icon = QIcon.fromTheme("edit-cut", QIcon(':/images/cut.png'))
        self._cut_act = QAction(icon, "Cu&t", self, shortcut=QKeySequence.Cut,
                                statusTip="Cut the current selection's "
                                "contents to the clipboard",
                                triggered=self._text_edit.cut)

        icon = QIcon.fromTheme("edit-copy", QIcon(':/images/copy.png'))
        self._copy_act = QAction(icon, "&Copy",
                                 self, shortcut=QKeySequence.Copy,
                                 statusTip="Copy the current selection's "
                                 "contents to the clipboard",
                                 triggered=self._text_edit.copy)

        icon = QIcon.fromTheme("edit-paste", QIcon(':/images/paste.png'))
        self._paste_act = QAction(icon, "&Paste",
                                  self, shortcut=QKeySequence.Paste,
                                  statusTip="Paste the clipboard's contents "
                                  "into the current selection",
                                  triggered=self._text_edit.paste)

        self._about_act = QAction("&About", self,
                                  statusTip="Show the tiny language "
                                  "compiler's About box",
                                  triggered=self.about)

        self._about_qt_act = QAction("About &Qt", self,
                                     statusTip="Show the Qt library's "
                                     "About box",
                                     triggered=qApp.aboutQt)

        self._cut_act.setEnabled(False)
        self._copy_act.setEnabled(False)
        self._text_edit.copyAvailable.connect(self._cut_act.setEnabled)
        self._text_edit.copyAvailable.connect(self._copy_act.setEnabled)

    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self._new_act)
        self._file_menu.addAction(self._open_act)
        self._file_menu.addAction(self._save_act)
        self._file_menu.addAction(self._save_as_act)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._exit_act)

        self._edit_menu = self.menuBar().addMenu("&Edit")
        self._edit_menu.addAction(self._cut_act)
        self._edit_menu.addAction(self._copy_act)
        self._edit_menu.addAction(self._paste_act)

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)
        self._help_menu.addAction(self._about_qt_act)

    def create_tool_bars(self):
        self._file_tool_bar = self.addToolBar("File")
        self._file_tool_bar.addAction(self._new_act)
        self._file_tool_bar.addAction(self._open_act)
        self._file_tool_bar.addAction(self._save_act)

        self._edit_tool_bar = self.addToolBar("Edit")
        self._edit_tool_bar.addAction(self._cut_act)
        self._edit_tool_bar.addAction(self._copy_act)
        self._edit_tool_bar.addAction(self._paste_act)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def read_settings(self):
        settings = QSettings('QtProject', 'Tiny Language Compiler')
        geometry = settings.value('geometry', QByteArray())
        if geometry.size():
            self.restoreGeometry(geometry)

    def write_settings(self):
        settings = QSettings('QtProject', 'Tiny Language Compiler')
        settings.setValue('geometry', self.saveGeometry())

    def maybe_save(self):
        if self._text_edit.document().isModified():
            ret = QMessageBox.warning(self, "Tiny Language Compiler",
                                      "The document has been modified."
                                      "\nDo you want to save "
                                      "your changes?",
                                      QMessageBox.Save | QMessageBox.Discard |
                                      QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def load_file(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            reason = file.errorString()
            QMessageBox.warning(self, "Tiny Language Compiler",
                                f"Cannot read file {fileName}:\n{reason}.")
            return

        inf = QTextStream(file)
        with QApplication.setOverrideCursor(Qt.WaitCursor):
            self._text_edit.setPlainText(inf.readAll())

        self.set_current_file(fileName)
        self.statusBar().showMessage("File loaded",
                                     self._status_bar_message_lifetime)

    def save_file(self, fileName):
        error = None
        with QApplication.setOverrideCursor(Qt.WaitCursor):
            file = QSaveFile(fileName)
            if file.open(QFile.WriteOnly | QFile.Text):
                outf = QTextStream(file)
                outf << self._text_edit.toPlainText()
                if not file.commit():
                    reason = file.errorString()
                    error = f"Cannot write file {fileName}:\n{reason}."
            else:
                reason = file.errorString()
                error = f"Cannot open file {fileName}:\n{reason}."

        if error:
            QMessageBox.warning(self, "Tiny Language Compiler", error)
            return False

        self.set_current_file(fileName)
        self.statusBar().showMessage("File saved",
                                     self._status_bar_message_lifetime)
        return True

    def set_current_file(self, fileName):
        self._cur_file = fileName
        self._text_edit.document().setModified(False)
        self.setWindowModified(False)

        if self._cur_file:
            shown_name = self.stripped_name(self._cur_file)
        else:
            shown_name = 'untitled.txt'

        self.setWindowTitle(f"{shown_name}[*] - Tiny Language Compiler")

    def stripped_name(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


if __name__ == '__main__':
    argument_parser = ArgumentParser(description='Tiny Language Compiler',
                                     formatter_class=RawTextHelpFormatter)
    argument_parser.add_argument("file", help="File",
                                 nargs='?', type=str)
    options = argument_parser.parse_args()

    app = QApplication(sys.argv)
    main_win = MainWindow()
    if options.file:
        main_win.load_file(options.file)
    main_win.show()
    sys.exit(app.exec())
