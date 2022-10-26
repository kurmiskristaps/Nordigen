The Nordigen homework project.
Made in Django, bundled with Docker and using npm.

To start the project:

    - add a .env file, containing USER_SECRET_ID and USER_SECRET_KEY

    - run "docker-compose up" to start the Django server, Redis, and Celery 

    - run "npm run build" to build the frontend dependencies

Afterwards the project will be accessible at localhost:8000/index

When authenticated with a bank account you will be redirected to the /details page where the user can:

    - fetch their transactions with or without inputting a date range and a country ID, which is usable only if premium can be accessed

    - fetch account details

    - fetch account balances
These requests will then be processed and validated, and Celery workers will make requests to Nordigen.


The responses are then processed by jQuery and rendered in the template.


Potential improvements:

    - As this was a small project, and I wanted to better understand both how django templates and jQuery work, I opted on not using a JS framework like Vue for frontend. This 100% could be improved and would make adding new changes, modal views etc. much simpler.

    - Passing the data to forms.py using a data model, so no manual data formatting has to take place afterwards, like with date_from/to.

    - Adding a better DB to django like Postgres so better functionality could be added to this project later down the line.

    - A way to check if the user has access to premium products, before displaying the country input field for transaction retrieval, otherwise some user input is required to know if such an option should be accessible. This could be achieved by adding some "check_premium" call to Nordigen, but I could not find one. Making a direct call to accounts/premium/../transactions beforehand and checking the response would not be wise.

    - Switching all imports used templates to npm dependencies so they are not relying on other sources to be working / accessible

    - Testing could be improved, since it does not cover all possible cases for user input and celery tasks.
