import tkinter as tk 

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Carrito Discretas")
        self.state("zoomed")
        self.minsize(1080, 900)

        
if __name__ == "__main__":

    app = App()
    app.mainloop()