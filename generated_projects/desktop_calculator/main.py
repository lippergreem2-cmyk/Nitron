import tkinter as tk

window = tk.Tk()

window.title("Nitron Desktop App")
window.geometry("500x300")

label = tk.Label(
    window,
    text="Welcome to your Nitron Desktop App",
    font=("Arial",16)
)

label.pack(pady=20)

button = tk.Button(
    window,
    text="Click Me",
    command=lambda: label.config(text="Button Clicked!")
)

button.pack()

window.mainloop()
