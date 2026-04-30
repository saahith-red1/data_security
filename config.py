import os

# Where the copied files on disk are kept
STORE_DIR = "files"

# sqlite database for metadata
DB_FILE = "store.db"

# Path search dirs for file upload
HOME = os.path.expanduser("~")
SEARCH_DIRS = [
    os.path.join(HOME, "Desktop"),
    os.path.join(HOME, "Downloads"),
]

# these are the only roles we allow in this mvp
VALID_ROLES = {"admin", "editor", "viewer"}


SMTP_SENDER_EMAIL = "saahired@gmail.com"   
SMTP_APP_PASSWORD  = "imux qwff vvub pajd"  
