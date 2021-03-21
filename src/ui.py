from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import encryption
import passwordAnalysis
import time


class View:
    def __init__(self):
        self.closeFlag = False
        pass


    def main_popup(self, root):
        self.root = root

        self.tree = ttk.Treeview(self.root, selectmode='browse')
        self.tree.pack(side='left')
        self.tree.bind("<Button-2>", self.popup)
        self.tree.bind("<Button-3>", self.popup)

        self.vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree["columns"]=("one","two","three", "four")
        self.tree.column("#0", width=30, minwidth=30, stretch=NO)
        self.tree.column("one", width=180, minwidth=180, stretch=NO)
        self.tree.column("two", width=180, minwidth=180, stretch=NO)
        self.tree.column("three", width=400, minwidth=200, stretch=NO)
        self.tree.column("four", width=180, minwidth=180, stretch=NO)

        self.tree.heading("#0",text="ID",anchor=W)
        self.tree.heading("one", text="Title",anchor=W)
        self.tree.heading("two", text="Username",anchor=W)
        self.tree.heading("three", text="URL",anchor=W)
        self.tree.heading("four", text="Strength",anchor=W)

        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Delete",command=self.delete_selected)
        self.popup_menu.add_command(label="Clone",command=self.clone_selected)
        self.popup_menu.add_command(label="View/Edit Info",command=self.edit_selected_popup)

        self.popup_menu2 = Menu(self.root, tearoff=0)
        self.popup_menu2.add_command(label="New Entry",command=self.insert_item_popup)

        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Entry", command=self.insert_item_popup)
        self.filemenu.add_command(label="Change Master Password", command=self.change_master_popup)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


        arr = self.getAll()

        try:
            for i in range(len(arr)):
                self.tree.insert("",1, text=arr[i]['id'], values=(encryption.decrypt(arr[i]['title'], self.masterkey), encryption.decrypt(arr[i]['username'], self.masterkey) ,encryption.decrypt(arr[i]['url'], self.masterkey), passwordAnalysis.passwordStrength(encryption.decrypt(arr[i]['password'], self.masterkey))))
        except Exception as e:
            print(e)

            if self.closeFlag:
                messagebox.showerror("Wrong Passwords", "The password you entered is wrong!")
                self.force_close()
            else:
                self.force_close()


    def setmaster(self, event=None):
        self.masterkey = self.passwordText1.get("1.0", END).strip("\n")
        self.firstPopup.destroy()



    def change_master_popup(self):
        pass

    def masterkey_popup(self):
        popup = Tk()
        popup.wm_title("Enter Master Password")
        popup.bind('<Return>', self.setmaster)

        self.firstPopup = popup;

        label2 = ttk.Label(popup, text="Welcome to the password manager \nIf this is your first time, set your master password otherwise enter your exsisting one").grid(row=0, column=1, padx=10, pady=10)

        label1 = ttk.Label(popup, text="Password").grid(row=1, column=0, padx=10, pady=10)
        self.passwordText1 = Text(popup, height=1)
        self.passwordText1.grid(row=1, column=1, padx=10, pady=10)


        B1 = ttk.Button(popup, text="Ok", command = lambda:[self.setmaster()]).grid(row=2, column=2)

        B2 = ttk.Button(popup, text="Cancel", command = lambda:[self.force_close()]).grid(row=2, column=3)

        popup.mainloop()

    def insert_item(self):

        if self.newText3.get("1.0", END) != self.newText4.get("1.0", END):
            self.newText3.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            self.newText4.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            messagebox.showwarning("Mismatched Passwords", "The entered passwords are not the same.")
            self.newPopup.focus_force()
            return

        title = ""
        username = self.newText2.get("1.0", END)
        password = self.newText3.get("1.0", END)
        url = self.newText5.get("1.0", END)
        notes = self.newText6.get("1.0", END)

        if len(self.newText1.get("1.0", END)) <= 1:
            title = "Untitled"
        else:
            title = self.newText1.get("1.0", END)

        self.newPopup.destroy()
        uuid = self.writePassword(title, username, password, url, notes)
        self.tree.insert("",1, text=uuid, values=(title,username,url,passwordAnalysis.passwordStrength(password)))
        self.root.update()

    def insert_item_popup(self):
        self.entry_popup()


    def donothing(self):
       pass


    def force_close(self):
        self.closeflag = True
        try:
            self.newPopup.destroy()
        except:
            pass

        try:
            self.entryPopup.destroy()
        except:
            pass

        try:
            self.firstPopup.destroy()
        except:
            pass

        self.root.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):

            try:
                self.newPopup.destroy()
            except:
                pass

            try:
                self.entryPopup.destroy()
            except:
                pass

            try:
                self.firstPopup.destroy()
            except:
                pass

            self.root.destroy()

    def delete_selected(self):
        item = self.tree.item(self.tree.focus())
        self.tree.delete(self.tree.focus())
        self.deletePassword(item["text"])

    def confirm_entry(self, rawitem):

        if self.entryPassword.get("1.0", END) != self.entryConfirm.get("1.0", END):
            self.entryPassword.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            self.entryConfirm.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            messagebox.showwarning("Mismatched Passwords", "The entered passwords are not the same.")
            self.entryPopup.focus_force()
            return

        title = self.entryTitle.get("1.0", END+"-1c")
        username = self.entryUsername.get("1.0", END+"-1c")
        password = self.entryPassword.get("1.0", END+"-1c")
        url = self.entryURL.get("1.0", END+"-1c")
        notes = self.entryNotes.get("1.0", END+"-1c")

        if len(title) <= 0:
            title = "Untitled"

        if rawitem is not None:
            item = self.tree.item(rawitem)
            id = item["text"]
            with open('data.txt') as json_file:
                try:
                    data = json.load(json_file)
                    arr = data['data']
                    for i in range(len(arr)):
                        if arr[i]['id'] == id:
                            arr[i]['title'] = encryption.encrypt(title, self.masterkey)
                            arr[i]['username'] = encryption.encrypt(username, self.masterkey)
                            arr[i]['password'] = encryption.encrypt(password, self.masterkey)
                            arr[i]['url'] = encryption.encrypt(url, self.masterkey)
                            arr[i]['notes'] = encryption.encrypt(notes, self.masterkey)
                except Exception as e:
                    print(e)

            with open('data.txt', 'w') as outfile:
                json.dump(data, outfile)

            self.tree.insert("",1, text=id, values=(title,username,url,passwordAnalysis.passwordStrength(password)))
            self.tree.delete(rawitem)
        else:
            uuid = self.writePassword(title, username, password, url, notes)
            self.tree.insert("",1, text=uuid, values=(title,username,url,passwordAnalysis.passwordStrength(password)))

        self.entryPopup.destroy()
        self.root.update()


    def edit_selected_popup(self):

        rawitem = self.tree.focus()
        item = self.tree.item(self.tree.focus())
        item2 = self.getByID(item["text"])

        title = encryption.decrypt(item2["title"], self.masterkey)
        username = encryption.decrypt(item2["username"], self.masterkey)
        password = encryption.decrypt(item2["password"], self.masterkey)
        url = encryption.decrypt(item2["url"], self.masterkey)
        notes = encryption.decrypt(item2["notes"], self.masterkey)

        self.entry_popup(title=title, username=username,
                        password=password, url=url,
                        notes=notes, focus=True)



    def entry_popup(self, title="", username="", password="", url="", notes="", focus=False):
        if focus:
            rawitem = self.tree.focus()
        else:
            rawitem = None
        item = self.tree.item(self.tree.focus())
        item2 = self.getByID(item["text"])

        popup = Tk()
        popup.wm_title("Edit Entry")

        self.entryPopup = popup

        label1 = ttk.Label(popup, text="Title").grid(row=0, column=0, padx=10, pady=10)
        self.entryTitle = Text(popup, height=1)
        self.entryTitle.grid(row=0, column=1, padx=10, pady=10)
        self.entryTitle.insert(END,title)

        label2 = ttk.Label(popup, text="Username").grid(row=1, column=0, padx=10, pady=10)
        self.entryUsername = Text(popup, height=1)
        self.entryUsername.grid(row=1, column=1, padx=10, pady=10)
        self.entryUsername.insert(END,username)

        label3 = ttk.Label(popup, text="Password").grid(row=2, column=0, padx=10, pady=10)
        self.entryPassword = Text(popup, height=1)
        self.entryPassword.grid(row=2, column=1, padx=10, pady=10)
        self.entryPassword.insert(END,password)

        label4 = ttk.Label(popup, text="Repeat").grid(row=3, column=0, padx=10, pady=10)
        self.entryConfirm = Text(popup, height=1)
        self.entryConfirm.grid(row=3, column=1, padx=10, pady=10)
        self.entryConfirm.insert(END,password)

        label5 = ttk.Label(popup, text="URL").grid(row=4, column=0, padx=10, pady=10)
        self.entryURL = Text(popup, height=1)
        self.entryURL.grid(row=4, column=1, padx=10, pady=10)
        self.entryURL.insert(END,url)

        label6 = ttk.Label(popup, text="Notes").grid(row=5, column=0, padx=10, pady=10)
        self.entryNotes = Text(popup, height=5)
        self.entryNotes.grid(row=5, column=1, padx=10, pady=10)
        self.entryNotes.insert(END,notes)

        B1 = ttk.Button(popup, text="Ok", command = lambda:[self.confirm_entry(rawitem)]).grid(row=6, column=2)

        B2 = ttk.Button(popup, text="Cancel", command = lambda:[popup.destroy()]).grid(row=6, column=3)

        popup.mainloop()


    def clone_selected(self):
        item = self.tree.item(self.tree.focus())

        item2 = self.getByID(item["text"])

        self.writePassword(item2['title'], item2['username'], item2['password'], item2['url'], item2['notes'])
        self.tree.insert("",1, text=self.getLastID(), values=item["values"])

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

    def getAll(self):
        # creates file if not exsists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = json.load(json_file)
                return data['data']
            except Exception as e:
                print(e)

        return []

    def getByID(self, id):
        # creates file if not exsists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = json.load(json_file)
                arr = data['data']
                for i in range(len(arr)):
                    if(arr[i]['id'] == id):
                        return arr[i]
            except Exception as e:
                print(e)

    def getLastID(self):
        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = json.load(json_file)
                arr = data['data']
                id = arr[len(arr) - 1]["id"]
                return id
            except Exception as e:
                print(e)
        return -1


    def deletePassword(self, id):
        with open('data.txt', 'r') as data_file:
            data = json.load(data_file)

        arr = data['data']

        for i in range(len(arr)):
            if arr[i]['id'] == id:
                arr.pop(i)
                break

        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

    def writePassword(self, title, username, password, url, notes=""):

        data = {}
        data['data'] = []
        id = 1

        # creates file if not exsists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = json.load(json_file)
                arr = data['data']
                id = arr[len(arr) - 1]["id"]
                id = id + 1
            except Exception as e:
                print(e)

        # appends new password
        data['data'].append({"id":id, "title":encryption.encrypt(title,self.masterkey), "username":encryption.encrypt(username,self.masterkey), "password":encryption.encrypt(password,self.masterkey), "url":encryption.encrypt(url,self.masterkey), "notes":encryption.encrypt(notes, self.masterkey)})

        # writes new password
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

        return id
