import customtkinter as ctk
from tkinter import messagebox
import time
import json
import os

# Pengaturan Tema CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MesinKasirApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Kasir Pintar")
        self.geometry("1920x1200")
        self.resizable(True, True) 
        
        self.file_json = "stok_uang.json"
        self.stok_uang = self.muat_stok_uang()
        self.stok_entries = {}

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3) 
        self.grid_rowconfigure(0, weight=1)

        self.buat_panel_kiri()
        self.buat_panel_kanan()

    def muat_stok_uang(self):
        """Membaca stok uang dari file JSON. Jika tidak ada, buat baru dengan stok default."""
        if not os.path.exists(self.file_json):
            stok_awal = {
                "100000": 10, "50000": 10, "20000": 10, "10000": 10,
                "5000": 10, "2000": 20, "1000": 20, "500": 20,
                "200": 20, "100": 20
            }
            with open(self.file_json, "w") as file:
                json.dump(stok_awal, file, indent=4)
            return stok_awal
        else:
            with open(self.file_json, "r") as file:
                return json.load(file)

    def simpan_stok_uang(self):
        """Menyimpan perubahan stok uang kembali ke file JSON."""
        with open(self.file_json, "w") as file:
            json.dump(self.stok_uang, file, indent=4)

    def buat_panel_kiri(self):
        """Membuat area input dan manajemen stok di sebelah kiri"""
        self.panel_kiri = ctk.CTkFrame(self, corner_radius=0)
        self.panel_kiri.grid(row=0, column=0, sticky="nsew")

        self.label_judul = ctk.CTkLabel(self.panel_kiri, text="Area Transaksi Kasir", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_judul.pack(pady=(30, 20), padx=20)

        self.input_belanja = ctk.CTkEntry(self.panel_kiri, placeholder_text="Total Belanja (Rp)", font=ctk.CTkFont(size=14))
        self.input_belanja.pack(pady=10, padx=20, fill="x")

        self.input_bayar = ctk.CTkEntry(self.panel_kiri, placeholder_text="Uang Dibayar (Rp)", font=ctk.CTkFont(size=14))
        self.input_bayar.pack(pady=10, padx=20, fill="x")

        self.btn_hitung = ctk.CTkButton(self.panel_kiri, text="Hitung Kembalian", font=ctk.CTkFont(weight="bold"), command=self.jalankan_greedy)
        self.btn_hitung.pack(pady=(20, 10), padx=20, fill="x")

        self.btn_reset = ctk.CTkButton(self.panel_kiri, text="Reset", fg_color="gray", hover_color="darkgray", command=self.reset_data)
        self.btn_reset.pack(pady=5, padx=20, fill="x")

        pembatas = ctk.CTkFrame(self.panel_kiri, height=2, fg_color="#404040")
        pembatas.pack(pady=20, padx=20, fill="x")

        self.label_stok = ctk.CTkLabel(self.panel_kiri, text="Jumlah Pecahan Uang", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_stok.pack(pady=(0, 10), padx=20)

        self.frame_stok = ctk.CTkScrollableFrame(self.panel_kiri, height=250)
        self.frame_stok.pack(pady=5, padx=20, fill="both", expand=True)

        pecahan_urut = sorted(self.stok_uang.keys(), key=int, reverse=True)
        for pecahan in pecahan_urut:
            row_frame = ctk.CTkFrame(self.frame_stok, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(row_frame, text=f"Rp {int(pecahan):,}", width=100, anchor="w", font=ctk.CTkFont(weight="bold"))
            lbl.pack(side="left")
            
            ent = ctk.CTkEntry(row_frame, width=80, justify="center")
            ent.insert(0, str(self.stok_uang[pecahan]))
            ent.pack(side="right")
            
            self.stok_entries[pecahan] = ent 

        self.btn_simpan_stok = ctk.CTkButton(self.panel_kiri, text="Simpan Perubahan Stok", fg_color="#2FA572", hover_color="#248058", command=self.simpan_stok_manual)
        self.btn_simpan_stok.pack(pady=(15, 30), padx=20, fill="x")

    def simpan_stok_manual(self):
        """Fungsi untuk menyimpan perubahan angka yang diketik manual oleh pengguna di UI"""
        try:
            for pecahan, ent in self.stok_entries.items():
                nilai_baru = int(ent.get())
                if nilai_baru < 0: nilai_baru = 0 
                self.stok_uang[pecahan] = nilai_baru
            
            self.simpan_stok_uang()
            messagebox.showinfo("Stok Diperbarui", "Jumlah uang di dalam kasir berhasil diperbarui secara manual!")
        except ValueError:
            messagebox.showerror("Error Input Stok", "Pastikan semua input stok berupa angka bulat (tidak boleh kosong/huruf).")
            self.perbarui_ui_stok()

    def perbarui_ui_stok(self):
        """Fungsi untuk memperbarui angka di layar secara otomatis (Real-time) saat transaksi berhasil"""
        for pecahan, ent in self.stok_entries.items():
            ent.delete(0, 'end')
            ent.insert(0, str(self.stok_uang[pecahan]))

    def buat_panel_kanan(self):
        """Membuat area hasil dan visualisasi di sebelah kanan"""
        self.panel_kanan = ctk.CTkFrame(self, corner_radius=0)
        self.panel_kanan.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.panel_kanan.grid_rowconfigure(0, weight=2)
        self.panel_kanan.grid_rowconfigure(1, weight=1)
        self.panel_kanan.grid_columnconfigure(0, weight=1)

        self.area_visual_uang = ctk.CTkFrame(self.panel_kanan, fg_color="transparent")
        self.area_visual_uang.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_hasil = ctk.CTkLabel(self.area_visual_uang, text="Visualisasi Pecahan Uang", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_hasil.pack(pady=(10, 10))

        self.label_kembalian = ctk.CTkLabel(self.area_visual_uang, text="Total Kembalian: Rp 0", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2FA572")
        self.label_kembalian.pack(pady=(0, 20))

        self.container_uang = ctk.CTkFrame(self.area_visual_uang, fg_color="transparent")
        self.container_uang.pack(fill="x", padx=10)

        self.area_log_greedy = ctk.CTkFrame(self.panel_kanan, fg_color="transparent")
        self.area_log_greedy.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.label_log = ctk.CTkLabel(self.area_log_greedy, text="Log Eksekusi Greedy Algorithm", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_log.pack(pady=(0, 10))

        self.teks_output = ctk.CTkTextbox(self.area_log_greedy, width=400, height=150, font=ctk.CTkFont(size=14))
        self.teks_output.pack(pady=10, padx=20, fill="both", expand=True)
        self.teks_output.insert("0.0", "Menunggu input pengguna...\n")
        self.teks_output.configure(state="disabled") 

    def buat_widget_uang(self, parent_container, pecahan, jumlah):
        """Membuat satu widget visual uang (kertas) menggunakan teks"""
        is_kertas = pecahan >= 1000
        nama_pecahan = f"Rp {pecahan:,}"
        text_jumlah = f"{jumlah}x"

        if is_kertas:
            frame_gaya = {
                "master": parent_container,
                "fg_color": "#1F1F1F",
                "border_width": 2,
                "border_color": "#2FA572",
                "corner_radius": 10
            }
            text_ikon = "💵"
            main_font_size = 18
            count_font_size = 14
        else:
            frame_gaya = {
                "master": parent_container,
                "fg_color": "#1F1F1F",
                "border_width": 2,
                "border_color": "#404040",
                "corner_radius": 90 
            }
            text_ikon = "🪙"
            main_font_size = 16
            count_font_size = 12

        widget_frame = ctk.CTkFrame(**frame_gaya)
        widget_frame.pack(side="left", padx=10, pady=10)

        icon_label = ctk.CTkLabel(widget_frame, text=text_ikon, font=ctk.CTkFont(size=36))
        icon_label.pack(pady=(10, 0))

        pecahan_label = ctk.CTkLabel(widget_frame, text=nama_pecahan, font=ctk.CTkFont(size=main_font_size, weight="bold"))
        pecahan_label.pack(pady=(5, 0))

        jumlah_label = ctk.CTkLabel(widget_frame, text=text_jumlah, font=ctk.CTkFont(size=count_font_size))
        jumlah_label.pack(pady=(0, 10))

    def perbarui_visual_uang(self, rincian_hasil):
        """Hapus visual lama dan buat yang baru dari rincian hasil"""
        for child in self.container_uang.winfo_children():
            child.destroy()
        if not rincian_hasil:
             return
        for pecahan, jumlah in rincian_hasil:
            self.buat_widget_uang(self.container_uang, pecahan, jumlah)

    def jalankan_greedy(self):
        try:
            belanja = int(self.input_belanja.get())
            bayar = int(self.input_bayar.get())
        except ValueError:
            messagebox.showerror("Error Input", "Mohon masukkan angka yang valid tanpa titik atau koma!")
            return

        if bayar < belanja:
            messagebox.showwarning("Uang Kurang", "Uang yang dibayarkan tidak cukup untuk membayar total belanja!")
            self.perbarui_visual_uang([])
            return

        kembalian = bayar - belanja
        self.label_kembalian.configure(text=f"Total Kembalian: Rp {kembalian:,}")

        pecahan_rupiah_str = sorted(self.stok_uang.keys(), key=int, reverse=True)
        sisa_kembalian = kembalian
        rincian_hasil = []
        
        stok_sementara = self.stok_uang.copy()

        self.teks_output.configure(state="normal")
        self.teks_output.delete("1.0", "end")
        self.teks_output.insert("end", "=== LOG EKSEKUSI GREEDY (STOK TERBATAS) ===\n\n")
        
        waktu_mulai = time.perf_counter()

        for pecahan_str in pecahan_rupiah_str:
            pecahan = int(pecahan_str)
            stok_tersedia = stok_sementara[pecahan_str]

            if sisa_kembalian >= pecahan and stok_tersedia > 0:
                jumlah_dibutuhkan = sisa_kembalian // pecahan
                jumlah_diambil = min(jumlah_dibutuhkan, stok_tersedia)
                
                sisa_kembalian -= (jumlah_diambil * pecahan)
                stok_sementara[pecahan_str] -= jumlah_diambil
                
                rincian_hasil.append((pecahan, jumlah_diambil))
                self.teks_output.insert("end", f"[Step] Ambil pecahan Rp {pecahan:,} sebanyak {jumlah_diambil}x (Sisa Stok: {stok_sementara[pecahan_str]}). Sisa Kembalian: Rp {sisa_kembalian:,}\n")

        waktu_selesai = time.perf_counter()
        waktu_eksekusi_ms = (waktu_selesai - waktu_mulai) * 1000

        self.teks_output.insert("end", "\n=== HASIL AKHIR (REKAPITULASI) ===\n\n")

        if sisa_kembalian > 0:
            self.perbarui_visual_uang([])
            
            self.teks_output.insert("end", f"⚠️ GAGAL: Sisa Rp {sisa_kembalian:,} tidak memiliki solusi pecahan.\n")
            self.teks_output.insert("end", "❌ TRANSAKSI DIBATALKAN. Stok laci tidak dikurangi.\n")
            
            pesan_error = (
                f"Transaksi gagal karena stok pecahan uang tidak memadai!\n\n"
                f"Target Kembalian: Rp {kembalian:,}\n"
                f"Sisa yang tidak tertutup: Rp {sisa_kembalian:,}\n\n"
                f"Sistem membatalkan transaksi untuk mencegah kerugian kasir."
            )
            messagebox.showerror("Gagal Menemukan Solusi (Greedy Error)", pesan_error)

        else:
            self.perbarui_visual_uang(rincian_hasil)
            if not rincian_hasil:
                 self.teks_output.insert("end", "Tidak ada kembalian (Uang Pas).\n")
            else:
                for pecahan, jumlah in rincian_hasil:
                    jenis = "lembar" if pecahan >= 1000 else "keping"
                    self.teks_output.insert("end", f"✔️ {jumlah} {jenis} Rp {pecahan:,}\n")
            
            self.teks_output.insert("end", "\n✅ Kembalian berhasil diberikan sepenuhnya.\n")
            
            self.stok_uang = stok_sementara
            self.simpan_stok_uang()
            
            self.perbarui_ui_stok()

        self.teks_output.insert("end", f"\n⏱️ Waktu Eksekusi Algoritma: {waktu_eksekusi_ms:.4f} milidetik")
        self.teks_output.configure(state="disabled")

    def reset_data(self):
        """Mengembalikan aplikasi ke kondisi awal"""
        self.input_belanja.delete(0, 'end')
        self.input_bayar.delete(0, 'end')
        self.label_kembalian.configure(text="Total Kembalian: Rp 0")
        
        self.perbarui_visual_uang([])

        self.teks_output.configure(state="normal")
        self.teks_output.delete("1.0", "end")
        self.teks_output.insert("0.0", "Menunggu input pengguna...\n")
        self.teks_output.configure(state="disabled")

if __name__ == "__main__":
    app = MesinKasirApp()
    app.mainloop()