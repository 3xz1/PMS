import os
# Secret key for app
SECRET_KEY = os.urandom(12).hex()
# MySQL config
#uri = 'mysql://%s:%s@%s/%s' % (os.getenv("MYSQL_USER"), os.getenv('MYSQL_PASSOWRD'), os.getenv('MYSQL_HOST'), os.getenv('MYSQL_DB'))
#print(uri)
SQLALCHEMY_DATABASE_URI = 'mysql://root:nOtSeCuRe@db/pms'
