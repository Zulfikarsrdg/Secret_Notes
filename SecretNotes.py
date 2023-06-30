from tkinter import *
from tkinter import messagebox, Tk
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt():
    title = title_entry.get()
    message = secret_entry.get("1.0", END)
    master_secret = master_entry.get()

    if len(title) == 0 or len(message) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="ERROR!", message="Lütfen gerekli yerleri doldurunuz.")
    else:
        message_encrypted = encode(master_secret, message)

        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
            messagebox.showinfo(title="BAŞARILI!", message="Notunuz şifrelendi ve kaydedildi.")
        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
            messagebox.showinfo(title="BAŞARILI!", message="Notunuz şifrelendi ve kaydedildi.")
        finally:
            title_entry.delete(0, END)
            secret_entry.delete("1.0", END)
            master_entry.delete(0, END)

def decrypt_notes():
    message_encrpted = secret_entry.get("1.0", END)
    master_secret = master_entry.get()

    if len(message_encrpted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="ERROR!", message="Yanlış Şifre")
    else:
        try:
            decrypt_message = decode(master_secret, message_encrpted)
            secret_entry.delete("1.0", END)
            secret_entry.insert("1.0", decrypt_message)
            messagebox.showinfo(title="BAŞARILI!", message="Notunuzun şifresi çözüldü.")
        except:
            messagebox.showinfo(title="ERROR!", message="Şifre çözme başarısız oldu. Lütfen şifrenizi kontrol edin.")

def read_notes():
    try:
        with open("mysecret.txt", "r") as data_file:
            notes = data_file.read()
            secret_entry.delete("1.0", END)
            secret_entry.insert("1.0", notes)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR!", message="Not bulunamadı.")

window = Tk()
window.minsize(width=200, height=150)
window.title("Secret Notes")

title_label = Label(window, text="Enter Your Title")
title_label.pack()
title_entry = Entry(window)
title_entry.pack()

secret_label = Label(window, text="Enter Your Secret")
secret_label.pack()
secret_entry = Text(window, width=30, height=10)
secret_entry.pack()

master_label = Label(window, text="Enter Master Secret")
master_label.pack()
master_entry = Entry(window, show="*")
master_entry.pack()
secret_label = Label(text="")
secret_label.pack()
save_button = Button(window, text="Save & Encrypt", bg="white", command=save_and_encrypt)
save_button.pack()

secret_label = Label(text="")
secret_label.pack()

decrypt_button = Button(window, text="Decrypt", bg="white", command=decrypt_notes)
decrypt_button.pack()
secret_label = Label(text="")
secret_label.pack()
read_button = Button(window, text="Read Notes", bg="white", command=read_notes)
read_button.pack()

window.mainloop()
