import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

window = tk.Tk()
window.title("Takip Sistemi")


conn = sqlite3.connect("kullanici_veritabani.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS kullanıcılar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT,
        soyad TEXT,
        kullanici_adi TEXT,
        password TEXT,
        tc_kimlik_no TEXT,
        telefon TEXT,
        email TEXT,
        adres TEXT,
        kullanici_type TEXT
    )
""")

def show_login_screen():
    login_frame.grid(row=1, column=1)
    register_frame.grid_forget()

def show_register_screen():
    login_frame.grid_forget()
    register_frame.grid(row=1, column=1)

def register():
    ad = entry_ad.get()
    soyad = entry_soyad.get()
    kullanici_adi = entry_kullanici_adi.get()
    password = entry_password.get()
    tc_kimlik_no = entry_tc_kimlik_no.get()
    telefon = entry_telefon.get()
    email = entry_email.get()
    adres = entry_adres.get()
    kullanici_type = kullanici_type_var.get()

    if not ad or not soyad or not kullanici_adi or not password or not tc_kimlik_no or not telefon or not email or not adres:
        messagebox.showerror("Hata", "Lütfen istenen bilgileri eksiksiz doldurun!")
        return

    cursor.execute("""
        INSERT INTO kullanıcılar (ad, soyad, kullanici_adi, password, tc_kimlik_no, telefon, email, adres, kullanici_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ad, soyad, kullanici_adi, password, tc_kimlik_no, telefon, email, adres, kullanici_type))
    conn.commit()

    messagebox.showinfo("Başarılı", "Kayıt Başarılı!")

def login():
    kullanici_adi = entry_login_kullanici_adi.get()
    password = entry_login_password.get()

    cursor.execute("""
        SELECT * FROM kullanıcılar WHERE kullanici_adi = ? AND password = ?
    """, (kullanici_adi, password))
    user = cursor.fetchone()

    if user is not None:
        messagebox.showinfo("Başarılı", "Giriş Başarılı!")
    else:
        messagebox.showerror("Hata", "Giriş Reddedildi!")

# Ana başlık
label_baslik = tk.Label(window, text="Takip Sistemi", font=("Arial", 18, "bold"))
label_baslik.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Giriş Ekranı
login_frame = tk.Frame(window)
login_frame.grid(row=1, column=1)

label_login_kullanici_adi = tk.Label(login_frame, text="Kullanıcı Adı:")
label_login_kullanici_adi.grid(row=0, column=0)
entry_login_kullanici_adi = tk.Entry(login_frame)
entry_login_kullanici_adi.grid(row=0, column=1)

label_login_password = tk.Label(login_frame, text="Password:")
label_login_password.grid(row=1, column=0)
entry_login_password = tk.Entry(login_frame, show="*")
entry_login_password.grid(row=1, column=1)

button_login = tk.Button(login_frame, text="Giriş", command=login)
button_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Kayıt Ol Ekranı
register_frame = tk.Frame(window)

label_ad = tk.Label(register_frame, text="Ad:")
label_ad.grid(row=0, column=0)
entry_ad = tk.Entry(register_frame)
entry_ad.grid(row=0, column=1)

label_soyad = tk.Label(register_frame, text="Soyad:")
label_soyad.grid(row=1, column=0)
entry_soyad = tk.Entry(register_frame)
entry_soyad.grid(row=1, column=1)

label_kullanici_adi = tk.Label(register_frame, text="Kullanıcı Adı:")
label_kullanici_adi.grid(row=2, column=0)
entry_kullanici_adi = tk.Entry(register_frame)
entry_kullanici_adi.grid(row=2, column=1)

label_password = tk.Label(register_frame, text="Password:")
label_password.grid(row=3, column=0)
entry_password = tk.Entry(register_frame, show="*")
entry_password.grid(row=3, column=1)

label_tc_kimlik_no = tk.Label(register_frame, text="TC Kimlik No:")
label_tc_kimlik_no.grid(row=4, column=0)
entry_tc_kimlik_no = tk.Entry(register_frame)
entry_tc_kimlik_no.grid(row=4, column=1)

label_telefon = tk.Label(register_frame, text="Telefon:")
label_telefon.grid(row=5, column=0)
entry_telefon = tk.Entry(register_frame)
entry_telefon.grid(row=5, column=1)

label_email = tk.Label(register_frame, text="Email:")
label_email.grid(row=6, column=0)
entry_email = tk.Entry(register_frame)
entry_email.grid(row=6, column=1)

label_adres = tk.Label(register_frame, text="Adres:")
label_adres.grid(row=7, column=0)
entry_adres = tk.Entry(register_frame)
entry_adres.grid(row=7, column=1)

label_kullanici_type = tk.Label(register_frame, text="Kullanıcı Type:")
label_kullanici_type.grid(row=8, column=0)

kullanici_type_options = ["Admin", "Kullanıcı"]
kullanici_type_var = tk.StringVar(register_frame)
kullanici_type_var.set(kullanici_type_options[0])

kullanici_type_menu = tk.OptionMenu(register_frame, kullanici_type_var, *kullanici_type_options)
kullanici_type_menu.grid(row=8, column=1)

button_register = tk.Button(register_frame, text="Kayıt Ol", command=register)
button_register.grid(row=9, column=0, columnspan=2)

# İlk olarak giriş ekranını göster
show_login_screen()

# Butonlar
button_login_screen = tk.Button(window, text="Giriş Yap", command=show_login_screen)
button_login_screen.grid(row=1, column=0, padx=10, pady=10)

button_register_screen = tk.Button(window, text="Kayıt Ol", command=show_register_screen)
button_register_screen.grid(row=1, column=2, padx=10, pady=10)

window.protocol("WM_DELETE_WINDOW", lambda: conn.close())

window.mainloop()