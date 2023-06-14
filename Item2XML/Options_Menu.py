import PySimpleGUI as sg
import xml.etree.ElementTree as ET
class OptionsMenu:
    def __init__(self):
        self.layout = self.create_layout()
        self.window = sg.Window('Settings', self.layout, finalize=True)

    def create_layout(self):
        """Create the GUI layout for the settings menu."""
        layout = [
            # Add your settings options here
            [sg.Text('Window Color:'), sg.Input(key='-WINDOW_COLOR-')],
            [sg.Text('Button Color:'), sg.Input(key='-BUTTON_COLOR-')],
            [sg.Text('Font Color:'), sg.Input(key='-FONT_COLOR-')],
            [sg.Text('Default Window Size:'), sg.Input(key='-WINDOW_SIZE-')],
            [sg.Checkbox('Lock Window Resizing', key='-LOCK_RESIZE-')],
            [sg.Button('Apply'), sg.Button('Cancel')]
        ]
        return layout

def run(self):
    """Start the main event loop for the settings menu."""
    while True:
        event, values = self.window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Apply':
            # Apply the settings here
            window_color = values['-WINDOW_COLOR-']
            button_color = values['-BUTTON_COLOR-']
            font_color = values['-FONT_COLOR-']
            window_size = values['-WINDOW_SIZE-']
            lock_resize = values['-LOCK_RESIZE-']

            # Save the settings
            root = ET.Element("settings")
            for key, value in values.items():
                child = ET.SubElement(root, key)
                child.text = str(value)
            tree = ET.ElementTree(root)
            tree.write("settings.xml")

            # You'll need to close and re-open your main window for the changes to take effect
            self.window.close()
            self.window = sg.Window('FirstWLO', self.layout, finalize=True)
