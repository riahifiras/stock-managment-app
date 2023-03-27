from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

conn = sql.connect("first1.db")
cur = conn.cursor()
root = Tk()
root.title('stock manager')
root.geometry('250x220')

class Table:
    def __init__(self, gui):
        for i in range(total_rows):
            for j in range(total_columns):
                if i == 0:
                    self.entry = Entry(gui, width=20, bg='LightSteelBlue',fg='Black',
                                       font=('Arial', 8, 'bold'))
                elif j == 11:
                    self.entry = Entry(gui, width=20,fg='red' ,font=('Arial', 8, ''))
                else:
                    self.entry = Entry(gui, width=20,fg='blue' ,font=('Arial', 8, ''))

                self.entry.grid(row=i, column=j)
                try:
                    self.entry.insert(END, str(item_list[i][j]))
                except (IndexError):
                    pass

cur.execute("SELECT * FROM stock")
cur.execute("SELECT id FROM stock")
ids = [i[0]for i in cur.fetchall()]

def refresh(win):
    win.destroy()
    show_table()

def show_table():
    conn = sql.connect("first1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock")
    global item_list
    global total_columns
    global total_rows
    item_list = cur.fetchall()
    item_list = [list(i) for i in item_list]
    item_list.insert(0, ['id', 'model', 'ref','description', 'diametre nominale(m)', 'pression nominale(bar)', 'KVS', 'frequence(Hz)' ,'nb_disponible'])
    total_rows = len(item_list)+1
    total_columns = len(item_list[0])
    gui = Toplevel()
    gui.title('stock')
    table = Table(gui)
    note = Label(gui, text="Note that changes to this table have no effect on the actual database!")
    note.grid(row=total_rows+1, column=0, columnspan=3)
    button = Button(gui, text="refresh", command=lambda: refresh(gui))
    button.grid(row = total_rows+1, column=total_columns-1)
    button.config(width=16, borderwidth=5)

def add(a,b,x,c,d,e,g,i,window):
    global ids
    conn = sql.connect("first1.db")
    cur = conn.cursor()
    req = "INSERT INTO stock(model,ref,description,diametre_nominale_mm,pression_nominale_bar,KVS,frequence_Hz,nb_disponible) VALUES(?,?,?,?,?,?,?,?)"
    cur.execute(req, (a.get(),x.get(), b.get(), c.get(),d.get(), e.get(),g.get(), i.get()))
    conn.commit()
    a.delete(0, END)
    b.delete(0, END)
    x.delete(0, END)
    c.delete(0, END)
    d.delete(0, END)
    e.delete(0, END)
    g.delete(0, END)
    i.delete(0, END)
    cur.execute("SELECT id FROM stock")
    ids = [i[0]for i in cur.fetchall()]
    msg= Label(window, text="item was added successfully", bg="#4BB543", fg="white")
    msg.grid(row=11, column=0, columnspan=3)

def confirm(a,b,x,c,d,e,g,i,id,window):
    conn = sql.connect("first1.db")
    cur = conn.cursor()
    req = """UPDATE stock
             SET model = ?, ref = ?, description = ?, diametre_nominale_mm = ?, pression_nominale_bar = ?, KVS = ?, frequence_Hz = ?, nb_disponible = ?
             WHERE id = {}""".format(id)
    cur.execute(req, (a.get(),b.get(), x.get(), c.get(),d.get(), e.get(),g.get(), i.get()))
    conn.commit()
    msg= Label(window, text="item values were updated successfully", bg="#4BB543", fg="white")
    msg.grid(row=11, column=0, columnspan=3)

def model_confirmation(model,l):
    l.delete(0, END)
    if model.get() == "other":
        selection_win.destroy()
        messagebox.showinfo("info", "type-in the model in the model selection box")
        
    else:
        l.insert(0, model.get())
        selection_win.destroy()

def model_selection(l):
    global selection_win
    selection_win = Toplevel()
    selection_win.title("Selection window")
    cur.execute("SELECT DISTINCT model FROM stock")
    model_list = cur.fetchall()
    models = [(i[0],i[0]) for i in model_list]
    model = StringVar()
    for text, modell in models:
        Radiobutton(selection_win, text=text, variable=model, value=modell).pack(anchor=W)
    Radiobutton(selection_win, text="other", variable=model, value="other").pack(anchor=W)
    conf = Button(selection_win, text="confirm", command=lambda: model_confirmation(model, l)).pack()

