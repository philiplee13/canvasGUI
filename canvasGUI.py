import tkinter as tk
from tkmacosx import Button
import os
from canvas_gmail_api import Canvas_Gmail_Script
import webbrowser


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
        # entry fields
        # entry field for gmail
        self.gmail_label = tk.Label(
            window, text="Please enter in your G-Mail below")
        self.gmail_label.pack()
        self.email_entry = tk.Entry()
        self.email_entry.pack()
        # entry field for term start date
        self.term_start_label = tk.Label(
            window, text="Please enter in your terms start date in the format YYYY-MM-DD (2021-05-19)"
        )
        self.term_start_label.pack()
        self.term_start_entry = tk.Entry()
        self.term_start_entry.pack()
        # entry field for school name
        self.school_label = tk.Label(
            window, text="Please enter in your school name in the following format -> Auburn University -> Auburn"
        )
        self.school_label.pack()
        self.school_label_entry = tk.Entry()
        self.school_label_entry.pack()
        # entry field for api token
        self.canvas_api_label = tk.Label(
            window, text="Please enter in your Canvas API Key below")
        self.canvas_api_label = tk.Label(
            window, text="If you do not know how to obtain a Canvas API Key, please visit the link below to obtain an API token")
        self.canvas_api_label.pack()
        self.api_entry = tk.Entry()
        self.api_entry.pack()

        self.canvas_link = Button(
            window, text="Click me for instructions to get a Canvas API Token", bg="light grey", fg="blue"
        )
        self.canvas_link.pack()
        self.canvas_link.bind("<Button-1>", lambda e: self.callback("https://kb.iu.edu/d/aaja"))

        # buttons to handle click and close GUI
        # the sync button here will call both the "return_info" function as well as call the script
        self.sync_button = Button(window, text="Click me to start the Sync", command=self.run_app, bg="green", fg="white")
        self.sync_button.pack()

        self.close_gui = Button(
            window, text="Click me to close the GUI", command=self.close_gui, bg="red", fg="black")
        self.close_gui.pack()

    """
    Functions for Canvas GUI
    """

    def callback(self,url):
        webbrowser.open_new(url)

    def close_gui(self):
        window.destroy()

    def run_app(self):
        self.gmail= self.email_entry.get()
        self.canvas_api = self.api_entry.get()
        self.term_start = self.term_start_entry.get()
        self.school = self.school_label_entry.get().lower()
        canvas_app = Canvas_Gmail_Script(self.gmail, self.canvas_api, self.term_start, self.school)
        data = canvas_app.get_canvas_data()
        all_courses = canvas_app.get_courses(data)
        canvas_app.get_all_assignments(all_courses)
        canvas_app.create_events()
        # canvas_app.delete_all_events()

if __name__ == "__main__":
    window = tk.Tk()
    canvas_gui = CanvasApp(window)
    window.mainloop()
