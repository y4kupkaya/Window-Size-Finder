# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/Window-Size-Finder > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/Window-Size-Finder/blob/master/LICENSE/ >
# ================================================================

__updated__ = "2023-04-08 23:26:59"

import tkinter as tk
import win32gui


class WindowSelector:
    def __init__(self, master: tk.Tk):
        self.master = master  # root
        self.x, self.y = 0, 0  # pencere koordinatları

        self.select_button = tk.Button(
            self.master, text="Pencere Seç", command=self.get_window
        )  # pencere seç butonu
        self.select_button.pack()  # pencere seç butonunu ekle

        self.coordinates_label = tk.Label(self.master, text="")
        self.coordinates_label.pack()

        self.copy_button = tk.Button(
            self.master, text="Kopyala", command=self.copy_coords
        )  # kopyala butonu

    def get_window(self):
        windows = []  # pencerelerin listesi

        def enum_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):  # pencere görünürse
                text = win32gui.GetWindowText(hwnd)  # pencere başlığını al
                if text:  # başlık varsa
                    windows.append(
                        (hwnd, text)
                    )  # başlığı ve pencere numarasını listeye ekle

        win32gui.EnumWindows(enum_callback, [])  # tüm pencereleri dolaş

        self.window_selection = tk.Toplevel(self.master)  # pencere seçme penceresi
        self.window_selection.title(
            "Boyutunu bulmak istediğiniz pencereyi seçin"
        )  # pencere başlığı
        self.window_selection.state("zoomed")  # pencereyi tam ekran yap
        self.window_selection.attributes("-topmost", True)  # pencereyi üstte tut

        for i, (hwnd, text) in enumerate(windows):  # pencereleri dolaş
            b = tk.Button(
                self.window_selection,
                text=text,
                command=lambda hwnd=hwnd: self.get_coords(hwnd),
            )  # <pencere> seç butonu
            b.pack()  # <pencere> seç butonunu ekle

    def get_coords(self, hwnd):
        rect = win32gui.GetWindowRect(hwnd)  # pencerenin koordinatlarını al
        x = rect[0]  # x koordinatı
        y = rect[1]  # y koordinatı
        w = rect[2] - x  # genişlik
        h = rect[3] - y  # yükseklik
        self.x, self.y, self.w, self.h = x, y, w, h  # koordinatları kaydet
        self.window_selection.destroy()  # pencere seçme penceresini kapat
        self.coordinates_label.configure(
            text=f"x={self.w}, y={self.h}"
        )  # koordinatları ekrana yaz
        self.copy_button.pack()

    def copy_coords(self):
        self.master.clipboard_clear()  # kopyalama yapmadan önce temizle
        self.master.clipboard_append(f"x={self.w}, y={self.h}")  # kopyala
        self.master.update()

        popup = tk.Toplevel()
        popup.geometry(
            "150x50+{}+{}".format(root.winfo_width() // 2, root.winfo_height() // 2)
        )  # Pencere Boyutu
        popup.config(bg="black")
        popup.title("Kopyalandı")
        popup.resizable(False, False)  #  boyutlandırmayı engelle
        popup.overrideredirect(True)  # üst yönetim panelini kapatır

        popup_label = tk.Label(
            popup, text="Kopyalandı", font=("Arial", 16), bg="black", fg="white"
        )  # popup mesajı
        popup_label.pack(pady=10)
        close_button = tk.Button(popup, text="Kapat", command=popup.destroy)
        close_button.pack(pady=5)  # 1 saniye sonra popup mesajı kapa
        popup.after(1000, popup.destroy)


root = tk.Tk()  # root penceresi
app = WindowSelector(root)  # pencere seçme sınıfı
root.mainloop()  # Programı çalıştır
