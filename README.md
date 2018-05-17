## About

This project triggers an Authy Push Notification from an incoming SMS message

## Setup

- Install the requirements and setup the development environment.

        virtualenv env
        source env/bin/activate
        
        pip install -r requirements.txt


- Run the application.

        gunicorn app:app

- Navigate to [localhost:8000](localhost:8000).


## Deploy to Heroku with Git

Create a [Heroku account](https://signup.heroku.com/)

Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

        heroku create
        git push heroku master


## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.

Forked with much appreciation from https://github.com/MaxHalford/flask-boilerplate
