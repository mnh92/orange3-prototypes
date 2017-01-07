import numpy as np
import pyqtgraph as pg
import re

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
    description = "Visualize genome data with the Chaos Game Representation."
    icon = "icons/Chaosgame.svg"
    priority = 9999

    inputs = [("Sequence", Table, "set_data")]
    outputs = []

    kmer_length_idx = settings.Setting(0)
    scoring_idx = settings.Setting(0)

    def __init__(self):
        super().__init__()

        self.kmers = {}

        self.kmer_length = self.__get_kmer_length_selected()

        self.controlBox = gui.widgetBox(self.controlArea, 'Controls')
        self.sequence = None

        self.box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(self.box, 'Hover over image\nto get k-mer value.')

        def _on_kmer_length_changed():
            self.kmer_length = self.__get_kmer_length_selected()
            self.plot_cgr()

        gui.comboBox(self.controlBox, self, 'kmer_length_idx',
             orientation=Qt.Horizontal,
             label='k-mer length:',
             items=[i[0] for i in KMER_LENGTHS],
             callback=_on_kmer_length_changed)

        def _on_scoring_changed():
            self.plot_cgr()

        gui.comboBox(self.controlBox, self, 'scoring_idx',
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

    def __get_kmer_length_selected(self):
        return KMER_LENGTHS[self.kmer_length_idx][1]

    def set_data(self, data):
        typerrmsg = 'Invalid data type! This widget is expecting strings.'
        self.error()
        self.warning()
        self.imview.clear()

        # data type checking.
        seq = ''
        if data == None:
            self.sequence = None
        elif any(type(d.list[0]) != str for d in data):
            self.error(typerrmsg)
            self.sequence = None
        else:
            for d in data:
                if d.list[0][0] == ';':
                    continue
                else:
                    seq += d.list[0]

            seq = re.sub(r'\s+', '', seq, flags = re.UNICODE)
            oldseq = seq
            seq = re.sub(r'[^ACGT]', '', seq)
            if len(oldseq) != len(seq):
                self.warning('Removed invalid characters from data! Only A, C, G and T allowed!')

        self.sequence = seq
        self.plot_cgr()

    def __cgr(self):
        if self.scoring_idx == 0:
            probabilities = chaosgame.raw_count(self.sequence, self.kmer_length)
        elif self.scoring_idx == 1:
            probabilities = chaosgame.probabilities(self.sequence, self.kmer_length)
        else:
            probabilities = chaosgame.log_odds(self.sequence, self.kmer_length)

        return chaosgame.cgr(probabilities, self.kmer_length)

    def plot_cgr(self):
        if self.sequence is None:
            return
        self.imview.clear()
        chaos, self.kmers = self.__cgr()
        self.imview.setImage(chaos)
        self.imview.scene.sigMouseMoved.connect(self.mouseMoved)

    def mouseMoved(self, viewPos):
        data = self.imview.image
        nRows, nCols = data.shape
        scenePos = self.imview.getImageItem().mapFromScene(viewPos)
        row, col = int(scenePos.x()), int(scenePos.y())

        if (0 <= row < nRows) and (0 <= col < nCols):
            value = data[row, col]
            if self.scoring_idx == 0:
                valuestr = "%d" % value
            else:
                valuestr = "%.5f" % value
            self.infoa.setText("k-mer coord: (%d, %d)\n\nK-mer: %s\n\nValue: %s" % (col, row, self.kmers[row, col], valuestr))
        else:
            self.infoa.setText("Hover over image\nto get k-mer value.")
