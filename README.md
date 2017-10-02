# Health services waiting times
The application shows the health services waiting times in South Tyrol. It is possible to filter the different services. The application is available on [https://tempi-attesa.herokuapp.com/](https://tempi-attesa.herokuapp.com/).

The data are taken from the [Open Data Alto Adige/Suedtirol/South Tyrol portal](http://dati.retecivica.bz.it/it/dataset/southtyrolean-healthservices-waitingtimes)


## Getting Started

### Prerequisites

In order to execute the application locally, you need Python 3.x, pip and gunicorn.
If you want to create an isolated Python environment, you can install [virtualenv](https://pypi.python.org/pypi/virtualenv)

```
pip install virtualenv
```
You can find more information on how to install Python and on how to use pip and virtualenv [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

### Installing
First, you should obtain a local copy of the repository with the following commands :
```
git clone https://github.com/abonte/southtyrolean-healthservices-waitingtimes.git healthservices-waitingtimes
cd healthservices-waitingtimes
```
Then, you can create an isolated Python environment with
```
virtualenv -p python3 healthservices-waitingtimes
source healthservices-waitingtimes/bin/activate
```
and install the dependencies that are required for the application to work

```
pip install -r requirements.txt
```

Finally, you can run the application with the following command

```
gunicorn app:app --log-file=-
```

The application is available on [http://127.0.0.1:8000](http://127.0.0.1:8000)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


Open Iconic — [www.useiconic.com/open](www.useiconic.com/open)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)