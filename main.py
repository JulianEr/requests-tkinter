import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
import requests
import TextWidget

import re

class App(tk.Tk):
    top_pady = (10, 0)
    bot_pady = (0, 10)
    left_padx = (10, 0)
    right_padx = (0, 10)

    def __init__(self) -> None:
        super().__init__()
        
        self.geometry('600x200')
        self.title('Requests')

        self.columnconfigure(0, weight=1)

        self.url = tk.StringVar()
        self.endpoint = tk.StringVar()

        self.cert_path = tk.StringVar()
        self.key_path = tk.StringVar()

        self.response_status = tk.StringVar()
        self.response_text = tk.StringVar()

        self.create_widgets()

    def create_url_frame(self):
        
        url_frame = ttk.Frame(self)
        
        url_frame.columnconfigure(0, weight=1)
        url_frame.columnconfigure(1, weight=0)
        url_frame.columnconfigure(2, weight=1)

        url_label = ttk.Label(url_frame, text='url', anchor='e')
        separator_top_label = ttk.Label(url_frame, text='/')
        endpoint_label = ttk.Label(url_frame, text='endpoint')

        url_entry = ttk.Entry(url_frame, textvariable=self.url)
        separator_bot_label = ttk.Label(url_frame, text='/')
        endpoint_entry = ttk.Entry(url_frame, textvariable=self.endpoint)

        
        url_label.grid(column=0, row=0, sticky=tk.EW)
        separator_top_label.grid(column=1, row=0)
        endpoint_label.grid(column=2, row=0, sticky=tk.EW)

        url_entry.grid(column=0, row=1, sticky=tk.EW)
        separator_bot_label.grid(column=1, row=1)
        endpoint_entry.grid(column=2, row=1, sticky=tk.EW)

        return url_frame

    def create_cert_frame(self):
        cert_frame = ttk.Frame(self)

        display_frame = ttk.Frame(cert_frame)

        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)

        cert_title = ttk.Label(display_frame, text='certificate')
        key_title = ttk.Label(display_frame, text='private key')
        cert_path = ttk.Label(display_frame, textvariable=self.cert_path)
        key_path = ttk.Label(display_frame, textvariable=self.key_path)

        cert_title.grid(column=0, row=0, sticky=tk.EW)
        key_title.grid(column=1, row=0, sticky=tk.EW)
        cert_path.grid(column=0, row=1, sticky=tk.EW)
        key_path.grid(column=1, row=1, sticky=tk.EW)

        choose_frame = ttk.Frame(cert_frame)

        cert_button = ttk.Button(choose_frame, text='choose cert', command=self.choose_cert_path, width=15)
        key_button = ttk.Button(choose_frame, text='choose key', command=self.choose_key_path, width=15)
        clean_button = ttk.Button(choose_frame, text='clear', command=self.clear_key_and_cert_path, width=15)

        cert_button.grid(column=0, row=0, sticky=tk.W)
        key_button.grid(column=1, row=0)
        clean_button.grid(column=2, row=0, sticky=tk.E)

        display_frame.pack(fill='x')
        choose_frame.pack(fill='x')

        return cert_frame

    def create_call_frame(self):
        call_frame = ttk.Frame(self)

        call_button = ttk.Button(call_frame, text='call', command=self.make_request, width=10)
        call_button.pack(side=tk.LEFT)

        return call_frame


    def create_widgets(self):
        self.create_url_frame().pack(fill='x', padx=10, pady=10)
        self.create_cert_frame().pack(fill='x', padx=10, pady=10)
        self.create_call_frame().pack(fill='x', padx=10, pady=10)

    def make_request(self):
        url_pattern = re.compile(r"https?://.")

        url = self.url.get()
        endpoint = self.endpoint.get()

        if not url_pattern.match(url):
            msgbox.showerror("False URL", f"This is a false URL: {url}")
            return

        if len(self.cert_path.get()) == 0 and len(self.key_path.get()) == 0:
            response = requests.get(f'{url}/{endpoint}')
        elif len(self.cert_path.get()) != 0 and len(self.key_path.get()) == 0:
            msgbox.showerror("No private key", "You provided a certificate but not a private key")
            return
        elif len(self.cert_path.get()) == 0 and len(self.key_path.get()) != 0:
            msgbox.showerror("No certificate", "You provided a private key but not a certificate")
            return
        else:
            response = requests.get(f'{url}/{endpoint}', cert=(self.cert_path.get(), self.key_path.get()))
        
        self.response_status.set(str(response.status_code))
        self.response_text.set(response.text)

        TextWidget.TextWidget(self, response.text)

    def choose_cert_path(self):
        self.cert_path.set(fd.askopenfilename())

    def choose_key_path(self):
        self.key_path.set(fd.askopenfilename())
    
    def clear_key_and_cert_path(self):
        self.cert_path.set("")
        self.key_path.set("")

if __name__ == "__main__":
    app = App()
    app.mainloop()