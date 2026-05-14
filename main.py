import customtkinter as ctk
from tkinter import messagebox

# Pengaturan Tema CustomTkinter
ctk.set_appearance_mode("Dark")  # Bisa diubah ke "Light" atau "System"
ctk.set_default_color_theme("blue")  # Pilihan: "blue", "green", "dark-blue"

class MesinKasirApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Utama
        self.title("Sistem Kasir Pintar")
        self.geometry("900x650")
        self.resizable(False, False)

        # Membagi layout menjadi 2 kolom (Kiri dan Kanan)
        self.grid_columnconfigure(0, weight=1) # Panel Kiri
        self.grid_columnconfigure(1, weight=2) # Panel Kanan
        self.grid_rowconfigure(0, weight=1)

        self.buat_panel_kiri()
        self.buat_panel_kanan()

    def buat_panel_kiri(self):
        """Membuat area input di sebelah kiri"""
        self.panel_kiri = ctk.CTkFrame(self, corner_radius=0)
        self.panel_kiri.grid(row=0, column=0, sticky="nsew")

        self.label_judul = ctk.CTkLabel(self.panel_kiri, text="Area Kasir", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_judul.pack(pady=(40, 20), padx=20)

        self.input_belanja = ctk.CTkEntry(self.panel_kiri, placeholder_text="Total Belanja (Rp)", font=ctk.CTkFont(size=14))
        self.input_belanja.pack(pady=10, padx=20, fill="x")

        self.input_bayar = ctk.CTkEntry(self.panel_kiri, placeholder_text="Uang Dibayar (Rp)", font=ctk.CTkFont(size=14))
        self.input_bayar.pack(pady=10, padx=20, fill="x")

        self.btn_hitung = ctk.CTkButton(self.panel_kiri, text="Hitung Kembalian", font=ctk.CTkFont(weight="bold"), command=self.jalankan_greedy)
        self.btn_hitung.pack(pady=(30, 10), padx=20, fill="x")

        self.btn_reset = ctk.CTkButton(self.panel_kiri, text="Reset", fg_color="gray", hover_color="darkgray", command=self.reset_data)
        self.btn_reset.pack(pady=5, padx=20, fill="x")

    def buat_panel_kanan(self):
        """Membuat area hasil dan visualisasi di sebelah kanan"""
        self.panel_kanan = ctk.CTkFrame(self, corner_radius=0)
        self.panel_kanan.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.panel_kanan.grid_rowconfigure(0, weight=2) # Area Visual
        self.panel_kanan.grid_rowconfigure(1, weight=1) # Area Log
        self.panel_kanan.grid_columnconfigure(0, weight=1)

        self.area_visual_uang = ctk.CTkFrame(self.panel_kanan, fg_color="transparent")
        self.area_visual_uang.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_hasil = ctk.CTkLabel(self.area_visual_uang, text="Visualisasi Pecahan Uang", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_hasil.pack(pady=(10, 10))

        self.label_kembalian = ctk.CTkLabel(self.area_visual_uang, text="Total Kembalian: Rp 0", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2FA572")
        self.label_kembalian.pack(pady=(0, 20))

        self.container_uang = ctk.CTkFrame(self.area_visual_uang, fg_color="transparent")
        self.container_uang.pack(fill="x", padx=10)


        # --- Area Bawah: Log Eksekusi Greedy ---
        self.area_log_greedy = ctk.CTkFrame(self.panel_kanan, fg_color="transparent")
        self.area_log_greedy.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.label_log = ctk.CTkLabel(self.area_log_greedy, text="Log Eksekusi Greedy Algorithm", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_log.pack(pady=(0, 10))

        self.teks_output = ctk.CTkTextbox(self.area_log_greedy, width=400, height=150, font=ctk.CTkFont(size=14))
        self.teks_output.pack(pady=10, padx=20, fill="both", expand=True)
        self.teks_output.insert("0.0", "Menunggu input pengguna...\n")
        self.teks_output.configure(state="disabled") # Kunci agar tidak bisa diedit manual

    def buat_widget_uang(self, parent_container, pecahan, jumlah):
        """Membuat satu widget visual uang (kertas) menggunakan teks"""
        is_kertas = pecahan >= 1000
        nama_pecahan = f"Rp {pecahan:,}"
        text_jumlah = f"{jumlah}x"

        # Konfigurasi gaya visual
        if is_kertas:
            frame_gaya = {
                "master": parent_container,
                "fg_color": "#1F1F1F",
                "border_width": 2,
                "border_color": "#2FA572",
                "corner_radius": 10
            }
            text_ikon = "$"
            main_font_size = 18
            count_font_size = 14
        else:
            # Koin lingkaran abu-abu
            frame_gaya = {
                "master": parent_container,
                "fg_color": "#1F1F1F",
                "border_width": 2,
                "border_color": "#404040",
                "corner_radius": 90 
            }
            text_ikon = "O" #
            main_font_size = 16
            count_font_size = 12

        widget_frame = ctk.CTkFrame(**frame_gaya)
        widget_frame.pack(side="left", padx=10, pady=10)

        icon_label = ctk.CTkLabel(widget_frame, text=text_ikon, font=ctk.CTkFont(size=36))
        icon_label.pack(pady=(10, 0))

        # 2. Pecahan
        pecahan_label = ctk.CTkLabel(widget_frame, text=nama_pecahan, font=ctk.CTkFont(size=main_font_size, weight="bold"))
        pecahan_label.pack(pady=(5, 0))

        # 3. Jumlah
        jumlah_label = ctk.CTkLabel(widget_frame, text=text_jumlah, font=ctk.CTkFont(size=count_font_size))
        jumlah_label.pack(pady=(0, 10))

    def perbarui_visual_uang(self, rincian_hasil):
        """Hapus visual lama dan buat yang baru dari rincian hasil"""
        # Hapus semua widget di container_uang
        for child in self.container_uang.winfo_children():
            child.destroy()

        if not rincian_hasil:
             return

        # Iterasi dan buat widget uang baru
        for pecahan, jumlah in rincian_hasil:
            self.buat_widget_uang(self.container_uang, pecahan, jumlah)

    # === Modifikasi Fungsi Utama yang Ada ===

    def jalankan_greedy(self):
        """Fungsi utama (Sama seperti sebelumnya, dengan penambahan update visual)"""
        try:
            # Mengambil nilai input dan memastikan itu angka
            belanja = int(self.input_belanja.get())
            bayar = int(self.input_bayar.get())
        except ValueError:
            messagebox.showerror("Error Input", "Mohon masukkan angka yang valid tanpa titik atau koma!")
            return

        # Validasi logika kasir
        if bayar < belanja:
            messagebox.showwarning("Uang Kurang", "Uang yang dibayarkan tidak cukup untuk membayar total belanja!")
            self.perbarui_visual_uang([])
            return

        kembalian = bayar - belanja
        self.label_kembalian.configure(text=f"Total Kembalian: Rp {kembalian:,}")

        # Daftar pecahan uang Rupiah
        pecahan_rupiah = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]
        
        sisa_kembalian = kembalian
        rincian_hasil = []

        # Membuka kunci kotak teks untuk memasukkan log baru
        self.teks_output.configure(state="normal")
        self.teks_output.delete("1.0", "end")
        self.teks_output.insert("end", "=== LOG EKSEKUSI GREEDY ===\n\n")

        # LOGIKA ALGORITMA GREEDY
        for pecahan in pecahan_rupiah:
            if sisa_kembalian >= pecahan:
                # Cari berapa lembar/keping yang bisa didapat
                jumlah = sisa_kembalian // pecahan
                # Sisa uang yang belum dikembalikan
                sisa_kembalian = sisa_kembalian % pecahan
                
                rincian_hasil.append((pecahan, jumlah))
                self.teks_output.insert("end", f"[Step] Ambil pecahan Rp {pecahan:,} sebanyak {jumlah}x. Sisa: Rp {sisa_kembalian:,}\n")

        # --- Update Visualisasi Uang (Penambahan) ---
        self.perbarui_visual_uang(rincian_hasil)

        self.teks_output.insert("end", "\n=== HASIL AKHIR (REKAPITULASI) ===\n\n")
        
        # Menampilkan rekapitulasi akhir di log teks
        if not rincian_hasil:
             self.teks_output.insert("end", "Tidak ada kembalian (Uang Pas).\n")
        else:
            for pecahan, jumlah in rincian_hasil:
                jenis = "lembar" if pecahan >= 1000 else "keping"
                self.teks_output.insert("end", f"✔️ {jumlah} {jenis} Rp {pecahan:,}\n")
        
        # Mengecek jika ada sisa (misal sisa Rp 50 yang tidak ada pecahannya)
        if sisa_kembalian > 0:
            self.teks_output.insert("end", f"\n⚠️ Peringatan: Terdapat sisa Rp {sisa_kembalian:,} yang tidak dapat dikembalikan karena pecahan tidak tersedia.")

        self.teks_output.configure(state="disabled") # Kunci kembali kotak teks

    def reset_data(self):
        """Mengembalikan aplikasi ke kondisi awal (Perlu memanggil reset visual)"""
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