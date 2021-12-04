from hashlib import sha1
import requests
import json

def check_hibp(password):
	sha1_hash = sha1(password.encode('UTF-8'))
	sha1_hexed_hash = sha1_hash.hexdigest()
	url = 'https://api.pwnedpasswords.com/range/%s' %sha1_hexed_hash[:5]
	r = requests.get(url)
	if(sha1_hexed_hash[5:].upper() in r.text):
		return True
	else:
		return False

def check_password_criteria(password):
	special_chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')','*','+','-',',','.','/',':',';', '<', '=', '>', '?', '@', '[', '\\',']','^','_','`','{', '|', '}','~']
	with open('pms/password_config.json') as json_file:
		password_config = json.load(json_file)['password_config']


	if(len(password) < password_config['password_min_length']):
		return False
	if(len(password) > password_config['password_max_length']):
		return False
	if(password_config['digit'] == True and not any(char.isdigit() for char in password)):
		return False
	if(password_config['lower char'] == True and not any(char.islower() for char in password)):
		return False
	if(password_config['upper char'] == True and not any(char.isupper() for char in password)):
		return False
	if(password_config['special char'] == True and not any(char in special_chars for char in password)):
		return False
	return True

def return_password_criteria():
	with open('pms/password_config.json') as json_file:
		password_config = json.load(json_file)['password_config']

	note = "Password needs to have "
	for config in password_config:
		if(password_config[config] == True):
			print(config)
			note += config + ', '
		if(config == 'password_min_length'):
			note += 'minimum password length of ' + str(password_config[config])

	return note