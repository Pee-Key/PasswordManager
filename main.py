from passgenerator import PasswordGenerator
from manager import PasswordManager
from database import init_database
from vault import VaultMethods

if __name__ == '__main__':
    db, cursor = init_database()
    cursor.execute("SELECT * FROM master")
    manager = PasswordManager()
    if cursor.fetchall():
        manager.login_user()
    else:
        manager.welcome_new_user()
    manager.window.mainloop()
