from PyQt5 import QtCore, QtGui, QtWidgets, uic
from iFeature_core import *
import sys

#Stylesheet to cater toUser Preferences
DARK_STYLESHEET = LIGHT_STYLESHEET = STYLESHEET = ""

#For returning to a stackw after displayiung Project Info
CURRENT_STACKW = ""

#For generating error msg popups
ERROR_MSG = "Input Required"

in_file = ""

class UI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_MainWindow, self).__init__()

        #Load UI file
        uic.loadUi("iFeaturizer_v3.ui", self)   

        self.setWindowTitle("iFeaturizer")
        self.setFixedSize(800,550)

        #MenuBar
        self.help_menu = self.findChild(QtWidgets.QMenu, "menuInfo")
                
        #Widgets
        self.stackw = self.findChild(QtWidgets.QStackedWidget, "stackw")
        self.input_page = self.findChild(QtWidgets.QWidget, "input_page_1")
        self.output_page = self.findChild(QtWidgets.QWidget, "output_page_2")
        self.help_page = self.findChild(QtWidgets.QWidget, "info_page_3")

        #Stackw 1
        self.multiseq_radio = self.findChild(QtWidgets.QRadioButton, "mult_seq_bn")
        self.multiseq_openFile = self.findChild(QtWidgets.QPushButton, "openFile_pushButton")
        self.in_file_path = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.in_fasta_col_name = self.findChild(QtWidgets.QLineEdit, "lineEdit_5")

        self.singleseq_radio = self.findChild(QtWidgets.QRadioButton, "single_seq_bn")
        self.single_fasta_sequence = self.findChild(QtWidgets.QPlainTextEdit, "input_singleseq_textbox")
        
        self.continue_btn = self.findChild(QtWidgets.QPushButton, "continue_bn")

    
        #Stackw 2
        self.in_iFeature_dir = self.findChild(QtWidgets.QLineEdit,"in_iFeature_dir")
        self.iFeatureDir_openFile = self.findChild(QtWidgets.QPushButton, "openFile_pushButton_3")
        self.in_destination_path = self.findChild(QtWidgets.QLineEdit, "in_destination_path")
        self.destinationPath_openFile = self.findChild(QtWidgets.QPushButton, "openFile_pushButton_2")
        self.in_merged_df_name = self.findChild(QtWidgets.QLineEdit, "in_mergedDf_name")
        self.output_type = self.findChild(QtWidgets.QComboBox, "delimiter_choice_comboBox")

        self.extract_btn = self.findChild(QtWidgets.QPushButton, "extract_bn")
        self.prev_btn = self.findChild(QtWidgets.QPushButton, "prev_bn")

        #Stackw 3
        self.back_btn = self.findChild(QtWidgets.QPushButton, "extract_bn_2")
        

        #MenuBar Operations
        self.help_menu.triggered.connect(lambda: self.display_help_info())
        # self.actionLight_Theme.triggered.connect(lambda: self.set_lightTheme())
        # self.actionDark_Theme.triggered.connect(lambda: self.set_darkTheme())


        #Stackw 1 Operations
        self.multiseq_radio.click()
        self.accept_multiseq_file()

        self.multiseq_radio.clicked.connect(lambda: self.accept_multiseq_file())
        self.singleseq_radio.clicked.connect(lambda: self.accept_multiseq_file(False))

        self.multiseq_openFile.clicked.connect(lambda: self.openFile(False))
        self.in_file_path.returnPressed.connect(lambda: self.in_fasta_col_name.setFocus() if not self.in_fasta_col_name.text() else self.continue_btn_clicked())
        self.in_fasta_col_name.returnPressed.connect(lambda: self.in_file_path.setFocus() if not self.in_file_path.text() else self.continue_btn_clicked())

        self.continue_btn.clicked.connect(lambda: self.continue_btn_clicked())

        #Stackw 2 Operations
        self.iFeatureDir_openFile.clicked.connect(lambda: self.openFile(True))
        self.destinationPath_openFile.clicked.connect(lambda: self.openFile(True, "destination"))

        self.in_iFeature_dir.returnPressed.connect(lambda: self.in_destination_path.setFocus() if not self.in_destination_path.text() else \
                                                   (self.in_merged_df_name.setFocus() if not self.in_merged_df_name.text() else self.extract_btn_clicked())
                                                   )
        self.in_destination_path.returnPressed.connect(lambda: self.in_merged_df_name.setFocus() if not self.in_merged_df_name.text() else self.extract_btn_clicked())
        self.in_merged_df_name.returnPressed.connect(lambda: self.extract_btn_clicked())

        self.prev_btn.clicked.connect(lambda: self.prev_btn_clicked())
        self.extract_btn.clicked.connect(lambda: self.extract_btn_clicked())
        
        #Stackw 3 Operations
        self.back_btn.clicked.connect(lambda: self.back_btn_clicked())



        #TEMPORARY DEBUGGING
        self.in_file_path.setText("C:/Users/prana/OneDrive/Desktop/Research/protein_research/GUI/lengths_test.csv")
        self.in_fasta_col_name.setText("fasta_seq")
        self.in_iFeature_dir.setText("C:/Users/prana/PycharmProjects/pythonProject/venv/iFeature")
        self.in_destination_path.setText("C:/Users/prana/PycharmProjects/pythonProject/venv/iFeaturizer/destination")
        # self.in_merged_df_name.setText("test")

        # self.single_fasta_sequence.setPlainText("MADTPTLFTQFLRHHLPGQRFRKDILKQAGRILANKGEDATIAFLRGKSEESPPDFQPPVKCPIIACSRPLTEWPIYQASVAIQGYVYGQSLAEFEASDPGCSKDGLLGWFDKTGVCTDYFSVQGLNLIFQNARKRYIGVQTKVTNRNEKRHKKLKRINAKRIAEGLPELTSDEPESALDETGHLIDPPGLNTNIYCYQQVSPKPLALSEVNQLPTAYAGYSTSGDDPIQPMVTKDRLSISKGQPGYIPEHQRALLSQKKHRRMRGYGLKARALLVIVRIQDDWAVIDLRSLLRNAYWRRIVQTKEPSTITKLLKLVTGDPVLDATRMVATFTYKPGIVQVRSAKCLKNKQGSKLFSERYLNETVSVTSIDLGSNNLVAVATYRLVNGNTPELLQRFTLPSHLVKDFERYKQAHDTLEDSIQKTAVASLPQGQQTEIRMWSMYGFREAQERVCQELGLADGSIPWNVMTATSTILTDLFLARGGDPKKCMFTSEPKKKKNSKQVLYKIRDRAWAKMYRTLLSKETREAWNKALWGLKRGSPDYARLSKRKEELARRCVNYTISTAEKRAQCGRTIVALEDLNIGFFHGRGKQEPGWVGLFTRKKENRWLMQALHKAFLELAHHRGYHVIEVNPAYTSQTCPVCRHCDPDNRDQHNREAFHCIGCGFRGNADLDVATHNIAMVAITGESLKRARGSVASKTPQPLAAE")

        # self.set_lightTheme()
        
        #Show application
        self.show()
        

    def clicked(self):
        print("clicked")


    #Methods to set Theme based on User Preferences
    def set_lightTheme(self):
        global STYLESHEET
        global LIGHT_STYLESHEET
    
        STYLESHEET = LIGHT_STYLESHEET
        self.setStyleSheet(STYLESHEET)
        #need to avoid Qlabels from getting affected. 
        #QPushButton, QLineEdit, QRadioButton, QPlainTextEdit, QComboBox and QMenu and QWidget only

    def set_darkTheme(self):
        global STYLESHEET
        global DARK_STYLESHEET
    
        STYLESHEET = DARK_STYLESHEET
        self.setStyleSheet(STYLESHEET)


    #Methods for opening of input file
    def accept_multiseq_file(self, radiobtn_checked=True):
        self.multiseq_openFile.setEnabled(radiobtn_checked)
        self.in_file_path.setEnabled(radiobtn_checked)
        self.in_fasta_col_name.setEnabled(radiobtn_checked)
        self.single_fasta_sequence.setDisabled(radiobtn_checked)


    def openFile(self, dir_mode = False, dir_type = 'iFeature'):
        if dir_mode:
            dirname = QtWidgets.QFileDialog.getExistingDirectory(self.openFile_pushButton_2, "Select Destination Folder")
            if dirname:
                if dir_type == 'iFeature':
                    self.in_iFeature_dir.clear()
                    self.in_iFeature_dir.setText(dirname)
                else:
                    self.in_destination_path.clear()
                    self.in_destination_path.setText(dirname)
        else:
            fname = QtWidgets.QFileDialog.getOpenFileName(self.openFile_pushButton, "Open File", "", "All Files (*)")   
            self.in_file_path.clear()
            self.in_file_path.setText(fname[0])


    #Methods for handling display of Project Info through Menubar
    def display_help_info(self):
        global CURRENT_STACKW
        CURRENT_STACKW = self.stackw.currentWidget()
        self.stackw.setCurrentWidget(self.help_page)


    def back_btn_clicked(self):
        self.stackw.setCurrentWidget(CURRENT_STACKW)


    #Methods for handling transition between stackw 1 and 2
    def continue_btn_clicked(self):
        self.validate_page1()
        if ERROR_MSG == 'VALID':
            self.stackw.setCurrentWidget(self.output_page)
        else:
            self.show_error_popup()
    

    def prev_btn_clicked(self):
        self.stackw.setCurrentWidget(self.input_page)


    def extract_btn_clicked(self):
        global ERROR_MSG

        self.validate_page2()
        if ERROR_MSG == "VALID":
            
            # self.hide()
            # msg = QtWidgets.QMessageBox()
            # msg.setWindowTitle("Extract")
            # msg.setText("Running Feature Extraction...")
            # msg.setIcon(QtWidgets.QMessageBox.Information)
            # msg.addButton(QtWidgets.QMessageBox.Ok)
            # msg.exec_()

            iF = iFeature_set(  self.in_file_path.text().strip(),      \
                                in_file,                               \
                                self.in_fasta_col_name.text().strip(), \
                                self.in_iFeature_dir.text().strip() )
            

            iF.generate_intermediate_files()
            
            print("Extracting...\n")

            try:
                iF.extract()
            except:
                ERROR_MSG = "Error while extracting"
                print("extraction didnt work")
                self.show_error_popup()
                #self.reset to beginning
            

            try:
                iF.postprocess_and_merge(destination_dir= self.in_destination_path.text().strip(), \
                                         df_merged_name= self.in_merged_df_name.text().strip(),    \
                                         out_type= self.output_type.currentText().strip('.'))
            except:
                print("postprocess didnt work")
            
            finally:
                print("\n\nFeature Extraction Complete!\n\n")
            # self.show()
            
            
        else:
            self.show_error_popup()


    def show_error_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(ERROR_MSG)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()


    def validate_page1(self):
        global ERROR_MSG

        #Check for Radio Button, Existing File, Valid Extension, existent FASTA Column
        if self.multiseq_radio.isChecked():
            input_path = self.in_file_path.text().strip(' ')
            if not os.path.isfile(input_path):
                ERROR_MSG = "File not found"        
            else:
                if input_path.split(".")[-1] not in ["xlsx", "csv", "tsv"]:
                    ERROR_MSG = "Invalid Extension. Acceptable types are *.xlsx, *.csv, *.tsv"
                else:
                    if self.in_fasta_col_name.text():
                        ERROR_MSG = self.load_input_file()
                    else:
                        ERROR_MSG = "FASTA Column Not Specified"

        elif self.singleseq_radio.isChecked():
            global single_fasta

            single_fasta = self.single_fasta_sequence.toPlainText().strip('\n ')
        
            if len(single_fasta) <= 31:
                ERROR_MSG = "Length of fasta sequence must be > 31"
            else:
                for letter in single_fasta:
                    if letter not in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
                        ERROR_MSG = "Invalid letter in input fasta sequence"
                if ERROR_MSG != "Invalid letter in input fasta sequence":
                    ERROR_MSG = 'VALID'                  


    def validate_page2(self):
        global ERROR_MSG

        if self.in_iFeature_dir.text() and os.path.isfile("{}/iFeature.py".format(self.in_iFeature_dir.text())):
            if self.in_destination_path.text() and os.path.isdir(self.in_destination_path.text()):
                if self.in_merged_df_name.text():
                            ERROR_MSG = "VALID"
                else:
                    ERROR_MSG = "Invalid name for Merged iFeature df"
            else:
                ERROR_MSG = "Invalid Destination Directory"
        else:
            ERROR_MSG = "Invalid iFeature Directory"


    def load_input_file(self):
        global in_file 

        ftype = self.in_file_path.text().split(".")[-1]
        try:
            if ftype == "xlsx":
                in_file = pd.read_excel(self.in_file_path.text(), engine='openpyxl')
            elif ftype == "csv":
                in_file = pd.read_csv(self.in_file_path.text())
            elif ftype == "tsv":
                in_file = pd.read_csv(self.in_file_path.text(), delimiter='\t')
            
            #check if in_file[col] exists
            in_file[self.in_fasta_col_name.text().strip()] #this can raise KeyError if does not exist
            return "VALID"

        except:
            return "Parsing Error. Provided column name could be invalid"




if __name__ == "__main__":    
    
    with open("styles/light_theme.css") as light_theme:
        LIGHT_STYLESHEET = light_theme.read()

    with open("styles/dark_theme.css") as dark_theme:
        DARK_STYLESHEET = dark_theme.read()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    sys.exit(app.exec_())