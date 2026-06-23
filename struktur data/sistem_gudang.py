"""
=============================================================
  SISTEM MANAJEMEN GUDANG
  Struktur Data: Linked List + Stack
  Database: CSV
  Operasi: CRUD (Create, Read, Update, Delete)
=============================================================
"""

import csv
import os
from datetime import datetime

CSV_FILE = "gudang.csv"
CSV_FIELDNAMES = ["id", "nama_barang", "kategori", "jumlah", "satuan", "lokasi", "tanggal_masuk"]

# ─────────────────────────────────────────────
# STRUKTUR DATA 1: LINKED LIST
# ─────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Menyimpan semua data barang dalam memori sebagai Linked List."""

    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def delete_by_id(self, id_barang):
        current = self.head
        prev = None
        while current:
            if current.data["id"] == id_barang:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def update_by_id(self, id_barang, field, nilai_baru):
        current = self.head
        while current:
            if current.data["id"] == id_barang:
                current.data[field] = nilai_baru
                return True
            current = current.next
        return False

    def find_by_id(self, id_barang):
        current = self.head
        while current:
            if current.data["id"] == id_barang:
                return current.data
            current = current.next
        return None

    def search_by_name(self, keyword):
        """Linear search berdasarkan nama (case-insensitive)."""
        hasil = []
        current = self.head
        while current:
            if keyword.lower() in current.data["nama_barang"].lower():
                hasil.append(current.data)
            current = current.next
        return hasil

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def sort_by_nama(self):
        """Bubble sort berdasarkan nama_barang (A-Z)."""
        if not self.head or not self.head.next:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if current.data["nama_barang"].lower() > current.next.data["nama_barang"].lower():
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

    def sort_by_jumlah(self):
        """Bubble sort berdasarkan jumlah (besar ke kecil)."""
        if not self.head or not self.head.next:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if int(current.data["jumlah"]) < int(current.next.data["jumlah"]):
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next


# ─────────────────────────────────────────────
# STRUKTUR DATA 2: STACK (Riwayat Operasi)
# ─────────────────────────────────────────────

class Stack:
    """Stack untuk menyimpan riwayat operasi terakhir (undo sederhana)."""

    def __init__(self, max_size=20):
        self._stack = []
        self._max = max_size

    def push(self, operasi):
        if len(self._stack) >= self._max:
            self._stack.pop(0)
        self._stack.append(operasi)

    def pop(self):
        if self._stack:
            return self._stack.pop()
        return None

    def peek(self):
        if self._stack:
            return self._stack[-1]
        return None

    def is_empty(self):
        return len(self._stack) == 0

    def tampilkan(self):
        if self.is_empty():
            print("   (Belum ada riwayat operasi)")
            return
        print(f"   {'No':<4} {'Waktu':<22} {'Operasi'}")
        print("   " + "-" * 55)
        for i, op in enumerate(reversed(self._stack), 1):
            print(f"   {i:<4} {op['waktu']:<22} {op['keterangan']}")


# ─────────────────────────────────────────────
# DATABASE CSV
# ─────────────────────────────────────────────

def init_csv():
    """Buat file CSV jika belum ada."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()

def load_from_csv(linked_list):
    """Baca semua data CSV ke Linked List."""
    linked_list.head = None
    linked_list.size = 0
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            linked_list.append(dict(row))

def save_to_csv(linked_list):
    """Tulis semua data Linked List ke CSV."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        current = linked_list.head
        while current:
            writer.writerow(current.data)
            current = current.next

def generate_id(linked_list):
    """Generate ID unik secara otomatis."""
    existing_ids = [int(d["id"]) for d in linked_list.to_list() if d["id"].isdigit()]
    return str(max(existing_ids) + 1) if existing_ids else "1"


# ─────────────────────────────────────────────
# TAMPILAN / UI
# ─────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(judul=""):
    print("=" * 60)
    print("       📦 SISTEM MANAJEMEN GUDANG")
    if judul:
        print(f"          [ {judul} ]")
    print("=" * 60)

def cetak_tabel(data_list):
    if not data_list:
        print("   ⚠  Tidak ada data.")
        return
    print(f"\n   {'ID':<5} {'Nama Barang':<22} {'Kategori':<14} {'Jml':<6} {'Sat':<7} {'Lokasi':<10} {'Tgl Masuk'}")
    print("   " + "-" * 78)
    for d in data_list:
        print(f"   {d['id']:<5} {d['nama_barang']:<22} {d['kategori']:<14} "
              f"{d['jumlah']:<6} {d['satuan']:<7} {d['lokasi']:<10} {d['tanggal_masuk']}")
    print(f"\n   Total: {len(data_list)} barang\n")

