# Data Security — File Storage System

Terminal-based/terminal-local file storage system with user accounts, role-based access control, and encryption. You use it by loggin in, uploading files, and those files are encrypted and stored on disk. Anyone can see the list of files, but you need the correct encryption key to read the actual contents. If you type the wrong key, the file just shows gibberish (the encryption).

---

## Components

- **User accounts** — sign up with a username and get assigned a role
- **Three roles:**
  - `admin` — can upload files and read any file
  - `editor` — can upload files and read any file
  - `viewer` — can read files but cannot upload
- **File upload** — drop a file in your Desktop or Downloads folder, then type the filename. The system finds it, encrypts it, and stores a copy
- **Encryption** — every uploaded file is encrypted with a shared 2-digit key. Without the key the file contents are unreadable and gibberish
- **Two Factor Authentication** - every time a user logs in, they are sent an email with a code that they must type in to get into their account
- **Interactive terminal** — everything runs through a simple numbered menu in the terminal

---

## Setup

No external packages required

---

## Run

# Data Security — File Storage System

Terminal-based file storage system with user accounts, role-based access control, encryption, and email login verification.

Users log in with name and email verification code, upload files, and read files from the terminal. Files are encrypted, and if the wrong key is entered while reading a file, the output appears as gibberish

From the project folder:

```bash
python3 store.py
```

This opens the interactive terminal menu.

---

## Upload

1. Put the file in **Desktop** or **Downloads**
2. Log in as `admin` or `editor`
3. Choose `1) upload file`
4. Enter the filename (example: `report.txt`)

---

## Read

1. Log in as any user
2. Enter the emailed 6-digit login code
3. Choose `2) list files i can see`
4. Choose `3) read a file (by name)`
5. Enter the 2-digit encryption key when prompted

Correct encryption key shows readable text. Wrong key shows scrambled 
---

## Project files

- [store.py](store.py) — main entry point
- [config.py](config.py) — constants and SMTP settings
- [db.py](db.py) — SQLite setup and table creation
- [users.py](users.py) — users, roles, and user emails
- [files.py](files.py) — upload, listing, and read behavior
- [crypto.py](crypto.py) — XOR encryption/decryption
- [auth.py](auth.py) — email code generation + verification
- [files/](files/) — encrypted file storage
- `store.db` — SQLite database
