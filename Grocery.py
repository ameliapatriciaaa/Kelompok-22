import csv
import os
import random
import subprocess
import tkinter as tk
from datetime import datetime
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

        image_path = r".\Images\Inventori.png"
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
                "No Vendor."
            )
        )

        self.tree.heading("Kode Produk", text="Kode Produk", anchor=W)
        self.tree.heading("Nama", text="Nama", anchor=W)
        self.tree.heading("Kategori", text="Kategori", anchor=W)
        self.tree.heading("Sub-Kategori", text="Sub-Kategori", anchor=W)
        self.tree.heading("Stock", text="Stock", anchor=W)
        self.tree.heading("MRP", text="MRP", anchor=W)
        self.tree.heading("Harga Pokok", text="Harga Pokok", anchor=W)
        self.tree.heading("No Vendor.", text="No Vendor.", anchor=W)

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
            next (file)
            for line in file:
                data = line.strip().split(",")
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
        inv_window = Toplevel(self.root)
        inv_window.geometry("1200x600")
        inv_window.title("Inventory")
        inv_window.resizable(0, 0)

        label_image = Label(inv_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r".\images\tambahproduk.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.entrynama = Entry(inv_window)
        self.entrynama.place(relx=0.107, rely=0.305, width=240, height=25)
        self.entrynama.configure(font="-family {arial} -size 12")
        self.entrynama.configure(relief="flat")

        self.entrykategori = Entry(inv_window)
        self.entrykategori.place(relx=0.107, rely=0.446, width=240, height=25)
        self.entrykategori.configure(font="-family {arial} -size 12")
        self.entrykategori.configure(relief="flat")

        self.entrykuantitas = Entry(inv_window)
        self.entrykuantitas.place(relx=0.107, rely=0.587, width=240, height=25)
        self.entrykuantitas.configure(font="-family {arial} -size 12")
        self.entrykuantitas.configure(relief="flat")

        self.entryhargajual = Entry(inv_window)
        self.entryhargajual.place(relx=0.107, rely=0.727, width=240, height=25)
        self.entryhargajual.configure(font="-family {arial} -size 12")
        self.entryhargajual.configure(relief="flat")

        self.entryidproduk = Entry(inv_window)
        self.entryidproduk.place(relx=0.532, rely=0.305, width=240, height=25)
        self.entryidproduk.configure(font="-family {arial} -size 12")
        self.entryidproduk.configure(relief="flat")

        self.entrysubkategori = Entry(inv_window)
        self.entrysubkategori.place(relx=0.532, rely=0.446, width=240, height=25)
        self.entrysubkategori.configure(font="-family {arial} -size 12")
        self.entrysubkategori.configure(relief="flat")

        self.entryhargapokok = Entry(inv_window)
        self.entryhargapokok.place(relx=0.532, rely=0.587, width=240, height=25)
        self.entryhargapokok.configure(font="-family {arial} -size 12")
        self.entryhargapokok.configure(relief="flat")

        self.entrynotelp = Entry(inv_window)
        self.entrynotelp.place(relx=0.532, rely=0.727, width=240, height=25)
        self.entrynotelp.configure(font="-family {arial} -size 12")
        self.entrynotelp.configure(relief="flat")

        button_update = Button(inv_window, text="Add", command=lambda: self.add(inv_window), bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_update.place(relx=0.395, rely=0.898, width=119, height=47)

        button_clear = Button(inv_window, text="Clear", command=self.clear, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_clear.place(relx=0.518, rely=0.898, width=119, height=47)
    

    def add(self,p_tambah):
        pknt = self.entrykuantitas.get()
        pktg = self.entrykategori.get()  
        phjl = self.entryhargajual.get()  
        pnama = self.entrynama.get()  
        psubkat = self.entrysubkategori.get()  
        phpp = self.entryhargapokok.get()  
        pvendor = self.entrynotelp.get() 
        pid =self.entryidproduk.get() 

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
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_tambah)
                            else:
                                if phjl:
                                    try:
                                        float(phjl)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_tambah)
                                    else:
                                        if valid_phone(pvendor):
                                            new_product = [pid,pnama, pktg, psubkat, int(pknt), float(phjl), float(phpp), pvendor]
                                            with open('inventory_data.csv', 'a', newline='') as file:
                                                writer = csv.writer(file)
                                                writer.writerow(new_product)
                                            messagebox.showinfo("Success!!", "Product successfully added in inventory.", parent=p_tambah)
                                            p_tambah.destroy()
                                            self.tree.delete(*self.tree.get_children())
                                            self.display_data()
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=p_tambah)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_tambah)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_tambah)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_tambah)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_tambah)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_tambah)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_tambah)

        
    def open_updateproduk(self):
        inv_window = Toplevel(self.root)
        inv_window.geometry("1200x600")
        inv_window.title("Inventory")
        inv_window.resizable(0, 0)

        label_image = Label(inv_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r".\images\updateproduk.png"
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
                                            csv_file = r"inventory_data.csv"
                                            
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
        bill_window = Toplevel(self.root)
        bill_window.geometry("1200x600")
        bill_window.title("Billing System")
        bill_window.resizable(0, 0)

        label_image = Label(bill_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r".\Images\billingsystem.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.entrynamacust = Entry(bill_window)
        self.entrynamacust.place(relx=0.515, rely=0.155, width=200, height=25)
        self.entrynamacust.configure(font="-family {arial} -size 12")
        self.entrynamacust.configure(relief="flat")

        self.entrynocust = Entry(bill_window)
        self.entrynocust.place(relx=0.775, rely=0.155, width=200, height=25)
        self.entrynocust.configure(font="-family {arial} -size 12")
        self.entrynocust.configure(relief="flat")

        self.entrycustcarinota = Entry(bill_window)
        self.entrycustcarinota.place(relx=0.110, rely=0.155, width=200, height=25)
        self.entrycustcarinota.configure(font="-family {arial} -size 12")
        self.entrycustcarinota.configure(relief="flat")

        button_caritagihan = Button(bill_window, text="Cari", command=self.cari_tagihan, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_caritagihan.place(relx=0.302, rely=0.145, width=93, height=35)

        button_total = Button(bill_window, text="Total", command=self.total, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_total.place(relx=0.041, rely=0.881, width=101, height=27)

        button_buat = Button(bill_window, text="Buat", command=self.buat, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_buat.place(relx=0.041, rely=0.933, width=101, height=27)

        button_print = Button(bill_window, text="Print", command=self.print, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_print.place(relx=0.169, rely=0.881, width=103, height=27)

        button_email = Button(bill_window, text="Email", command=self.email, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_email.place(relx=0.169, rely=0.933, width=103, height=27)

        button_clearbill = Button(bill_window, text="Clear", command=self.clear_bill, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_clearbill.place(relx=0.304, rely=0.881, width=103, height=27)

        button_keluarbill = Button(bill_window, text="Keluar", command=self.keluar_bill, bg="#82736F", fg="white", font=("Arial", 11, "bold"))
        button_keluarbill.place(relx=0.304, rely=0.933, width=103, height=27)

        button_tambahkan = Button(bill_window, text="Tambahkan", command=self.tambahkan, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_tambahkan.place(relx=0.088, rely=0.720, width=94, height=35)

        button_hapus = Button(bill_window, text="Hapus", command=self.hapus, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_hapus.place(relx=0.177, rely=0.720, width=94, height=35)

        button_clearpilihan = Button(bill_window, text="Clear", command=self.clear_pilihan, bg="#82736F", fg="white", font=("Arial", 12, "bold"))
        button_clearpilihan.place(relx=0.266, rely=0.720, width=94, height=35)

        text_font = ("times new roman", "10")
        self.combokat = ttk.Combobox(bill_window)
        self.combokat.place(relx=0.130, rely=0.325, width=250, height=20)
        self.combokat.configure(font=text_font)
        self.combokat.configure(state="readonly")

        cat = self.read_csv_categories()
        self.combokat['values'] = cat
        self.combokat.configure(state="readonly")
        self.combokat.option_add("*TCombobox*Listbox.font", text_font)
        self.combokat.option_add("*TCombobox*Listbox.selectBackground", "#82736F")

        self.combosubkat = ttk.Combobox(bill_window)
        self.combosubkat.place(relx=0.130, rely=0.410, width=250, height=20)
        self.combosubkat.configure(font=text_font)
        self.combosubkat.option_add("*TCombobox*Listbox.font", text_font) 
        self.combosubkat.configure(state="disabled")

        self.comboproduk = ttk.Combobox(bill_window)
        self.comboproduk.place(relx=0.130, rely=0.485, width=250, height=20)
        self.comboproduk.configure(font=text_font)
        self.comboproduk.configure(state="disabled") 
        self.comboproduk.option_add("*TCombobox*Listbox.font", text_font) 

        self.entryjumlah = ttk.Entry(bill_window)
        self.entryjumlah.place(relx=0.130, rely=0.572, width=250, height=20)
        self.entryjumlah.configure(font=("times new roman", 10))
        self.entryjumlah.configure(foreground="#82736F")
        self.entryjumlah.configure(state="disabled")

        self.Scrolledtext1 = scrolledtext.ScrolledText(bill_window)
        self.Scrolledtext1.place(relx=0.420, rely=0.300, width=665, height=400)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font=("times new roman", 10))
        self.Scrolledtext1.configure(state="disabled")

        self.qty_label = Label(bill_window)
        self.qty_label.place(relx=0.130, rely=0.620, width=70, height=20)
        self.qty_label.configure(font=("times new roman", 8))
        self.qty_label.configure(anchor="w")

        self.combokat.bind("<<ComboboxSelected>>", self.update_subkategori)
        self.combosubkat.bind("<<ComboboxSelected>>", self.update_produk)
        self.comboproduk.bind("<<ComboboxSelected>>", self.show_qty)

    def read_csv_categories(self):
        categories = []
        with open('inventory_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row['product_cat']
                if category not in categories:
                    categories.append(category)
        return categories

    def update_subkategori(self, event=None):
        selected_category = self.combokat.get()
        subcategories = self.get_sub_kategori(selected_category)
        self.combosubkat.configure(values=subcategories, state="readonly")
        self.combosubkat.set('')
        self.comboproduk.set('')
        self.comboproduk.configure(state="disabled")

    def get_sub_kategori(self, selected_category):
        subcategories = []
        with open('inventory_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['product_cat'] == selected_category:
                    subcategory = row['product_subcat']
                    if subcategory not in subcategories:
                        subcategories.append(subcategory)
        self.combosubkat.bind("<<ComboboxSelected>>", self.update_produk)
        return subcategories

    def update_produk(self, event=None):
        selected_category = self.combokat.get()
        selected_subcategory = self.combosubkat.get()
        products = self.get_produk(selected_category, selected_subcategory)
        self.comboproduk.configure(values=products, state="readonly")
        self.comboproduk.set('')
        self.entryjumlah.configure(state="normal")

    def get_produk(self, selected_category, selected_subcategory):
        products = []
        with open('inventory_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'product_name' not in reader.fieldnames:
                raise KeyError("Kolom 'product_name' tidak ditemukan dalam file CSV.")
            for row in reader:
                if row['product_cat'] == selected_category and row['product_subcat'] == selected_subcategory:
                    product = row['product_name']
                    if product not in products:
                        products.append(product)
        self.comboproduk.bind("<<ComboboxSelected>>", self.show_qty)
        return products

    def show_qty(self, event=None):
        self.entryjumlah.configure(state="normal")
        product_name = self.comboproduk.get()
        with open('inventory_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['product_name'] == product_name:
                    self.qty_label.configure(text="In Stock: {}".format(row['stock']))
                    break
            else:
                self.qty_label.configure(text="In Stock: 0")
        self.qty_label.configure(background="white")
        self.qty_label.configure(foreground="black")

    def tambahkan(self):
        with open('inventory_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inventory_data = list(reader)

        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', 'end-1c')
        if strr.find('Total') == -1:
            product_name = self.comboproduk.get()
            if product_name:
                product_qty = self.entryjumlah.get()
                stock, mrp = self.get_stock_mrp(inventory_data, product_name)
                if stock is not None and mrp is not None:
                    if product_qty.isdigit():
                        if stock >= int(product_qty):
                            sp = mrp * int(product_qty)
                            bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                            self.Scrolledtext1.insert('insert', bill_text)
                            self.Scrolledtext1.configure(state="disabled")
                        else:
                            messagebox.showerror("Oops!", "Stok tidak mencukupi. Periksa kuantitas.")
                    else:
                        messagebox.showerror("Oops!", "Kuantitas tidak valid.")
                else:
                    messagebox.showerror("Oops!", "Produk tidak ditemukan dalam inventaris.")
            else:
                messagebox.showerror("Oops!", "Pilih produk.")
        else:
            self.Scrolledtext1.delete('1.0', 'end')  # Hapus isi sebelum penambahan baru

    def get_stock_mrp(self, inventory_data, product_name):
        for row in inventory_data:
            if row['product_name'] == product_name:
                return int(row['stock']), float(row['mrp'])
        return None, None  # Produk tidak ditemukan

    def hapus(self):
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total') == -1:
            lines = self.Scrolledtext1.get('1.0', 'end-1c').split('\n')
            if lines:
                lines.pop(-2)  # Remove the last product line
                self.Scrolledtext1.delete('1.0', END)
                self.Scrolledtext1.insert('insert', '\n'.join(lines) + '\n')
        self.Scrolledtext1.configure(state="disabled")

    def clear_pilihan(self):
        self.entrynamacust.delete(0, END)
        self.entrynocust.delete(0, END)
        self.entrycustcarinota.delete(0, END)
        self.combokat.set('')
        self.combosubkat.set('')
        self.comboproduk.set('')
        self.entryjumlah.delete(0, END)
        self.qty_label.configure(text="")

    def total(self):
        if self.isEmpty():
            messagebox.showerror("Oops!", "Add a product.")
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', 'end-1c')
        if strr.find('Total') == -1:
            divider = "\n\n\n" + ("─" * 65)
            self.Scrolledtext1.insert('insert', divider)
            total_amount = self.calculate_total()
            total_text = "\nTotal\t\t\t\t\t\t\t\t\t\tRp. {}".format(total_amount)
            self.Scrolledtext1.insert('insert', total_text)
            divider2 = "\n" + ("─" * 65)
            self.Scrolledtext1.insert('insert', divider2)
            self.Scrolledtext1.configure(state="disabled")

    def isEmpty(self):
        return not self.Scrolledtext1.get('1.0', 'end-1c').strip()

    def calculate_total(self):
        lines = self.Scrolledtext1.get('1.0', 'end-1c').split('\n')
        total = 0
        for line in lines:
            if line.strip():
                parts = line.split()
                total += float(parts[-1])
                return total
            
    def random_bill_number(self, length):
        return ''.join(random.choices('0123456789', k=length))
    
    def valid_phone(self, phone):
        if phone.isdigit() and len(phone) in [10, 11, 12]:
            return True
        return False

    def write_to_file(filename, content):
        with open(filename, "a") as file:
            file.write(content + "\n")

    def update_inventory_file(filename, updates):
        lines = []
        with open(filename, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            fields = line.strip().split(',')
            if fields[0] in updates:
                fields[1] = str(int(fields[1]) - updates[fields[0]])
            new_lines.append(','.join(fields) + "\n")

        with open(filename, "w") as file:
            file.writelines(new_lines)

    state = 1
    def buat(self):
        global state
        if self.state == 1:
        # Mengambil teks dari scrolled text
            strr = self.Scrolledtext1.get('1.0', 'end-1c')
            cust_name = self.entrynamacust.get()
            cust_num = self.entrynocust.get()

            # Validasi input
            if cust_name == "":
                messagebox.showerror("Oops!", "Please enter a name.")
            elif cust_num == "":
                messagebox.showerror("Oops!", "Please enter a number.")
            elif not self.valid_phone(cust_num):
                messagebox.showerror("Oops!", "Please enter a valid number.")
            elif self.isEmpty():
                messagebox.showerror("Oops!", "Cart is empty.")
            else:
                # Menambahkan detail customer ke dalam ScrolledText
                if 'Total' not in strr:
                    self.total()
                    self.buat()
                else:
                    self.Scrolledtext1.configure(state="normal")

                    # Menghapus teks yang ada di ScrolledText
                    self.Scrolledtext1.delete('1.0', END)

                    # Menyisipkan baris-baris sesuai format yang diminta
                    self.Scrolledtext1.insert(END, f"{' '*76}DUA PULUH DUAHH\n")
                    self.Scrolledtext1.insert(END, f"{' '*80}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    cust_new_bill = self.random_bill_number(8)
                    self.Scrolledtext1.insert(END, f"{' '}Bill Number    : {cust_new_bill}\n")
                    self.Scrolledtext1.insert(END, f"{' '}Customer Name  : {cust_name}\n")
                    self.Scrolledtext1.insert(END, f"{' '}Customer Number: {cust_num}\n\n")
                    self.Scrolledtext1.insert(END, strr)

                    self.Scrolledtext1.configure(state="disabled")

                    # Menampilkan nomor nota ke Entry dan menonaktifkannya
                    self.entrycustcarinota.delete(0, END)
                    self.entrycustcarinota.insert(END, cust_new_bill)
                    self.entrycustcarinota.configure(state="disabled")

                    # Menulis detail tagihan ke file baru
                    with open(f'bill_{cust_new_bill}.txt', 'w', encoding='utf-8') as bill_file:
                        bill_file.write(f"{' '}DUA PULUH DUAHH\n")
                        bill_file.write(f"{' '}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        bill_file.write(f"{' '}Bill Number    : {cust_new_bill}\n")
                        bill_file.write(f"{' '}Customer Name  : {cust_name}\n")
                        bill_file.write(f"{' '}Customer Number: {cust_num}\n\n")
                        bill_file.write(strr)
                    
                    with open('data.txt', 'a', encoding='utf-8') as data_file:
                        data_file.write(f"{cust_new_bill},{datetime.now().strftime('%Y-%m-%d')},{cust_name},{cust_num}")

                    # Update jumlah inventaris di file CSV
                    inventory_updates = {}
                    lines = strr.split('\n')
                    for line in lines:
                        parts = line.split()
                        if len(parts) > 2 and parts[-2].replace('.', '', 1).isdigit():  # Check for valid quantity
                            product_name = ' '.join(parts[:-2])
                            qty = int(float(parts[-2].replace('.', '', 1)))
                            inventory_updates[product_name] = inventory_updates.get(product_name, 0) + qty

                    self.update_inventory_file('inventory_data.csv', inventory_updates)

                    messagebox.showinfo("Sukses!!", "Nota telah dibuat")

                    self.entrynamacust.focus()

    def update_inventory_file(self, filename, updates):
        lines = []
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['product_name'] in updates:
                    row['stock'] = str(int(row['stock']) - updates[row['product_name']])
                lines.append(row)

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(lines)

    def print(self):
        cust_new_bill = self.entrycustcarinota.get()
        filename = f'bill_{cust_new_bill}.txt'

        # Melakukan pencetakan
        try:
            # Mencetak file menggunakan perintah print system
            subprocess.run(["notepad.exe", "/p", filename], check=True)
            messagebox.showinfo("Success", "Nota telah berhasil dicetak.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def email (self):
        pass

    def clear_bill(self):
        self.Scrolledtext1.configure(state="normal")
        self.Scrolledtext1.delete('1.0', END)
        self.Scrolledtext1.configure(state="disabled")
        self.entrynamacust.delete(0, END)
        self.entrynocust.delete(0, END)
        self.entrycustcarinota.configure(state="normal")
        self.entrycustcarinota.delete(0, END)
        self.entrycustcarinota.configure(state="disabled")

    def keluar_bill(self):
        billeer = self.root
        sure = messagebox.askyesno("Yakin mau keluar ?")
        if sure == True:
            billeer.destroy()
            root.deiconify()
            
    def cari_tagihan(self):
        bill_number = self.entrycustcarinota.get()
        if bill_number:
            file_path = f"bill_{bill_number}.txt"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    bill_content = file.read()
                self.Scrolledtext1.configure(state="normal")
                self.Scrolledtext1.delete("1.0", "end")
                self.Scrolledtext1.insert("1.0", bill_content)
                self.Scrolledtext1.configure(state="disabled")
            else:
                messagebox.showerror("Oops!", "Bill not found.")
        else:
            messagebox.showerror("Oops!", "Please enter a bill number.")

    def invoices(self):
        invo_window = Toplevel(self.root)
        invo_window.geometry("1200x600")
        invo_window.title("Invoce")
        invo_window.resizable(0, 0)

        label_image = Label(invo_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r".\Images\Invoice.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.kodeinvo = Entry(invo_window)
        self.kodeinvo.place(relx=0.112, rely=0.286, width=163, height=25)
        self.kodeinvo.configure(font="-family {arial} -size 12")
        self.kodeinvo.configure(relief="flat")

        button_kodeinvo = Button(invo_window)
        button_kodeinvo.place(relx=0.265, rely=0.277,width=76,height=34)
        button_kodeinvo.configure(relief="flat")
        button_kodeinvo.configure(overrelief="flat")
        button_kodeinvo.configure(background="#82736F")
        button_kodeinvo.configure(cursor="hand2")
        button_kodeinvo.configure(foreground="#ffffff")
        button_kodeinvo.configure(font="Arial")
        button_kodeinvo.configure(borderwidth="0")
        button_kodeinvo.configure(text="Search")
        button_kodeinvo.configure(command=self.search_invo)

        button_keluarinvo = Button(invo_window)
        button_keluarinvo.place(relx=0.183, rely=0.865,width=86,height=32)
        button_keluarinvo.configure(relief="flat")
        button_keluarinvo.configure(overrelief="flat")
        button_keluarinvo.configure(background="#82736F")
        button_keluarinvo.configure(cursor="hand2")
        button_keluarinvo.configure(foreground="#ffffff")
        button_keluarinvo.configure(font="Arial")
        button_keluarinvo.configure(borderwidth="0")
        button_keluarinvo.configure(text="Keluar")
        button_keluarinvo.configure(command=self.keluar_invo)

        button_hapusinvo = Button(invo_window)
        button_hapusinvo.place(relx=0.112, rely=0.422,width=264,height=32)
        button_hapusinvo.configure(relief="flat")
        button_hapusinvo.configure(overrelief="flat")
        button_hapusinvo.configure(background="#82736F")
        button_hapusinvo.configure(cursor="hand2")
        button_hapusinvo.configure(foreground="#ffffff")
        button_hapusinvo.configure(font="Arial")
        button_hapusinvo.configure(borderwidth="0")
        button_hapusinvo.configure(text="Hapus Invoice")
        button_hapusinvo.configure(command=self.hapus_invo)

        self.scrollbarx = Scrollbar(invo_window,orient=HORIZONTAL)
        self.scrollbary = Scrollbar(invo_window,orient=VERTICAL)
        self.tree = ttk.Treeview(invo_window)
        self.tree.place(relx=0.345, rely=0.203, width=760, height=450)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.double_tap)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.205, width=10, height=300)
        self.scrollbarx.place(relx=0.350, rely=0.920, width=200, height=22)

        self.tree.configure(
            columns=(
                "Bill Number",
                "Date",
                "Customer Name",
                "Customer Phone No.",
            )
        )

        self.tree.heading("Bill Number", text="Bill Number", anchor=W)
        self.tree.heading("Date", text="Date", anchor=W)
        self.tree.heading("Customer Name", text="Customer Name", anchor=W)
        self.tree.heading("Customer Phone No.", text="Customer Phone No.", anchor=W)
        

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=219)
        self.tree.column("#2", stretch=NO, minwidth=0, width=219)
        self.tree.column("#3", stretch=NO, minwidth=0, width=219)
        self.tree.column("#4", stretch=NO, minwidth=0, width=219)
        

        self.DisplayData()

    def search_invo(self):
        to_search = self.kodeinvo.get()
        found = False

        # Lakukan pencarian di treeview
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            if to_search in values:
                self.tree.selection_set(child)
                self.tree.focus(child)
                found = True
                break
        
        if not found:
            messagebox.showerror("Oops!!", f"Bill Number: {to_search} not found.", parent=self.root)
    
    def keluar_invo(self):
        invoice = self.root
        sure = messagebox.askyesno("Yakin mau keluar ?")
        if sure == True:
            invoice.destroy()
            root.deiconify()
            
    
    def hapus_invo(self):
        to_delete = []
        invoice = self.root

        # Memeriksa apakah ada item yang dipilih di Treeview
        if len(self.tree.selection()) != 0:
            # Menampilkan dialog konfirmasi
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoices?", parent=invoice)
            if sure:
                with open('data.txt', 'r') as file:
                    lines = file.readlines()

                # Mendapatkan indeks item yang dipilih
                for item in self.tree.selection():
                    index = self.tree.index(item)
                    to_delete.append(index)

                # Menghapus baris yang sesuai dengan indeks yang dipilih
                new_lines = [line for index, line in enumerate(lines) if index not in to_delete]

                # Menulis kembali data ke file
                with open('data.txt', 'w') as file:
                    file.writelines(new_lines)

                # Menghapus file tagihan terkait
                for item in self.tree.selection():
                    bill_number = self.tree.item(item, 'values')[0]
                    filename = f"bill_{bill_number}.txt"
                    if os.path.exists(filename):
                        os.remove(filename)

                # Menampilkan pesan sukses
                messagebox.showinfo("Success!!", "Invoices deleted from database.", parent=invoice)

                # Menghapus item dari Treeview
                for item in reversed(self.tree.selection()): # Hapus terbalik untuk menghindari masalah indeks
                    self.tree.delete(item)

                # Memperbarui tampilan data
                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select an invoice.", parent=invoice)

    def DisplayData(self):
        with open("data.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                self.tree.insert("", tk.END, values=data)

    def double_tap(self,event):
        item = self.tree.identify('item', event.x, event.y)
        global bill_num
        bill_num = self.tree.item(item)['values'][0]

        self.open_bill()
    
    def open_bill(self):
        openbill_window = Toplevel(self.root)
        openbill_window.geometry("1200x600")
        openbill_window.title("Invoce")
        openbill_window.resizable(0, 0)

        label_image = Label(openbill_window)
        label_image.place(relx=0, rely=0, width=1200, height=600)

        image_path = r".\Images\Openbill.png"
        img = PhotoImage(file=image_path)
        label_image.config(image=img)
        label_image.image = img

        self.Scrolledtext1 = scrolledtext.ScrolledText(openbill_window)
        self.Scrolledtext1.place(relx=0.050, rely=0.05, width=1100, height=500)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {times new roman} -size 12")
        self.Scrolledtext1.configure(state="disabled")

        # Membaca file data.txt
        try:
            filename = f"bill_{bill_num}.txt"
            with open(filename, 'r', encoding='utf-8') as file:
                # Membaca seluruh isi file
                content = file.read()
                self.Scrolledtext1.configure(state="normal")
                self.Scrolledtext1.insert(END, content)
                self.Scrolledtext1.configure(state="disabled")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Bill file '{filename}' not found.")

if __name__ == "__main__":
    root = Tk()
    app = AdminPanel(root)
    root.mainloop()