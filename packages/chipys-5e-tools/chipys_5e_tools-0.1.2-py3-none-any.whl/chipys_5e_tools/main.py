from PyQt5 import QtCore, QtGui, QtWidgets
import QT.gui
import QT.gui_report
import sys
import dice

# define globals
formula_log = [""]
formula_log_model = None
dice_log = []
dice_log_model = None
dice_tower = dice.Dice()

gui_main = None
MainWindow = None
gui_report = None
ReportWindow = None

def apply_ui_connections():
    """Overlay that connects up the GUI so that we can modularly replace the gui.py from QT5

    Args:
        gui_obj (gui.Ui_MainWindow): Main window GUI object
    """
    global gui_main, MainWindow, gui_report, reportWindow

    # set window icon
    MainWindow.setWindowIcon(QtGui.QIcon('Chipy128.ico'))
    MainWindow.setWindowTitle("Chipy's 5E Dice Sim")

    # link menus
    gui_main.actionProject_GitHub.triggered.connect(lambda: show_popup("Thanks for your curiosity! Please feel free to check out the project at https://github.com/iamchipy/chipys-5e-companion"))
    gui_main.actionChipy_Dev.triggered.connect(lambda: show_popup("Thanks for your curiosity! You can find more of my stuff at www.chipy.dev"))

    # link buttons
    gui_main.simulate.clicked.connect(lambda: run_sim(gui_main))
    gui_main.roll_active.clicked.connect(lambda: roll_active(gui_main))

    # connect listView log to click even with index
    gui_main.dice_log.clicked[QtCore.QModelIndex].connect(click_dice_log)
    gui_main.formula_log.clicked[QtCore.QModelIndex].connect(click_formula_log)

def show_popup( in_str):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Results!")
    msg.setText(in_str)
    msg_instance = msg.exec_()  # exec with instanciation

def click_dice_log(index):
    global dice_log_model, gui_main
    item = dice_log_model.itemFromIndex(index)
    log_str = str(item.text())
    log_list = log_str.split("'")
    formula_used_was = log_list[1]
    gui_main.attack_formula.setText(formula_used_was)

def click_formula_log(index):
    global formula_log_model, gui_main
    item = formula_log_model.itemFromIndex(index)
    formula_used_was = str(item.text())
    gui_main.attack_formula.setText(formula_used_was)    

def roll_active(gui_obj):
    global dice_log, dice_log_model, formula_log, formula_log_model
    dice_tower = dice.Dice()
    formula = gui_obj.attack_formula.text()
    flag_adv = gui_obj.flag_adv.isChecked()
    flag_bls = gui_obj.flag_bls.isChecked()
    flag_dis = gui_obj.flag_dis.isChecked()
    flag_ela = gui_obj.flag_ela.isChecked()
    flag_ins = gui_obj.flag_ins.isChecked()
    flag_gwm = gui_obj.flag_gwm.isChecked()
    ac= gui_obj.armor_class.value()
    hit_rate = [0,0]
  

    roll, log, formula = dice_tower.r(formula, show_rolls=True,
                                                flag_adv = flag_adv,
                                                flag_bls = flag_bls,
                                                flag_dis = flag_dis,
                                                flag_ela = flag_ela,
                                                flag_ins = flag_ins,
                                                flag_gwm = flag_gwm)

    # build log
    dice_log.append([formula,roll,log])
    dice_log_model = QtGui.QStandardItemModel()
    gui_obj.dice_log.setModel(dice_log_model)
    dice_log_model.clear()
    for r in dice_log[-8:]:
        dice_log_model.appendRow(QtGui.QStandardItem(str(r)))
        # log hits
        if  int(r[1]) > ac:
            hit_rate[0] +=1
        hit_rate[1] +=1

    # build log last used formula
    expanded_var = formula_log[-1:][0]
    if formula != expanded_var:
        formula_log.append(formula)
    formula_log_model = QtGui.QStandardItemModel()
    gui_obj.formula_log.setModel(formula_log_model)
    formula_log_model.clear()
    for r in formula_log[-8:]:
        formula_log_model.appendRow(QtGui.QStandardItem(str(r)))        

    # build hit rate
    hit_rate = (100*hit_rate[0])//hit_rate[1]

    # display the current roll results
    gui_obj.result.setText(str(roll))
    gui_obj.hit_chance.setText(str(hit_rate))
    return roll
    
