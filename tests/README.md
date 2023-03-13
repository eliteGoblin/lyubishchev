# TODO

* Add unit test for functions in day_parser.py
* Add integration test for day record parsing logic:
  * Grab real response from ClockifyAPI, feed into logic

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
# @pytest.mark.focus
# -s means show code's stdout in pytest's output
pytest -m focus -s tests -vv
```

```shell
# show all markers
pytest --markers
```

skip some tests:
```shell
# decorate function like following, run `py.test -rX -vv tests/unit $@`
@pytest.mark.skip(reason="no way of currently testing this")
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
