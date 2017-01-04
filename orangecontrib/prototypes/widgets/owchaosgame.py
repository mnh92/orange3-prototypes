import numpy as np
import pyqtgraph as pg

from ..chaos import chaosgame

from PyQt4.QtCore import Qt
from Orange.data import Table
from Orange.widgets import widget, gui, settings


KMER_LENGTHS = (
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6)
)

SCORINGS = (
    ('raw count', 0),
    ('probability', 1),
    ('log odds', 2)
)

class OWChaosGame(widget.OWWidget):
    name = "Chaos Game"
    description = ""
    icon = ""
    priority = 9999

    inputs = [("Sequence", Table, "set_data")]
    outputs = []

    kmer_length = settings.Setting(KMER_LENGTHS[0][1])
    scoring = settings.Setting(SCORINGS[0][1])

    def __init__(self):
        super().__init__()

        self.controlBox = gui.widgetBox(self.controlArea, 'Controls')
        self.sequence = None
        self.chaos = np.zeros

        def _on_kmer_length_changed():
            self.__cgr()

        gui.comboBox(self.controlBox, self, 'kmer_length',
             orientation=Qt.Horizontal,
             label='Kmer length:',
             items=[i[0] for i in KMER_LENGTHS],
             callback=_on_kmer_length_changed)

        def _on_scoring_changed():
            self.plot_cgr()

        gui.comboBox(self.controlBox, self, 'scoring',
             orientation=Qt.Horizontal,
             label='Scoring:',
             items=[i[0] for i in SCORINGS],
             callback=_on_scoring_changed)

        self.imview = pg.ImageView()

        colors = [
            (255, 255, 255),
            (0, 0, 0)
        ]

        colormap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 2), color=colors)
        self.imview.setColorMap(colormap)

        self.mainArea.layout().addWidget(self.imview)
        self.plot_cgr()

    def set_data(self, data):
        self.imview.clear()
        self.sequence = ''.join([d.list[0] for d in data])
        self.plot_cgr()

    def __cgr(self):
        if self.scoring == 0:
            probabilities = chaosgame.raw_count(self.sequence, self.kmer_length)
        elif self.scoring == 1:
            probabilities = chaosgame.probabilities(self.sequence, self.kmer_length)
        else:
            probabilities = chaosgame.log_odds(self.sequence, self.kmer_length)

        chaos = chaosgame.cgr(probabilities, self.kmer_length)
        return chaos

    def plot_cgr(self):
        if self.sequence is None:
            return
        self.imview.clear()
        chaos = self.__cgr()
        self.imview.setImage(chaos)
