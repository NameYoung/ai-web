# Backend

> backend server for ai-web

## Requirements

- [Python 3.8]()
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/intro.html#installation)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [scikit-learn](https://scikit-learn.org/stable/install.html)

> For more details, see requirements.txt

## Run By Command

```shell
> cd src/
> python3 -m uvicorn main:app --port 8000
```

### See API Docs

address: http://127.0.0.1:8000/docs

### Shut Down

> Press CTRL+C to quit

## Run By Docker

```shell
> docker build --tag ai-backend-docker .
> docker run --publish 8000:8000 ai-backend-docker
```
