# Dokumentasi lengkap untuk `main.py`

## Ringkasan

`main.py` mengimplementasikan aplikasi GUI bernama `MesinKasirApp` menggunakan `customtkinter` (wrapper modern untuk `tkinter`). Aplikasi ini menerima input total belanja dan uang yang dibayarkan, lalu menghitung kembalian dan menampilkan rincian pecahan menggunakan algoritma greedy (coin-change greedy) serta visualisasi pecahan.

## Dependensi

- Python 3.8+ (disarankan 3.10+)
- `customtkinter` (tercantum di `requirements.txt`)
- Sistem: paket `tk`/`tkinter` pada beberapa distribusi Linux harus diinstal melalui package manager (contoh: `sudo apt install python3-tk`).

Lihat juga: [README.md](README.md) untuk instruksi menjalankan.

## Struktur file

- `main.py` — kode aplikasi utama dan UI
- `requirements.txt` — daftar dependensi Python
- `README.md` — instruksi run umum
- `MAIN_DOCS.md` — dokumentasi ini

## Arsitektur dan Komponen Utama

- Kelas utama: `MesinKasirApp(ctk.CTk)` — turunan dari `customtkinter.CTk` yang merepresentasikan jendela aplikasi.
- UI dibagi menjadi dua panel:
  - Panel kiri: input pengguna (total belanja, uang bayar) dan tombol aksi (`Hitung Kembalian`, `Reset`).
  - Panel kanan: area visualisasi pecahan uang (widget per pecahan) dan area log teks yang menampilkan langkah-langkah eksekusi algoritma.

## Deskripsi fungsi / metode

- `__init__(self)`
  - Inisialisasi jendela, set tema `ctk.set_appearance_mode("Dark")` dan tema warna, konfigurasi layout grid, pemanggilan `buat_panel_kiri()` dan `buat_panel_kanan()`.

- `buat_panel_kiri(self)`
  - Membuat frame kiri, label judul, dua entry (`input_belanja`, `input_bayar`), tombol `btn_hitung` (memanggil `jalankan_greedy`) dan `btn_reset` (memanggil `reset_data`).

- `buat_panel_kanan(self)`
  - Membuat frame kanan yang berisi: label hasil, label total kembalian, `container_uang` (tempat widget pecahan), dan `teks_output` (CTkTextbox) untuk log.

- `buat_widget_uang(self, parent_container, pecahan, jumlah)`
  - Membuat satu widget visual untuk setiap pecahan uang. Jika `pecahan >= 1000` dianggap kertas (desain berbeda), jika kurang dianggap koin. Widget berisi ikon, teks pecahan, dan jumlah.

- `perbarui_visual_uang(self, rincian_hasil)`
  - Menghapus widget lama di `container_uang` dan membuat widget baru berdasarkan `rincian_hasil` (list of tuples `(pecahan, jumlah)`).

- `jalankan_greedy(self)`
  - Fungsi utama untuk menghitung kembalian:
    1. Ambil input dari `self.input_belanja` dan `self.input_bayar` lalu konversi ke `int`. Jika gagal, tampilkan `messagebox.showerror`.
    2. Validasi: jika `bayar < belanja`, tampilkan peringatan dan kosongkan visual.
    3. Hitung `kembalian = bayar - belanja` dan perbarui label kembalian.
    4. Definisikan daftar pecahan Rupiah: `[100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]`.
    5. Iterasi pecahan dari besar ke kecil, gunakan pembagian bulat (`//`) untuk mendapatkan jumlah lembar/keping untuk setiap pecahan, lalu hitung sisa (`%`). Untuk setiap langkah, tambahkan baris ke `teks_output` (log).
    6. Panggil `perbarui_visual_uang(rincian_hasil)` untuk membuat widget visual.
    7. Jika masih ada sisa setelah memakai semua pecahan yang ada (mis. Rp 50), tampilkan peringatan di log.

- `reset_data(self)`
  - Menghapus isi entry, reset label kembalian, kosongkan visual `container_uang`, dan kembalikan `teks_output` ke pesan awal.

## Algoritma Greedy (Penjelasan langkah demi langkah)

Masalah: berikan kembalian sejumlah X menggunakan jumlah lembar/keping minimal dari himpunan pecahan yang tersedia.

Strategi greedy dipilih karena untuk pecahan mata uang Rupiah (nilai bernilai 'canonical' / sistem mata uang berbasis polinomial umum), algoritma greedy menghasilkan solusi optimal (jumlah koin/lembar minimal). Langkah-langkah:

