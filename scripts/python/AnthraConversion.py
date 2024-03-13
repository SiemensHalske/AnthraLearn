import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton
import xmltodict


class UnitConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setMinimumSize(400, 200)  # Set minimum size for the window

        self.input_label = QLabel("Input Value:", self)
        self.input_label.setGeometry(20, 20, 100, 20)

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(120, 20, 100, 20)

        self.input_unit_label = QLabel("Input Unit:", self)
        self.input_unit_label.setGeometry(20, 60, 100, 20)

        self.input_unit_combo = QComboBox(self)
        self.input_unit_combo.setGeometry(120, 60, 100, 20)

        self.output_unit_label = QLabel("Output Unit:", self)
        self.output_unit_label.setGeometry(20, 100, 100, 20)

        self.output_unit_combo = QComboBox(self)
        self.output_unit_combo.setGeometry(120, 100, 100, 20)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.setGeometry(250, 20, 100, 100)
        self.convert_button.clicked.connect(self.convert_units)

        self.output_label = QLabel("Converted Value:", self)
        self.output_label.setGeometry(20, 140, 100, 20)

        self.output_field = QLineEdit(self)
        self.output_field.setGeometry(120, 140, 100, 20)
        self.output_field.setReadOnly(True)

        # Add supported conversions to the input and output unit combo boxes
        self.add_supported_conversions()

        self.show()

    def add_supported_conversions(self):
        # Add supported conversions for web development
        web_development_conversions = {
            "Length": ["px", "em", "rem", "%", "vh", "vw"],
            "Font Size": ["pt", "px", "em", "rem"],
            "Color Formats": ["hex", "RGB", "CMYK"],
            "Image Formats": ["JPEG", "PNG", "GIF"]
        }

        # Add supported conversions for backend programming
        backend_programming_conversions = {
            "Data Types": ["int", "float", "string", "list", "dictionary"],
            "Storage Units": ["bytes", "KB", "MB", "GB", "TB"],
            "Time Units": ["seconds", "milliseconds", "microseconds", "nanoseconds"],
            "API Response Formats": ["JSON", "XML"]
        }

        # Add web development conversions to the combo boxes
        for category, units in web_development_conversions.items():
            self.input_unit_combo.addItem(category)
            self.output_unit_combo.addItem(category)
            self.input_unit_combo.addItems(units)
            self.output_unit_combo.addItems(units)

        # Add backend programming conversions to the combo boxes
        for category, units in backend_programming_conversions.items():
            if category not in web_development_conversions:
                self.input_unit_combo.addItem(category)
                self.output_unit_combo.addItem(category)
                self.input_unit_combo.addItems(units)
                self.output_unit_combo.addItems(units)

    def convert_units(self):
        input_value = self.input_field.text()
        input_unit = self.input_unit_combo.currentText()
        output_unit = self.output_unit_combo.currentText()

        # Implement conversion logic here based on the selected units
        converted_value = self.perform_conversion(
            input_value, input_unit, output_unit)

        self.output_field.setText(str(converted_value))

    def perform_conversion(self, input_value, input_unit, output_unit):
        # Implement the conversion logic for each supported conversion type
        # You can use if-elif statements or a dictionary to handle different conversion types
        # Example:
        if input_unit == "Length" and output_unit == "Length":
            return self.convert_length(input_value)
        elif input_unit == "Font Size" and output_unit == "Font Size":
            return self.convert_font_size(input_value)
        elif input_unit == "Color Formats" and output_unit == "Color Formats":
            return self.convert_color_formats(input_value)
        elif input_unit == "Image Formats" and output_unit == "Image Formats":
            return self.convert_image_formats(input_value)
        elif input_unit == "Data Types" and output_unit == "Data Types":
            return self.convert_data_types(input_value)
        elif input_unit == "Storage Units" and output_unit == "Storage Units":
            return self.convert_storage_units(input_value)
        elif input_unit == "Time Units" and output_unit == "Time Units":
            return self.convert_time_units(input_value)
        elif input_unit == "API Response Formats" and output_unit == "API Response Formats":
            return self.convert_api_response_formats(input_value)
        else:
            return "Invalid conversion"

    def convert_length(self, value):
        # Implement the conversion logic for length units
        # Example:
        # Convert px to em
        conversion_factor = 0.0625
        converted_value = value * conversion_factor
        return converted_value

    def convert_font_size(self, value):
        # Implement the conversion logic for font size units
        # Example:
        # Convert pt to px
        conversion_factor = 1.333
        converted_value = value * conversion_factor
        return converted_value

    def convert_color_formats(self, value):
        # Implement the conversion logic for color formats
        # Example:
        # Convert hex to RGB
        converted_value = self.hex_to_rgb(value)
        return converted_value

    def convert_image_formats(self, value):
        # Implement the conversion logic for image formats
        # Example:
        # Convert JPEG to PNG
        converted_value = self.jpeg_to_png(value)
        return converted_value

    def convert_data_types(self, value):
        # Implement the conversion logic for data types
        # Example:
        # Convert int to float
        converted_value = float(value)
        return converted_value

    def convert_storage_units(self, value):
        # Implement the conversion logic for storage units
        # Example:
        # Convert bytes to KB
        conversion_factor = 0.001
        converted_value = value * conversion_factor
        return converted_value

    def convert_time_units(self, value):
        # Implement the conversion logic for time units
        # Example:
        # Convert seconds to milliseconds
        conversion_factor = 1000
        converted_value = value * conversion_factor
        return converted_value

    def convert_api_response_formats(self, value):
        # Implement the conversion logic for API response formats
        # Example:
        # Convert JSON to XML
        converted_value = self.json_to_xml(value)
        return converted_value

    def hex_to_rgb(self, value):
        # Implement the conversion logic for hex to RGB
        # Example:
        r = int(value[1:3], 16)
        g = int(value[3:5], 16)
        b = int(value[5:7], 16)
        return f"RGB({r}, {g}, {b})"

    def jpeg_to_png(self, value):
        # Implement the conversion logic for JPEG to PNG
        # Example:
        return value.replace(".jpeg", ".png")

    def json_to_xml(self, value):
        # Implement the conversion logic for JSON to XML
        # Example:
        # You can use a library like xmltodict to convert JSON to XML
        xml = xmltodict.unparse(value)
        return xml


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter_app = UnitConverterApp()
    sys.exit(app.exec_())
