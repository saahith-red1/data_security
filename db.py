import os
import sqlite3

from config import DB_FILE, STORE_DIR, VALID_ROLES


def get_db():
    # sqlite connection
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row

    # Creates users table
    db.execute(
        """
        create table if not exists users (
            id integer primary key autoincrement,
            username text unique not null
        )
        """
    )

    # creates roles table
    db.execute(
        """
        create table if not exists roles (
            id integer primary key autoincrement,
            role_name text unique not null
        )
        """
    )

    # Join table so each user can have multiple roles
    db.execute(
        """
        create table if not exists user_roles (
            user_id integer not null,
            role_id integer not null,
            unique(user_id, role_id),
            foreign key(user_id) references users(id),
            foreign key(role_id) references roles(id)
        )
        """
    )

    # files table — tracks who uploaded what
    db.execute(
        """
        create table if not exists files (
            id integer primary key autoincrement,
            owner_user_id integer,
            original_name text not null,
            stored_path text not null,
            foreign key(owner_user_id) references users(id)
        )
        """
    )

    # add encrypted column if this is an older DB without it
    try:
        db.execute("alter table files add column encrypted integer default 0")
        db.commit()
    except Exception:
        pass  # column already exists

    # add email column to users if missing
    try:
        db.execute("alter table users add column email text")
        db.commit()
    except Exception:
        pass  # column already exists

    db.commit()
    return db


def seed_default_roles():
    # makes sure basic roles always exist
    db = get_db()
    for role in sorted(VALID_ROLES):
        db.execute("insert or ignore into roles (role_name) values (?)", (role,))
    db.commit()
    db.close()


def ensure_dirs():
    os.makedirs(STORE_DIR, exist_ok=True)
