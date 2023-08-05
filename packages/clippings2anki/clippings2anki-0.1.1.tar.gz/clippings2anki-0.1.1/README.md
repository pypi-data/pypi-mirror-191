# Clippings2Anki

This is a simple script to convert the clippings.txt file from the Kindle to a txt file that can be imported into Anki.

## Installation

Install from PyPI ([pypi.org/project/clippings2anki](https://pypi.org/project/clippings2anki/)):

```
pip install clippings2anki
```

## Usage

Basic usage:

```
python -m clippings2anki [My Clippings.txt] [language] -o [output.txt]
```

Language  is the language of the words in the clippings file. It is used to get the definitions from wiktionary. It's format is the english name of the language, e.g. "english", "german", "french", etc.

The script will read the words saved in the clippings file and output them **along with their definitions from wiktionary** to a txt file that can be imported into Anki.

For help see:

```
python -m clippings2anki --help
```
