# alias test='bash test.sh'
python -m pytest --cov=app app/tests/ --cov-report=term-missing
# python -m pytest -v -k test_activation_router