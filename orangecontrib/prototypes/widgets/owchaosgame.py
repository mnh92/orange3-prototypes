import numpy as np
import pyqtgraph as pg

from ..chaos import chaosgame

from PyQt4.QtCore import Qt
from Orange.data import Table
from Orange.widgets import widget, gui, settings


class KmerLengths:
    two, three, four, five, six = range(5)


class Scorings:
    raw_count, probability, log_odds = range(3)


class OWChaosGame(widget.OWWidget):
    name = "Chaos Game"
    description = ""
    icon = ""
    priority = 9999

    inputs = [("Sequence", Table, "set_data")]
    outputs = []

    #kmer_length = settings.Setting(2)
    scoring = settings.Setting(0)

    kmer_length = 2

    def __init__(self):
        super().__init__()

        self.controlBox = gui.widgetBox(self.controlArea, 'Controls')
        self.sequence = None
        self.chaos = np.zeros

        def _on_kmer_length_changed():
                pass

        """
        gui.comboBox(self.controlBox, self, 'kmer_length',
                     orientation=Qt.Horizontal,
                     label='Kmer length:',
                     items=[i[0] for i in KmerLengths],
                     callback=_on_kmer_length_changed)
        """

        def _on_scoring_changed():
            pass

        """
        gui.comboBox(self.controlBox, self, 'scoring',
                     orientation=Qt.Horizontal,
                     label='Scoring:',
                     items=[i[0] for i in Scorings],
                     callback=_on_scoring_changed())
        """

        self.imview = pg.ImageView()

        colors = [
            (255, 255, 255),
            (0, 0, 0)
        ]

        colormap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 2), color=colors)
        self.imview.setColorMap(colormap)

        self.mainArea.layout().addWidget(self.imview)

    def set_data(self, data):
        self.imview.clear()
        self.sequence = ''.join([d.list[0] for d in data])

        self.plot_cgr()

    def __cgr(self):
        #TODO: switch for probabilities, log-odds..
        probabilities = chaosgame.raw_count(self.sequence, self.kmer_length)
        chaos = chaosgame.cgr(probabilities, self.kmer_length)
        return chaos

    def plot_cgr(self):
        chaos = self.__cgr()
        self.imview.setImage(chaos)
