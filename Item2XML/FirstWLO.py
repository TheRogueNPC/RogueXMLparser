import PySimpleGUI as sg
import pandas as pd
from FirstIO import load_xml_file, reset_xml_values, save_xml_file, generate_schema_type, get_element_name
from Schema_Window import SchemaWindow

class FirstWLO:
    def __init__(self):
        self.df_xml = pd.DataFrame(columns=['Row', 'Element Name', 'Tag', 'Type', 'Schema', 'Default Values'])
        self.df_custom_values = pd.DataFrame(columns=['Row', 'Element Name', 'Default Value', 'Custom Value'])
        self.tree = None

        self.layout = [
            [sg.Text('XML File:'), sg.Input(key='-FILE-'), sg.FileBrowse()],
            [sg.Button('Load XML'), sg.Button("Ima'Schema"), sg.Button('Exit')],
            [sg.Frame('XML Data', [
                [sg.Table(
                    values=self.df_xml.to_numpy().tolist(),
                    headings=['Row', 'Element Name', 'Tag', 'Type', 'Schema', 'Default Values'],
                    display_row_numbers=False,
                    key='-TABLE-XML-', justification='left', auto_size_columns=False,
                    col_widths=[10, 30, 30, 15, 20, 20],
                    num_rows=20
                )]
            ], pad=(5, 5), element_justification='center', relief='raised', border_width=2)],
            [sg.Frame('Custom Values', [
                [sg.Table(
                    values=self.df_custom_values.to_numpy().tolist(),
                    headings=['Row', 'Element Name', 'Default Value', 'Custom Value'],
                    display_row_numbers=False,
                    key='-TABLE-CUSTOM-VALUES-', justification='left', auto_size_columns=False,
                    col_widths=[10, 30, 30, 30],
                    enable_events=True,
                    bind_return_key=True
                )]
            ], pad=(5, 5), element_justification='center', relief='raised', border_width=2)],
            [
                sg.Button('Reset XML Values'),
                sg.Button('Reset Custom Values'),
                sg.Button('Save Custom Values')
            ]
        ]
        self.window = sg.Window('FirstWLO', self.layout, finalize=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            elif event == 'Load XML':
                self.load_xml_file(values['-FILE-'])
            elif event == "Ima'Schema":
                if self.tree is not None:
                    sw = SchemaWindow(self.df_xml, self.tree)
                    sw.run()
                else:
                    sg.popup('Please load an XML file first.')
            elif event == 'Reset Custom Values':
                self.df_custom_values = reset_xml_values(self.df_custom_values)
                self.window['-TABLE-CUSTOM-VALUES-'].update(values=self.df_custom_values.to_numpy().tolist())
            elif event == 'Save Custom Values':
                self.save_xml_values(values['-FILE-'])

        self.window.close()

    def load_xml_file(self, xml_file):
        try:
            self.df_xml, self.df_custom_values, self.tree = load_xml_file(xml_file)
            # Update the 'Schema' column using the generate_schema_type function
            self.df_xml['Schema'] = self.df_xml.apply(lambda row: generate_schema_type(self.tree.find(row['Tag'])), axis=1)
            # Update the 'Element Name' column to display bracketed element names
            self.df_xml['Element Name'] = self.df_xml['Tag'].apply(lambda tag: f"<{get_element_name(tag)}/>")
            self.window['-TABLE-XML-'].update(values=self.df_xml.to_numpy().tolist())
            self.window['-TABLE-CUSTOM-VALUES-'].update(values=self.df_custom_values.to_numpy().tolist())
        except Exception as e:
            sg.popup_error(f"Error occurred while loading XML file: {str(e)}")

    def save_xml_values(self, xml_file):
        try:
            save_xml_file(self.df_custom_values, self.tree, xml_file)
        except Exception as e:
            sg.popup_error(f"Error occurred while saving XML file: {str(e)}")
