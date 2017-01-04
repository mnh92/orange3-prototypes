import numpy as np

from PyQt4.QtCore import Qt
from Orange.data import Table
from Orange.widgets import widget, gui, settings
from ..chaos import chaosgame

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

if __name__ == '__main__':
    class OWChaosGame(widget.OWWidget):
        name = "Chaos Game"
        description = ""
        icon = ""
        priority = 9999

        inputs = [("Sequence", Table, "set_data")]
        outputs = []

        #kmer_length = settings.Setting(KMER_LENGTHS[0][1])
        #scoring = settings.Setting(SCORINGS[0][1])
        kmer_length = 2
        scoring = 0
        chaos = np.empty

        def __init__(self):
            super().__init__()

            self.controlBox = gui.widgetBox(self.controlArea, 'Controls')
            self.sequence = None

            def _on_kmer_length_changed():
                pass

            gui.comboBox(self.controlBox, self, 'kmer_length',
                         orientation=Qt.Horizontal,
                         label='Kmer length:',
                         items=[i[0] for i in KMER_LENGTHS],
                         callback=_on_kmer_length_changed)

            def _on_scoring_changed():
                pass

            gui.comboBox(self.controlBox, self, 'scoring',
                         orientation=Qt.Horizontal,
                         label='Scoring:',
                         items=[i[0] for i in SCORINGS],
                         callback=_on_scoring_changed())

        def set_data(self, data):
            self.sequence = ''.join([d.list[0] for d in data])
            self.cgr()

        def cgr(self):
            #TODO: switch for probabilities, log-odds..
            probabilities = chaosgame.raw_count(self.sequence, self.kmer_length)

            self.chaos = chaosgame.cgr(probabilities, self.kmer_length)
