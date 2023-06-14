import PySimpleGUI as sg
import xml.etree.ElementTree as ET

class OptionsMenu:
    def __init__(self):
        self.layout = self.create_layout()
        self.window = sg.Window('Settings', self.layout, finalize=True)
        self.main_window = None
        self.settings = self.load_settings()

    def load_settings(self):
        """Load the settings from the settings.xml file."""
        try:
            tree = ET.parse('settings.xml')
            root = tree.getroot()
            settings = {child.tag: child.text for child in root}
        except (FileNotFoundError, ET.ParseError):
            settings = {}

        return settings

    def save_settings(self):
        """Save the settings to the settings.xml file."""
        root = ET.Element("settings")
        for key, value in self.settings.items():
            child = ET.SubElement(root, key)
            child.text = value
        tree = ET.ElementTree(root)
        tree.write("settings.xml")

    def create_layout(self):
        """Create the GUI layout for the settings menu."""
        layout = [
            [sg.Text('Window Color:'), sg.Input(key='-WINDOW_COLOR-', background_color='white'),
             sg.ColorChooserButton('Choose', key='-CHOOSE_WINDOW_COLOR-')],
            [sg.Text('Button Color:'), sg.Input(key='-BUTTON_COLOR-', background_color='white'),
             sg.ColorChooserButton('Choose', key='-CHOOSE_BUTTON_COLOR-')],
            [sg.Text('Font Color:'), sg.Input(key='-FONT_COLOR-', background_color='white'),
             sg.ColorChooserButton('Choose', key='-CHOOSE_FONT_COLOR-')],
            [sg.Text('Default Window Size:'), sg.Input(key='-WINDOW_SIZE-', default_text=self.settings.get('-WINDOW_SIZE-', ''))],
            [sg.Checkbox('Lock Window Resizing', key='-LOCK_RESIZE-', default=self.settings.get('-LOCK_RESIZE-', 'false').lower() == 'true')],
            [sg.Button('Apply'), sg.Button('Cancel'), sg.Button('Refresh Windows')]
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
                self.settings['-WINDOW_COLOR-'] = values['-WINDOW_COLOR-']
                self.settings['-BUTTON_COLOR-'] = values['-BUTTON_COLOR-']
                self.settings['-FONT_COLOR-'] = values['-FONT_COLOR-']
                self.settings['-WINDOW_SIZE-'] = values['-WINDOW_SIZE-']
                self.settings['-LOCK_RESIZE-'] = 'true' if values['-LOCK_RESIZE-'] else 'false'

                # Save the settings
                self.save_settings()

                # You'll need to close and re-open your main window for the changes to take effect
                self.window.close()
                if self.main_window is not None:
                    self.main_window.close()
                self.main_window = None
                self.window = None
                return

            elif event == '-CHOOSE_WINDOW_COLOR-':
                # Open color chooser dialog for the window color
                color_key = '-WINDOW_COLOR-'
                color_value = values[color_key]
                new_color = sg.popup_get_color(color_value, no_titlebar=True)

                if new_color is not None:
                    self.window[color_key].update(new_color)
                    self.window[color_key].set_background_color(new_color)
                    self.window['-WINDOW_COLOR_LABEL-'].update(background_color=new_color)

            elif event == '-CHOOSE_BUTTON_COLOR-':
                # Open color chooser dialog for the button color
                color_key = '-BUTTON_COLOR-'
                color_value = values[color_key]
                new_color = sg.popup_get_color(color_value, no_titlebar=True)

                if new_color is not None:
                    self.window[color_key].update(new_color)
                    self.window[color_key].set_background_color(new_color)
                    self.window['-BUTTON_COLOR_LABEL-'].update(background_color=new_color)

            elif event == '-CHOOSE_FONT_COLOR-':
                # Open color chooser dialog for the font color
                color_key = '-FONT_COLOR-'
                color_value = values[color_key]
                new_color = sg.popup_get_color(color_value, no_titlebar=True)

                if new_color is not None:
                    self.window[color_key].update(new_color)
                    self.window[color_key].set_background_color(new_color)
                    self.window['-FONT_COLOR_LABEL-'].update(background_color=new_color)

            elif event == 'Refresh Windows':
                self.save_settings()  # Save the current settings to settings.xml
                if self.main_window is not None:
                    self.main_window.close()
                self.main_window = None
                self.window.close()
                self.window = sg.Window('Settings', self.layout, finalize=True)
                break

        self.window.close()
