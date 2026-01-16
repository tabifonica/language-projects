https://github.com/tabifonica/language-projects 
A repository for projects to assist with language learning. Currently I have made one project.
# Khmer Phonetics Game
A simple quiz, in which the user is shown two letters from the Khmer alphabet, and needs to choose the aspirated one. If you are unfamiliar with the Khmer alphabet, and are familiar with the International Phonetic Alphabet (IPA), the Wikipedia page can be used for reference: https://en.wikipedia.org/wiki/Khmer_script (scroll down to the table, and check the "IPA" column. Aspirated consonants will include a little "ʰ" in their IPA transcription, such as [kʰ], [cʰ], [tʰ], [pʰ])

**SEE THIS PROJECT LIVE AT:** https://tabifonica.github.io/language-projects/
## Framework
The PyScript (Python for front-end) framework is used, to leverage numpy vectors within a single front-end application that can be hosted on GitHub Pages.
## Structure
- **Khmer_phonetics/alphabet.py** - A class that populates a numpy 2D vector with Khmer consonant Unicode codepoints, along with information about their phonetic features. The **choose** method, allows consonants to be randomly selected based on certain features (in this case, aspiration or lack thereof).
- **Khmer_phonetics/Khmer_stops_game_pyscript.py** - functions that manage the front-end buttons, and that call the KhmerAlphabet class.
## Future Developments
- Options to quiz more phonetic features, such as voice, place of articulation and manner of articulation. These are already encoded into the Khmer alphabet numpy vector.
