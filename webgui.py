from tkinter import *
import webview

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x450")
        self.root.title("Webview Tabs Example")

        # Create a notebook to manage tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        # Create two frames for the tabs
        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)

        # Add the frames to the notebook
        self.notebook.add(self.frame1, text='Geeks for Geeks')
        self.notebook.add(self.frame2, text='Another Website')

        # Create webview windows in the frames
        self.webview1 = webview.create_window('Geeks for Geeks', 'https://geeksforgeeks.org', parent=self.frame1.winfo_id())
        self.webview2 = webview.create_window('Another Website', 'https://example.com', parent=self.frame2.winfo_id())

        # Start the webview
        webview.start()

# Create the main window
root = Tk()
app = App(root)
root.mainloop()
