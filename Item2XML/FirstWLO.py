import PySimpleGUI as sg
import pandas as pd
import xml.etree.ElementTree as ET
from FirstIO import load_xml_file, save_xml_file, get_element_family
from Schema_Window import SchemaWindow
from Options_Menu import OptionsMenu  # Import the new OptionsMenu class


class FirstWLO:
    def __init__(self):
        self.xml_data = pd.DataFrame(
            columns=["Tag", "Element Name", "Schema", "Default Values", "Type"]
        )
        self.custom_values = pd.DataFrame(
            columns=["Element Name", "Default Value", "Custom Value"]
        )
        self.tree = None
        self.settings = self.load_settings()  # Load the settings
        self.layout = self.create_layout()
        self.window = sg.Window(
            "FirstWLO",
            self.layout,
            finalize=True,
            resizable=not self.settings["-LOCK_RESIZE-"],
        )
        self.main_window = None

    def load_settings(self):
        """Load the settings from the settings file."""
        try:
            tree = ET.parse(
                "Settings/Defaults/default_settings.xml"
            )  # Update the path to the XML file
            root = tree.getroot()
            settings = {child.tag: child.text for child in root}
        except FileNotFoundError:
            settings = {}

        settings["-LOCK_RESIZE-"] = (
            settings.get("-LOCK_RESIZE-", "false").lower() == "true"
        )  # Convert the string to a boolean
        return settings

    def create_layout(self):
        """Create the GUI layout."""
        layout = [
            [sg.Text("XML File:"), sg.Input(key="-FILE-"), sg.FileBrowse()],
            [
                sg.Button("Load XML"),
                sg.Button("Ima'Schema"),
                sg.Button("Exit"),
                sg.Button("Settings"),
            ],
            [self.create_xml_data_frame()],
            [self.create_custom_values_frame()],
            [
                sg.Button("Reset Custom Values"),
                sg.Button("Save Custom Values"),
                sg.Button("Refresh Windows"),
            ],
        ]
        return layout

    def create_xml_data_frame(self):
        """Create the XML Data frame."""
        return sg.Frame(
            "XML Data",
            [
                [
                    sg.Table(
                        values=self.xml_data.to_numpy().tolist(),
                        headings=[
                            "Tag",
                            "Element Name",
                            "Schema",
                            "Default Values",
                            "Relations",
                        ],
                        display_row_numbers=True,
                        key="-TABLE-XML-",
                        justification="left",
                        auto_size_columns=False,
                        col_widths=[5, 10, 10, 30, 10, 20],
                        num_rows=20,
                    )
                ]
            ],
            pad=(5, 5),
            element_justification="center",
            relief="raised",
            border_width=2,
        )

    def create_custom_values_frame(self):
        """Create the Custom Values frame."""
        return sg.Frame(
            "Custom Values",
            [
                [
                    sg.Table(
                        values=self.custom_values.to_numpy().tolist(),
                        headings=["Element Name", "Default Value", "Custom Value"],
                        display_row_numbers=True,
                        key="-TABLE-CUSTOM-VALUES-",
                        justification="left",
                        auto_size_columns=False,
                        col_widths=[10, 30, 30, 30],
                        enable_events=True,
                        bind_return_key=True,
                    )
                ]
            ],
            pad=(5, 5),
            element_justification="center",
            relief="raised",
            border_width=2,
        )

    def run(self):
        """Start the main event loop for the GUI."""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "Load XML":
                self.load_xml_file(values["-FILE-"])
            elif event == "Ima'Schema":
                if self.tree is not None:
                    sw = SchemaWindow(self.xml_data, self.tree)
                    sw.run()
                else:
                    sg.popup("Please load an XML file first.")
            elif event == "Reset Custom Values":
                self.custom_values = self.custom_values.assign(Custom_Value="")
                self.window["-TABLE-CUSTOM-VALUES-"].update(
                    values=self.custom_values.to_numpy().tolist()
                )
            elif event == "Save Custom Values":
                self.save_xml_file(values["-FILE-"])
            elif event == "Settings":  # Handle the 'Settings' button event
                om = OptionsMenu()
                om.run()
                # Reload the settings and apply them to the window
                self.settings = self.load_settings()
                self.window.close()
                self.window = sg.Window(
                    "FirstWLO",
                    self.layout,
                    finalize=True,
                    resizable=not self.settings["-LOCK_RESIZE-"],
                )
            elif event == "Refresh Windows":
                if self.main_window is not None:
                    self.main_window.close()
                self.main_window = sg.Window(
                    "FirstWLO",
                    self.layout,
                    finalize=True,
                    resizable=not self.settings["-LOCK_RESIZE-"],
                )

        self.window.close()

    def load_xml_file(self, xml_file):
        """Load an XML file and update the data frames."""
        try:
            (
                self.xml_data,
                self.custom_values,
                self.tree,
                root,
                element_family,
            ) = load_xml_file(xml_file)
            self.xml_data["Relations"] = element_family
            self.window["-TABLE-XML-"].update(values=self.xml_data.to_numpy().tolist())
            self.window["-TABLE-CUSTOM-VALUES-"].update(
                values=self.custom_values.to_numpy().tolist()
            )
        except Exception as e:
            sg.popup("Failed to load XML file.", str(e))

    def save_xml_file(self, xml_file):
        """Save the XML file with the custom values."""
        try:
            self.custom_values = pd.DataFrame(
                self.window["-TABLE-CUSTOM-VALUES-"].get(),
                columns=["Element Name", "Default Value", "Custom Value"],
            )
            save_xml_file(self.custom_values, self.tree, xml_file)
            sg.popup("XML file saved successfully.")
        except Exception as e:
            sg.popup("Failed to save XML file.", str(e))


# Create an instance of the FirstWLO class and run the GUI
first_wlo = FirstWLO()
first_wlo.run()
