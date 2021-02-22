This project is my realisation of magic links with Django.

## Setup

`git clone git@github.com:zagorboda/django-magic-link.git`
    

```
python -m venv env
source env/bin/activate
cd django-magic-link
pip install -r requirements.txt
```

Configure DB

-Postgres

```
CREATE DATABASE mydb;

CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypass';

ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

  ​    
  -SQLite

  	Just add db file next to manage.py

  Environment

  -Set environmet varibles

  	SECRET_KEY=0x!b#(1*cd73w$&azzc6p+essg7v=g80ls#z&xcx*mpemx&@9$
  	DATABASE_NAME=db_name
  	DATABASE_USER=db_user 
  	DATABASE_PASSWORD=password
  	DATABASE_HOST=localhost
  	DATABASE_PORT=5432
  	
  	MAIL_GUN_API_LINK=https://api.mailgun.net/v3/sandbox_many_digits_and_chars.mailgun.org/messages
  	MAIL_GUN_API_TOKEN=token
  	MAIL_GUN_EMAIL=mailgun@sandbox_many_digits_and_chars.mailgun.org


  Run migrations

  	python manage.py migrate

  Create superuser

  	python manage.py createsuperuser

  ## Using

  ![image-20210222022818493](/home/bod/.config/Typora/typora-user-images/image-20210222022818493.png)

  ### Home page

  If you are authenticated you will see message with your username. 

  First 3 links do what thay say - manual login (username and password), logout and signup (username, password, email).

  Get_login_link redirects to page with single input line. User is promoted to enter valid email that was used while signup. If email is valid and there is user with this email, then : 

  * Generate random string (token)
  * Create hash from token (i use sha256)
  * Create new instance with token hash and information about user that request login link
  * Create login link with token, send email to entered email address

  Last url is just simple view that redirects not authenticated user to main page.


  If user entered correct email, will be received email with similar context 

  `[Link](https://your-app.com/handle_login_url/?token=some_token) to login into website. Mark this message as not spam (otherwise link will not show)`

  User is redirected to handle_magic_link_view that does next :
  * Retrieve token from get request
  * Generate hash from token
  * Check if objects with this hash exists in database
  * Check if user associated with this object exists and active
  * Increase number of hits for this url
  * Login user with session

### Django admin

![image-20210222105728547](/home/bod/.config/Typora/typora-user-images/image-20210222105728547.png)



Django admin will include one additional table, MagicLinkHash.

![image-20210222110126474](/home/bod/.config/Typora/typora-user-images/image-20210222110126474.png) 	

Table hold user email and id, hashed token, datetime when token were created and number of times this link was used.

User can request unlimited number of tokens, and all tokens would be valid. If you need to restrict user access just delete this object in db.
