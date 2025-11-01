import random, time
from enum import IntEnum

from pyscript.web import page, when

from alphabet import KhmerAlphabet

class Correctness(IntEnum):
    """
    Map correctness values to int
    """
    Incorrect = 0
    Correct = 1

def make_ready():
    """
    When the page loads, hide the loading text and show the content
    """
    loadingbox = page["#loadingbox"]
    loadingbox.classes.add("loaded")

    vertical = page["#vertical"]
    vertical.classes.remove("loading")

def set_options():
    """
    Select two letters from the Khmer alphabet for the option buttons
    """
    # get the buttons
    option1 = page["#option1"]
    option2 = page["#option2"]

    # select random choices for the buttons
    choices = A.choose("Aspirated")
    flip = [Correctness.Incorrect, Correctness.Correct] # choices[1] is correct, before shuffling
    random.shuffle(flip)

    # display unicode codepoint
    option1.innerText = chr(choices[flip[0].value])
    option2.innerText = chr(choices[flip[1].value])

    # Add "Correct" or "Incorrect" class names
    option1.classes.add(flip[0].name)
    option2.classes.add(flip[1].name)

def submit(event):
    """
    When on of the option buttons is clicked
    """
    # get button
    button = event.target
    button = page[f"#{button.id}"]

    # if button has been clickd before, do nothing
    if "unclickable" in button.classes:
        print("Button unclickable")
        return

    # get other button
    if button.id[0] == "option1":
        other_button_id = "option2"
    else:
        other_button_id = "option1"
    other_button = page[f"#{other_button_id}"]

    # make both buttons unclickable
    button.classes.add("unclickable")
    other_button.classes.add("unclickable")

    # get button's "Correct" or "Incorrect" class
    mark = page["#mark"]
    if "Correct" in button.classes:
        correctness = "Correct"
    else:
        correctness = "Incorrect"

    # display mark
    mark.classes.add(correctness) # add class for CSS
    mark.innerHTML = f"{correctness}!"
    print("Mark:", correctness)

    # display next
    nextbox = page["#nextbox"]
    if "hidden" in nextbox.classes:
        nextbox.classes.remove("hidden")

def reset(event):
    """
    Show the next question
    """
    button = event.target
    print("Button clicked:", button.id)

    # hide mark
    mark = page["#mark"]
    mark.innerHTML = ""

    # hide nextbox
    nextbox = page["#nextbox"]
    nextbox.classes.add("hidden")

    # clear classes
    option1 = page["#option1"]
    option2 = page["#option2"]
    option1.classList = ""
    option2.classList = ""
    mark.classList = ""

    # choose a new set of options
    set_options()

# ON PAGE LOAD
A = KhmerAlphabet() # load the Khmer alphabet once
make_ready() # hide loading, show content
set_options() # set the option buttons
