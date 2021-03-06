# Entail Core

## How to work on this library?

Tests are made to be run against installed package, not against the code inside
`src` directory. So to run tests, you need to install this package.

If you only want to run tests and not modify the code in `src` run:

    pip install .

On the other hand, if you want to modify the code in `src` and run tests
against your changes run:

    pip install -e .

This will make a link to the existing code in `src` and tests will always be
run against the latest code you have been working on.

Run the tests with:

    python -m unittest

### Note:
    
Files inside `src/entail_core/antlr` should never be touched because they are 
generated by ANTLR.