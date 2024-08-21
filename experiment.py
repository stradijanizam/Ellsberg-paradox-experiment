# Ellsberg paradox experiment created by Darko Stojilović

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from os import listdir
from random import randint
from ClickableLabel import *

app = QApplication([])
window = uic.loadUi("experiment.ui")  # loading .ui file created in qt designer

window.results = "Results.csv"  # creating new .csv file to save data in


# function to create new .csv file with variable names
def new_dataset():
    if window.results not in listdir():     # write a new .csv file if not already created
        write_dataset = open(window.results, 'w')
        write_dataset.write("Gender,Age,Education,Condition,Position,Urn1,Marble1,Urn2,Marble2")
    else:
        open(window.results, 'r')  # reading the file if it already exists

        # Gender: male, female
        # Age: any number from 18 to 99
        # Education: Primary School, High School, Bachelor's, Master's, PhD
        # Condition: 100, 10, 2
        # Position: 0 (urn A half, urn B unknown), 1 (urn A unknown, urn B half)
        # Urn 1: 0 (unknown), 1 (half)
        # Marble 1: blue, red
        # Urn 2: 0 (unknown), 1 (half)
        # Marble 2: blue, red


# function to save results in .csv file
def save_results():
    if window.results in listdir():
        write_dataset = open(window.results, 'a')
        write_dataset.write(f"\n{window.gender},{window.age_var},{window.education},{window.condition_var},"
                            f"{window.condition_position},{window.urn_selected[0]},"
                            f"{window.marble_list[0]},{window.urn_selected[1]},{window.marble_list[1]}")
        write_dataset.close()


# Page 1 (Consent Form)

# function to hide the widget only showed when refused to participate
def page1hide():
    window.refuse.hide()


# function to check whether the consent was checked
def page1consent():
    if window.consent_yes.isChecked():       # continue to next page if consent agreed upon
        window.frame.setCurrentIndex(1)
    elif window.consent_no.isChecked():      # show message and exit button if consent refused
        window.refuse.show()
    else:
        window.empty_lbl.setText("Please answer in order to continue.")  # making sure participants answer the question


page1hide()  # initialising function that hides the widget only showed when refused to participate
window.startButton.clicked.connect(page1consent)  # connecting proceed button with consent checking function
window.exitButton.clicked.connect(QApplication.quit)  # connecting exit button with quit app built-in function


# Page 2 (Demographics)

# function to hide errors in filling out demographics form
def page2hide():
    window.gender_miss.hide()
    window.age_miss.hide()
    window.educ_miss.hide()


# function to verify participant has provided appropriate values for demographics
def page2action():
    p2missing = False  # nothing is missing in the form until changed

    # loop that checks whether gender is filled in, and if not, displaying to be a required field
    if window.gender_male.isChecked():
        window.gender = "male"      # saving age value for a dataset if male
        window.gender_miss.hide()
    elif window.gender_female.isChecked():
        window.gender = "female"    # saving age value for a dataset if female
        window.gender_miss.hide()
    else:
        window.gender_miss.show()
        p2missing = True  # signaling a missing value in gender

    # loop that checks whether age is filled in, and if not, displaying to be a required field
    if window.age.value() < 18:  # making it impossible for those under the age of 18 to participate
        window.age_miss.show()
        p2missing = True  # signaling a missing value in age
    else:
        window.age_var = window.age.value()  # saving age value for a dataset
        window.age_miss.hide()

    # loop that checks whether education is selected, and if not, displaying to be a required field
    if window.educ_box.currentText() == "Choose:":  # checking if they chose education level from a list
        window.educ_miss.show()
        p2missing = True  # signaling a missing value in education
    else:
        window.education = window.educ_box.currentText()  # saving education value for a dataset
        window.educ_miss.hide()

    # enabling to proceed to the next page if there are no missing values
    if not p2missing:
        window.frame.setCurrentIndex(2)
        page3timer()    # starting a timer for the next page


page2hide()  # initialising function that hides errors only showed when there are no missing values in demographics
window.proceed_p2.clicked.connect(page2action)      # connecting proceed button with function that checks missing values


# Page 3 (experiment with two trials as in original experiment)

# defining condition position
def page3positions():
    window.condition_position = randint(0, 1)   # using random function to decide the condition position

    # saving urn positions
    if window.condition_position == 0:
        window.urn_half = "Urn A"       # setting urn A to be a half urn
        window.urn_unknown = "Urn B"    # setting urn B to be an unknown urn
    else:
        window.urn_half = "Urn B"       # setting urn B to be a half urn
        window.urn_unknown = "Urn A"    # setting urn A to be an unknown urn


