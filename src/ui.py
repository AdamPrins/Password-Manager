from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class View:
    def __init__(self, root):

        self.root = root

        self.tree = ttk.Treeview(self.root, selectmode='browse')
        self.tree.pack(side='left')
        self.tree.bind("<Button-3>", self.popup)

        self.vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree["columns"]=("one","two","three")
        self.tree.column("#0", width=180, minwidth=180, stretch=NO)
        self.tree.column("one", width=180, minwidth=180, stretch=NO)
        self.tree.column("two", width=400, minwidth=200, stretch=NO)

        self.tree.heading("#0",text="Title",anchor=W)
        self.tree.heading("one", text="Username",anchor=W)
        self.tree.heading("two", text="URL",anchor=W)

        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Delete",command=self.delete_selected)
        self.popup_menu.add_command(label="Clone",command=self.clone_selected)

        self.popup_menu2 = Menu(self.root, tearoff=0)
        self.popup_menu2.add_command(label="New Entry",command=self.insert_item_popup)

        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Entry", command=self.insert_item_popup)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.itemPopup = None
        self.text1 = None
        self.text2 = None
        self.text3 = None
        self.text4 = None
        self.text5 = None
        self.text6 = None

    def insert_item(self, item):

        if len(self.text1.get("1.0", END)) <= 1:
            pass


        self.tree.insert("",1, text="Entry Title", values=("username","http://www.google.com"))
        self.root.update()

    def insert_item_popup(self):
        popup = Tk()
        popup.wm_title("New Entry")

        self.itemPopup = popup

        label1 = ttk.Label(popup, text="Title").grid(row=0, column=0)
        self.text1 = Text(popup, height=1)
        self.text1.grid(row=0, column=1)


        label2 = ttk.Label(popup, text="Username").grid(row=1, column=0)
        self.text2 = Text(popup, height=1)
        self.text2.grid(row=1, column=1)

        label3 = ttk.Label(popup, text="Password").grid(row=2, column=0)
        self.text3 = Text(popup, height=1)
        self.text3.grid(row=2, column=1)
        button1 = ttk.Button(popup, text="Generate Password", command = self.donothing).grid(row=2, column=2)

        label4 = ttk.Label(popup, text="Repeat").grid(row=3, column=0)
        self.text4 = Text(popup, height=1)
        self.text4.grid(row=3, column=1)

        label5 = ttk.Label(popup, text="URL").grid(row=4, column=0)
        self.text5 = Text(popup, height=1)
        self.text5.grid(row=4, column=1)

        label6 = ttk.Label(popup, text="Notes").grid(row=5, column=0)
        self.text6 = Text(popup, height=5)
        self.text6.grid(row=5, column=1)

        item = "test"

        B1 = ttk.Button(popup, text="Ok", command = lambda:[self.insert_item(item), popup.destroy()]).grid(row=6, column=2)

        B2 = ttk.Button(popup, text="Cancel", command = lambda:[popup.destroy()]).grid(row=6, column=3)

        popup.mainloop()


    def donothing(self):
       x = 0

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.itemPopup.destroy()
            except:
                pass

            self.root.destroy()

    def delete_selected(self):
        self.tree.delete(self.tree.focus())

    def clone_selected(self):
        item = self.tree.item(self.tree.focus())

        print(item["values"])

        self.tree.insert("",1, text=item['text'], values=item["values"])

    def popup(self, event):
        """action in event of button 3 on tree view"""

        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.tree.focus(iid)
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            self.popup_menu2.tk_popup(event.x_root, event.y_root, 0)
            pass

    def writePassword(self, username, password, website, info=""):

        data = {}
        data['data'] = []

        # creates file if not exsists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = json.load(json_file)
            except:
                pass

        # appends new password
        data['data'].append({"title":title, "username":username, "password":password, "website":website, "info":info})

        # writes new password
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
