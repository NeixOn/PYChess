import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        pass

    def choose_file(self):
        filetypes = (("PGN", "*.PGN"),
                     ("Изображение", "*.jpg *.gif *.png"),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            return filename
        else:
            return False

    def choose_directory(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir="/")
        if directory:
            print(directory)


def TableFile():
    window = tk.Tk()
    window.title('FIle')
    frame_list = tk.Frame(window, bg='blue')
    frame_list.grid(column=0, row=1, columnspan=2, sticky="we")
    lst = [
        
        (1, 'Larsen V5', 'Mustang', '0-1', '09.12.2002'),
        (2, 'Matheus 1', 'Golem 0.4', '1-0', '14.12.2002'),
        (3, 'Larsen V5', 'Monik 2.1', '0-1', '03.01.2003'),
        (4, 'Mint 2', 'Monik 2.1', '0-1', '21.01.2003'),
        (5, "Van't Kruijs,M", 'De Heer,K', '1-0', '1851'),
        (6, 'Suhle,B', "Anderssen, A", '0-1', '1859'),
        (7, 'Czarmowski,H', "D'Andre,B", '0-1', '08.06.1867'),
        (8, 'Magnus', 'Schallopp,E', '0-1', '01.06.1868'),
        (9, 'Owen,J', 'Blackburne,J', '1-0', '1870'),
        (10, 'Owen,J', 'Green,V', '1-0', '1870'),
        (11, 'Owen,J', 'De Vere,C', '0-1', '04.07.1872')
    ]
    heads = ['№', 'white', 'black','result', 'date']
    table = ttk.Treeview(frame_list, show='headings')
    table['columns'] = heads
    table['displaycolumns'] = ['№', 'white', 'black','result', 'date']
    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')
    for row in lst:
        table.insert('', 'end', values=row)

    scroll_pane = ttk.Scrollbar(frame_list, command=table.yview)
    table.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    window.mainloop()

if __name__ == "__main__":
    app = App()
    TableFile()