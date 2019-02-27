#import hashlib, uuid
#salt = uuid.uuid4().hex
import bcrypt


def generate_password_hash(password):
	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
	return hashed #hashlib.sha512(password + salt).hexdigest()


def check_password_hash(password, user):
	#salt = bcrypt.gensalt()
	#hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
	#print 'hash pw', hashed, ',', bcrypt.hashpw(password.encode("utf-8"), hashed)#hashed.find(salt)
	##
	#print 'check pw', bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
	##
	if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
		print "It Matches!"
		return True
	else:
		print "It Does not Match"
		return False

"""
if __name__ == '__main__':
	print generate_password_hash('123'.encode("utf-8"))
	print check_password_hash('[REDACTED_VALUE]', '123'.encode("utf-8"))
"""