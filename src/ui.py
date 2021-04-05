from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import json
import encryption
import passwordAnalysis
import time
import inspect
import pyperclip
import scribble
import os


class View:
    def __init__(self):
        self.closeFlag = False
        pass


    def main_popup(self, root):
        self.root = root

        self.tree = ttk.Treeview(self.root, selectmode='browse')
        self.tree.pack(side='left')
        self.tree.bind("<Button-2>", self.popup) # Right click for mac
        self.tree.bind("<Button-3>", self.popup) # Right click for windows/linux

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
        self.popup_menu.add_command(label="View/Edit Info",command=self.edit_selected_popup)
        self.popup_menu.add_command(label="Clone",command=self.clone_selected)
        self.popup_menu.add_command(label="Delete",command=self.delete_selected)
        self.popup_menu.add_command(label="Copy Username",command=self.copy_selected_username)
        self.popup_menu.add_command(label="Copy Password",command=self.copy_selected_password)
        self.popup_menu.add_command(label="Export Password",command=self.export_selected_password_popup)

        self.popup_menu2 = Menu(self.root, tearoff=0)
        self.popup_menu2.add_command(label="New Entry",command=self.insert_item_popup)

        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Entry", command=self.insert_item_popup)
        self.filemenu.add_command(label="Generate Password", command=self.generate_password_popup)
        self.filemenu.add_command(label="Change Master Password", command=self.change_master_popup)
        self.filemenu.add_command(label="Import Password",command=self.import_selected_password_popup)
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

    def changemaster(self, event=None):
        newpass = self.changeText3.get("1.0", END).strip("\n")

        rawdata = encryption.file_decrypter("data.txt", self.masterkey)

        data = rawdata["data"]

        newdata = []


        for i in range(len(data)):
            newdata.append({"id":data[i]["id"], "title":encryption.encrypt(encryption.decrypt(data[i]["title"], self.masterkey),newpass), "username":encryption.encrypt(encryption.decrypt(data[i]["username"], self.masterkey),newpass), "password":encryption.encrypt(encryption.decrypt(data[i]["password"], self.masterkey),newpass), "url":encryption.encrypt(encryption.decrypt(data[i]["url"], self.masterkey),newpass), "notes":encryption.encrypt(encryption.decrypt(data[i]["notes"], self.masterkey),newpass)})

        self.masterkey = newpass
        rawdata["data"] = newdata



        with open('data.txt', 'w') as outfile:
            json.dump(rawdata, outfile)
        encryption.file_encrypter('data.txt', self.masterkey)


        self.changePopup.destroy()
        messagebox.showinfo("Password Change", "Password changed successfully")


    def beforechange(self):

        if self.changeText1.get("1.0", END).strip("\n") != self.masterkey:
            self.changeText1.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            messagebox.showwarning("Incorrect Passwords", "The password you entered is incorrect.")
            self.changePopup.focus_force()
            return
        else:
            self.changeText1.config(highlightbackground = "gray", highlightcolor= "gray", highlightthickness=1)


        if self.changeText3.get("1.0", END) != self.changeText2.get("1.0", END):
            self.changeText3.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            self.changeText2.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            messagebox.showwarning("Mismatched Passwords", "The entered passwords are not the same.")
            self.changePopup.focus_force()
            return
        else:
            self.changeText3.config(highlightbackground = "gray", highlightcolor= "gray", highlightthickness=1)
            self.changeText2.config(highlightbackground = "gray", highlightcolor= "gray", highlightthickness=1)

        self.changemaster()


    def change_master_popup(self):
        popup = Tk()
        popup.wm_title("Change Master Password")

        self.changePopup = popup

        label1 = ttk.Label(popup, text="Current Password").grid(row=1, column=0, padx=10, pady=10)
        self.changeText1 = Text(popup, height=1)
        self.changeText1.grid(row=1, column=1, padx=10, pady=10)

        label1 = ttk.Label(popup, text="New Password").grid(row=2, column=0, padx=10, pady=10)
        self.changeText2 = Text(popup, height=1)
        self.changeText2.grid(row=2, column=1, padx=10, pady=10)

        label1 = ttk.Label(popup, text="Confirm New Password").grid(row=3, column=0, padx=10, pady=10)
        self.changeText3 = Text(popup, height=1)
        self.changeText3.grid(row=3, column=1, padx=10, pady=10)

        B1 = ttk.Button(popup, text="Ok", command = lambda:[self.beforechange()]).grid(row=2, column=2)
        B2 = ttk.Button(popup, text="Cancel", command = lambda:[popup.destroy()]).grid(row=2, column=3)
        popup.mainloop()

    def masterkey_popup(self):
        popup = Tk()
        popup.wm_title("Enter Master Password")
        popup.bind('<Return>', self.setmaster)

        self.firstPopup = popup;

        label2 = ttk.Label(popup, text="Welcome to the password manager \nIf this is your first time, set your master password otherwise enter your existing one.\n To complete setup of your master password atleast one entry must be entered.").grid(row=0, column=1, padx=10, pady=10)

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


    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


    def donothing(self):
       pass


    def on_closing(self):
        """
        Asks for confirmation on trying to close
        """

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.force_close()


    def force_close(self):
        """
        Closes the program
        """

        self.closeflag = True
        try:
            self.newPopup.destroy()
        except:
            pass

        try:
            self.entry["popup"].destroy()
        except:
            pass

        try:
            self.generate["popup"].destroy()
        except:
            pass

        try:
            self.firstPopup.destroy()
        except:
            pass

        try:
            self.importPopup.destroy()
        except:
            pass

        try:
            self.exportPopup.destroy()
        except:
            pass

        try:
            self.changePopup.destroy()
        except:
            pass

        self.root.destroy()


    def delete_selected(self):
        item = self.tree.item(self.tree.focus())
        self.tree.delete(self.tree.focus())
        self.deletePassword(item["text"])

    def copy_selected_password(self):
        item = self.tree.item(self.tree.focus())
        item2 = self.getByID(item["text"])
        password = encryption.decrypt(item2["password"], self.masterkey)
        pyperclip.copy(password)

    def copy_selected_username(self):
        item = self.tree.item(self.tree.focus())
        pyperclip.copy(item["values"][1])

    def export_selected_password(self, extraarg=None):
        pin = self.pinText.get("1.0", END).strip("\n")
        item = self.tree.item(self.tree.focus())

        filename = datetime.now()
        format_string = "%y-%m-%d_%H.%M.%S"
        filename = filename.strftime(format_string)
        filename = filename + ".txt"

        scribble.export_pw(item["text"],filename, self.masterkey, pin)
        self.exportPopup.destroy()


    def export_selected_password_popup(self):
        popup = Tk()
        popup.wm_title("Export Password")
        popup.bind('<Return>', self.export_selected_password)

        self.exportPopup = popup;

        label3 = ttk.Label(popup, text="You can find exported passwords in the location this program is run in a folder called exportedpasswords.").grid(row=0, column=1, padx=10, pady=10)
        label2 = ttk.Label(popup, text="Choose a temporary passsword/pin to give to the other user.").grid(row=1, column=1, padx=10, pady=10)
        label1 = ttk.Label(popup, text="Password/Pin").grid(row=2, column=0, padx=10, pady=10)
        self.pinText = Text(popup, height=1)
        self.pinText.grid(row=2, column=1, padx=10, pady=10)

        B1 = ttk.Button(popup, text="Ok", command = lambda:[self.export_selected_password()]).grid(row=3, column=2)
        B2 = ttk.Button(popup, text="Cancel", command = lambda:[popup.destroy()]).grid(row=3, column=3)

        popup.mainloop()

    def browse_button(self, extraarg=None):
        path = os.getcwd()
        filename = filedialog.askopenfilename(initialdir = path,
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

        self.filename = filename
        self.import_selected_password()

    def import_selected_password(self):
        pin = self.importPinText.get("1.0", END).strip("\n")
        try:
            data = scribble.import_pw(self.filename, self.masterkey, pin)
            self.importPopup.destroy()
            self.tree.insert("",1, text=data['id'], values=(encryption.decrypt(data['title'], self.masterkey), encryption.decrypt(data['username'], self.masterkey) ,encryption.decrypt(data['url'], self.masterkey), passwordAnalysis.passwordStrength(encryption.decrypt(data['password'], self.masterkey))))
        except Exception as e:
            messagebox.showerror("Wrong Passwords", "The password you entered is wrong!")

    def import_selected_password_popup(self):
        popup = Tk()
        popup.wm_title("Import Password")
        popup.bind('<Return>', self.browse_button)

        self.importPopup = popup;

        label3 = ttk.Label(popup, text="Insert pin/password given to you.").grid(row=0, column=1, padx=10, pady=10)


        label1 = ttk.Label(popup, text="Password/Pin").grid(row=1, column=0, padx=10, pady=10)
        self.importPinText = Text(popup, height=1)
        self.importPinText.grid(row=1, column=1, padx=10, pady=10)

        B1 = ttk.Button(popup, text="Select File", command = lambda:[self.browse_button()]).grid(row=2, column=2)
        B2 = ttk.Button(popup, text="Cancel", command = lambda:[popup.destroy()]).grid(row=2, column=3)
        popup.mainloop()

    def insert_item_popup(self):
        """
        Used for adding a new entry into the table
        """

        self.entry_popup()


    def edit_selected_popup(self):
        """
        Used for editing an existing entry in the table
        """

        rawitem = self.tree.focus()
        item = self.tree.item(self.tree.focus())
        item2 = self.getByID(item["text"])

        # Retreives the values for the existing entry
        title = encryption.decrypt(item2["title"], self.masterkey)
        username = encryption.decrypt(item2["username"], self.masterkey)
        password = encryption.decrypt(item2["password"], self.masterkey)
        url = encryption.decrypt(item2["url"], self.masterkey)
        notes = encryption.decrypt(item2["notes"], self.masterkey)

        # Creates an entry popup with prefilled fields
        self.entry_popup(title=title, username=username,
                        password=password, url=url,
                        notes=notes, focus=True)


    def entry_popup(self, title="", username="", password="", url="", notes="", focus=False):
        """
        Defines the popup for creating/editing password entries
        the feilds populate the text fields with the existing values
        """

        if focus:
            rawitem = self.tree.focus()
        else:
            rawitem = None

        fields = [
            ("title", title),
            ("username", username),
            ("password", password),
            ("confirmation", password),
            ("url", url),
            ("notes", notes)
        ]

        self.entry = {}
        self.entry["popup"] = Tk()
        self.entry["popup"].wm_title("Edit Entry")

        # Creates a label and textbox for each field
        for i in range(len(fields)):
            ttk.Label(self.entry["popup"], text=fields[i][0].capitalize()).grid(row=i, column=0, padx=10, pady=10)
            self.entry[fields[i][0]] = Text(self.entry["popup"], height=1)
            self.entry[fields[i][0]].grid(row=i, column=1, padx=10, pady=10)
            self.entry[fields[i][0]].bind("<Tab>", self.focus_next_widget)
            self.entry[fields[i][0]].insert(END,fields[i][1])

        generateButton = ttk.Button(self.entry["popup"], text="Generate Password", command = lambda: [self.generate_password_popup(self.entry)] ).grid(row=2, column=3)
        B1 = ttk.Button(self.entry["popup"], text="Ok", command = lambda:[self.confirm_entry(rawitem)]).grid(row=6, column=2)
        B2 = ttk.Button(self.entry["popup"], text="Cancel", command = lambda:[self.entry["popup"].destroy()]).grid(row=6, column=3)

        self.entry["popup"].mainloop()


    def confirm_entry(self, rawitem):
        """
        Makes sure fields are valid
        If so, it stores and saves the values, and closes the entry popup
        """

        if self.entry["password"].get("1.0", END) != self.entry["confirmation"].get("1.0", END):
            self.entry["password"].config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            self.entry["confirmation"].config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            messagebox.showwarning("Mismatched Passwords", "The entered passwords are not the same.")
            self.entry["popup"].focus_force()
            return

        title = self.entry["title"].get("1.0", END+"-1c")
        username = self.entry["username"].get("1.0", END+"-1c")
        password = self.entry["password"].get("1.0", END+"-1c")
        url = self.entry["url"].get("1.0", END+"-1c")
        notes = self.entry["notes"].get("1.0", END+"-1c")

        if len(title) <= 0:
            title = "Untitled"

        if rawitem is not None:
            item = self.tree.item(rawitem)
            id = item["text"]
            with open('data.txt') as json_file:
                try:
                    data = encryption.file_decrypter('data.txt', self.masterkey)
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
            encryption.file_encrypter('data.txt', self.masterkey)

            self.tree.insert("",1, text=id, values=(title,username,url,passwordAnalysis.passwordStrength(password)))
            self.tree.delete(rawitem)
        else:
            uuid = self.writePassword(title, username, password, url, notes)
            self.tree.insert("",1, text=uuid, values=(title,username,url,passwordAnalysis.passwordStrength(password)))

        self.entry["popup"].destroy()
        self.root.update()


    def clone_selected(self):
        item = self.tree.item(self.tree.focus())

        item2 = self.getByID(item["text"])

        self.writePassword(item2['title'], item2['username'], item2['password'], item2['url'], item2['notes'])
        self.tree.insert("",1, text=self.getLastID(), values=item["values"])

    def generate_password_popup(self, parentWindow=None):
        """
        Creates a popup for generating passwords

        """

        self.generate = {}
        self.generate["popup"] = Tk()
        self.generate["popup"].wm_title("Generate Password")

        signature = inspect.signature(passwordAnalysis.generatePassword)
        signatureMem = inspect.signature(passwordAnalysis.generateMemorablePassword)
        items = list(signature.parameters.items())
        items.insert(1, ('words', signatureMem.parameters["words"]))

        self.generate["password"] = Text(self.generate["popup"], height=1)
        self.generate["password"].grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.generate["password"].bind("<Tab>", self.focus_next_widget)
        self.generate["password"].insert(END, passwordAnalysis.generatePassword())

        pos = 0
        initialRow = 3
        value = {}
        for k, v in items:
            if k == "length" or k == "words":
                # Creates the length slider
                self.generate[k] = Scale(self.generate["popup"], from_=1, to=60, orient=HORIZONTAL, label=k)
                self.generate[k].grid(row=initialRow+pos//2, column=pos%2, padx=10, pady=10)
                self.generate[k].set(v.default)
                value[k] = self.generate[k].get
            else:
                # Creates checkboxes for the flags, and sets them to the default value
                var = BooleanVar()
                self.generate[k] = ttk.Checkbutton(self.generate["popup"], text=k[3:], onvalue=True, offvalue=False, variable=var)
                self.generate[k].grid(row=initialRow+pos//2, column=pos%2, padx=10, pady=10)
                value[k] = lambda x=self.generate[k]: x.instate(['selected'])
                self.generate[k].state(['!alternate'])
                if v.default:
                    self.generate[k].state(['selected'])
                else:
                    self.generate[k].state(['!selected'])
            pos = pos+1

        ttk.Button(self.generate["popup"], text="Generate", command = lambda: self.generatePassword(value, self.generate["password"])).grid(row=1, column=0, columnspan=1)
        ttk.Button(self.generate["popup"], text="Generate Memorable", command = lambda: self.generateMemPassword(value, self.generate["password"])).grid(row=1, column=1, columnspan=1)
        ttk.Button(self.generate["popup"], text="Ok", command = lambda: self.generate_password_confirm(parentWindow)).grid(row=initialRow+1+pos//2, column=0)
        ttk.Button(self.generate["popup"], text="Cancel", command = lambda:[self.generate["popup"].destroy()]).grid(row=initialRow+1+pos//2, column=1)

        self.generate["popup"].mainloop()

    def generatePassword(self, dict, text):
        """
        Generates a password using the current values in the UI
        """

        text.delete(1.0,"end")
        signature = inspect.signature(passwordAnalysis.generatePassword)
        newDict = {}
        for k, v in signature.parameters.items():
            print('k: '+ str(k))
            print('v: '+ str(dict[k]()))
            newDict[k] = dict[k]()
        password = passwordAnalysis.generatePassword(**newDict)
        text.insert(1.0, password)

    def generateMemPassword(self, dict, text):
        """
        Generates a memorable password using the current values in the UI
        """

        text.delete(1.0,"end")

        characterPool = []
        if dict['hasDigits']():
            characterPool += list('1234567890')
        if dict['hasBasicSymbols']():
            characterPool += list("~!@#$%^&*_-+=,.?")
        if dict['hasAdvancedSymbos']():
            characterPool += list("<>{}[]()")

        password = passwordAnalysis.generateMemorablePassword(words=dict['words'](), hasCapitals=dict['hasCapitals'], paddingType=characterPool)
        text.insert(1.0, password)

    def generate_password_confirm(self, parentWindow):
        """
        Puts the password on the clipboard
        if an entry popup is open, it writes to its fields as well
        """

        password = self.generate["password"].get("1.0", END+"-1c")

        # copies password to clipboard
        self.generate["popup"].clipboard_clear()
        self.generate["popup"].clipboard_append(password)
        self.generate["popup"].update()

        # Writes the password to the parent entry popup, if there is one
        if parentWindow is not None:
            parentWindow["password"].delete(1.0,"end")
            parentWindow["confirmation"].delete(1.0,"end")

            parentWindow["password"].insert(1.0, password)
            parentWindow["confirmation"].insert(1.0, password)

        self.generate["popup"].destroy()


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
        # creates file if not exists
        with open('data.txt', 'a') as json_file:
            pass

#JSONDecodeError

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = encryption.file_decrypter('data.txt', self.masterkey)
                return data['data']
            except Exception as e:
                if e.args[0] == "Padding is incorrect.":
                    messagebox.showerror("Wrong Passwords", "The password you entered is wrong!")
                    self.force_close()
        return []

    def getByID(self, id):
        # creates file if not exists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = encryption.file_decrypter('data.txt', self.masterkey)
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
                data = encryption.file_decrypter('data.txt', self.masterkey)
                arr = data['data']
                id = arr[len(arr) - 1]["id"]
                return id
            except Exception as e:
                print(e)
        return -1


    def deletePassword(self, id):
        # with open('data.txt', 'r') as data_file:
        #     data = json.load(data_file)
        data = encryption.file_decrypter('data.txt', self.masterkey)
        arr = data['data']

        for i in range(len(arr)):
            if arr[i]['id'] == id:
                arr.pop(i)
                break

        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
        encryption.file_encrypter('data.txt', self.masterkey)

    def writePassword(self, title, username, password, url, notes=""):

        data = {}
        data['data'] = []
        id = 1

        # creates file if not exists
        with open('data.txt', 'a') as json_file:
            pass

        # gets data from file if its there
        with open('data.txt') as json_file:
            try:
                data = encryption.file_decrypter('data.txt', self.masterkey)
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
        encryption.file_encrypter('data.txt', self.masterkey)

        return id
