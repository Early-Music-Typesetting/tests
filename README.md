# Early Testing Suite

> [!TIP]
> Report of the last test run can be viewed [here](./report.md).

Welcome to the documentation on Early Testing Suite.

Early Testing Suite provides a unit testing framework for Early
– a Lilypond macro library for early music.

What do we test using this tool?
- Desired layout of the score output,
- Correct scheme structure of the Early "smobs"
- Coverage of MEI standard and Early-to-MEI converter correct results.

## "Testing suite" and "unit tests".

A _testing suite_ is an assemble of unit tests. Each testing suite adheres
to a specific versions of lilypond, mei-mensural and early versions. Those
versions are stored inside the `config.json` file. All unit tests inside suite
use this config.

You can manually copy a suite, change the versions to the desired ones
and run tests again to verify if this causes any breaks. We advise you
to keep both old and new test suite and upload your report to us
via pull request, as this helps us to cover real-life test cases
from actively used environments.

## Requirerments

> [!Caution]
> Current workflow of this suite is in prototype phase. The development can introduce violent changes to the workflow described below.

For now, we test Early as follows:
1) create one directory with all the required Early repositories
```
my-directory (make this one yourself)
│
└──–releases
│   │   early-0.0.0.ly
│   
└───tests
    │   main.py
    │   report.md
    └───src...
    └───suites...
```

To use this testing suite, you must have installed:
* LilyPond 2.24.4
* Python 3.13

## Running tests

```bash
cd path/to/early
python3 tests/run.py
```

## Adding tests

You can add a test to an existing suite or create a new suite with a new test.

```bash
cd path/to/early
python3 tests/add.py suite-name test-name
```

You can also add many tests to one suite at once:

```bash
python3 tests/add.py suite-name first-test second fourth ...
```
