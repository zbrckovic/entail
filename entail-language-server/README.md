# Entail

## How to work on this project?

You can use python `3.10.` It might work with older versions but this is the
one I used.

All requirements for this project are specified in `requirements.txt` except
for `entail-core` library. This is because `entail-core` is still under
development, and I install it manually with `pip install -e ../entail-core`
which creates a link to its actual source code. This makes for a convenient
development experience because changes in `../entail-core` have an immediate
effect here.

To start the server run:

    python ./src/server.py

To start tests run:

    python -m unittest