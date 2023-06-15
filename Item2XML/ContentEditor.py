# ContentEditor.py
import PySimpleGUI as sg
import pandas as pd


class ContentEditor:
    def __init__(self, app):
        self.app = app
        self.selected_row = None

        self.layout = [
            [sg.Text("Custom Values", font="Any 12 bold")],
            [
                sg.Table(
                    values=self.app.df_custom_values.to_numpy().tolist(),
                    headings=["Row", "Element Name", "Default Value", "Custom Value"],
                    key="-TABLE-CUSTOM-EDITOR-",
                    justification="left",
                    auto_size_columns=False,
                    col_widths=[10, 30, 30, 30],
                    num_rows=20,
                    enable_events=True,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                )
            ],
            [
                sg.Button(
                    "Save Custom Values", key="-SAVE-CUSTOM-VALUES-", disabled=True
                ),
                sg.Button("Close"),
            ],
        ]

        self.window = sg.Window("Content Editor", self.layout, finalize=True)
        self.table = self.window["-TABLE-CUSTOM-EDITOR-"]
        self.table.bind("<ButtonRelease-1>", self.handle_table_click)
        self.window["-SAVE-CUSTOM-VALUES-"].bind(
            "<ButtonRelease-1>", self.handle_save_custom_values
        )
        self.window.bind("<Escape>", self.handle_close)

    def handle_table_click(self, event):
        if self.selected_row is not None:
            self.table.TKWidget.itemconfig(self.selected_row, bg="white")
        self.selected_row = self.table.TKWidget.identify_row(event.y)
        self.table.TKWidget.itemconfig(self.selected_row, bg="red")

        self.window["-SAVE-CUSTOM-VALUES-"].update(disabled=False)

    def handle_save_custom_values(self, event):
        data = self.table.get()
        df_custom = pd.DataFrame(
            data, columns=["Row", "Element Name", "Default Value", "Custom Value"]
        )
        self.app.df_custom_values = df_custom

        # Reset selected row and table background color
        self.table.TKWidget.itemconfig(self.selected_row, bg="white")
        self.selected_row = None

        # Update the main window table with the updated custom values
        self.app.window["-TABLE-CUSTOM-"].update(values=df_custom.to_numpy().tolist())

        sg.popup("Custom values have been saved.")

    def handle_close(self, event):
        self.window.close()

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == "Close":
                break

        self.window.close()
