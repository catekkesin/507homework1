import sys
import re
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QTextEdit,
    QMessageBox,
    QScrollArea,
    QComboBox,
    QSplitter,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AlphabetMappingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alphabet Mapping and Frequency Analysis")
        self.selected_alphabet = "English"  # Default alphabet
        self.mappings = {}  # Stores the mappings
        self.external_frequencies = None  # Stores external frequencies
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        right_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)

        left_layout.addWidget(self.scroll_area)

        load_file_button = QPushButton("Load Text File")
        load_file_button.clicked.connect(self.load_text_file)
        right_layout.addWidget(load_file_button)

        load_freq_button = QPushButton("Load External Frequency File")
        load_freq_button.clicked.connect(self.load_frequency_file)
        right_layout.addWidget(load_freq_button)

        alphabet_selection_layout = QHBoxLayout()
        alphabet_selection_label = QLabel("Select Alphabet:")
        alphabet_selection_layout.addWidget(alphabet_selection_label)
        self.alphabet_combo = QComboBox()
        self.alphabet_combo.addItems(["English", "Turkish"])
        self.alphabet_combo.currentTextChanged.connect(self.change_alphabet)
        alphabet_selection_layout.addWidget(self.alphabet_combo)
        right_layout.addLayout(alphabet_selection_layout)

        self.original_text_edit = QTextEdit()
        self.original_text_edit.setReadOnly(True)
        self.original_text_edit.setPlaceholderText("Original Text")
        self.original_text_edit.setMinimumHeight(200)
        text_font = QFont()
        text_font.setPointSize(12)  # Adjust font size as desired
        self.original_text_edit.setFont(text_font)
        right_layout.addWidget(self.original_text_edit)

        self.processed_text_edit = QTextEdit()
        self.processed_text_edit.setReadOnly(True)
        self.processed_text_edit.setPlaceholderText("Processed Text")
        self.processed_text_edit.setMinimumHeight(200)
        self.processed_text_edit.setFont(text_font)
        right_layout.addWidget(self.processed_text_edit)

        self.graph_splitter = QSplitter(Qt.Vertical)

        self.figure_text_freq = Figure(figsize=(6, 4))
        self.canvas_text_freq = FigureCanvas(self.figure_text_freq)
        self.figure_external_freq = Figure(figsize=(6, 4))
        self.canvas_external_freq = FigureCanvas(self.figure_external_freq)

        self.graph_splitter.addWidget(self.canvas_text_freq)
        self.graph_splitter.addWidget(self.canvas_external_freq)

        self.graph_splitter.setSizes([300, 300])

        right_layout.addWidget(self.graph_splitter)

        self.main_layout.addLayout(left_layout)
        self.main_layout.addLayout(right_layout)

        self.setLayout(self.main_layout)

        self.update_alphabet()

    def load_text_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.original_text_edit.setText(content)
                    self.apply_mappings()
                    self.compute_and_plot_text_frequencies(content)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not read file: {e}")

    def load_frequency_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Frequency File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            try:
                frequencies = self.parse_frequency_file(file_name)
                self.external_frequencies = frequencies
                self.plot_external_frequencies(frequencies)
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"Could not read frequency file: {e}"
                )

    def parse_frequency_file(self, file_name):
        frequencies = {}
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        letter = parts[0].strip().upper()
                        freq = float(parts[1].strip())
                        frequencies[letter] = freq
        return frequencies

    def compute_and_plot_text_frequencies(self, text):
        text = text.upper()
        if self.selected_alphabet == "Turkish":
            letters = re.findall(r"[A-ZÇĞİÖŞÜ]", text)
        else:
            letters = re.findall(r"[A-Z]", text)
        total_letters = len(letters)
        frequencies = {}
        if total_letters > 0:
            counts = Counter(letters)
            for letter in self.alphabet_letters:
                freq = counts.get(letter, 0) / total_letters
                frequencies[letter] = freq
        else:
            frequencies = {letter: 0 for letter in self.alphabet_letters}

        self.plot_text_frequencies(frequencies)

    def plot_text_frequencies(self, frequencies):
        self.figure_text_freq.clear()
        ax = self.figure_text_freq.add_subplot(111)

        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        letters = [item[0] for item in sorted_freq]
        freqs = [item[1] for item in sorted_freq]

        ax.bar(letters, freqs, color="green")
        ax.set_xlabel("Letters")
        ax.set_ylabel("Frequency")
        ax.set_title("Text Letter Frequencies (Sorted)")
        ax.set_ylim(0, max(freqs) * 1.1 if freqs else 1)

        self.figure_text_freq.tight_layout()
        self.canvas_text_freq.draw()

    def plot_external_frequencies(self, frequencies):
        self.figure_external_freq.clear()
        ax = self.figure_external_freq.add_subplot(111)

        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        letters = [item[0] for item in sorted_freq]
        freqs = [item[1] for item in sorted_freq]

        ax.bar(letters, freqs, color="blue")
        ax.set_xlabel("Letters")
        ax.set_ylabel("Frequency")
        ax.set_title("External Letter Frequencies (Sorted)")
        ax.set_ylim(0, max(freqs) * 1.1 if freqs else 1)

        self.figure_external_freq.tight_layout()
        self.canvas_external_freq.draw()

    def change_alphabet(self, text):
        self.selected_alphabet = text
        self.update_alphabet()
        self.apply_mappings()
        original_text = self.original_text_edit.toPlainText()
        if original_text:
            self.compute_and_plot_text_frequencies(original_text)
        if self.external_frequencies:
            self.plot_external_frequencies(self.external_frequencies)

    def update_alphabet(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.selected_alphabet == "English":
            self.alphabet_letters = [chr(i) for i in range(65, 91)]  # A-Z
        elif self.selected_alphabet == "Turkish":
            self.alphabet_letters = [
                "A",
                "B",
                "C",
                "Ç",
                "D",
                "E",
                "F",
                "G",
                "Ğ",
                "H",
                "I",
                "İ",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "Ö",
                "P",
                "R",
                "S",
                "Ş",
                "T",
                "U",
                "Ü",
                "V",
                "Y",
                "Z",
            ]

        self.labels = {}
        self.inputs = {}
        self.mappings = {}

        font = QFont()
        font.setPointSize(10)

        for letter in self.alphabet_letters:
            h_layout = QHBoxLayout()
            label = QLabel(letter)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(30)
            label.setFont(font)
            self.labels[letter] = label
            h_layout.addWidget(label)

            input_field = QLineEdit()
            input_field.setMaxLength(1)
            input_field.setAlignment(Qt.AlignCenter)
            input_field.setFixedWidth(50)
            input_field.setFont(font)
            input_field.textChanged.connect(
                lambda text, l=letter: self.on_input_changed(l, text)
            )
            self.inputs[letter] = input_field
            h_layout.addWidget(input_field)

            self.scroll_layout.addLayout(h_layout)

    def on_input_changed(self, letter, text):
        if text:
            text = text[0]
            if not text.isalpha():
                QMessageBox.warning(
                    self, "Invalid Input", f"Please enter a letter for '{letter}'."
                )
                self.inputs[letter].setText("")
                if letter in self.mappings:
                    del self.mappings[letter]
                self.apply_mappings()
                return
            text = text.lower()
            self.inputs[letter].blockSignals(True)
            self.inputs[letter].setText(text)
            self.inputs[letter].blockSignals(False)
            self.mappings[letter] = text
        else:
            if letter in self.mappings:
                del self.mappings[letter]

        self.apply_mappings()

    def apply_mappings(self):
        original_text = self.original_text_edit.toPlainText()
        processed_text = original_text

        translation_table = {}

        for letter, mapped_char in self.mappings.items():
            translation_table[ord(mapped_char)] = letter

        processed_text = processed_text.translate(translation_table)

        self.processed_text_edit.setText(processed_text)


def main():
    app = QApplication(sys.argv)
    window = AlphabetMappingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
