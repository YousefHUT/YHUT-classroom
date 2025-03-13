#This library is made by YousefHUT (Yusuf Eren HUT) and if you want to use this project, you don't need to give credit to me. You can use it freely.
import tkinter as tk
import pygubu
import pathlib
import json
import pyotp
import hashlib

__version__ = '0.5.0'
__author__ = 'YousefHUT'

PROJECT_PATH = pathlib.Path(__file__).resolve().parent
LOGIN_UI = PROJECT_PATH / 'login.ui'
USER_DATA_FILE = PROJECT_PATH / 'user.json'
ICON_PATH = PROJECT_PATH / 'icons'

class AuthApp:
    def __init__(self, master=None):
        self.signed = False
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file(LOGIN_UI)
        self.loginwindow = self.builder.get_object('loginwindow', master)
        self.loginwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.builder.connect_callbacks(self)

        #Giriş ekranını tanımla
        self.username_entry = self.builder.get_object('usernameloginentry')
        self.password_entry = self.builder.get_object('keyloginentry')
        self.message_label = self.builder.get_object('messagelabel')
        self.login_button = self.builder.get_object('loginbutton')
        self.login_button.config(command=self.on_login_button_click)
        self.forgot_key_button = self.builder.get_object('forgotkeybutton')
        self.forgot_key_button.config(command=self.on_forgot_key_button_click)

        #Doğrulama anahtarı verme ekranını tanımla
        self.auth_key_dialog = self.builder.get_object('authkeygivedialog', self.loginwindow)
        self.auth_key_label = self.builder.get_object('authkey')

        #Parola unutma diyaloğunu tanımla
        self.forgot_password_dialog = self.builder.get_object('forgotpassworddialog', self.loginwindow)
        self.auth_key_entry = self.builder.get_object('authkeyentry')
        self.send_auth_key_button = self.builder.get_object('sendauthkeybutton')
        self.send_auth_key_button.config(command=self.on_send_auth_key_button_click)

        #İkonları Yükle
        self.login_icon = self.load_icon("login.png")
        self.forgot_key_icon = self.load_icon("forgotkey.png")

        self.login_button.config(image=self.login_icon)
        self.send_auth_key_button.config(image=self.login_icon)
        self.forgot_key_button.config(image=self.forgot_key_icon)

        #Kullanıcı bilgilerini yükle
        self.load_user_data()
        self.update_message()

    def load_icon(self, icon_name):
        #İconları yükle
        icon_path = ICON_PATH / icon_name
        if icon_path.exists():
            return tk.PhotoImage(file=str(icon_path))
        else:
            print(f"Icon {icon_name} not found.")
            return None

    def md5_hash(self,text):
        #Verilen değeri şifrele
        hash_object = hashlib.md5()
        hash_object.update(text.encode('utf-8'))
        return hash_object.hexdigest()

    def load_user_data(self):
        #Kullanıcı verilerini yükle
        try:
            with open(USER_DATA_FILE, 'r') as f:
                self.user_data = json.load(f)
            self.user_data["username"] = self.user_data["username"]
            self.user_data["password"] = self.user_data["password"]
            self.user_data["authkey"] = self.user_data["authkey"]
            self.signin = True
        except:
            self.user_data = {}
            self.signin = False

    def save_user_data(self):
        #Giriş bilgilerni kaydet
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(self.user_data, f)

    def on_login_button_click(self):
        #Giriş butonuna basıldığında
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.signin:
            #giriş
            if self.user_data["username"] == self.md5_hash(username) and self.user_data["password"] == self.md5_hash(password):
                #Doğru giriş
                self.signed = True
                self.loginwindow.destroy()
                self.master.destroy()
            else:
                #Hatalı giriş
                self.message_label.config(text="Geçersiz kullanıcı adı veya şifre.")
        else:
            #Kullanıcıyı kaydetme
            self.user_data["username"] = self.md5_hash(username)
            self.user_data["password"] = self.md5_hash(password)
            self.user_data["authkey"] = pyotp.random_base32()
            self.auth_key_dialog.run()
            self.save_user_data()
            self.auth_key_label.config(text=self.user_data["authkey"])
            self.auth_key_label.bind("<Button-1>", self.copy)
            self.signin = True
            self.update_message()

    def copy(self, event=None):
        #Panoya kopyala
        self.clipboard_clear()
        self.clipboard_append(self.user_data["authkey"])
        self.update()

    def update_message(self):
        #Giriş mesajını güncelle
        if self.signin:
            self.message_label.config(text="Lütfen giriş yapın.")
            self.login_button.config(text="Giriş Yap")
        else:
            self.message_label.config(text="Lütfen kayıt olun.")
            self.login_button.config(text="Kayıt Ol")

    def on_forgot_key_button_click(self):
        #Şifremi unuttum menüsünü aç
        if self.signin:
            self.forgot_password_dialog.run()

    def on_send_auth_key_button_click(self):
        #Doğrulama anahtarını kontrol et
        username = self.username_entry.get()
        authkey = self.auth_key_entry.get()

        if authkey == pyotp.TOTP(self.user_data["authkey"]).now():
            del self.user_data["username"]
            del self.user_data["password"]
            del self.user_data["authkey"]
            self.save_user_data()
            self.message_label.config(text="Kullanıcı verileri sıfırlandı. Lütfen tekrar kayıt olun.")
            self.signin= False
            self.forgot_password_dialog.close()
        else:
            self.message_label.config(text="Geçersiz doğrulama anahtarı.")
            self.forgot_password_dialog.close()

    def on_closing(self):
        #Uygulamayı kapat
        self.loginwindow.destroy()
        exit()

def open_login_window():
    #Giriş penceresini aç
    auth = tk.Tk()
    app = AuthApp(auth)
    auth.withdraw()
    auth.protocol("WM_DELETE_WINDOW", app.on_closing)
    auth.mainloop()
    return app.signed

if __name__ == '__main__':
    #Uygulamayı başlat
    open_login_window()