def new_item():
    temp_win = Toplevel()
    temp_win.title("Add new item")
    a1 = Label(temp_win, text='model selection',padx=50)
    a1.grid(row=0, column=0)
    a2 = Entry(temp_win, width=50, borderwidth=5)
    a2.grid(row=0, column=1)
    a3 = Button(temp_win,text="select", width=5, command=lambda: model_selection(a2))
    a3.grid(row=0, column=2)
    b1 = Label(temp_win, text='ref',padx=50)
    b1.grid(row=1, column=0)
    b2 = Entry(temp_win, width=50, borderwidth=5)
    b2.grid(row=1, column=1)
    x1 = Label(temp_win, text='description',padx=50)
    x1.grid(row=2, column=0)
    x2 = Entry(temp_win, width=50, borderwidth=5)
    x2.grid(row=2, column=1)
    c1 = Label(temp_win, text='diametre_nominale(mm)',padx=50)
    c1.grid(row=3, column=0)
    c2 = Entry(temp_win, width=50, borderwidth=5)
    c2.grid(row=3, column=1)
    d1 = Label(temp_win, text='pression_nominale(bar)',padx=50)
    d1.grid(row=4, column=0)
    d2 = Entry(temp_win, width=50, borderwidth=5)
    d2.grid(row=4, column=1)
    e1 = Label(temp_win, text='KVS',padx=50)
    e1.grid(row=5, column=0)
    e2 = Entry(temp_win, width=50, borderwidth=5)
    e2.grid(row=5, column=1)
    g1 = Label(temp_win, text='frequence(Hz)',padx=50)
    g1.grid(row=7, column=0)
    g2 = Entry(temp_win, width=50, borderwidth=5)
    g2.grid(row=7, column=1)
    i1 = Label(temp_win, text='nb_disponible',padx=50)
    i1.grid(row=9, column=0)
    i2 = Entry(temp_win, width=50, borderwidth=5)
    i2.grid(row=9, column=1)
    temp_Button1 = Button(temp_win, text="Submit", command=lambda: add(a2,b2,x2,c2,d2,e2,g2,i2,temp_win))
    temp_Button1.grid(row=10, column=1)
    temp_Button1 = Button(temp_win, text="Cancel", command=temp_win.destroy)
    temp_Button1.grid(row=10, column=2)

def update(id):
    if int(id.get()) not in ids:
        messagebox.showerror("error", "no item with the id {} was found".format(id.get()))
    else:
        conn = sql.connect("first1.db")
        cur = conn.cursor()
        req = "SELECT * FROM stock WHERE id = {}".format(id.get())
        cur.execute(req)
        item_info = cur.fetchone()
        temp_win = Toplevel()
        temp_win.title("update item values")

        a1 = Label(temp_win, text='model',padx=50)
        a1.grid(row=0, column=0)
        a2 = Entry(temp_win, width=50, borderwidth=5)
        a2.grid(row=0, column=1)
        a2.insert(0, item_info[1])
        b1 = Label(temp_win, text='ref',padx=50)
        b1.grid(row=1, column=0)
        b2 = Entry(temp_win, width=50, borderwidth=5)
        b2.grid(row=1, column=1)
        b2.insert(0, item_info[3])
        x1 = Label(temp_win, text='description',padx=50)
        x1.grid(row=2, column=0)
        x2 = Entry(temp_win, width=50, borderwidth=5)
        x2.grid(row=2, column=1)
        x2.insert(0, item_info[2])
        c1 = Label(temp_win, text='diametre_nominale(mm)',padx=50)
        c1.grid(row=3, column=0)
        c2 = Entry(temp_win, width=50, borderwidth=5)
        c2.grid(row=3, column=1)
        c2.insert(0, item_info[4])
        d1 = Label(temp_win, text='pression_nominale(bar)',padx=50)
        d1.grid(row=4, column=0)
        d2 = Entry(temp_win, width=50, borderwidth=5)
        d2.grid(row=4, column=1)
        d2.insert(0, item_info[5])
        e1 = Label(temp_win, text='KVS',padx=50)
        e1.grid(row=5, column=0)
        e2 = Entry(temp_win, width=50, borderwidth=5)
        e2.grid(row=5, column=1)
        e2.insert(0, item_info[6])
        g1 = Label(temp_win, text='frequence(Hz)',padx=50)
        g1.grid(row=6, column=0)
        g2 = Entry(temp_win, width=50, borderwidth=5)
        g2.grid(row=6, column=1)
        g2.insert(0, item_info[7])
        i1 = Label(temp_win, text='nb_disponible',padx=50)
        i1.grid(row=7, column=0)
        i2 = Entry(temp_win, width=50, borderwidth=5)
        i2.grid(row=7, column=1)
        i2.insert(0, item_info[8])
        temp_Button1 = Button(temp_win, text="Confirm", command=lambda: confirm(a2,b2,x2,c2,d2,e2,g2,i2,id.get(), temp_win))
        temp_Button1.grid(row=8, column=1)
        temp_Button1 = Button(temp_win, text="Cancel", command=temp_win.destroy)
        temp_Button1.grid(row=8, column=2)

