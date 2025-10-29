import random
from enum import IntEnum

from pyscript.web import page, when

from alphabet import KhmerAlphabet

class Correctness(IntEnum):
    """
    Map correctness values to int
    """
    Incorrect = 0
    Correct = 1

def set_options():
    """
    Select two letters from the Khmer alphabet for the option buttons
    """
    # get the buttons
    option1 = page["#option1"]
    option2 = page["#option2"]

    # select random choices for the buttons
    choices = A.choose(param=2, value=1)
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
    # get button's "Correct" or "Incorrect" class
    button = event.target
    print("Button clicked", button.id)
    correctness = button.classList

    # display mark
    mark = page["#mark"]
    mark.classList = "" # remove existing classes
    mark.classes.add(correctness) # add class for CSS
    mark.innerHTML = f"{correctness}!"
    print("Mark:", correctness)

# ON PAGE LOAD
A = KhmerAlphabet() # load the Khmer alphabet once
set_options() # set the option buttons