# defining new variables needed for calculating outcomes
window.condition = randint(0, 2)  # decide condition by random function: 0 (100 marbles), 1 (10 marbles), 2 (2 marbles)
window.condition_list = [100, 10, 2]    # setting up a list to hold number of marbles in each condition
window.round = 0  # creating variable to save which trial has taken place
window.urn_selected = [0, 0]   # empty list to save selected urns (half or unknown) in both trials
window.urn_list = ["", ""]  # empty list of strings to save whether urn a or urn b were chosen
window.marble_list = ["", ""]  # empty list of strings to save a marble chosen in both trials


def page3outcomes():
    window.split_half = int(window.condition_list[window.condition] / 2)  # splitting number of b and r marbles in half
    window.split_unknown = randint(0, window.condition_list[window.condition])  # randomising number of b and r marbles

    # connecting the click with a chosen urn
    click = window.sender()
    if click.x() == 297:
        window.urn_list[window.round] = "A"
    if click.x() == 757:
        window.urn_list[window.round] = "B"

    # disabling the option to click more than once
    window.urn_a.setEnabled(False)
    window.urn_b.setEnabled(False)

    # defining split point based on which urn is selected
    if window.urn_list[window.round] == "A":                 # if urn A selected
        if window.condition_position == 0:                   # if urn A is half
            window.urn_selected[window.round] = 1            # urn half is selected
            split = window.split_half                        # split point for half
        else:                                                # if urn A is unknown
            window.urn_selected[window.round] = 0            # urn unknown is selected
            split = window.split_unknown                     # split point for unknown
    else:                                                    # if urn B selected
        if window.condition_position == 1:                   # if urn B is half
            window.urn_selected[window.round] = 1
            split = window.split_half
        else:
            window.urn_selected[window.round] = 0
            split = window.split_unknown

    # generating random number and comparing it with split point to get the result
    window.random = randint(1, window.condition_list[window.condition])
    if window.random > split:
        window.marble_list[window.round] = "blue"   # participant draws blue if random number is larger than split point
    else:
        window.marble_list[window.round] = "red"

    # setting up outcome messages based on whether their attempt was successful or not
    if (window.round == 0 and window.marble_list[window.round] == "blue" or
            window.round == 1 and window.marble_list[window.round] == "red"):
        outcome_message = "Bravo, you drew a " + window.marble_list[window.round] + " marble. Please proceed"
    else:
        outcome_message = "Unfortunately, you drew a " + window.marble_list[window.round] + " marble. Please proceed"

    # adding a text to lead them onto a second trial, or save results if the second trial is finished
    if window.round == 0:
        outcome_message += " to start the next round."
    else:
        save_results()      # saving results after the second trial is finished

    window.outcome_text.setText(outcome_message)  # placing text in a pre-defined empty label
    page3_timer_animation()     # enabling animation on the third page


