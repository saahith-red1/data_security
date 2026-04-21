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

## How to Run

From inside the project folder:

```bash
python3 store.py
```

This opens the interactive menu. From there you can sign up, log in, upload files, and read files.

---

## How to Upload a File

1. Put the file you want to upload in your **Desktop** or **Downloads** folder
2. Log in as an `admin` or `editor` user
3. Choose option `1) upload file`
4. Type just the filename, like `report.txt` — no full path needed

---

## How to Read a File

1. Log in as any user
2. Choose option `2) list files i can see` to see what's stored
3. Choose option `3) read a file (by name)` and type the filename
4. Enter the encryption key when prompted — the key is a 2-digit number
5. Correct key → readable text. Wrong key → scrambled output

**The encryption key is: `42`** (set in `crypto.py` under `ENCRYPTION_KEY`)

---

## File Structure

```
store.py      — entry point, run this to start the app
config.py     — constants (storage folder, encryption key location, valid roles)
db.py         — database setup and table creation
users.py      — user and role management
files.py      — file upload, encryption wiring, and file reading
crypto.py     — XOR encryption implementation
files/        — where uploaded (encrypted) files are stored on disk
store.db      — SQLite database tracking users, roles, and file metadata
```

---

## Encryption

Files are encrypted using XOR encryption, implemented from scratch in `crypto.py`. The idea works like this: a number (the key) is used to seed Python's built-in random number generator, which produces a deterministic stream of bytes. Each byte of the file is XOR'd with the corresponding byte from that stream. To decrypt, you do the exact same operation — XOR is its own inverse, so running it again with the same key recovers the original file.

The encryption key concept and overall approach were discussed with an AI used as an external contributor, but the actual implementation in `crypto.py` was written by hand. The AI was also used as an external contributor to help set up the `store.db` SQLite schema.

---

## Command Line (Alternative to Interactive Mode)

You can also run individual commands directly:

```bash
python3 store.py signup <username> <role>        # create a user
python3 store.py users-list                      # list all users and roles
python3 store.py upload <filepath> <username>    # upload a file
python3 store.py files-list                      # list all stored files
```