def run_sim(gui_obj):
    global dice_tower, ReportWindow, gui_report
    gui_obj.result.setText("Init...")
    formula = gui_obj.attack_formula.text()
    max_roll = dice_tower.max_roll(formula)
    roll_tally = [0 for i in range(max_roll)]
    hit_tally = [0 for i in range(35)]
    sim_count = gui_obj.sim_count.text()
    ac= gui_obj.armor_class.value()
    print(f"Starting {sim_count} itterations...")

    for i in range(int(sim_count)):
    # for i in range(1000):
        # roll dice
        rolled = roll_active(gui_obj)
        
        # log the roll in our tallies
        roll_tally[rolled-1] += 1
        if ac <0:
            for dc in range(len(hit_tally)):
                if rolled >= dc:
                    hit_tally[dc-1] +=1
        elif rolled >= ac:
            hit_tally[ac-1] += 1

    # build report

    roll_tally = roll_tally[1:]
    roll_tally_ratios = [round((roll_tally[i]/int(sim_count))*100,1) for i in range(max_roll-1)]
    print("How hard did you hit:")
    print(roll_tally)
    print(roll_tally_ratios)

    hit_tally = hit_tally[:-1]
    hit_tally_ratios = [round((hit_tally[i]/int(sim_count))*100,1) for i in range(len(hit_tally))]
    print("How often did you hit(at what AC):")
    print(hit_tally)
    print(hit_tally_ratios)    

    table_data = {  'roll_tally':roll_tally,
                    'roll_tally_ratios':roll_tally_ratios,
                    'hit_tally':hit_tally,
                    'hit_tally_ratios':hit_tally_ratios}

    # display
    gui_obj.result.setText("Done!")
    build_report_table(table_data, f"Results for {sim_count} itterations of {formula} VS an ArmorClass [{ac}]")
        
def build_report_table(table_data:dict, report_title:str="Results of simulation:"):
    global gui_report, ReportWindow

    largest_row = 0
    for name, set in table_data.items():
        print(len(set))
        print(set)
        if len(set) > largest_row:
            largest_row = len(set)

    gui_report.report_title.setText(report_title)

    gui_report.report_table.setRowCount(len(table_data))
    gui_report.report_table.setColumnCount(largest_row)

    # gui_report.report_table.setHorizontalHeaderLabels(("a","aa"))
    # gui_report.report_table.setItem(0,0,QtWidgets.QTableWidgetItem("test"))
    gui_report.report_table.setVerticalHeaderLabels(("roll","roll","hit","hit"))

    r=0
    for name, list in table_data.items():
        gui_report.report_table.setRowHeight(r,10)
        for c in range(len(list)):
            gui_report.report_table.setItem(r,c,QtWidgets.QTableWidgetItem(str(list[c])))
            gui_report.report_table.setColumnWidth(c,33)
            
        r+=1

    ReportWindow.show()

if __name__ == "__main__":
    import sys

    # build main GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    gui_main = QT.gui.Ui_MainWindow()
    gui_main.setupUi(MainWindow)
    MainWindow.show()

    # build report GUI
    ReportWindow = QtWidgets.QWidget()
    gui_report = QT.gui_report.Ui_Form()
    gui_report.setupUi(ReportWindow)

    # Modify the gui with connections and links
    apply_ui_connections()  # here we modify actions to the GUI

    # clean up on exit
    sys.exit(app.exec_())
