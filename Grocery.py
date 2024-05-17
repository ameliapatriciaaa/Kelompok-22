import csv
import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import Toplevel
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Label
from tkinter import Button
from tkinter import PhotoImage


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Grocery Billing System")

        # Label untuk menampilkan gambar latar
        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1200, height=600)
        self.img = PhotoImage(file="./images/menu.png")  
        self.label1.configure(image=self.img)

        # Tombol Inventory
        self.button2 = Button(root, text="Inventory", command=self.open_inventory)
        self.button2.place(relx=0.240, rely=0.650, width=107, height=50)
        self.button2.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button2.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 17 -weight bold")
        self.button2.configure(borderwidth="0")

        # Tombol Billing System
        self.button3 = Button(root, text="Billing System", command=self.billingsystem)
        self.button3.place(relx=0.450, rely=0.670, width=127, height=30)
        self.button3.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button3.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 13 -weight bold")
        self.button3.configure(borderwidth="0")

        # Tombol Invoices
        self.button4 = Button(root, text="Invoices", command=self.invoices)
        self.button4.place(relx=0.665, rely=0.670, width=120, height=45)
        self.button4.configure(relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2")
        self.button4.configure(foreground="#333333", background="#ffffff", font="-family {Helvetica Bold} -size 16 -weight bold")
        self.button4.configure(borderwidth="0")

    def open_inventory(self):
        inv_window = Toplevel(self.root)
        inv_window.geometry("1200x600")
        inv_window.title("Inventory")
        inv_window.resizable(0, 0)

        label_image = Label(inv_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r"C:\Users\asus\Downloads\Grocery\images\Inventori.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.entry1 = Entry(inv_window)
        self.entry1.place(relx=0.041, rely=0.230, width=240, height=28)
        self.entry1.configure(font="-family {arial} -size 12")
        self.entry1.configure(relief="flat")

        button_cari = Button(inv_window, text="Cari", command=self.cari, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_cari.place(relx=0.220, rely=0.215, width=90, height=35)

        button_tambah_produk = Button(inv_window, text="Tambah Produk", command=self.tambahproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_tambah_produk.place(relx=0.041, rely=0.380, width=292, height=35)

        button_update_produk = Button(inv_window, text="Update Produk", command=self.open_updateproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_update_produk.place(relx=0.041, rely=0.460, width=292, height=35)      

        button_hapus_produk = Button(inv_window, text="Hapus Produk", command=self.hapusproduk, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_hapus_produk.place(relx=0.041, rely=0.540, width=292, height=35)    

        button_keluar = Button(inv_window, text="Keluar", command=self.keluar, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_keluar.place(relx=0.120, rely=0.889, width=105, height=38)  

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
            # Baca setiap baris
            for line in file:
                # Pisahkan data menggunakan delimiter tertentu, misalnya koma untuk CSV
                data = line.strip().split(",")
                # Masukkan data ke dalam treeview
                self.tree.insert("", "end", values=data)
    
    def cari(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=inv)
        else:
            for search in val:
                if search==to_search:
                    self.tree.selection_set(val[val.index(search)-1])
                    self.tree.focus(val[val.index(search)-1])
                    messagebox.showinfo("Success!!", "Product ID: {} found.".format(self.entry1.get()), parent=inv)
                    break
            else: 
                messagebox.showerror("Oops!!", "Product ID: {} not found.".format(self.entry1.get()), parent=inv)
    
    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def tambahproduk(self):
        pass

    def open_updateproduk(self):
        inv_window = Toplevel(self.root)
        inv_window.geometry("1200x600")
        inv_window.title("Inventory")
        inv_window.resizable(0, 0)

        label_image = Label(inv_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r"C:\Users\asus\Downloads\Grocery\images\updateproduk.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.entrynama = Entry(inv_window)
        self.entrynama.place(relx=0.115, rely=0.280, width=240, height=25)
        self.entrynama.configure(font="-family {arial} -size 12")
        self.entrynama.configure(relief="flat")

        self.entrykategori = Entry(inv_window)
        self.entrykategori.place(relx=0.115, rely=0.415, width=240, height=25)
        self.entrykategori.configure(font="-family {arial} -size 12")
        self.entrykategori.configure(relief="flat")

        self.entrykuantitas = Entry(inv_window)
        self.entrykuantitas.place(relx=0.115, rely=0.545, width=240, height=25)
        self.entrykuantitas.configure(font="-family {arial} -size 12")
        self.entrykuantitas.configure(relief="flat")

        self.entryhargajual = Entry(inv_window)
        self.entryhargajual.place(relx=0.115, rely=0.675, width=240, height=25)
        self.entryhargajual.configure(font="-family {arial} -size 12")
        self.entryhargajual.configure(relief="flat")

        self.entrysubkategori = Entry(inv_window)
        self.entrysubkategori.place(relx=0.515, rely=0.415, width=240, height=25)
        self.entrysubkategori.configure(font="-family {arial} -size 12")
        self.entrysubkategori.configure(relief="flat")

        self.entryhargapokok = Entry(inv_window)
        self.entryhargapokok.place(relx=0.515, rely=0.545, width=240, height=25)
        self.entryhargapokok.configure(font="-family {arial} -size 12")
        self.entryhargapokok.configure(relief="flat")

        self.entrynotelp = Entry(inv_window)
        self.entrynotelp.place(relx=0.515, rely=0.675, width=240, height=25)
        self.entrynotelp.configure(font="-family {arial} -size 12")
        self.entrynotelp.configure(relief="flat")

        button_update = Button(inv_window, text="Update", command=lambda: self.update(inv_window), bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_update.place(relx=0.388, rely=0.888, width=111, height=43)

        button_clear = Button(inv_window, text="Clear", command=self.clear, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_clear.place(relx=0.504, rely=0.888, width=111, height=43)

    def update(self, p_update):
        pknt = self.entrykuantitas.get()
        pktg = self.entrykategori.get()  
        phjl = self.entryhargajual.get()  
        pnama = self.entrynama.get()  
        psubkat = self.entrysubkategori.get()  
        phpp = self.entryhargapokok.get()  
        pvendor = self.entrynotelp.get()  
       
        def valid_phone(phone_number):
            return phone_number.isdigit() and len(phone_number) == 10

        if pnama.strip():
            if pktg.strip():
                if psubkat.strip():
                    if pknt:
                        if phpp:
                            try:
                                float(phpp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_update)
                            else:
                                if phjl:
                                    try:
                                        float(phjl)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_update)
                                    else:
                                        if valid_phone(pvendor):
                                            updated = False
                                            data = []
                                            csv_file = r"C:\Users\asus\Downloads\Grocery\inventory_data.csv"
                                            
                                            # Membaca data saat ini
                                            if os.path.exists(csv_file):
                                                with open(csv_file, mode='r', newline='') as file:
                                                    reader = csv.reader(file)
                                                    header = next(reader)  # Membaca header
                                                    for row in reader:
                                                        if row[1] == pnama:  # Menggunakan pnama sebagai pengenal unik
                                                            data.append([row[0], pnama, pktg, psubkat, pknt, phjl, phpp, pvendor])
                                                            updated = True
                                                        else:
                                                            data.append(row)
                                            
                                            # Jika produk ditemukan dan diperbarui
                                            if updated:
                                                with open(csv_file, mode='w', newline='') as file:
                                                    writer = csv.writer(file)
                                                    writer.writerow(header)  # Menulis header
                                                    writer.writerows(data)
                                                messagebox.showinfo("Success!!", "Produk berhasil diperbarui dalam inventaris.", parent=p_update)
                                                p_update.destroy()
                                            else:
                                                messagebox.showerror("Oops!", "Produk tidak ditemukan.", parent=p_update)
                                        else:
                                            messagebox.showerror("Oops!", "Nomor telepon tidak valid.", parent=p_update)
                                else:
                                    messagebox.showerror("Oops!", "Silakan masukkan MRP.", parent=p_update)
                        else:
                            messagebox.showerror("Oops!", "Silakan masukkan harga pokok produk.", parent=p_update)
                    else:
                        messagebox.showerror("Oops!", "Silakan masukkan kuantitas produk.", parent=p_update)
                else:
                    messagebox.showerror("Oops!", "Silakan masukkan sub-kategori produk.", parent=p_update)
            else:
                messagebox.showerror("Oops!", "Silakan masukkan kategori produk.", parent=p_update)
        else:
            messagebox.showerror("Oops!", "Silakan masukkan nama produk", parent=p_update)

    def clear(self):
        self.entrynama.delete(0, Tk.END)
        self.entrykategori.delete(0, Tk.END)
        self.entrykuantitas.delete(0, Tk.END)
        self.entryhargajual.delete(0, Tk.END)
        self.entrysubkategori.delete(0, Tk.END)
        self.entryhargapokok.delete(0, Tk.END)
        self.entrynotelp.delete(0, Tk.END)

    def hapusproduk(self):
        val = []
        to_delete = []

        inv = self.root

        if len(self.sel)!=0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=inv)
            if sure == True:
                with open('inventory_data.csv', 'r') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                to_delete_indexes = []
                for i in self.sel:
                    index = self.tree.index(i)
                    to_delete_indexes.append(index)

                # Hapus entri dari data berdasarkan indeks yang dipilih
                for index in sorted(to_delete_indexes, reverse=True):
                    del data[index]

                # Tulis kembali data yang telah diubah ke file CSV
                with open('inventory_data.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                messagebox.showinfo("Success!!", "Products deleted from database.", parent=inv)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.display_data()
        else:
            messagebox.showerror("Error!!","Please select a product.", parent=inv)

    def keluar(self):
        inv = self.root

        sure = messagebox.askyesno("Keluar","Yakin mau keluar nich?", parent=inv)
        if sure == True:
            inv.destroy()

    def billingsystem(self):
        pass

    def invoices(self):
        pass


if __name__ == "__main__":
    root = Tk()
    app = AdminPanel(root)
    root.mainloop()