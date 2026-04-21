import sqlite3

from config import VALID_ROLES
from db import get_db



def user_exists(db, username):
    row = db.execute("select 1 from users where username = ?", (username,)).fetchone()
    return row is not None


def get_user_roles(db, username):
    rows = db.execute(
        """
        select r.role_name
        from roles r
        join user_roles ur on ur.role_id = r.id
        join users u on u.id = ur.user_id
        where u.username = ?
        """,
        (username,),
    ).fetchall()
    return {row["role_name"] for row in rows}


def user_has_upload_permission(db, username):
    row = db.execute(
        """
        select 1
        from users u
        join user_roles ur on ur.user_id = u.id
        join roles r on r.id = ur.role_id
        where u.username = ?
          and r.role_name in ('admin', 'editor')
        limit 1
        """,
        (username,),
    ).fetchone()
    return row is not None



def add_user(username):
    db = get_db()
    try:
        db.execute("insert into users (username) values (?)", (username,))
        db.commit()
        print(f"user created: {username}")
    except Exception:
        print("that username already exists")
    finally:
        db.close()


def add_user_with_role(username, role_name):
    if role_name not in VALID_ROLES:
        print("invalid role (use admin/editor/viewer)")
        return

    db = get_db()
    try:
        db.execute("insert into users (username) values (?)", (username,))
        db.commit()
    except Exception:
        print("that username already exists")
        db.close()
        return

    user = db.execute("select id from users where username = ?", (username,)).fetchone()
    role = db.execute("select id from roles where role_name = ?", (role_name,)).fetchone()
    db.execute(
        "insert or ignore into user_roles (user_id, role_id) values (?, ?)",
        (user["id"], role["id"]),
    )
    db.commit()
    db.close()
    print(f"signup complete: {username} as {role_name}")


def add_role(role_name):
    db = get_db()
    try:
        db.execute("insert into roles (role_name) values (?)", (role_name,))
        db.commit()
        print(f"role created: {role_name}")
    except Exception:
        print("that role already exists")
    finally:
        db.close()


def assign_role(username, role_name):
    db = get_db()
    user = db.execute("select id from users where username = ?", (username,)).fetchone()
    role = db.execute("select id from roles where role_name = ?", (role_name,)).fetchone()

    if not user:
        print("user not found")
        db.close()
        return
    if not role:
        print("role not found")
        db.close()
        return

    db.execute(
        "insert or ignore into user_roles (user_id, role_id) values (?, ?)",
        (user["id"], role["id"]),
    )
    db.commit()
    db.close()
    print(f"assigned role '{role_name}' to '{username}'")


def list_users_and_roles():
    db = get_db()
    users = db.execute("select id, username from users order by username").fetchall()
    for user in users:
        roles = db.execute(
            """
            select r.role_name
            from roles r
            join user_roles ur on ur.role_id = r.id
            where ur.user_id = ?
            order by r.role_name
            """,
            (user["id"],),
        ).fetchall()
        role_names = [r["role_name"] for r in roles]
        pretty_roles = ", ".join(role_names) if role_names else "(no roles)"
        print(f"{user['username']}: {pretty_roles}")
    db.close()
