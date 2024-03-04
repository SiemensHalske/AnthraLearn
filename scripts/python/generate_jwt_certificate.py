import sys
import secrets
import string
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QSlider, QCheckBox,
    QTextEdit, QFileDialog, QVBoxLayout, QWidget, QComboBox
)
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


class KeyGenerator:
    def __init__(self,
                 algorithm,
                 length,
                 include_special,
                 include_digits,
                 include_uppercase,
                 include_lowercase
                 ):
        self.algorithm = algorithm
        self.length = length
        self.include_special = include_special
        self.include_digits = include_digits
        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase

    def generate(self):
        if self.algorithm == "Random":
            return self.generate_random()
        elif self.algorithm == "Custom":
            return self.generate_custom()
        else:
            return ""

    def generate_random(self):
        chars = ""
        if self.include_uppercase:
            chars += string.ascii_uppercase
        if self.include_lowercase:
            chars += string.ascii_lowercase
        if self.include_digits:
            chars += string.digits
        if self.include_special:
            chars += string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(self.length))

    def generate_custom(self):
        key = ""
        if self.include_uppercase:
            key += ''.join(secrets.choice(string.ascii_uppercase)
                           for _ in range(self.length // 4))
        if self.include_lowercase:
            key += ''.join(secrets.choice(string.ascii_lowercase)
                           for _ in range(self.length // 4))
        if self.include_digits:
            key += ''.join(secrets.choice(string.digits)
                           for _ in range(self.length // 4))
        if self.include_special:
            key += ''.join(secrets.choice(string.punctuation)
                           for _ in range(self.length // 4))
        return ''.join(secrets.choice(key) for _ in range(self.length))

    def generate_custom_secure(self):
        key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        encoded_key = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return encoded_key.decode('utf-8')


class UIElements(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.algorithm_label, self.algorithm_combobox = self.create_combobox(
            "Algorithm:", ["Random", "Custom"])
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combobox)

        self.key_length_label, self.key_length_slider = self.create_slider(
            "Key Length:", 8, 8192, 256)
        layout.addWidget(self.key_length_label)
        layout.addWidget(self.key_length_slider)

        self.include_special_checkbox = self.create_checkbox(
            "Include Special Characters", checked=False)
        layout.addWidget(self.include_special_checkbox)

        self.include_digits_checkbox = self.create_checkbox(
            "Include Digits", checked=True)
        layout.addWidget(self.include_digits_checkbox)

        self.include_uppercase_checkbox = self.create_checkbox(
            "Include Uppercase Letters", checked=True)
        layout.addWidget(self.include_uppercase_checkbox)

        self.include_lowercase_checkbox = self.create_checkbox(
            "Include Lowercase Letters", checked=True)
        layout.addWidget(self.include_lowercase_checkbox)

        self.key_display = QTextEdit(self)
        self.key_display.setReadOnly(True)
        layout.addWidget(self.key_display)

        self.generate_button = self.create_button(
            "Generate Key", self.parent.generate_key)
        layout.addWidget(self.generate_button)

        self.save_button = self.create_button(
            "Save Key", self.parent.save_key, enabled=False)
        layout.addWidget(self.save_button)

    def create_slider(self, label_text, min_val, max_val, default_val):
        label = QLabel(label_text + f" {default_val}", self)
        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider.valueChanged.connect(lambda: label.setText(
            label_text + f" {slider.value()}"))
        return label, slider

    def create_checkbox(self, text, checked=False):
        checkbox = QCheckBox(text, self)
        checkbox.setChecked(checked)
        return checkbox

    def create_combobox(self, label_text, items):
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def create_button(self, text, callback, enabled=True):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setEnabled(enabled)
        return button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secret Key Generator")
        self.setGeometry(100, 100, 480, 360)
        self.ui_elements = UIElements(self)
        self.setCentralWidget(self.ui_elements)

    def generate_key(self):
        algorithm = self.ui_elements.algorithm_combobox.currentText()
        length = self.ui_elements.key_length_slider.value()
        include_special = self.ui_elements.include_special_checkbox.isChecked()
        include_digits = self.ui_elements.include_digits_checkbox.isChecked()
        include_uppercase = \
            self.ui_elements.include_uppercase_checkbox.isChecked()
        include_lowercase = \
            self.ui_elements.include_lowercase_checkbox.isChecked()
        generator = KeyGenerator(
            algorithm,
            length,
            include_special,
            include_digits,
            include_uppercase,
            include_lowercase
        )
        generated_key = generator.generate()
        self.ui_elements.key_display.setText(generated_key)
        self.ui_elements.save_button.setEnabled(True)

    def save_key(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Key",
            "",
            "Certificate Files (*.cert);;All Files (*)",
            options=options
        )
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.ui_elements.key_display.toPlainText())
            self.ui_elements.save_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
