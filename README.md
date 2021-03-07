
# Search Facility Near You (SeF)

#### Overview

- This API powers a React App that helps you find the health facility near you. The data feeds from the KMFL API which has all facility data for the country.

### Design

-  The API utilize data from the KMFL system. To ensure that we don't hog KMFL system, data from KMFL API is staged in a remote server where preprocing of the data is done.
- Different attributes of the facility are important in this case, eg. the latitude and longitude coordinates, the type of the facity among other attributes.
- Since the goal is to have an API that helps the user find a health facility near him/her, there is a specific module that given the users coordinates, we are able to find the facilities that falls within a given radius in `km`.
-
	#### Project Structure Overview
  This is a Django package with the structure below. `sef` is the main package that has 3 main packages which include, `common`, `facility` and `user`. The `facility` package  holds all logic and utilities that facilitates the connection to the KMFL API, retrieving the data, staging the data and preprosing the data to feed to a web app.

		sef-api/
		   bin/
		      sef_manage.py
		   sef/
		      common/
		      facility/
		      user/
		      constants.py
			tests/
			   querry_db.py
			   format_query.py
			README.md/
			requirements.txt
			manage.py
			setup.py


### How to!
#### a) Running tests
-	Run `pytest`
#### b) Running the application
-	After cloning the app, create a virtual environment, install the requirements, setup the database and run ./manage.py runserver to run the app locally.
-	A deployed version of the API can be found through [this](https://api.sef.cislunar.co/v1/facility/facilities/) link.

### Regards!
