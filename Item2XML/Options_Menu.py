import PySimpleGUI as sg

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
                break

        self.window.close()
