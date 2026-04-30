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
- **Encryption at rest** — every uploaded file is encrypted on disk using XOR encryption with a shared 2-digit key. Without the key the file contents are unreadable
- **Interactive terminal UI** — everything runs through a simple numbered menu in the terminal

---

## Setup

No external packages required

---

## Run

# Data Security — File Storage System

Terminal-based file storage system with user accounts, role-based access control, encryption, and email login verification.

Users log in, upload files, and read files from the terminal. Files are encrypted at rest on disk. If the wrong key is entered while reading a file, the output appears as gibberish.

---

## Components

- **User accounts** — sign up with a username, role, and email
- **Roles**
  - `admin` — can upload and read files
  - `editor` — can upload and read files
  - `viewer` — can read files but cannot upload
- **File upload** — type only the filename (file should be in Desktop or Downloads)
- **Encryption at rest** — uploaded files are encrypted with a shared 2-digit key
- **Login verification (2FA-style)** — login requires a one-time 6-digit code sent by email
- **Interactive terminal UI** — all functionality is in a numbered terminal menu

---

## Setup

No external Python packages are required.

### Requirements

- Python 3.9+

### Email setup for login verification

To send one-time login codes by email, set the sender account in [config.py](config.py):

- `SMTP_SENDER_EMAIL`
- `SMTP_APP_PASSWORD`

Use a Gmail account with an App Password enabled.

Recipients can be any email address entered at signup, and the same email can be reused across multiple users for demos.

---

## Run

From the project folder:

```bash
python3 store.py
```

This opens the interactive terminal menu.

---

## Upload flow

1. Put the file in **Desktop** or **Downloads**
2. Log in as `admin` or `editor`
3. Choose `1) upload file`
4. Enter the filename (example: `report.txt`)

---

## Read flow

1. Log in as any user
2. Enter the emailed 6-digit login code
3. Choose `2) list files i can see`
4. Choose `3) read a file (by name)`
5. Enter the 2-digit encryption key when prompted

Correct encryption key shows readable text. Wrong key shows scrambled output.

Encryption key is set in [crypto.py](crypto.py) as `ENCRYPTION_KEY`.

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
