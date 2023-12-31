# seedphrase-fixer

This is a simple project that fixes a passphrase if one of the words was noted down incorrectly. Note: It currently only works for English BIP-39 words.

## Installation

### Python

You can download Python from the official website: https://www.python.org/downloads/

After downloading the installer, run it and follow the instructions.

### pip

pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org. If you are using a different version of Python, you can get pip by following instructions here: https://pip.pypa.io/en/stable/installation/

### Project requirements

After installing Python and pip, navigate to the project directory in your terminal and run the following command to install the project requirements:

```
pip install -r requirements.txt
```

## Environment Variables

Before running the program, you need to set up your environment variables. Copy the `.env.example` file to a new file named `.env` and replace the placeholder values with your actual values.

## Usage

To run this program, use the following command:

```
python main.py "witch collapse practice feed shame open despair creek road again ice least" "passphrase" 7
```

Replace `witch collapse practice feed shame open despair creek road again ice least` with your 12 or 24 word BIP-39 seedphrase, `passphrase` with your passphrase (if any), and the number 7 with the word that you think is incorrect (level blank and we will iterate through all the words).

For example:

```
python main.py "witch collapse practice feed shame open despair creek road again ice least" ""
```

This will attempt to fix the seedphrase by replacing each word one by one and checking the Bitcoin balances for the derived addresses. If a balance is found, the program will print the corrected seedphrase and the balances.
