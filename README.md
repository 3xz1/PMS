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

```mermaid
sequenceDiagram
    participant Alice
    participant NGINX
    Alice->>NGINX: create credential set
    NGINX->>HIBP: request if hash from pw was breached
    HIBP->>NGINX: returns jason of possible hashed
    loop check HIBP answer
    	NGINX->>NGINX: check if hash is inside the answer
    end
    NGINX->>Alice: if hash inside the answer return pw has been breached
    NGINX->>MYSQL_DB: else try insert credentials
    MYSQL_DB->>NGINX: return success or duplicate entry
    NGINX->>Alice: Report status if user was created

```

2. http://"IP"/login
- login a existing user with username and password
Implementation:
```mermaid
sequenceDiagram
    participant Alice
    participant NGINX
    loop Check pw config
        NGINX->>NGINX: Check if new password criteria was set
    end
    Alice->>NGINX: send login credentials
    NGINX->>MYSQL_DB: get pw_hash from user
    MYSQL_DB->>NGINX: return pw_hash
    loop hash and compare
    	NGINX->>NGINX: Hash pw with salt and compare with db pw_hash
    end
    NGINX->>Alice: Login successful if compare true, pw date still good and pw meets pw criteria
    NGINX->>Alice: elif compare false return login unseccessful
    NGINX->>Alice: else new pw criteria promt user to set new pw
    Alice->>NGINX: Send new pw
    NGINX->>HIBP: request if hash from pw was breached
    HIBP->>NGINX: returns jason of possible hashed
    loop check HIBP answer
    	NGINX->>NGINX: check if hash is inside the answer
    end
    NGINX->>Alice: if hash inside the answer return pw has been breached
    NGINX->>MYSQL_DB: set new password hash
    MYSQL_DB->>NGINX: Return status
    NGINX->>Alice: return status
```
3. http://"IP"/changePassword
- change users password need to send old password aswell to check if he is allowed to change his password
Implementation:
```mermaid
sequenceDiagram
    participant Alice
    participant NGINX
    Alice->>NGINX: send login credentials and new password
    NGINX->>MYSQL_DB: get pw_hash from user
    MYSQL_DB->>NGINX: return pw_hash
    loop hash and compare
    	NGINX->>NGINX: Hash pws with salt and compare with db pw hash
    end
    NGINX->>HIBP: request if hash from pw was breached
    HIBP->>NGINX: returns jason of possible hashed
    loop check HIBP answer
    	NGINX->>NGINX: check if hash is inside the answer
    end
    NGINX->>Alice: if hash inside the answer return pw has been breached
    NGINX->>MYSQL_DB: else set new password hash
    MYSQL_DB->>Alice: Return status
```

Haveibeenpwned is included as saftey check for password. The API calls /create and /changePassword are checking the hash if it already was included in a breach. If so user needs to create a secure password.




```mermaid
sequenceDiagram
    participant User
    participant Marketplace
    participant Provider
    participant Operator-Service
    participant Operator-Engine
    participant pod-configuration
    participant algorithem-container
    participant pod-publishing

    User->>Marketplace: Buy assets.
    Marketplace->>Provider: Initialzie Compute Job.
    Provider->>Operator-Service: Generate Workflow and call /compute from Operator-Serivce.
    Operator-Service->>Operator-Engine: Setup worklflow and execute SQL command to trigger job execution.
    Operator-Engine->>pod-configuration: Trigger pod-configuration container. That will download asset dataset into /data/inputs/.
    pod-configuration->>Operator-Engine: Return if configuration was successful.
    Operator-Engine->>algorithem-container: After pod-configuration was successful start algorithem container.
    algorithem-container->>Operator-Engine: When algorithem-container has finished callback to Operator-Engine to publish results.
    Operator-Engine->>pod-publishing: Start pod to publish results to S3 buckets.
```
