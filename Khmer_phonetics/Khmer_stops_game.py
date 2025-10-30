import random
import time

import numpy
import ipywidgets as widgets
from IPython.display import HTML, display
from pyscript import display as pydisplay

class FlashCardGame():
  def __init__(self, option="aspirated", same_place=True, debug=False):
    self.debug = debug
    self.same_place = same_place

    options = ["plain", "aspirated", "voiced", "nasal", "voiced stop", "affricate"]
    inv_options = {"unaspirated": 1, "voiceless": 2, "obstruent": 3}
    if option in options:
      self.inverse = False
      self.test = options.index(option)
    elif option in inv_options:
      self.inverse = True
      self.test = inv_options[option]
    else:
      raise ValueError(f"Option {option} not recognised")
    self.option = option

    # affricates can only occur in postalveolar place
    if option == "affricate":
      self.same_place = False

    if self.debug: print(self.test)

    # initialise empty widgets
    self.q = widgets.HTML()

    choice_layout = widgets.Layout(width="120px", height="80px")
    self.b1 = widgets.Button(layout=choice_layout)
    self.b1._dom_classes = ["choice"]
    self.b1.b_id = 1
    self.b1.on_click(self.submit)
    self.b1.clickable = False # don't make clickable until question is set up

    self.b2 = widgets.Button(layout=choice_layout)
    self.b2._dom_classes = ["choice"]
    self.b2.b_id = 2
    self.b2.on_click(self.submit)
    self.b1.clickable = False # don't make clickable until question is set up

    self.mark = widgets.HTML()

    self.b_reset = widgets.Button(description="Reset",
      layout=widgets.Layout(display='none')) # hide it
    self.b_reset.style.font_size = "10px !important;"
    self.b_reset._dom_classes = ["reset"]
    self.b_reset.on_click(self.reset)
    self.b_reset.clickable = False # don't make clickable until quesiton is answered

    # unfortunately the style.font_size attribute of buttons doesn't seem to work
    # so I need to use CSS below
    display(HTML("""
    <style>
    .choice {
        font-size: 40px !important;
        color: white !important;
    }
    .reset {
        font-size: 20px !important;
    }
    </style>
    """))

    # Set up flip attribute
    self.f = None

    # lay out the widgets
    choices = widgets.HBox([self.b1, self.b2], layout=widgets.Layout(justify_content="center"))
    box = widgets.VBox(
      [self.q, choices, self.mark, self.b_reset],
      layout=widgets.Layout(align_items="center"))
    pydisplay(box, target="app")

    self.play()


  def get_choices(self):
    K = numpy.zeros((25, 4), dtype=int)
    Ki = 0
    r = 0
    for i in range(25):
      cp = 0x1780 + i

      pl = 3 if r == 2 else r

      if i % 5 in [1, 3]:
        h = 1
      elif i % 5 == 4 or (i % 5 in [0, 2] and r == 2) or (i % 5 == 0 and r == 4):
        h = 2
      else:
        h = 0

      if i % 5 == 4:
        m = 2
      elif r == 1:
        m = 1
      else:
        m = 0

      K[Ki] = (cp, pl, h, m)
      Ki += 1

      if i % 5 == 4:
        r += 1

    match self.test:
      case 5:
        K1 = K[K[:, 3] != 1]
        K2 = K[K[:, 3] == 1]
      case 4:
        K1 = K[(K[:, 2] != 2) | (K[:, 3] != 0)]
        K2 = K[(K[:, 2] == 2) & (K[:, 3] == 0)]
      case 3:
        K1 = K[K[:, 3] != 2]
        K2 = K[K[:, 3] == 2]
      case _:
        K1 = K[K[:, 2] != self.test]
        K2 = K[K[:, 2] == self.test]

    k2 = random.choice(K2)
    if self.debug: print(f"k2: {chr(k2[0])}")

    if self.same_place:
      alpha_pl = K1[K1[:, 1] == k2[1]]
      if self.debug: print(f"alpha_pl: {', '.join(chr(c) for c in alpha_pl[:,0])}")
      k1 = random.choice(alpha_pl)
    else:
      if self.debug: print(f"K1 cands: {', '.join(chr(c) for c in K1[:,0])}")
      k1 = random.choice(K1)

    if self.debug: print(f"k1: {chr(k1[0])}")
    return [k1[0], k2[0]] if not self.inverse else [k2[0], k1[0]]


  def play(self):
    # Get question
    if self.option == "plain":
      sound_name = "a plain (voiceless unaspirated) sound"
    elif self.option[0] in ["a", "e", "i", "o", "u"]:
      sound_name = f"an {self.option} sound"
    else:
      sound_name = f"a {self.option} sound"
    self.q.value = f"<h1>Which of these Khmer letters represents {sound_name}?</h1>"

    # Get chocies
    a = self.get_choices()
    self.f = random.randint(0,1)
    self.b1.description = chr(a[self.f])
    self.b2.description = chr(a[(self.f+1)%2])

    # set the buttons to a random colour
    colours = ["purple", "blue", "red", "green", "brown", "gray", "magenta", "orange", "teal", "black", "navy"]
    colour1 = random.choice(colours)
    self.b1.style.button_color = colour1
    colours.remove(colour1) # remove existing colour so the buttons don't have the same colours
    self.b2.style.button_color = random.choice(colours)

    # make buttons clickable
    self.b1.clickable = True
    self.b2.clickable = True


  def submit(self, b):
    results = (("Correct!", "green"), ("Incorrect!", "red"))
    res = results[(b.b_id + self.f)%2]
    if b.clickable is True:
      self.mark.value = f"<h2 style='color:{res[1]};'> {res[0]} </h2>"

      # freeze these buttons
      self.b1.clickable = False
      self.b2.clickable = False

      # show reset button
      time.sleep(1)
      self.b_reset.clickable = True
      self.b_reset.layout = widgets.Layout()


  def reset(self, b):
    if b.clickable is True:
      b.clickable = False
      self.mark.value = ""
      self.b_reset.layout = widgets.Layout(display="none")
      self.play()

FlashCardGame(option = "nasal")
