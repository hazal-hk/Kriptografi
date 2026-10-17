import os
import socket
import sys
import threading


from common import PORT, recv_msg, send_msg

CHUNK = 16 * 1024
IN_DIR = "client_received"
os.makedirs(IN_DIR, exist_ok=True)


def receiver(sock):
    try:
        while True:
            hdr, payload = recv_msg(sock)
            if hdr["type"] == "text":
                print(f"\n[{hdr['from']}] {payload.decode(errors='replace')}")
            elif hdr["type"] == "file":
                path = os.path.join(IN_DIR, os.path.basename(hdr["name"]))
                with open(path, "wb" if hdr["seq"] == 0 else "ab") as f:
                    f.write(payload)
                if hdr["last"]:
                    print(f"\n[{hdr['from']}] dosya alindi: {path}")
    except (ConnectionError, OSError):
        print("\nbaglanti kapandi")
        os._exit(0)


def pick_pdf():
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        p = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        root.destroy()
        return p
    except Exception:
        return input("PDF yolu: ").strip()


def send_file(sock, path):
    name = os.path.basename(path)
    size = os.path.getsize(path)
    sent, seq = 0, 0
    with open(path, "rb") as f:
        while sent < size:
            chunk = f.read(CHUNK)
            sent += len(chunk)
            send_msg(sock, {"type": "file", "name": name, "seq": seq, "last": sent >= size}, chunk)
            seq += 1
    print(f"{name} gonderildi ({size} byte, {seq} parca)")


def main():
    # Terminalden IP ve ID alinarak calistirilacak
    if len(sys.argv) != 3:
        print("Kullanim: python client.py <sunucu_ip> <istemci_id>")
        sys.exit(1)
        
    host, cid = sys.argv[1], sys.argv[2]

    # Master'a (Sunucuya) baglanti kuruluyor
    sock = socket.create_connection((host, PORT))
    send_msg(sock, {"type": "hello", "id": cid})
    
    # Gelen mesajlari dinlemek icin arka plan gorevi baslatiliyor
    threading.Thread(target=receiver, args=(sock,), daemon=True).start()

    while True:
        # MENU: Harmanlanmis yapi
        choice = input("\n1) Metin Yaz  2) PDF Sec  3) Hazir Guvensiz Mesaj Testi  q) Cikis > ").strip()
        
        if choice == "1":
            # Manuel girilen guvensiz metin
            send_msg(sock, {"type": "text"}, input("mesaj: ").encode())
            
        elif choice == "2":
            # PDF dosyasi gonderimi
            path = pick_pdf()
            if path and os.path.isfile(path):
                send_file(sock, path)
            else:
                print("Dosya secilmedi.")
                
        elif choice == "3":
            # Ikinci koddan alinan hazir guvensiz test mesaji
            test_mesaj = "Merhaba Master! Bu mesaj guvensiz modda, hicbir sifreleme olmadan gonderilmistir."
            send_msg(sock, {"type": "text"}, test_mesaj.encode('utf-8'))
            print("Hazir güvensiz mesaj iletildi.")
            
        elif choice == "q":
            break
            
    sock.close()

if __name__ == "__main__":
    main()