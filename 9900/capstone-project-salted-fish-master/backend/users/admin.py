#!/usr/bin/python3

from users.util import sha256

class Admin():
    """Site admin user class"""
    def __init__(self, name, email, password_plain='', password_encrypted='', id='', create_time='', last_update=''):
        self.name = name
        self.email = email.lower()
        if password_encrypted == '':
            self.password_encrypted = sha256(password_plain)
        else:
            self.password_encrypted = password_encrypted
        self.id = id
        self.create_time = create_time
        self.last_update = last_update

    @staticmethod
    def login(conn, email, password_plain='', password_encrypted=''):
        """Login method to check password match
        Params:
        conn -- database connection
        email -- user email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Admin user info (if success) or None
        """
        # ignore case
        email = email.lower()
        query = "select * from admin where email = \'" + email + "\';"
        result = conn.execute(query)
        if result.rowcount == 0:
            # user email not exist
            return None
        row = result.fetchone()
        # use encrypted password to compare
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            # password match, return user info
            return Admin(row['name'], row['email'], password_encrypted=row['password'], id=row['ID'], create_time=row['create_time'], last_update=row['last_update']).info()
        # password not match
        return None

    @staticmethod
    def check_password(conn, email, password_plain='', password_encrypted=''):
        """check password match
        Params:
        conn -- database connection
        email -- user email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        Return:
        Boolean True/False if password match or not
        """
        # ignore case
        email = email.lower()
        query = "select * from admin where email = \'" + email + "\';"
        result = conn.execute(query)
        row = result.fetchone()
        # use encrypted password to compare
        if password_encrypted == '':
            enc_pass = sha256(password_plain)
        else:
            enc_pass = password_encrypted
        if enc_pass == row['password']:
            return True
        return False

    @staticmethod
    def commit_newpassword(conn, email, password_plain='', password_encrypted=''):
        """commit new password on password change
        Params:
        conn -- database connection
        email -- user email address
        password_plain -- plain text password
        password_encrypted -- sha256 encrypted password
        """
        # ignore case
        email = email.lower()
        # use encrypted password
        if password_encrypted == '':
            new_pass = sha256(password_plain)
        else:
            new_pass = password_encrypted
        # write in database
        query = "UPDATE admin set password = \'" + new_pass + "\' where email = \'" + email + "\';"
        conn.execute(query)

    def info(self):
        """return admin user info"""
        return {'role': 'Admin', 'name': self.name, 'email': self.email, 'id': self.id, 'creation_time': self.create_time, 'last_update': self.last_update}

    def commit(self, conn):
        """commit a new Admin user into database
        Params:
        conn -- database connection
        """
        query = "INSERT INTO admin (name, email, password) VALUES (\'" + self.name.replace("'", "\\\'") + "\', \'" + self.email + "\', \'" + self.password_encrypted + "\') ON DUPLICATE KEY UPDATE `name`= \'" + self.name.replace("'", "\\\'") + "\', `password` = \'" + self.password_encrypted + "\';"
        conn.execute(query)
