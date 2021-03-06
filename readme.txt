Setup Project
Step 1 :Create a virtual environment and activate it
virtualenv --distribute talkenv
source talkenv/bin/activate

step2: Install the requirements
pip install -r requirements.txt

Step3 : Run stunnel
sudo stunnel4 dev_https

Step4 : Run django server
HTTPS=on ./manage.py runserver 0.0.0.0:8000
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
------------------------------------------------------------------------------------------------------------------------------------
For running server on HTTPS (required for speech recognition)
//Setup stunnel
//Run the following commands on terminal

sudo aptitude install stunnel4
sudo su -
cd /etc
mkdir stunnel
cd stunnel
openssl req -new -x509 -days 365 -nodes -out stunnel.pem -keyout stunnel.pem
openssl gendh 2048 >> stunnel.pem
chmod 600 stunnel.pem
logout
cd

//Now create a file called dev_https with the following text:

pid=
foreground=yes
debug = 7

[https]
accept=8443
connect=8000
TIMEOUTclose=1
cert = /etc/stunnel/stunnel.pem

//Note: this assumes your web server is running on port 8000. If it’s not, change the value of “connect” to the appropriate port.

//Finally, run:

sudo stunnel4 dev_https
HTTPS=on ./manage.py runserver 0.0.0.0:8000

//In browser type https://0.0.0.0:8443/questionnaire/ to run .
----------------------------------------------------------------------------------------------------------------------------------------

For setting up django user registration
//Download registration templates at location /talktome/templates using the following command
wget https://bitbucket.org/devdoodles/registration_templates/get/3fa26711b938.zip

//Add csrf token to each form in each template using {% csrf_token %}

//Add the following url for the registration templates in urls.py

(r'^$', direct_to_template, 
            { 'template': 'index.html' }, 'index'), 

//Make the following changes  to settings.py file

ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
LOGIN_REDIRECT_URL = '/'

Add  'registration' to INSTALLED_APPS 

----------------------------------------------------------------------------------------------------------------------------------------
Although the table "myapp_tablename" already exists error stop raising after I did ./manage.py migrate myapp --fake, the DatabaseError shows no such column: myapp_mymodel.added_field.

Got exactly the same problem!

1.Firstly check the migration number which is causing this. Lets assume it is: 0010.

2.You need to:

./manage.py schemamigration myapp --add-field MyModel.added_field
./manage.py migrate myapp
if there is more than one field missing you have to repeat it for each field.

3.Now you land with a bunch of new migrations so remove their files from myapp/migrations (0011 and further if you needed to add multiple fields).

4.Run this:

./manage.py migrate myapp 0010
Now try ./manage.py migrate myapp
