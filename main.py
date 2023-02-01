# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import config
from tkinter import *
from MyWindow import *

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #print(type(config.dim_data.get("gold_dim_category")))
    #db = DbOpt()
    #db.create_table_dim("gold_dim_crime")
    #db.create_table_dim("gold_dim_category")
    root = Tk()
    app = MyWindow(root)
    root.wm_title("Tkinter button")
    root.geometry("320x400")
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
