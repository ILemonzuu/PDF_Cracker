import pypdf 
from tqdm import tqdm
import itertools
import string
import time

def dictionary_cracker(pdf_path, wordlist_path):
    """
    Mencoba menemukan kata sandi PDF menggunakan serangan kamus (dictionary attack).
    """
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist_file:
            passwords = [line.strip() for line in wordlist_file]
        
        print(f"[+] Memulai Dictionary Attack pada '{pdf_path}' dengan {len(passwords)} kata sandi.")
        
        for password in tqdm(passwords, "Mencoba Kata Sandi"):
            try:
                with open(pdf_path, 'rb') as file:
                    reader = pypdf.PdfReader(file) 
                    if reader.is_encrypted:
                        if reader.decrypt(password):
                            print(f"\n[SUCCESS] Kata sandi ditemukan: {password}")
                            return password
            except Exception:
                continue
                
    except FileNotFoundError:
        print(f"[ERROR] File wordlist tidak ditemukan: '{wordlist_path}'. Pastikan path benar.")
        return None
        
    print("\n[FAIL] Kata sandi tidak ditemukan dalam wordlist.")
    return None

def brute_force_cracker(pdf_path, max_length=5):
    """
    Mencoba menemukan kata sandi PDF menggunakan serangan brute-force.
    """
    chars = string.ascii_lowercase + string.digits 
    print(f"[+] Memulai Brute-Force Attack pada '{pdf_path}' (maksimum {max_length} karakter).")
    print("[!] Ini bisa memakan waktu SANGAT LAMA.")
    
    total_attempts = sum(len(chars)**i for i in range(1, max_length + 1))
    
    with tqdm(total=total_attempts, desc="Mencoba Kombinasi") as pbar:
        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = "".join(attempt)
                pbar.update(1)
                try:
                    with open(pdf_path, 'rb') as file:
                        # DIUBAH KEMBALI: Panggil PdfReader dari pypdf
                        reader = pypdf.PdfReader(file) 
                        if reader.is_encrypted:
                            if reader.decrypt(password):
                                print(f"\n[SUCCESS] Kata sandi ditemukan: {password}")
                                return password
                except Exception:
                    continue

    print(f"\n[FAIL] Kata sandi tidak ditemukan dengan metode brute-force (hingga panjang {max_length}).")
    return None

if __name__ == "__main__":
    try:
        pdf_file = input("Masukkan path ke file PDF yang terkunci: ")
        
        print("\nPilih metode serangan:")
        print("1. Dictionary Attack (Direkomendasikan, lebih cepat)")
        print("2. Brute-Force Attack (Sangat lambat, coba jika metode 1 gagal)")
        
        choice = input("Masukkan pilihan (1/2): ")
        
        start_time = time.time()

        if choice == '1':
            wordlist_file = input("Masukkan path ke file wordlist (.txt): ")
            found_password = dictionary_cracker(pdf_file, wordlist_file)
        elif choice == '2':
            try:
                max_len = int(input("Masukkan panjang maksimum kata sandi untuk dicoba (misal: 4): "))
                found_password = brute_force_cracker(pdf_file, max_len)
            except ValueError:
                print("[ERROR] Masukkan harus berupa angka.")
                found_password = None
        else:
            print("[ERROR] Pilihan tidak valid.")
            found_password = None

        end_time = time.time()
        
        if found_password:
            print(f"\nProses selesai dalam {end_time - start_time:.2f} detik.")
            
    except FileNotFoundError:
        print(f"[ERROR] File PDF tidak ditemukan. Pastikan path yang Anda masukkan sudah benar.")
    except Exception as e:
        print(f"Terjadi error yang tidak terduga: {e}")