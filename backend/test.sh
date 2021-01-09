# Run all tests: ./test.sh 
# Run test following pattern: ./test.sh test

if [ $# == 0 ]; then
    python -m pytest --cov=app app/tests/ --cov-report=term-missing
else
    python -m pytest -v -k "$@"
fi