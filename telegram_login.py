import os
from telethon import TelegramClient, events

# API ID dan API Hash (ganti dengan nilai yang valid dari Telegram)
API_ID = 1234567  # Masukkan API ID Anda
API_HASH = "abcdef1234567890abcdef1234567890"  # Masukkan API Hash Anda

# Folder untuk menyimpan sesi
SESSION_FOLDER = "sessions"

# Pastikan folder sesi ada
if not os.path.exists(SESSION_FOLDER):
    os.makedirs(SESSION_FOLDER)

# Fungsi untuk menambahkan nomor baru
def add_account():
    api_id = int(input("Masukkan API ID: "))
    api_hash = input("Masukkan API Hash: ")
    phone_number = input("Masukkan nomor telepon (format internasional, misal +628xxx): ")

    # Nama sesi berdasarkan nomor telepon
    session_name = os.path.join(SESSION_FOLDER, f"{phone_number.replace('+', '')}")
    client = TelegramClient(session_name, api_id, api_hash)

    async def login():
        await client.start(phone_number)
        print(f"Login berhasil untuk nomor: {phone_number}")
        await client.disconnect()

    client.loop.run_until_complete(login())

# Fungsi untuk membaca pesan dari akun tertentu
def read_messages():
    # Menampilkan daftar akun yang sudah ada
    print("Pilih nomor akun yang ingin dibaca pesannya:")
    accounts = [session_file for session_file in os.listdir(SESSION_FOLDER)]
    if not accounts:
        print("Belum ada akun yang ditambahkan.")
        return

    for idx, session_file in enumerate(accounts):
        nomor = session_file.replace(".session", "")
        print(f"{idx + 1}. {nomor}")

    choice = int(input("Pilih nomor akun (angka): ")) - 1
    if choice < 0 or choice >= len(accounts):
        print("Pilihan tidak valid.")
        return

    selected_session = accounts[choice]
    session_path = os.path.join(SESSION_FOLDER, selected_session)
    client = TelegramClient(session_path, API_ID, API_HASH)

    @events.register(events.NewMessage)
    async def message_handler(event):
        sender = await event.get_sender()
        print(f"[{event.chat_id}] Pesan baru dari {sender.username or sender.phone}: {event.text}")
        if "OTP" in event.text or "kode login" in event.text:
            print(f"Kode OTP: {event.text}")

    # Menjalankan client untuk membaca pesan
    client.add_event_handler(message_handler)
    client.start()

    print("Menunggu pesan masuk...")
    print("Tekan Ctrl+C untuk berhenti membaca pesan.")
    try:
        client.run_until_disconnected()
    except KeyboardInterrupt:
        print("Berhenti membaca pesan dan kembali ke menu.")

# Fungsi untuk melihat daftar akun yang sudah ditambahkan
def list_accounts():
    print("Daftar akun yang sudah ditambahkan:")
    if not os.listdir(SESSION_FOLDER):
        print("Belum ada akun yang ditambahkan.")
    else:
        for session_file in os.listdir(SESSION_FOLDER):
            nomor = session_file.replace(".session", "")
            print(f"- {nomor}")

# Menu utama
def main():
    while True:
        print("\nMenu:")
        print("1. Tambahkan Nomor Baru")
        print("2. Mulai Membaca Pesan")
        print("3. Lihat Daftar Akun")
        print("4. Keluar")
        choice = input("Pilih opsi (1/2/3/4): ")

        if choice == "1":
            add_account()
        elif choice == "2":
            read_messages()
        elif choice == "3":
            list_accounts()
        elif choice == "4":
            print("Keluar dari aplikasi.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
