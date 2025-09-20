## Setup

- Linux:

```sh
python3 -m venv venv
source venv/bin/activate
```

- Windows:

```bat
python -m venv venv
venv\Scripts\activate
```

## Instalar dependencias

```sh
pip install -r requirements.txt
```


## Ejecutar

- Linux

```sh
python3 -m src.main
```
- Windows

```bat
python -m src.main
```


## Tests

- Con GNU Make

```sh
make test
```
- O usar:

```sh
python -m coverage run --source src -m pytest --html=reports/pytest/index.html
python -m coverage html -d reports/coverage
```
