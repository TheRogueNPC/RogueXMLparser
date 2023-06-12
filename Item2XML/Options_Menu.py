import PySimpleGUI as sg

class OptionsMenu:
    def __init__(self):
        self.layout = [
            [sg.Text('lol settings')]
        ]
        self.window = sg.Window('Options Menu', self.layout, finalize=True)

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break

        self.window.close()
