import os
from tkinter import *
from tkinter import messagebox

def Exit():
    sure = messagebox.askyesno('Exit', 'Are you sure you want to exit?', parent=main)
    if sure:
        main.destroy()

def dd():
    main.withdraw()
    os.system("python kedua.py")
    main.deiconify()

main = Tk()
main.geometry('1360x670')
main.title('duapuluhduAH')
main.resizable(0, 0)
main.protocol('WM_DELETE_WINDOW', Exit)

Label1 = Label(main)
Label1.place(relx=0, rely=0, width=1366, height=670)
img = PhotoImage(file="./image/tes.png")
Label1.configure(image=img)

button1 = Button(main)
button1.place(x=530, y=484, width=305, height=45)
button1.configure(text="Start", font=("times new roman", 20, "bold"))
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#D9D9D9")
button1.configure(cursor="hand2")
button1.configure(foreground="#D9D9D9")
button1.configure(command=dd)

# Keep a reference to the image to avoid garbage collection
Label1.image = img

main.mainloop()
