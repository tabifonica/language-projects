from pyscript import document

from Khmer_phonetics.alphabet import KhmerAlphabet

def main():
    """
    The main function, that runs when the page is loaded
    """
    # populate the Khmer alphabet once
    A = KhmerAlphabet()

    option1 = document.querySelector("#option1")
    option2 = document.querySelector("#option2")

    # select random choices for the buttons
    choices = A.choose(param=2, value=1)
    option1.innerText = chr(choices[0]) # display unicode codepoint
    option2.innerText = chr(choices[1])


# when the page is loaded, call the main function
main()
