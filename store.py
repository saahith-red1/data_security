import sys

from db import ensure_dirs, seed_default_roles, get_db
from users import (
    add_user,
    add_user_with_role,
    add_role,
    assign_role,
    list_users_and_roles,
    get_user_roles,
    user_exists,
)
from files import (
    upload_file,
    list_files,
    list_files_for_user,
    list_visible_files_for_user,
    show_file,
    show_file_for_user,
    read_file_for_user,
)


def interactive_app():
    print("welcome to file store mvp")
    current_user = None

    while True:
        if current_user is None:
            print("\nnot logged in")
            print("1) signup")
            print("2) login")
            print("3) exit")
            choice = input("choose: ").strip()

            if choice == "1":
                username = input("new username: ").strip()
                role = input("role (admin/editor/viewer): ").strip().lower()
                if not username:
                    print("username cannot be empty")
                    continue
                add_user_with_role(username, role)

            elif choice == "2":
                username = input("username: ").strip()
                db = get_db()
                exists = user_exists(db, username)
                db.close()
                if not exists:
                    print("user not found, signup first")
                else:
                    current_user = username
                    print(f"logged in as {current_user}")

            elif choice == "3":
                print("bye")
                return
            else:
                print("invalid choice")

        else:
            db = get_db()
            roles = get_user_roles(db, current_user)
            db.close()
            pretty_roles = ", ".join(sorted(roles)) if roles else "(no roles)"

            print(f"\nlogged in: {current_user} | roles: {pretty_roles}")
            print("1) upload file")
            print("2) list files i can see")
            print("3) read a file (by name)")
            print("4) logout")
            print("5) exit")
            action = input("choose: ").strip()

            if action == "1":
                path_input = input("file name: ").strip()
                upload_file(path_input, current_user)

            elif action == "2":
                list_visible_files_for_user(current_user)

            elif action == "3":
                fname = input("file name (e.g. drseuss.txt): ").strip()
                read_file_for_user(fname, current_user)

            elif action == "4":
                current_user = None
                print("logged out")

            elif action == "5":
                print("bye")
                return

            else:
                print("invalid choice")


def usage():
    print("usage:")
    print("  python store.py user-add <username>")
    print("  python store.py role-add <role_name>")
    print("  python store.py role-assign <username> <role_name>")
    print("  python store.py signup <username> <role_name>")
    print("  python store.py users-list")
    print("  python store.py upload <file_path> <owner_username>")
    print("  python store.py files-list")
    print("  python store.py files-list-user <username>")
    print("  python store.py file-show <file_id>")
    print("  python store.py app")


def main():
    ensure_dirs()
    seed_default_roles()

    if len(sys.argv) < 2:
        interactive_app()
        return

    cmd = sys.argv[1]

    if cmd == "user-add" and len(sys.argv) == 3:
        add_user(sys.argv[2])
    elif cmd == "role-add" and len(sys.argv) == 3:
        add_role(sys.argv[2])
    elif cmd == "role-assign" and len(sys.argv) == 4:
        assign_role(sys.argv[2], sys.argv[3])
    elif cmd == "signup" and len(sys.argv) == 4:
        add_user_with_role(sys.argv[2], sys.argv[3].lower())
    elif cmd == "users-list":
        list_users_and_roles()
    elif cmd == "upload" and len(sys.argv) == 4:
        upload_file(sys.argv[2], sys.argv[3])
    elif cmd == "files-list":
        list_files()
    elif cmd == "files-list-user" and len(sys.argv) == 3:
        list_files_for_user(sys.argv[2])
    elif cmd == "file-show" and len(sys.argv) == 3:
        show_file(sys.argv[2])
    elif cmd == "app":
        interactive_app()
    else:
        usage()


if __name__ == "__main__":
    main()
