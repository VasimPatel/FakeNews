# FakeNews

### Requirements
 - [Python 3](https://www.python.org/downloads/)
 
### Recommendations
 - [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
   - Virtualenv is a Python module built to built separate Python environments for project development. I would highly recommend that everyone install virtualenv and create a new clean virtual environment of Python for this project so that we can all operate using the same modules.
 - [PostgreSQL](https://www.postgresql.org/download/)
   - Technically, we only need to have the server running this, but I would recommend everyone download a local copy so that they can play around with it themselves so we don't have any datapocalypses happen on the server.
 - [PGAdmin](https://www.pgadmin.org/download/)
   - This may actually come with a PSQL install, but you might also have to download the newest version on your own. This represents a nice GUI for interacting with PSQL databases. It should work for **both** local databases as well as server connected databases. This will likely be a very helpful tool for viewing how all the data is structured once the server is up and running.

#### Setup
##### Install the required python modules
You can do this by simply passing the requirements.txt file (located within the repository) into pip. The command to do this is ```pip install -r requirements.txt```. If you've setup a virtual environment, make sure to activate it first so that you install the modules within your virtual environment and not in your global python environment. You can find more information on how to activate/use a virtual environment in the [virtualenv user guide](https://virtualenv.pypa.io/en/stable/userguide/).
##### Creating your .env file
If you want to try to run the setup_db.py file, you will need to create an environment file (.env file) in your project directory in order to load database host, name, user, and password. I have structured the script in this way so that everyone can have their own settings for accessing databases without having to sync them across github. This is also for security purposes, so that database database acesss passwords, hosts, and users are not hardcoded and then inadvertently stored in the cloud.
A .env file should look something like this:
```
DBHOST="localhost"
DBNAME="fakenews"
DBUSER="postgres"
DBPASS="PASSWORD"
```
Hopefully everything is fairly self-explanatory. The given DBUSER seen above is the default PSQL admin superuser. Likely we will either be logging in as this user, or we will be creating users for each one of us (this might be the better option, as it PSQL might be able to determine who editted the database last and would also allow more than 1 person to be logged in at once). Obviously you would replace the DBPASS field with the password associated with logging into PSQL as the given DBUSER.

Note that in the furture, the .env file also contain a DBPORT key if we need it in order to connect to server database.
