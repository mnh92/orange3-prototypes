import numpy as np
import pyqtgraph as pg
import re
import math
import itertools

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
        self.alphabet = []

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
        self.imview.ui.histogram.setEnabled(False)
        self.imview.ui.menuBtn.hide()
        self.imview.ui.roiBtn.hide()

        self.mainArea.layout().addWidget(self.imview)
        self.plot_cgr()

    def __get_kmer_length_selected(self):
        return KMER_LENGTHS[self.kmer_length_idx][1]

    def __update_kmer_table(self):
        size = int(math.sqrt(4 ** self.kmer_length))
        self.kmers = {}
        all_kmers = [''.join(c) for c in \
                     itertools.product(self.alphabet, repeat=self.kmer_length)]

        for kmer in all_kmers:
            x_max = size
            y_max = size
            x_pos = 0
            y_pos = 0
            for c in kmer:
                if c == 'G':
                    x_pos += x_max / 2
                elif c == 'C':
                    y_pos += y_max / 2
                elif c == 'T' or c == 'U':
                    x_pos += x_max / 2
                    y_pos += y_max / 2
                x_max /= 2
                y_max /= 2
            self.kmers[int(x_pos), int(y_pos)] = kmer

    def set_data(self, data):
        typerr_msg = 'Invalid data type! This widget is expecting strings.'
        warn_msg = ''
        self.error()
        self.warning()
        self.imview.clear()

        # data type checking.
        seq = ''
        if data == None:
            self.sequence = None
        elif any(type(d.list[0]) != str for d in data):
            self.error(typerr_msg)
            self.sequence = None
        else:
            for d in data:
                if d.list[0][0] == ';':
                    continue
                else:
                    seq += d.list[0]

            # Determine if string is RNA or DNA.
            n_u = seq.count('U')
            n_t = seq.count('T')

            is_dna = n_t >= n_u
            self.alphabet = ['A', 'C', 'G', 'T'] if is_dna else ['A', 'C', 'G', 'U']

            if n_u != 0 and n_t != 0:
                seq_type = " DNA" if is_dna else "n RNA"
                warn_msg += "Sequence is ambiguous! Assuming it's a%s sequence. " % seq_type

            alpha_re = r'[^ACGT]' if is_dna else r'[^ACGU]'
            seq = re.sub(r'\s+', '', seq, flags=re.UNICODE)
            oldseq = seq
            seq = re.sub(alpha_re, '', seq)
            if len(oldseq) != len(seq):
                warn_msg += 'Removed invalid characters from data!'

            self.sequence = seq

        self.warning(warn_msg)
        self.plot_cgr()

    def __cgr(self):
        if self.scoring_idx == 0:
            probabilities = chaosgame.raw_count(self.sequence, self.kmer_length)
        elif self.scoring_idx == 1:
            probabilities = chaosgame.probabilities(self.sequence, self.kmer_length)
        else:
            probabilities = chaosgame.log_odds(self.sequence, self.kmer_length)

        return chaosgame.cgr(probabilities, self.kmer_length, log=self.scoring_idx == 2)

    def __mouse_moved(self, viewPos):
        if self.sequence is None:
            return
        data = self.imview.image
        nRows, nCols = data.shape
        scenePos = self.imview.getImageItem().mapFromScene(viewPos)
        row, col = int(scenePos.x()), int(scenePos.y())

        if (0 <= scenePos.x() < nRows) and (0 <= scenePos.y() < nCols):
            value = data[row, col]
            if self.scoring_idx == 0:
                valuestr = "%d" % value
            else:
                valuestr = "%.5f" % value if value > -1e100 else "-Inf"
            self.infoa.setText("k-mer coord: (%d, %d)\n\nK-mer: %s\n\nValue: %s" % (col, row, self.kmers[row, col], valuestr))
        else:
            self.infoa.setText("Hover over image\nto get k-mer value.")

    def plot_cgr(self):
        if self.sequence is None:
            return
        self.imview.clear()
        self.__update_kmer_table()
        chaos = self.__cgr()
        self.imview.setImage(chaos)
        self.imview.scene.sigMouseMoved.connect(self.__mouse_moved)
