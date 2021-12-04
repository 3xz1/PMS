@login_manager.user_loader
def user_loader(username):
    return get_user(username[0])

#create database pms if not set
def create_db():
        curs = mysql.connection.cursor()
        cur.execute("CREATE DATABASE pms")
        mysql.connection.commit()
        cur.close()

# create table credentials to store username and password hash
def create_table():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE credentials (id INT(10) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE, pw_hash VARCHAR(255))")
    mysql.connection.commit()
    cur.close()

# Insert user into dabase with user name and hashed pw+salt
def insert_user(username, pw_hash):
    cur = mysql.connection.cursor()
    query = "INSERT INTO credentials(username, pw_hash) VALUES ('%s', '%s')" % (username, pw_hash)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

# Fetch user and return pw_hash + salt
def get_user_hash(username):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM credentials WHERE username ='%s' LIMIT 1" % (username)
    cur.execute(query)
    result = cur.fetchone()
    cur.close() 
    return result[2]
def get_user(username):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM credentials WHERE username = '%s' LIMIT 1" % (username)
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    if(result):
        return True
    else:
        return False

# update new password hash
def alter_hash(username, pw_hash):
    cur = mysql.connection.cursor()
    query = "update credentials SET pw_hash='%s' WHERE username ='%s'" % (pw_hash, username)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()   