# creating core function to incorporate appropriate text for each condition (2, 10 or 100 marbles)
def page3core():
    if window.round == 0:  # setting the text for the first trial for each of the conditions

        window.mar100 = "Consider the following problem carefully, then make your decision. \n" \
                        "You can see two urns, labeled A and B, both containing red and blue marbles. \n" \
                        "Your task is to draw a marble from one of the urns. \n" \
                        "If you get a BLUE marble, you will win. \n\n" \
                        "" + window.urn_half + " contains 50 red marbles and 50 blue marbles. \n\n" \
                        "" + window.urn_unknown + " contains 100 marbles in an unknown color ratio, " \
                        "from 100 red marbles and 0 blue marbles to 0 red marbles and 100 blue marbles. \n" \
                        "The mixture of red and blue marbles in " + window.urn_unknown + " has been decided by " \
                        "writing the numbers 0, 1, 2,... 100 on separate slips of paper,\nshuffling the slips " \
                        "thoroughly, and then drawing one of them at random. The number chosen was used to determine " \
                        "the number of blue\nmarbles to be put into " + window.urn_unknown + ", but you do not know " \
                        "the number. Every possible mixture of red and blue marbles in " + window.urn_unknown + " " \
                        "is equally likely. \n\nYou have to decide whether you prefer to draw a marble from Urn A " \
                        "or Urn B. \nWhat you hope is to draw a BLUE marble to win. \n\n" \
                        "Consider carefully from which urn you prefer to draw the marble, then click on the urn. "

        window.mar10 = "Consider the following problem carefully, then make your decision. \n" \
                        "You can see two urns, labeled A and B, both containing red and blue marbles. \n" \
                        "Your task is to draw a marble from one of the urns. \n" \
                        "If you get a BLUE marble, you will win. \n\n" \
                        "" + window.urn_half + " contains 5 red marbles and 5 blue marbles. \n\n" \
                        "" + window.urn_unknown + " contains 10 marbles in an unknown color ratio, " \
                        "from 10 red marbles and 0 blue marbles to 0 red marbles and 10 blue marbles. \n" \
                        "The mixture of red and blue marbles in " + window.urn_unknown + " has been decided by " \
                        "writing the numbers 0, 1, 2,... 10 on separate slips of paper,\nshuffling the slips " \
                        "thoroughly, and then drawing one of them at random. The number chosen was used to determine " \
                        "the number of blue\nmarbles to be put into " + window.urn_unknown + ", but you do not know " \
                        "the number. Every possible mixture of red and blue marbles in " + window.urn_unknown + " " \
                        "is equally likely. \n\nYou have to decide whether you prefer to draw a marble from Urn A " \
                        "or Urn B. \nWhat you hope is to draw a BLUE marble to win. \n\n" \
                        "Consider carefully from which urn you prefer to draw the marble, then click on the urn. "

        window.mar2 = "Consider the following problem carefully, then make your decision. \n" \
                        "You can see two urns, labeled A and B, both containing red and blue marbles. \n" \
                        "Your task is to draw a marble from one of the urns. \n" \
                        "If you get a BLUE marble, you will win. \n\n" \
                        "" + window.urn_half + " contains 1 red marble and 1 blue marble. \n\n" \
                        "" + window.urn_unknown + " contains 2 marbles in an unknown color ratio, " \
                        "from 2 red marbles and 0 blue marbles to 0 red marbles and 2 blue marbles. \n" \
                        "The mixture of red and blue marbles in " + window.urn_unknown + " has been decided by " \
                        "writing the numbers 0, 1 and 2 on separate slips of paper,\nshuffling the slips " \
                        "thoroughly, and then drawing one of them at random. The number chosen was used to determine " \
                        "the number of blue\nmarbles to be put into " + window.urn_unknown + ", but you do not know " \
                        "the number. Every possible mixture of red and blue marbles in " + window.urn_unknown + " " \
                        "is equally likely. \n\nYou have to decide whether you prefer to draw a marble from Urn A " \
                        "or Urn B. \nWhat you hope is to draw a BLUE marble to win. \n\n" \
                        "Consider carefully from which urn you prefer to draw the marble, then click on the urn. "

        # connecting clickable label function to the urn picture
        # urn a
        window.urn_a = ClickableLabel(window.page3)
        window.urn_a.setPixmap(QPixmap("urn.png"))
        window.urn_a.setScaledContents(True)
        window.urn_a.setGeometry(297, 420, 170, 203)
        window.urn_a.setEnabled(False)
        window.urn_a.clicked.connect(page3outcomes)

        # urn b
        window.urn_b = ClickableLabel(window.page3)
        window.urn_b.setPixmap(QPixmap("urn.png"))
        window.urn_b.setScaledContents(True)
        window.urn_b.setGeometry(757, 420, 170, 203)
        window.urn_b.setEnabled(False)
        window.urn_b.clicked.connect(page3outcomes)

    else:       # setting the text for the second trial for each of the conditions
        window.mar100 = "Now you need to draw a RED marble.\n\n" \
                        "Bear in mind that the marble you have chosen was re-entered into the urn and the " \
                        "ratios of marbles in both urns are the same as in the first round.\n" \
                        "As was the case in the first round, " + window.urn_half + " contains 50 red " \
                        "marbles and 50 blue marbles, while " + window.urn_unknown + " contains 100 marbles in " \
                        "an unknown color ratio,\nfrom 100 red marbles and 0 blue marbles to 0 red marbles " \
                        "and 100 blue marbles.\n\n" \
                        "Please draw a marble from Urn A or Urn B by clicking on the urn."

        window.mar10 = "Now you need to draw a RED marble.\n\n" \
                        "Bear in mind that the marble you have chosen was re-entered into the urn and the " \
                        "ratios of marbles in both urns are the same as in the first round.\n" \
                        "As was the case in the first round, " + window.urn_half + " contains 5 red " \
                        "marbles and 5 blue marbles, while " + window.urn_unknown + " contains 10 marbles in " \
                        "an unknown color ratio,\nfrom 10 red marbles and 0 blue marbles to 0 red marbles " \
                        "and 10 blue marbles.\n\n" \
                        "Please draw a marble from Urn A or Urn B by clicking on the urn."

        window.mar2 = "Now you need to draw a RED marble.\n\n" \
                      "Bear in mind that the marble you have chosen was re-entered into the urn and the " \
                      "ratios of marbles in both urns are the same as in the first round.\n" \
                      "As was the case in the first round, " + window.urn_half + " contains 1 red " \
                      "marble and 1 blue marble, while " + window.urn_unknown + " contains 2 marbles in " \
                      "an unknown color ratio,\nfrom 2 red marbles and 0 blue marbles to 0 red marbles " \
                      "and 2 blue marbles.\n\n" \
                      "Please draw a marble from Urn A or Urn B by clicking on the urn."

        # putting marbles back in the starting position
        window.urn_a_blue.setGeometry(360, 500, 50, 50)
        window.urn_a_red.setGeometry(360, 500, 50, 50)
        window.urn_b_blue.setGeometry(819, 500, 50, 50)
        window.urn_b_red.setGeometry(819, 500, 50, 50)
        page3timer()    # enabling timer function

    # setting text based on the condition and saving new condition variable for exporting
    if window.condition == 0:
        window.instructions.setText(window.mar100)
        window.condition_var = 100
    elif window.condition == 1:
        window.instructions.setText(window.mar10)
        window.condition_var = 10
    elif window.condition == 2:
        window.instructions.setText(window.mar2)
        window.condition_var = 2

    window.outcome.hide()  # hiding outcome message until participant clicks on the urn


