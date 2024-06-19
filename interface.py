import tkinter as tk

class ResponsiveScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Configure the root window
        self.title("Responsive Screen")
        self.geometry("400x300")  # Initial size
        self.bind("<Configure>", self.on_resize)  # Bind resize event

        # Create and place widgets
        self.label = tk.Label(self, text="Resize the window to see responsiveness")
        self.label.pack(fill=tk.BOTH, expand=True)

        # Button to do nothing (Yes)
        self.yes_button = tk.Button(self, text="Yes")
        self.yes_button.pack()

        # Button to close the window (No)
        self.no_button = tk.Button(self, text="No", command=self.close_window)
        self.no_button.pack()

    def on_resize(self, event):
        # Adjust widget properties based on window size
        width = event.width
        height = event.height

        # Example: Make the label text size responsive
        font_size = max(int((width + height) / 100), 10)
        self.label.config(font=("Helvetica", font_size))

    def close_window(self):
        # Close the window
        self.destroy()

if __name__ == "__main__":
    app = ResponsiveScreen()
    app.mainloop()
