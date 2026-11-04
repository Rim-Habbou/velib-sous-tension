import urllib.request
import hashlib
import os

URL = "https://docs.ambroise.cloud/velib/velib-2026-10-08.csv.gz"
EXPECTED_MD5 = "02ab1e3fdac10579e4ce93d1540a5dc7"
OUTPUT_DIR = "data/raw"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "velib-2026-10-08.csv.gz")

def check_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Téléchargement depuis {URL}...")
    urllib.request.urlretrieve(URL, OUTPUT_PATH)
    
    print("Vérification de l'empreinte MD5...")
    actual_md5 = check_md5(OUTPUT_PATH)
    
    if actual_md5 == EXPECTED_MD5:
        print("Succès : L'empreinte MD5 est correcte.")
    else:
        print(f"Erreur : MD5 attendu {EXPECTED_MD5}, obtenu {actual_md5}")

if __name__ == "__main__":
    main()