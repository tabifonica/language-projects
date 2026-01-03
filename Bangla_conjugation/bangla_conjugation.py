import csv, dataclass

from pyscript.web import page, when

ENDINGS = {
    "PRES": {
        "1": "i",
        "2_inf": "o",
        "2_fam": "is",
        "3": "e",
        "23_form": "en",
    },
    "PAST": {
        "1": "lam",
        "2_inf": "le",
        "2_fam": "li",
        "3": "lo",
        "23_form": "len",
    },
    "FUT": {
        "1": "bo",
        "2_inf": "be",
        "2_fam": "bi",
        "3": "be",
        "23_form": "ben",
    },
    "HAB": {
        "1": "i",
        "2_inf": "o",
        "2_fam": "is",
        "3": "e",
        "23_form": "en"
    }
}

def make_ready():
    """
    When the page loads, hide the loading text and show the content
    """
    loadingbox = page["#loadingbox"]
    loadingbox.classes.add("loaded")

    vertical = page["#vertical"]
    vertical.classes.remove("loading")

class Verb():
    """
    An object that represents a verb from Bangla with all of its conjugations
    """
    def __init__(self, verbal_noun, English):
        self.verbal_noun = verbal_noun
        self.root = verbal_noun[:-1]
        self.english = English
        self.forms = self._conjugate(self.root)

    def _conjugate(self, root):
        forms = {}
        for tense in ENDINGS:
            endings = {}
            for ending in tense:
                endings[ending] = root + ending
            forms[tense] = endings
        return forms

def load_verbs(filename):
    """
    Loads a csv with verbs and returns a list of Verb objects
    """
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        verbs = list(reader)

    verb_list = []
    for verb in verbs:
        verb_list.append(Verb(verb[0], verb[1]))
    return verbs

# ON PAGE LOAD
make_ready() # hide loading, show content
verbs = load_verbs("bangla_verbs.csv")
