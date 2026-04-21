import os
import shutil

from config import STORE_DIR, SEARCH_DIRS
from crypto import encrypt_bytes, decrypt_bytes, ENCRYPTION_KEY
from db import get_db
from users import get_user_roles, user_has_upload_permission


def resolve_path(user_input_path):
    #try as-is (absolute or relative to cwd)
    if os.path.isfile(user_input_path):
        return os.path.abspath(user_input_path)

    filename = os.path.basename(user_input_path)

    # check flat in Desktop / Downloads
    for folder in SEARCH_DIRS:
        candidate = os.path.join(folder, filename)
        if os.path.isfile(candidate):
            return candidate

    # Recursive walk so skips hidden folders
    for folder in SEARCH_DIRS:
        if not os.path.isdir(folder):
            continue
        for dirpath, dirnames, filenames in os.walk(folder):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if filename in filenames:
                return os.path.join(dirpath, filename)

    return None



def upload_file(path_input, owner_username=None):
    real_path = resolve_path(path_input)

    if not real_path:
        print(f"can't find '{path_input}'")
        return

    original_name = os.path.basename(real_path)
    destination = os.path.join(STORE_DIR, original_name)

    # If source is already in files/, give it a _copy name
    if os.path.abspath(real_path) == os.path.abspath(destination):
        base, ext = os.path.splitext(original_name)
        original_name = f"{base}_copy{ext}"
        destination = os.path.join(STORE_DIR, original_name)

    # If destination already exists, add a counter suffix
    if os.path.exists(destination):
        base, ext = os.path.splitext(original_name)
        counter = 1
        while os.path.exists(destination):
            destination = os.path.join(STORE_DIR, f"{base}_{counter}{ext}")
            counter += 1
        original_name = os.path.basename(destination)

    shutil.copy(real_path, destination)

    # encrypt the stored copy in-place
    with open(destination, "rb") as f:
        raw = f.read()
    with open(destination, "wb") as f:
        f.write(encrypt_bytes(raw, ENCRYPTION_KEY))

    db = get_db()

    if not owner_username:
        print("upload blocked: provide a username (owner)")
        db.close()
        return

    user = db.execute("select id from users where username = ?", (owner_username,)).fetchone()
    if not user:
        print("upload blocked: owner user not found")
        db.close()
        return

    if not user_has_upload_permission(db, owner_username):
        print("upload blocked: only admin or editor can upload")
        db.close()
        return

    db.execute(
        "insert into files (owner_user_id, original_name, stored_path, encrypted) values (?, ?, ?, 1)",
        (user["id"], original_name, destination),
    )
    db.commit()
    db.close()
    print(f"stored: {original_name}")



def list_files():
    db = get_db()
    rows = db.execute(
        """
        select f.id, f.original_name, f.stored_path, u.username as owner
        from files f
        left join users u on u.id = f.owner_user_id
        order by f.id desc
        """
    ).fetchall()

    if not rows:
        print("no files stored yet")
    else:
        for row in rows:
            owner = row["owner"] if row["owner"] else "(no owner)"
            print(f"[{row['id']}] {row['original_name']} | owner: {owner} | path: {row['stored_path']}")
    db.close()


def list_files_for_user(username):
    db = get_db()
    rows = db.execute(
        """
        select f.id, f.original_name, f.stored_path, u.username as owner
        from files f
        join users u on u.id = f.owner_user_id
        where u.username = ?
        order by f.id desc
        """,
        (username,),
    ).fetchall()

    if not rows:
        print("no files found for that user")
    else:
        for row in rows:
            print(f"[{row['id']}] {row['original_name']} | owner: {row['owner']} | path: {row['stored_path']}")
    db.close()


def list_visible_files_for_user(username):
    # all logged-in users see all files; encryption protects the contents
    db = get_db()
    rows = db.execute(
        """
        select f.id, f.original_name, f.stored_path, u.username as owner,
               f.encrypted
        from files f
        left join users u on u.id = f.owner_user_id
        order by f.id desc
        """
    ).fetchall()

    if not rows:
        print("no files stored")
    else:
        for row in rows:
            owner = row["owner"] if row["owner"] else "(no owner)"
            enc_tag = "[encrypted]" if row["encrypted"] else ""
            print(f"[{row['id']}] {row['original_name']} {enc_tag}| owner: {owner}")
    db.close()


def show_file(file_id):
    db = get_db()
    row = db.execute(
        """
        select f.id, f.original_name, f.stored_path, u.username as owner
        from files f
        left join users u on u.id = f.owner_user_id
        where f.id = ?
        """,
        (file_id,),
    ).fetchone()

    if not row:
        print("file id not found")
    else:
        owner = row["owner"] if row["owner"] else "(no owner)"
        print(f"[{row['id']}] {row['original_name']} | owner: {owner} | path: {row['stored_path']}")
    db.close()


def read_file_for_user(filename, username):
    """Any logged-in user can attempt to read a file.
    Encrypted files require the correct 2-digit key to see real content.
    A wrong key shows the file as gibberish.
    """
    db = get_db()
    row = db.execute(
        """
        select f.id, f.original_name, f.stored_path, f.encrypted,
               u.username as owner
        from files f
        left join users u on u.id = f.owner_user_id
        where f.original_name = ?
        order by f.id desc
        limit 1
        """,
        (filename,),
    ).fetchone()
    db.close()

    if not row:
        print(f"file not found: '{filename}'")
        return

    stored_path = row["stored_path"]
    if not os.path.isfile(stored_path):
        print(f"error: '{filename}' is in the database but missing from disk")
        return

    with open(stored_path, "rb") as f:
        data = f.read()

    owner = row["owner"] if row["owner"] else "(no owner)"

    if row["encrypted"]:
        raw_key = input("enter encryption key (2-digit number): ").strip()
        try:
            key = int(raw_key)
        except ValueError:
            key = -1  # guaranteed wrong

        decrypted = decrypt_bytes(data, key)
        text = decrypted.decode("utf-8", errors="replace")

        if key == ENCRYPTION_KEY:
            print(f"\n--- {row['original_name']} (owner: {owner}) ---")
            print(text)
            print(f"--- end of {row['original_name']} ---\n")
        else:
            print(f"\n--- {row['original_name']} (owner: {owner}) [wrong key — showing raw] ---")
            print(text)
            print(f"--- end of {row['original_name']} ---\n")
    else:
        # legacy unencrypted file
        text = data.decode("utf-8", errors="replace")
        print(f"\n--- {row['original_name']} (owner: {owner}) [not encrypted] ---")
        print(text)
        print(f"--- end of {row['original_name']} ---\n")


def show_file_for_user(file_id, username):  # kept for CLI compat
    db = get_db()
    roles = get_user_roles(db, username)

    if "admin" in roles or "editor" in roles:
        row = db.execute(
            """
            select f.id, f.original_name, f.stored_path, u.username as owner
            from files f
            left join users u on u.id = f.owner_user_id
            where f.id = ?
            """,
            (file_id,),
        ).fetchone()
    else:
        row = db.execute(
            """
            select f.id, f.original_name, f.stored_path, u.username as owner
            from files f
            join users u on u.id = f.owner_user_id
            where f.id = ? and u.username = ?
            """,
            (file_id, username),
        ).fetchone()

    if not row:
        print("not allowed or file not found")
        db.close()
        return

    owner = row["owner"] if row["owner"] else "(no owner)"
    print(f"[{row['id']}] {row['original_name']} | owner: {owner} | path: {row['stored_path']}")
    db.close()