def update_item():
    update_win = Toplevel()
    update_win.title("item selection")
    a1 = Label(update_win, text="input the item id", padx=50)
    a1.grid(row=0, column=0)
    a2 = Entry(update_win, width=50, borderwidth=5)
    a2.grid(row=0, column=1)
    a3 = Button(update_win, text="update", command=lambda: update(a2))
    a3.grid(row=0, column=2)

"""def delete(id, window):
    if int(id.get()) not in ids:
        messagebox.showerror("error", "no item with the id {} was found".format(id.get()))
    else:
        conn = sql.connect("first1.db")
        cur = conn.cursor()
        req = "DELETE FROM stock WHERE id = {}".format(id.get())
        cur.execute(req)
        conn.commit()
        id.delete(0, END)
        msg= Label(window, text="item was deleted successfully", bg="#4BB543", fg="white")
        msg.grid(row=11, column=0, columnspan=3)

def delete_item():
    deletion_win = Toplevel()
    deletion_win.title("item deletion")
    a1 = Label(deletion_win, text="input the item id", padx=50)
    a1.grid(row=0, column=0)
    a2 = Entry(deletion_win, width=50, borderwidth=5)
    a2.grid(row=0, column=1)
    a3 = Button(deletion_win, text="Delete", command=lambda: delete(a2, deletion_win))
    a3.grid(row=0, column=2)"""

def search(model):
    conn = sql.connect("first1.db")
    cur = conn.cursor()
    req = "SELECT * FROM stock"
    cur.execute(req)
    global item_list
    global total_columns
    global total_rows
    item_list1 = cur.fetchall()
    item_list = []
    for i in item_list1:
        if i[1] == str(model):
            item_list.append(i)
    item_list = [list(i) for i in item_list]
    item_list.insert(0, ['id', 'model', 'ref','description', 'diametre nominale(m)', 'pression nominale(bar)', 'KVS', 'frequence(Hz)','nb_disponible'])
    total_rows = len(item_list)+1
    total_columns = len(item_list[0])
    gui = Toplevel()
    gui.title('stock')
    table = Table(gui)
    note = Label(gui, text="Note that changes to this table have no effect on the actual database!")
    note.grid(row=total_rows+1, column=0, columnspan=3)

def model_confirmation2(model, l):
    l.insert(0, model.get())
    selection_win.destroy()

def select(l):
    global selection_win
    selection_win = Toplevel()
    selection_win.title("Selection window")
    cur.execute("SELECT DISTINCT model FROM stock")
    model_list = cur.fetchall()
    models = [(i[0],i[0]) for i in model_list]
    model = StringVar()
    for text, modell in models:
        Radiobutton(selection_win, text=text, variable=model, value=modell).pack(anchor=W)
    conf = Button(selection_win, text="confirm", command=lambda: model_confirmation2(model, l)).pack()

def model_search():
    temp_win = Toplevel()
    a1 = Label(temp_win, text="search for a specific model")
    a1.grid(row=0, column=0)
    a2 = Entry(temp_win, width=50, borderwidth=5)
    a2.grid(row=0, column=1)
    a3 = Button(temp_win, text="select", command=lambda: select(a2))
    a3.grid(row=0, column=2)
    a4 = Button(temp_win, text="search", command=lambda: search(str(a2.get())))
    a4.grid(row=1, column=2)

space0 = Label(root, text="  ", pady=2)
space0.pack()

myButton1 = Button(root, text="Add item", command=new_item)
myButton1.config(width=30)
myButton1.pack()

space1 = Label(root, text="  ", pady=2)
space1.pack()

myButton2 = Button(root, text="Show table", command=show_table)
myButton2.config(width=30)
myButton2.pack()

space2 = Label(root, text="  ", pady=2)
space2.pack()

myButton3 = Button(root, text="update item values", command=update_item)
myButton3.config(width=30)
myButton3.pack()

space3 = Label(root, text="  ", pady=2)
space3.pack()

myButton4 = Button(root, text="search for model", command=model_search)
myButton4.config(width=30)
myButton4.pack()

"""space4 = Label(root, text="  ", pady=2)
space4.pack()

myButton5 = Button(root, text="Delete item", command=delete_item)
myButton5.config(width=30)
myButton5.pack()
"""
root.mainloop()