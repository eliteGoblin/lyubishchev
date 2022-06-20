# Run test

```shell
# unit test
pytest -rP -v tests/unit/*
# integration 
pytest -rP -v tests/integration/*
```

# Only run a particular test

configure own mark in `pytest.ini`

decorate the method using: `@pytest.mark.focus`

then run 

```shell
pytest -m focus tests
```

```shell
# show all markers
pytest --markers
```

# Show extra output

```shell
# Extra summary info can be shown using the '-r' option, recommended way
# shows the captured output of passed tests
pytest -rP
# shows the captured output of failed tests (default behaviour).
pytest -rx
# Another way: The `-s` switch disables per-test capturing (only if a test fails). `-s` is equivalent to --capture=no
pytest -s
```
