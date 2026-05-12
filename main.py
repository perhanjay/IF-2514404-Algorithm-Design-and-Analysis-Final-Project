import customtkinter as ctk
from tkinter import messagebox

# Pengaturan Tema CustomTkinter
ctk.set_appearance_mode("Dark")  # Bisa diubah ke "Light" atau "System"
ctk.set_default_color_theme("blue")  # Pilihan: "blue", "green", "dark-blue"

class MesinKasirApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Utama
        self.title("Sistem Kasir Pintar - Algoritma Greedy")
        self.geometry("800x500")
        self.resizable(False, False)

        # Membagi layout menjadi 2 kolom (Kiri dan Kanan)
        self.grid_columnconfigure(0, weight=1) # Panel Kiri (lebih sempit)
        self.grid_columnconfigure(1, weight=2) # Panel Kanan (lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        self.buat_panel_kiri()
        self.buat_panel_kanan()

    def buat_panel_kiri(self):
        """Membuat area input di sebelah kiri"""
        self.panel_kiri = ctk.CTkFrame(self, corner_radius=0)
        self.panel_kiri.grid(row=0, column=0, sticky="nsew")

        # Judul Input
        self.label_judul = ctk.CTkLabel(self.panel_kiri, text="Area Kasir", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_judul.pack(pady=(40, 20), padx=20)

        # Input Total Belanja
        self.input_belanja = ctk.CTkEntry(self.panel_kiri, placeholder_text="Total Belanja (Rp)", font=ctk.CTkFont(size=14))
        self.input_belanja.pack(pady=10, padx=20, fill="x")

        # Input Uang Dibayar
        self.input_bayar = ctk.CTkEntry(self.panel_kiri, placeholder_text="Uang Dibayar (Rp)", font=ctk.CTkFont(size=14))
        self.input_bayar.pack(pady=10, padx=20, fill="x")

        # Tombol Proses
        self.btn_hitung = ctk.CTkButton(self.panel_kiri, text="Hitung Kembalian", font=ctk.CTkFont(weight="bold"), command=self.jalankan_greedy)
        self.btn_hitung.pack(pady=(30, 10), padx=20, fill="x")

        # Tombol Reset
        self.btn_reset = ctk.CTkButton(self.panel_kiri, text="Reset", fg_color="gray", hover_color="darkgray", command=self.reset_data)
        self.btn_reset.pack(pady=5, padx=20, fill="x")

    def buat_panel_kanan(self):
        """Membuat area hasil dan visualisasi di sebelah kanan"""
        self.panel_kanan = ctk.CTkFrame(self)
        self.panel_kanan.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Judul Hasil
        self.label_hasil = ctk.CTkLabel(self.panel_kanan, text="Visualisasi Algoritma Greedy", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_hasil.pack(pady=(20, 10), padx=20)

        # Label Total Kembalian
        self.label_kembalian = ctk.CTkLabel(self.panel_kanan, text="Total Kembalian: Rp 0", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2FA572")
        self.label_kembalian.pack(pady=5, padx=20)

        # Kotak Teks untuk menampilkan rincian / log algoritma
        self.teks_output = ctk.CTkTextbox(self.panel_kanan, width=400, height=300, font=ctk.CTkFont(size=14))
        self.teks_output.pack(pady=10, padx=20, fill="both", expand=True)
        self.teks_output.insert("0.0", "Menunggu input pengguna...\n")
        self.teks_output.configure(state="disabled") # Kunci agar tidak bisa diedit manual

    def jalankan_greedy(self):
        """Fungsi utama yang memproses input dan menjalankan Algoritma Greedy"""
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
            return

        kembalian = bayar - belanja
        self.label_kembalian.configure(text=f"Total Kembalian: Rp {kembalian:,}")

        # Daftar pecahan uang Rupiah (dari terbesar ke terkecil - Syarat utama Greedy)
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

        self.teks_output.insert("end", "\n=== HASIL AKHIR (PECAHAN YANG DISERAHKAN) ===\n\n")
        
        # Menampilkan rekapitulasi akhir
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
        """Mengembalikan aplikasi ke kondisi awal"""
        self.input_belanja.delete(0, 'end')
        self.input_bayar.delete(0, 'end')
        self.label_kembalian.configure(text="Total Kembalian: Rp 0")
        
        self.teks_output.configure(state="normal")
        self.teks_output.delete("1.0", "bhend")
        self.teks_output.insert("0.0", "Menunggu input pengguna...\n")
        self.teks_output.configure(state="disabled")

if __name__ == "__main__":
    app = MesinKasirApp()
    app.mainloop()  