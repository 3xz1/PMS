import unittest
from password_check import check_hibp, check_password_criteria
import json

class TestPasswordCheck(unittest.TestCase):
	def test_check_password(self):
		with open('pms/password_config.json') as json_file:
			password_config = json.load(json_file)['password_config']
			
		pwTestMinLength = '!asAH12' # Min length should be 8 
		pwTestMaxLength = 'a12345678§0123456789012F4567890' # max pw length 30
		pwTestGreaterMaxLength = 'a12345678§0123456789012F4567890X' # pw length 31
		pwTestHibp = 'Password!' # should fail at hibp
		pwTestDigit = 'nOt!SeCurePW' # pw without Digit
		pwTestLower = "SOME1PWNO!$X" # pw without lower case letters
		pwTestHigher = "some1pwno!§x" # pw without upper case letters
		pwTestSpecialChar = "somepWdo1xa3" # pw without special char
		pw = 't@6cLY$YkZM?t#kP'

		# Test cases
		if(password_config['digit'] == True):
			self.assertFalse(check_password_criteria(pwTestDigit))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestDigit))
			self.assertTrue(check_password_criteria(pw))
		if(password_config['lower char'] == True):
			self.assertFalse(check_password_criteria(pwTestLower))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestLower))
			self.assertTrue(check_password_criteria(pw))
		if(password_config['upper char'] == True):
			self.assertFalse(check_password_criteria(pwTestHigher))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestHigher))
			self.assertTrue(check_password_criteria(pw))
		if(password_config['special char'] == True):
			self.assertFalse(check_password_criteria(pwTestSpecialChar))
			self.assertTrue(check_password_criteria(pw))
		else:
			self.assertTrue(check_password_criteria(pwTestSpecialChar))
			self.assertTrue(check_password_criteria(pw))
		
		self.assertFalse(check_password_criteria(pwTestMinLength))
		self.assertFalse(check_password_criteria(pwTestMaxLength))
		self.assertTrue(check_password_criteria(pw))

if __name__ == '__main__':
	unittest.main()