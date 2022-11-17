from tkinter import simpledialog

# import cipher
from Crypto.Cipher import AES
from database import init_database

# from cipher import encryption

key = b'\x9e)\xbb\x06\x85\x11\x0f\x9a/\xd7\xe2\xfel\x18\x92q'


class VaultMethods:

    def __init__(self):
        self.db, self.cursor = init_database()

    def popup_entry(self, heading):
        answer = simpledialog.askstring("Enter details", heading)

        return answer

    def encryption(self, password):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))

        return nonce, ciphertext, tag

    def decryption(self, nonce, ciphertext, tag):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            return plaintext.decode('utf-8')
        except:
            return False

    def add_password(self, vault_screen):
        platform = self.popup_entry("Platform")
        userid = self.popup_entry("Username/Email")
        password = self.popup_entry("Password")

        nonce, ciphertext, tag = self.encryption(password)

        insert_cmd = """INSERT INTO vault(platform, userid, password, tag, nonce) VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_cmd, (platform, userid, ciphertext, tag, nonce))
        self.db.commit()
        vault_screen()

    def update_password(self, id, vault_screen):
        password = self.popup_entry("Enter New Password")

        nonce, ciphertext, tag = self.encryption(password)

        self.cursor.execute(
            "UPDATE vault SET password = ?, tag = ?, nonce = ? WHERE id = ?", (ciphertext, tag, nonce, id))
        self.db.commit()
        vault_screen()

    def remove_password(self, id, vault_screen):
        self.cursor.execute("DELETE FROM vault WHERE id = ?", (id,))
        self.db.commit()
        vault_screen()
