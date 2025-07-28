import sys
import shutil
import sqlite3
import os

save_key_key = bytes.fromhex("63 13 15 F3 25 22 86 93 12 32 47 3F 2A 6A B3 01 51 E1 17 71 F1 82 AA B1 24 6B 46 A3 45 F2 3F 57 D3 90 50 37 42 C7 46 B0 70 07 C5 22")
save_value_key = bytes.fromhex("17 5B 2A 48 18 D3 E2 9F CC EA 2B 35 51 27 85 33 DC 11 BA 6D 61 09 F2 42 87 56 F9 0D BB 14 1A B9 36 81 FE 49 26 DA 64 97 32 58 BF CD")

def to_bytes(value):
    if isinstance(value, str):
        return value.encode('utf-8')
    elif isinstance(value, int):
        return str(value).encode('ascii')
    else:
        return value

def copy_database(src_path, dst_path):
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"file not exist: {src_path}")
    shutil.copyfile(src_path, dst_path)
    print(f"copy done：{src_path} -> {dst_path}")

def modify_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT save_key, save_value FROM AppSetting ORDER BY rowid ASC;")
        keys = cursor.fetchall()

        for row in keys:
            if row[0] != b'\x00':
                result = bytes([b ^ save_key_key[i % len(save_key_key)] for i, b in enumerate(to_bytes(row[0]))])
                cursor.execute("UPDATE AppSetting SET save_key = ? WHERE save_key = ?", (result, row[0]))
            if row[1] != b'\x00':
                result = bytes([b ^ save_value_key[i % len(save_value_key)] for i, b in enumerate(to_bytes(row[1]))])
                cursor.execute("UPDATE AppSetting SET save_value = ? WHERE save_value = ?", (result, row[1]))

        conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()
        print(f"Done：{db_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py your_database_name")
        sys.exit(1)

    source_db = sys.argv[1]

    copied_db = source_db.split('.')[0] + '_EncDec.db'

    copy_database(source_db, copied_db)
    modify_database(copied_db)

if __name__ == '__main__':
    main()
