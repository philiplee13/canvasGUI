import tkinter as tk
from tkinter import ttk
import os
from canvas_gmail_api import Canvas_Gmail_Script


class CanvasApp:
    def __init__(self, window):
        self.window = window
        window.title("Canvas Calendar Sync")
        # Welcome instructions
        self.welcome_label = tk.Label(
            window, text="Welcome to the Canvas GMail Calendar Sync GUI!")
        self.welcome_label.pack()
        self.instructions_label = tk.Label(
            window, text="You'll be asked to input your email, Canvas API Key, as well as your term start date")
        self.instructions_label.pack()
        # entry fields for gmail email and canvas api and term start date
        self.gmail_label = tk.Label(
            window, text="Please enter in your GMail Calendar Email below")
        self.gmail_label.pack()
        self.email_entry = tk.Entry()
        self.email_entry.pack()

        self.term_start_label = tk.Label(
            window, text="Please enter in your terms start date in the format YYYY-MM-DD"
        )
        self.term_start_label.pack()
        self.term_start_entry = tk.Entry()
        self.term_start_entry.pack()

        self.canvas_api_label = tk.Label(
            window, text="Please enter in your Canvas API Key below")
        self.canvas_api_label = tk.Label(
            window, text="If you do not know how to obtain a Canvas API Key, please visit the Repo where you downloaded this from to view the instructions")
        self.canvas_api_label.pack()
        self.api_entry = tk.Entry()
        self.api_entry.pack()

        # buttons to handle click and close GUI
        # the sync button here will call both the "return_info" function as well as call the script
        self.sync_button = tk.Button(window, text="Click me to start the Sync", command=self.get_user_input, highlightbackground="red")
        self.sync_button.pack()

        self.close_gui = tk.Button(
            window, text="Click me to close the GUI", command=self.close_gui, highlightbackground="blue")
        self.close_gui.pack()

    """
    Functions for Canvas GUI
    """

    def close_gui(self):
        window.destroy()

    def get_user_input(self):
        self.gmail= self.email_entry.get()
        self.canvas_api = self.api_entry.get()
        self.term_start = self.term_start_entry.get()
        canvas_app = Canvas_Gmail_Script(self.gmail, self.canvas_api, self.term_start)
        data = canvas_app.get_canvas_data()
        all_courses = canvas_app.get_courses(data)
        canvas_app.get_all_assignments(all_courses)
        canvas_app.create_events()
        # canvas_app.delete_all_events()

if __name__ == "__main__":
    window = tk.Tk()
    canvas_gui = CanvasApp(window)
    window.mainloop()