1. Diberi kembalian awal `sisa = kembalian`.
2. Urutkan atau gunakan daftar pecahan dari yang terbesar ke terkecil.
3. Untuk setiap `pecahan` di daftar:
   - Jika `sisa >= pecahan`, hitung `jumlah = sisa // pecahan` (berapa banyak lembar/keping pecahan ini bisa digunakan).
   - Kurangi sisa: `sisa = sisa % pecahan`.
   - Simpan pasangan `(pecahan, jumlah)` jika `jumlah > 0`.
   - Catat langkah/hasil ke log untuk transparansi.
4. Setelah iterasi semua pecahan, jika `sisa > 0`, berarti ada nilai sisa yang tidak dapat dipecahkan dengan pecahan yang tersedia (contoh: ada sisa 50 saat pecahan terkecil 100), tampilkan peringatan.

Contoh eksekusi singkat:
- belanja = 1750, bayar = 5000 → kembalian = 3250
- pecahan 2000 → ambil 1 (sisa 1250)
- pecahan 1000 → ambil 1 (sisa 250)
- pecahan 200 → ambil 1 (sisa 50)
- pecahan 100 → ambil 0 (sisa 50)
- sisa 50 > 0 → peringatan: tidak ada pecahan 50

## Kompleksitas

- Time: O(m) di mana m = jumlah pecahan (konstant kecil, di sini m=10). Input parsing adalah O(1) relatif terhadap ukuran pecahan.
- Space: O(k) untuk menyimpan `rincian_hasil`, di mana k ≤ m.

## Validasi input dan penanganan error

- Input diambil dari `CTkEntry` dan dikonversi ke `int`. Jika input tidak bisa dikonversi (mis. berisi huruf atau tanda koma/desimal), aplikasi menampilkan dialog error.
- Validasi untuk `bayar < belanja` menampilkan peringatan.

Rekomendasi perbaikan validasi:
- Terima angka dengan pemisah ribuan (mis. `1.750` atau `1,750`) dengan melakukan pra-pembersihan string sebelum `int()` (hapus titik/komas), atau gunakan input bertipe `float` dan pembulatan ke integer jika perlu.

## Edge cases dan catatan

- Pecahan terkecil di daftar adalah 100, sehingga sisa yang bukan kelipatan 100 tidak bisa dikembalikan.
- Asumsi: input dalam satuan Rupiah utuh (tanpa desimal).
- Aplikasi GUI akan berjalan hanya pada platform yang memiliki `tkinter`.

## Tes manual yang disarankan

1. Kasus normal: belanja=12000, bayar=20000 → kembalian=8000 → 1x5000 + 1x2000 + 1x1000
2. Uang pas: belanja=5000, bayar=5000 → tidak ada kembalian
3. Uang kurang: belanja=6000, bayar=5000 → munculkan peringatan
4. Nilai non-kelipatan: belanja=9950, bayar=10000 → sisa 50 → peringatan sisa
5. Input invalid: belanja='abc' → munculkan error input

## Saran pengembangan / peningkatan

- Ekstraksi logika bisnis ke modul terpisah (`change_calculator.py`) sehingga UI hanya memanggil fungsi yang diuji secara independen.
- Tambahkan unit tests untuk fungsi greedy (mis. gunakan `pytest`).
- Tambahkan parsing input yang lebih toleran (mengizinkan pemisah ribuan dan simbol mata uang).
- Tambah konfigurasi pecahan sebagai file konfigurasi (mis. `json`/`yaml`) untuk mendukung mata uang lain.
- Tambah fitur pengembalian stok atau simulasi ketersediaan koin/lembar (keterbatasan jumlah tiap pecahan) — ubah algoritma menjadi bounded-change (greedy mungkin perlu disesuaikan atau diganti dengan DP untuk optimalitas jika ada batasan jumlah per pecahan).
- Paket sebagai executable (`PyInstaller`) atau `Dockerfile` untuk portability.

## Cara menjalankan (ringkasan)

Ikuti langkah di [README.md](README.md). Ringkasan singkat:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Referensi tambahan

- Dokumentasi `customtkinter`: https://github.com/TomSchimansky/CustomTkinter
- PyInstaller: https://www.pyinstaller.org/

---

Dokumentasi ini dibuat otomatis berdasarkan isi `main.py`.
