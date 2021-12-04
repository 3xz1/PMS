import unittest
from pms.password_check import check_hibp, check_password_criteria
import json
import requests

class TestPasswordCheck(unittest.TestCase):
	#def test_check_user_creation(self):
	#	checker = False
	#	url_create = "http://localhost/signup"
	#	data = {'username':'pms', 'password':'Nuv2sRNaBbMdhnf!', 'password_check':'Nuv2sRNaBbMdhnf!'}
	#	r = requests.post(url_create, data = data)
	#	if(r.status_code == 200):
	#		checker = True
	#		url_login = "http://localhost/login"
	#		data = {'username':'pms', 'password':'Nuv2sRNaBbMdhnf!'}
	#		r = requests.post(url_login, data=data)
	#		if(r.status_code == 200):
	#			checker = True
	#		else:
	#			checker = False
	#	self.assertTrue(checker)


	def test_check_password_digit(self):
		with open('pms/password_config.json') as json_file:
			password_config = json.load(json_file)['password_config']

		pwTestDigit = 'nOt!SeCurePW' # pw without Digit
		pw = 't@6cLY$YkZM?t#kP' # Pw matching all criterias
		if(password_config['digit'] == True):
			self.assertFalse(check_password_criteria(pwTestDigit))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestDigit))
			self.assertTrue(check_password_criteria(pw))

	def test_check_password_LowerChar(self):
		with open('pms/password_config.json') as json_file:
			password_config = json.load(json_file)['password_config']

		pwTestLower = "SOME1PWNO!$X" # pw without lower case letters
		pw = 't@6cLY$YkZM?t#kP'

		# Test cases
		if(password_config['lower char'] == True):
			self.assertFalse(check_password_criteria(pwTestLower))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestLower))
			self.assertTrue(check_password_criteria(pw))

	def test_check_password_specialChar(self):
		with open('pms/password_config.json') as json_file:
			password_config = json.load(json_file)['password_config']

		pwTestSpecialChar = "somepWdo1xa3" # pw without special char
		pw = 't@6cLY$YkZM?t#kP'

		if(password_config['special char'] == True):
			self.assertFalse(check_password_criteria(pwTestSpecialChar))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestSpecialChar))
			self.assertTrue(check_password_criteria(pw))

	def test_check_password_upper_char(self):
		with open('pms/password_config.json') as json_file:
			password_config = json.load(json_file)['password_config']

		pwTestHigher = "some1pwno!§x" # pw without upper case letters
		pw = 't@6cLY$YkZM?t#kP'

		if(password_config['upper char'] == True):
			self.assertFalse(check_password_criteria(pwTestHigher))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestHigher))
			self.assertTrue(check_password_criteria(pw))
		
		
		
	def test_check_password_hipb(self):
		pwTestHibp = 'Password!' # should fail at hibp
		pw = 't@6cLY$YkZM?t#kP'

		self.assertFalse(check_password_criteria(pwTestHibp))
		self.assertTrue(check_password_criteria(pw))


		# Test cases

	def test_check_password_lengths(self):
		pwTestMinLength = 'SeCRe3!"' # pw exaxt 8 chars
		pwTestLesserMinLength = '!asAH12' # Min length should be 8
		pwTestMaxLength = 'a12345678!01236789012F45678027' # max pw length 30
		pwTestGreaterMaxLength = 'a12345678!01234569012F4567890X§' # pw length 31


		self.assertTrue(check_password_criteria(pwTestMinLength))
		self.assertFalse(check_password_criteria(pwTestLesserMinLength))
		self.assertTrue(check_password_criteria(pwTestMaxLength))
		self.assertFalse(check_password_criteria(pwTestGreaterMaxLength))

if __name__ == '__main__':
	unittest.main()
