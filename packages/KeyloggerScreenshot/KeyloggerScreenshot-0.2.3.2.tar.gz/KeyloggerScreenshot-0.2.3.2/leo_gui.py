import tkinter as tk

tkWindow = tk.Tk()
tkWindow.geometry('295x367')
tkWindow.title('KeyloggerScreenshot by Fawaz Abolagi Temitaiu Martin Junior Bashiru')
started = False
def changecol(newstate):
    if newstate == True:
        startbutton.configure(bg="green")
        startbutton["text"] = "Stop KLS"
        start()
    else:
        startbutton.configure(bg="white")
        startbutton["text"] = "Start KLS"
        stop()
def start():
    print("started")
def stop():
    print("stopped")
def start_stop():
    global started
    started = not started
    changecol(started)
def show_files():
    print("showing_files")

startbutton = tk.Button(tkWindow, text="Start KLS", command=start_stop, height=10, width=30)
startbutton.grid(row=1, column=0)
tk.Button(tkWindow, text="Show Files", command=show_files, height=10, width=30).grid(row=2, column=0)
tkWindow.mainloop()