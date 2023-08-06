# CodeRadar

Identifying the highest threats to your code quality by analyzing code metrics of your project using pytest and pylint.

**Status:**  Beta (runs, but certainly has bugs)\
**Authors:** Carsten König

## Purpose

In order to quickly see where an existing project needs refactoring, an overview of the worst code smells is needed. This package therefore summarizes these in a very brief report, that should guide you directly to the places in your software where an improvement would have the highest impact when you want to improve code quality.


## Installation

```bash
pip install coderadar
```

## How to use
In order to analyze your sourcecode, go to your project root folder and run

```bash
coderadar <path-to-source>
```
This will run pytest, pylint and flake8 to get the metrics that will be analyzed.

The following artifacts will be created:

- ``coverage.xml``
- ``coverage.txt``
- ``pylint.json``
- ``pylint.txt``
- ``code_quality_report.html``
- ``code_quality_report.txt``


## License
[GNU GPLv3 License](https://choosealicense.com/licenses/gpl-3.0/)

## Author
**Carsten König**

- [GitLab](https://gitlab.com/ck2go "Carsten König")
- [GitHub](https://github.com/ck2go "Carsten König")
- [LinkedIn](https://www.linkedin.com/in/ck2go/ "Carsten König")
- [Website](https://www.carsten-koenig.de "Carsten König")