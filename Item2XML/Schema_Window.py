import PySimpleGUI as sg
from xml.etree import ElementTree as ET
from xml.dom import minidom


class SchemaWindow:
    def __init__(self, df_xml, tree):
        sg.set_options(font=("Courier New", 12))
        self.df_xml = df_xml
        self.tree = tree

        layout = [
            [
                sg.Column(
                    [[sg.Multiline("", size=(50, 20), key="-SCHEMA-", disabled=True)]],
                    size=(None, None),
                )
            ],
            [sg.Button("Export", key="-EXPORT-")],
        ]

        self.window = sg.Window("Ima'Schema", layout, finalize=True)
        self.xml_string = self.generate_xml_with_schema_comments()

        self.window["-SCHEMA-"].update(self.xml_string)
        self.window["-SCHEMA-"].Widget.config(
            wrap="none"
        )  # Disable line wrapping for the text field

    def generate_xml_with_schema_comments(self):
        """
        Creates a copy of the original XML tree, then adds schema comments to each tag.
        The XML tree is then converted to a pretty-printed string.
        """
        if self.tree is None:
            return "No XML file loaded. Please load an XML file first."

        root = self.tree.getroot()

        for _, row in self.df_xml.iterrows():
            tag = row["Tag"]
            schema = row["Schema"]

            for elem in root.iter(tag):
                # Add comment directly above the corresponding element
                comment = ET.Comment(" Schema Type: " + schema)
                if (
                    elem.text is not None and elem.text.strip()
                ):  # Check if the element has text content
                    elem.text = None  # remove the text content
                elem.insert(0, comment)

        # Convert the XML tree to a string and pretty-print it
        xml_string = ET.tostring(root, encoding="utf-8")
        pretty_xml_string = minidom.parseString(xml_string).toprettyxml(indent="\t")
        return pretty_xml_string

    def export_xml(self):
        """
        Exports the XML schema to a file chosen by the user.
        """
        if self.tree is None:
            sg.popup_error("No XML file loaded. Please load an XML file first.")
            return

        save_path = sg.popup_get_file(
            "Save XML File", save_as=True, file_types=(("XML Files", "*.xml"),)
        )
        if save_path:
            with open(save_path, "w") as file:
                file.write(self.xml_string)
            sg.popup(f"XML file has been exported to: {save_path}")

    def run(self):
        """
        Starts the PySimpleGUI event loop for the window.
        """
        while True:
            event, _ = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break

            if event == "-EXPORT-":
                self.export_xml()

        self.window.close()
