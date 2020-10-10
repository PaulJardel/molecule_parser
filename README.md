# molecule_parser

### Introduction 

This project is used to talk about Python programming.

You can find the goal of this project here :
https://gist.github.com/mlvernay/57ed73edfc875ecc11f1671481ce6b23

2 main classes are available on this project.
* MoleculeParser : final class, working fine
* MoleculeParserAlpha : first class developed, not working as it should. But I wanted to add it, it can be useful for our future talks.

### Project architecture

```sh
 $ tree -L 2
.
├── Makefile
├── README.md
├── molecular
│   ├── __init__.py
│   ├── __pycache__
│   ├── molecule_parser.py          # Class containing the final molecule parser
│   ├── molecule_parser_alpha.py    # First class developed for contructing the molecule parser, from nowhere
│   ├── monitoring
│   └── venv
├── requirements.txt
├── setup.cfg
├── tests
│   ├── __init__.py
│   └── test_molecule_parser.py

### Libraries
 
All required libraries are decalred on requirement.txt. To install them all, use:
 
```sh
 $ pip install -r requirements.txt
```

### Linter
This project uses Flake8 linter. To launch the linter scan, use:
 
```sh
 $ make lint
```

### Tests
 
This library uses pytest and coverage. The following command will run the tests and generate a covergae report:
 
```sh
 $ make test
```