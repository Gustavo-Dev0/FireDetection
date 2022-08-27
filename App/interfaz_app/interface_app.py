import tkinter as tk
from client.gui_app import MainFrame

def main():
    root = tk.Tk()
    root.title("Detección de fuego")
    root.geometry("1000x600")

    app = MainFrame(root=root)
    
    app.mainloop()

if __name__ == '__main__':
    main()