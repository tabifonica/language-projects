import random

import numpy as np

# Map phonetic values to ints
PLACE = {
    "ParamIndex": 1,
    "Velar": 0,
    "Postalveolar": 1,
    "Alveolar": 2,
    "Labial": 3
}
GLOTTAL = {
    "ParamIndex": 2,
    "Tenuis": 0,
    "Aspirated": 1,
    "Voiced": 2
}
MANNER = {
    "ParamIndex": 3,
    "Stop": 0,
    "Affricate": 1,
    "Nasal": 2
}
PARAMS = [PLACE, GLOTTAL, MANNER]

def lookup_param(field):
    """
    Get param from only a field
    """
    for param in PARAMS:
        if field in param:
            return param
    raise ValueError

class KhmerAlphabet():
    """
    A class that stores representations of the Khmer alphabet, with codepoints and features,
    and can select letters from it for phonetics games.
    """
    def __init__(self):
        """
        Populate the Khmer consonants, annotates them with their features.
        """
        self.K = np.zeros((25, 4), dtype=int) # shape of the Khmer alphabet
        row = 0                         # row of the Khmer alphabet
        for i in range(25):
            col = i % 5                 # column of the Khmer alphabet

            # get codepoint
            cp = 0x1780 + i

            # account for 'retroflex' letters being alveolar
            place = PLACE["Alveolar"] if row == 2 else row

            # annotate letters with glottal articulation (aspiration or voice)
            if col in [1, 3]:
                h = GLOTTAL["Aspirated"]
            elif col == 4 or (col in [0, 2] and row == 2) or (col == 0 and row == 4):
                h = GLOTTAL["Voiced"]
            else:
                h = GLOTTAL["Tenuis"]

            # annotate letters with manner of articulation
            if col == 4:
                manner = MANNER["Nasal"]
            elif row == 1:
                manner = MANNER["Affricate"]
            else:
                manner = MANNER["Stop"]

            # populate the numpy array with codepoint and annotations
            self.K[i] = (cp, place, h, manner)

            # increment the row of the letter
            if col == 4:
                row += 1

    def choose(self, field: str):
        """
        Selects options from the Khmer alphabet
        """
        param = lookup_param(field)
        value = param[field]

        # selects range of possibilities according to the game type
        K1 = self.K[self.K[:, param["ParamIndex"]] != value]
        K2 = self.K[self.K[:, param["ParamIndex"]] == value]

        # randomly select two letters from the same place of articulation
        k2 = random.choice(K2)
        alpha_pl = K1[K1[:, 1] == k2[1]]
        k1 = random.choice(alpha_pl)

        return [k1[0], k2[0]]
