# BACKEND

## Data objects

- Characteristics
- Values


## TODO

* Automatic import all files under `services\__init__`, `models\__ini__` and `routes\__ini__`
* Automatic test automation creation. Check whether schema and model are compatible! (https://docs.pytest.org/en/stable/parametrize.html)


### Low priority
- Replace pifile by poetry
- Add https://github.com/kolypto/py-sa2schema (does not work with devcontainer apparently) (Default schema along model creation)
- Update to python 3.9 (not working INFO:     127.0.0.1:46772 - "GET /%5Bobject%20Module%5D HTTP/1.1" 404 Not Found, on 9.Jan.20 )


## Requirements

- Admin can add

## Test

- `alias test_='python -m pytest --cov=app app/tests/ --cov-report=term-missing'`
- `pytest -v`
- `pytest -v -k TestName`
- `--pdb`: runs the debugger when an error is encountered
- `--lf`: runs only the tests that failed on the last attempt.
- Use mjml extension of VSCode to export to j2/hmtl
- `# type: ignore`


## References

* https://stackoverflow.com/questions/5929107/decorators-with-parameters