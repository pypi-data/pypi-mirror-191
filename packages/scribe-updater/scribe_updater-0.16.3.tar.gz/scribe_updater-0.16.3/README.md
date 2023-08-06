### Setup
poetry runs a venv, so you need to run `poetry install` from the root of the repo first

#### Run
`poetry run updater`

#### Test
`poetry run pytest` 

#### Coverage
`poetry run pytest --cov` or `poetry run pytest --cov --cov-report=term-missing`

### Publish to PyPi
After adding credentials to be able to push to the python package index run the following cmd:
`poetry publish --build`

#### Linting
Install nox with:
`pip3 install nox`
add the path to your .bashrc and source it

run `nox -rs black`

#### Caveats
if you are getting an error that looks like this :<br> `Failed to create the collection: Prompt dismissed..`<br>
then export the following environment variable: <br>
`export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring`

# PBA Customer Spreadsheet Updater (`update.py`)

Injects new scenarios from the ground truth into a customer spreadsheet.

# Testing with console.py

from within the src/scribe_updater/ directory run the following:
`poetry run updater --target ../tests/test_input_1.json --ground ../tests/test_ground_1.json --output ./test_output`