# Page 3 (Timer)

# setting up the timer to not enable participants to click on urns before reading instructions
def page3_timer_act():
    window.default += 1
    if window.default == 5:  # setting a short timer to enable participants to read instructions
        window.page3timer.stop()
        window.urn_a.setEnabled(True)
        window.urn_b.setEnabled(True)


# setting up timer for the third page
def page3timer():
    window.page3timer = QTimer()
    window.default = 0
    window.page3timer.start(1000)
    window.page3timer.timeout.connect(page3_timer_act)


# Page 3 (animation)

# function to animate marbles going out of the urns
def page3animation():
    if window.urn_list[window.round] == "B":                # setting for an urn b
        if window.marble_list[window.round] == "blue":      # setting for a blue marble
            y_axis = window.urn_b_blue.y()
            if window.urn_b_blue.y() > 350:
                window.urn_b_blue.setGeometry(819, y_axis - 10, 50, 50)
            else:
                window.timer_animation.stop()
                window.outcome.show()

        else:                                               # setting for a red marble
            y_axis = window.urn_b_red.y()
            if window.urn_b_red.y() > 350:
                window.urn_b_red.setGeometry(819, y_axis - 10, 50, 50)
            else:
                window.timer_animation.stop()
                window.outcome.show()
    else:                                                   # setting for an urn a
        if window.marble_list[window.round] == "blue":      # setting for a blue marble
            y_axis = window.urn_a_blue.y()
            if window.urn_a_blue.y() > 350:
                window.urn_a_blue.setGeometry(360, y_axis - 10, 50, 50)
            else:
                window.timer_animation.stop()
                window.outcome.show()
        else:                                               # setting for a red marble
            y_axis = window.urn_a_red.y()
            if window.urn_a_red.y() > 350:
                window.urn_a_red.setGeometry(360, y_axis - 10, 50, 50)
            else:
                window.timer_animation.stop()
                window.outcome.show()


# function for an animation timer
def page3_timer_animation():
    window.timer_animation = QTimer()
    window.timer_animation.timeout.connect(page3animation)
    window.timer_animation.start(35)


# Page 3 (continue and debrief)

# function to go from first to second trial, or from second trial to debrief page
def page3continue():
    if window.round == 0:
        window.round += 1
        page3core()
    else:
        window.frame.setCurrentIndex(3)


window.proceed_p3.clicked.connect(page3continue)    # initialising function to continue
window.finish.clicked.connect(QApplication.quit)    # connecting finish button on debrief page with quit function

# calling functions from third page necessary for execution of the program
new_dataset()
page3positions()
page3core()


window.show()
app.exec_()
