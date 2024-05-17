import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Grocery Billing System")

        # Label to display the background image
        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1200, height=600)
        self.img = PhotoImage(file="./image/Judul.png")  
        self.label1.configure(image=self.img)

        # Inventory button
        self.button_inventory = Button(root, text="Inventory", command=self.open_inventory)
        self.button_inventory.place(relx=0.240, rely=0.650, width=107, height=50)
        self.button_inventory.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button_inventory.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 17 -weight bold")
        self.button_inventory.configure(borderwidth="0")

        # Billing System button
        self.button_billing = Button(root, text="Billing System", command=self.billingsystem)
        self.button_billing.place(relx=0.450, rely=0.670, width=127, height=30)
        self.button_billing.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button_billing.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 13 -weight bold")
        self.button_billing.configure(borderwidth="0")

        # Invoices button
        self.button_invoices = Button(root, text="Invoices", command=self.invoices)
        self.button_invoices.place(relx=0.665, rely=0.670, width=120, height=45)
        self.button_invoices.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button_invoices.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 16 -weight bold")
        self.button_invoices.configure(borderwidth="0")

    def open_inventory(self):
        inv_window = Toplevel(self.root)
        inv_window.geometry("1200x600")
        inv_window.title("Inventory")
        inv_window.resizable(0, 0)

        label_image = Label(inv_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r"D:\Kelompok-22\image\Inventori.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.entry_search = Entry(inv_window)
        self.entry_search.place(relx=0.041, rely=0.230, width=240, height=28)
        self.entry_search.configure(font="-family {arial} -size 12")
        self.entry_search.configure(relief="flat")

        button_search = Button(inv_window, text="Cari", command=self.cari, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_search.place(relx=0.220, rely=0.215, width=90, height=35)

        button_add_product = Button(inv_window, text="Tambah Produk", command=self.tambahproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_add_product.place(relx=0.041, rely=0.380, width=292, height=35)

        button_update_product = Button(inv_window, text="Update Produk", command=self.updateproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_update_product.place(relx=0.041, rely=0.460, width=292, height=35)      

        button_delete_product = Button(inv_window, text="Hapus Produk", command=self.hapusproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_delete_product.place(relx=0.041, rely=0.540, width=292, height=35)    

        button_exit = Button(inv_window, text="Keluar", command=self.keluar, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_exit.place(relx=0.120, rely=0.889, width=105, height=38)  

        self.scrollbarx = Scrollbar(inv_window, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(inv_window, orient=VERTICAL)
        self.tree = ttk.Treeview(inv_window)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Kode Produk",
                "Nama",
                "Kategori",
                "Sub-Kategori",
                "Stock",
                "MRP",
                "Harga Pokok",
                "No Vendor.",
            )
        )

        self.tree.heading("Kode Produk", text="Kode Produk", anchor=W)
        self.tree.heading("Nama", text="Nama", anchor=W)
        self.tree.heading("Kategori", text="Kategori", anchor=W)
        self.tree.heading("Sub-Kategori", text="Sub-Kategori", anchor=W)
        self.tree.heading("Stock", text="Stock", anchor=W)
        self.tree.heading("MRP", text="MRP", anchor=W)
        self.tree.heading("Harga Pokok", text="Harga Pokok", anchor=W)
        self.tree.heading("#8", text="No Vendor", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=120)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)
        self.tree.column("#8", stretch=NO, minwidth=0, width=100)

        self.display_data()

    def display_data(self):
        with open("inventory_data.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.tree.insert("", "end", values=row)
    
    def cari(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry_search.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=self.root)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", f"Product ID: {self.entry_search.get()} found.", parent=self.root)
                    break
            else: 
                messagebox.showerror("Oops!!", f"Product ID: {self.entry_search.get()} not found.", parent=self.root)
    
    sel = []

    def on_tree_select(self, event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def tambahproduk(self):
        tambahproduk_window = Toplevel(self.root)
        tambahproduk_window.geometry("1366x768")
        tambahproduk_window.title("Add Product")
        tambahproduk(self, tambahproduk_window)

    def updateproduk(self):
        pass

    def hapusproduk(self):
        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=self.root)
            if sure:
                with open('inventory_data.csv', 'r') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                to_delete_indexes = []
                for i in self.sel:
                    index = self.tree.index(i)
                    to_delete_indexes.append(index)

                # Remove entries from data based on selected indexes
                for index in sorted(to_delete_indexes, reverse=True):
                    del data[index]

                # Write the modified data back to the CSV file
                with open('inventory_data.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                messagebox.showinfo("Success!!", "Products deleted from database.", parent=self.root)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())
                self.display_data()
        else:
            messagebox.showerror("Error!!", "Please select a product.", parent=self.root)

    def keluar(self):
        sure = messagebox.askyesno("Keluar", "Yakin mau keluar nich?", parent=self.root)
        if sure:
            self.root.destroy()

    def billingsystem(self):
        pass

    def invoices(self):
        pass


class tambahproduk:
    def __init__(self, parent, top=None):
        self.parent = parent
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")

        self.label1 = Label(top)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./image/Tambah Produk.png")
        self.label1.configure(image=self.img)

        self.clock = Label(top)
        self.clock.place(relx=0.70, rely=0.045, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")
        self.time()

        self.entry1 = Entry(top)
        self.entry1.place(relx=0.160, rely=0.322, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(top)
        self.entry2.place(relx=0.160, rely=0.423, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = top.register(self.testint)

        self.entry3 = Entry(top)
        self.entry3.place(relx=0.160, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(top)
        self.entry4.place(relx=0.160, rely=0.643, width=374, height=20)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        self.entry6 = Entry(top)
        self.entry6.place(relx=0.518, rely=0.425, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")

        self.entry7 = Entry(top)
        self.entry7.place(relx=0.518, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")

        self.entry8 = Entry(top)
        self.entry8.place(relx=0.518, rely=0.646, width=374, height=20)
        self.entry8.configure(font="-family {Poppins} -size 12")
        self.entry8.configure(relief="flat")
        self.entry8.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.button1 = Button(top)
        self.button1.place(relx=0.402, rely=0.803, width=110, height=40)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#82736F")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#82736F")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(top)
        self.button2.place(relx=0.504, rely=0.803, width=110, height=40)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#82736F")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#82736F")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def add(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()  
        pmrp = self.entry4.get()  
        pname = self.entry1.get()  
        psubcat = self.entry6.get()  
        pcp = self.entry7.get()  
        pvendor = self.entry8.get()  

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=self.label1.master)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=self.label1.master)
                                    else:
                                        if valid_phone(pvendor):
                                            new_product = [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp), pvendor]
                                            with open('inventory_data.csv', 'a', newline='') as file:
                                                writer = csv.writer(file)
                                                writer.writerow(new_product)
                                            messagebox.showinfo("Success!!", "Product successfully added in inventory.", parent=self.label1.master)
                                            self.label1.master.destroy()
                                            self.parent.tree.delete(*self.parent.tree.get_children())
                                            self.parent.display_data()
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=self.label1.master)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=self.label1.master)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=self.label1.master)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=self.label1.master)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=self.label1.master)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=self.label1.master)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=self.label1.master)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

def valid_phone(phone):
    return phone.isdigit() and len(phone) in [10, 12]

if __name__ == "__main__":
    root = Tk()
    app = AdminPanel(root)
    root.mainloop()
