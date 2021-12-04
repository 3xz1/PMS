PMS by Alexander Eger


## Labor Software Security
## Password Management System by
## Alexander Eger ENITS 1 email: aeger1@stud.hs-offenburg.de

## Frameworks and setup
-Frameworks in use:
Docker
  - NGING
  - MYSQL
  - Python Flask

GITLAB CI to automaticaly test new function

Possible API Calls:

1. http://"IP"/create 
- create a new set of username and password hash for a user.
How its implemented:
<img width="705" alt="Bildschirmfoto 2021-12-04 um 17 19 12" src="https://user-images.githubusercontent.com/40068802/144716816-4a9825ec-6050-4dc5-b3e5-6fd0e9d9e094.png">


2. http://"IP"/login
- login a existing user with username and password
Implementation:
<img width="625" alt="Bildschirmfoto 2021-12-04 um 17 18 50" src="https://user-images.githubusercontent.com/40068802/144716787-a5d260d2-f25d-46dd-8914-9fed651d0895.png">

3. http://"IP"/changePassword
- change users password need to send old password aswell to check if he is allowed to change his password
Implementation:

<img width="705" alt="Bildschirmfoto 2021-12-04 um 17 19 12" src="https://user-images.githubusercontent.com/40068802/144716774-da2bc490-3172-4659-8f55-46f2f7a8c23e.png">


Haveibeenpwned is included as saftey check for password. The API calls /create and /changePassword are checking the hash if it already was included in a breach. If so user needs to create a secure password.
