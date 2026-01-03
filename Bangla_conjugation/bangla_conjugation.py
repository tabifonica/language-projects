import csv, os

from pyscript.web import page, when

ENDINGS = {
    "PRES": {
        "1": "ি",
        "2_inf": "ো",
        "2_fam": "িস",
        "3": "ে",
        "23_form": "েন",
    },
    "PAST": {
        "1": "লাম",
        "2_inf": "লে",
        "2_fam": "লি",
        "3": "লো", # explicit inherent vowel
        "23_form": "লেন",
    },
    "FUT": {
        "1": "বো", # explicit inherent vowel
        "2_inf": "বে",
        "2_fam": "বি",
        "3": "বে",
        "23_form": "বেন",
    },
    "HAB": {
        "1": "তাম",
        "2_inf": "তে",
        "2_fam": "তি",
        "3": "তো", # explicit inherent vowel
        "23_form": "তেন",
    },
}
ASPECTS = {
    "PRES": {
        "PRES_CONT": "ছ",
        "PRES_PERF": "েছ"
    },
    "PAST": {
        "PAST_CONT": "ছি",
        "PAST_PERF": "েছি"
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

def load_verbs(filename):
    """
    Loads a csv with verbs and returns a list of dictionaries, including verb conjugations
    """
    print(os.listdir(os.path.dirname(filename)))
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        verbs = list(reader)

    verb_list = []
    for verb in verbs:
        conjugations = conjugate(verb["root"])
        verb_list.append(verb | conjugations)
    return verb_list

def conjugate(root):
    """
    Take a verb root, and return a dictionary containing all the conjugations
    """
    forms = {}
    for tense_name, endings in ENDINGS.items():
        person_forms = {}
        for person_name, ending in endings.items():
            person_forms[person_name] = root + ending
        forms[tense_name] = person_forms

        # add aspects
        if tense_name in ASPECTS:
            for aspect_name, aspect_suffix in ASPECTS[tense_name].items():
                person_forms = {}
                for person_name, ending in endings.items():
                    person_forms[person_name] = root + aspect_suffix + ending
                forms[aspect_name] = person_forms

    return forms

# ON PAGE LOAD
make_ready() # hide loading, show content
verbs = load_verbs("./bangla_verbs.csv")
for verb in verbs:
    print(verb)