def input_str(prompt, wajib=True):
    while True:
        val = input(f"   {prompt}: ").strip()
        if val or not wajib:
            return val
        print("   ⚠  Field ini tidak boleh kosong.")

def input_angka(prompt):
    while True:
        val = input(f"   {prompt}: ").strip()
        if val.isdigit() and int(val) >= 0:
            return val
        print("   ⚠  Masukkan angka yang valid (≥ 0).")


# ─────────────────────────────────────────────
# OPERASI CRUD
# ─────────────────────────────────────────────

def tambah_barang(ll, stack):
    clear()
    header("TAMBAH BARANG")
    nama     = input_str("Nama Barang")
    kategori = input_str("Kategori (misal: Elektronik, Furnitur)")
    jumlah   = input_angka("Jumlah")
    satuan   = input_str("Satuan (pcs/kg/box/dll)")
    lokasi   = input_str("Lokasi di gudang (misal: RAK-A1)")

    new_id = generate_id(ll)
    tanggal = datetime.now().strftime("%Y-%m-%d")
    data = {
        "id": new_id,
        "nama_barang": nama,
        "kategori": kategori,
        "jumlah": jumlah,
        "satuan": satuan,
        "lokasi": lokasi,
        "tanggal_masuk": tanggal
    }
    ll.append(data)
    save_to_csv(ll)
    stack.push({"waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "keterangan": f"TAMBAH → ID {new_id} ({nama})"})
    print(f"\n   ✅ Barang '{nama}' berhasil ditambahkan! (ID: {new_id})")
    input("\n   Tekan Enter untuk kembali...")

def lihat_semua(ll):
    clear()
    header("DAFTAR SEMUA BARANG")
    data = ll.to_list()
    cetak_tabel(data)
    input("   Tekan Enter untuk kembali...")

def cari_barang(ll):
    clear()
    header("CARI BARANG")
    keyword = input_str("Masukkan nama/kata kunci")
    hasil = ll.search_by_name(keyword)
    print(f"\n   Hasil pencarian untuk '{keyword}':")
    cetak_tabel(hasil)
    input("   Tekan Enter untuk kembali...")

def update_barang(ll, stack):
    clear()
    header("UPDATE BARANG")
    lihat_ringkas(ll)
    id_barang = input_str("Masukkan ID barang yang ingin diupdate")
    barang = ll.find_by_id(id_barang)
    if not barang:
        print("   ⚠  Barang tidak ditemukan!")
        input("\n   Tekan Enter untuk kembali...")
        return

    print(f"\n   Data saat ini → {barang['nama_barang']} | Jumlah: {barang['jumlah']} | Lokasi: {barang['lokasi']}")
    print("\n   Field yang bisa diupdate:")
    print("   1. Nama Barang   2. Kategori   3. Jumlah   4. Satuan   5. Lokasi")
    pilihan = input("\n   Pilih field (1-5): ").strip()

    field_map = {
        "1": ("nama_barang", "Nama baru"),
        "2": ("kategori",    "Kategori baru"),
        "3": ("jumlah",      "Jumlah baru"),
        "4": ("satuan",      "Satuan baru"),
        "5": ("lokasi",      "Lokasi baru"),
    }
    if pilihan not in field_map:
        print("   ⚠  Pilihan tidak valid.")
        input("\n   Tekan Enter untuk kembali...")
        return

    field, label = field_map[pilihan]
    nilai_baru = input_angka(label) if field == "jumlah" else input_str(label)
    ll.update_by_id(id_barang, field, nilai_baru)
    save_to_csv(ll)
    stack.push({"waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "keterangan": f"UPDATE → ID {id_barang}, {field} = '{nilai_baru}'"})
    print(f"\n   ✅ Data berhasil diperbarui!")
    input("\n   Tekan Enter untuk kembali...")

def hapus_barang(ll, stack):
    clear()
    header("HAPUS BARANG")
    lihat_ringkas(ll)
    id_barang = input_str("Masukkan ID barang yang ingin dihapus")
    barang = ll.find_by_id(id_barang)
    if not barang:
        print("   ⚠  Barang tidak ditemukan!")
        input("\n   Tekan Enter untuk kembali...")
        return

    konfirmasi = input(f"\n   Yakin hapus '{barang['nama_barang']}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        ll.delete_by_id(id_barang)
        save_to_csv(ll)
        stack.push({"waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "keterangan": f"HAPUS → ID {id_barang} ({barang['nama_barang']})"})
        print(f"\n   ✅ Barang berhasil dihapus!")
    else:
        print("   ℹ  Penghapusan dibatalkan.")
    input("\n   Tekan Enter untuk kembali...")

def sorting_menu(ll):
    clear()
    header("SORTING DATA")
    print("   1. Urutkan A-Z berdasarkan Nama")
    print("   2. Urutkan berdasarkan Jumlah (terbanyak)")
    pilihan = input("\n   Pilih (1/2): ").strip()
    if pilihan == "1":
        ll.sort_by_nama()
        print("\n   ✅ Data diurutkan A-Z!")
    elif pilihan == "2":
        ll.sort_by_jumlah()
        print("\n   ✅ Data diurutkan berdasarkan jumlah terbanyak!")
    else:
        print("   ⚠  Pilihan tidak valid.")
        input("\n   Tekan Enter untuk kembali...")
        return
    cetak_tabel(ll.to_list())
    input("   Tekan Enter untuk kembali...")

def riwayat_operasi(stack):
    clear()
    header("RIWAYAT OPERASI (Stack)")
    print(f"\n   Total operasi tersimpan: {len(stack._stack)}\n")
    stack.tampilkan()
    print()
    input("   Tekan Enter untuk kembali...")

def lihat_ringkas(ll):
    data = ll.to_list()
    if data:
        print(f"\n   {'ID':<5} {'Nama Barang':<25} {'Jumlah':<8} {'Lokasi'}")
        print("   " + "-" * 50)
        for d in data:
            print(f"   {d['id']:<5} {d['nama_barang']:<25} {d['jumlah']:<8} {d['lokasi']}")
        print()

def statistik(ll):
    clear()
    header("STATISTIK GUDANG")
    data = ll.to_list()
    if not data:
        print("   ℹ  Belum ada data.")
        input("\n   Tekan Enter untuk kembali...")
        return

    total_jenis = len(data)
    total_stok = sum(int(d["jumlah"]) for d in data)
    
    # Hitung per kategori
    kategori_count = {}
    for d in data:
        k = d["kategori"]
        kategori_count[k] = kategori_count.get(k, 0) + int(d["jumlah"])

    # Barang terbanyak (sequential search)
    max_item = max(data, key=lambda x: int(x["jumlah"]))
    min_item = min(data, key=lambda x: int(x["jumlah"]))

    print(f"\n   📊 Total Jenis Barang : {total_jenis}")
    print(f"   📦 Total Stok        : {total_stok}")
    print(f"   ⬆  Stok Terbanyak   : {max_item['nama_barang']} ({max_item['jumlah']} {max_item['satuan']})")
    print(f"   ⬇  Stok Terendah    : {min_item['nama_barang']} ({min_item['jumlah']} {min_item['satuan']})")
    print(f"\n   📁 Stok per Kategori:")
    for kat, jml in sorted(kategori_count.items()):
        print(f"      • {kat:<20} : {jml}")
    print()
    input("   Tekan Enter untuk kembali...")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    init_csv()
    ll = LinkedList()
    stack = Stack()
    load_from_csv(ll)

    while True:
        clear()
        header()
        print(f"   Total barang saat ini: {ll.size}")
        print()
        print("   ┌─────────────────────────────────────┐")
        print("   │  1. Tambah Barang  (Create)          │")
        print("   │  2. Lihat Semua    (Read)             │")
        print("   │  3. Cari Barang    (Search)           │")
        print("   │  4. Update Barang  (Update)           │")
        print("   │  5. Hapus Barang   (Delete)           │")
        print("   │  6. Sorting Data                      │")
        print("   │  7. Statistik Gudang                  │")
        print("   │  8. Riwayat Operasi (Stack)           │")
        print("   │  9. Keluar                            │")
        print("   └─────────────────────────────────────┘")
        pilihan = input("\n   Pilih menu (1-9): ").strip()

        if pilihan == "1":
            tambah_barang(ll, stack)
        elif pilihan == "2":
            lihat_semua(ll)
        elif pilihan == "3":
            cari_barang(ll)
        elif pilihan == "4":
            update_barang(ll, stack)
        elif pilihan == "5":
            hapus_barang(ll, stack)
        elif pilihan == "6":
            sorting_menu(ll)
        elif pilihan == "7":
            statistik(ll)
        elif pilihan == "8":
            riwayat_operasi(stack)
        elif pilihan == "9":
            clear()
            print("\n   Terima kasih! Sistem gudang ditutup.\n")
            break
        else:
            print("   ⚠  Pilihan tidak valid!")
            input("   Tekan Enter untuk kembali...")

if __name__ == "__main__":
    main()
