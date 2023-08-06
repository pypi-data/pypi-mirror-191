**[Installation](#installation)** |
**[Execution](#execution)** |
**[Further documentation](#further-documentation)** |
**[Getting help](#getting-help)** |
**[Acknowledgments](#acknowledgments)** |

# JuMonC-llview

A plugin for [JuMonC](https://gitlab.jsc.fz-juelich.de/coec/jumonc) to enable interaction with llview
---

## Installation

jumonc-llview can be installed using [pip](https://pypi.org/project/jumonc-llview):

`pip install jumonc-llview`

This automatically registers as a JuMonC plugin, and will be started with the next JuMonC (if they are both in the same enviroment)

### Runtime dependencies inherited from JuMonC

- [python3](https://www.python.org/) minimum version 3.6
- [mpi4py](https://mpi4py.readthedocs.io/en/stable/)
- [flask](https://flask.palletsprojects.com/en/2.0.x/)
- [flask-login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy)
- [pluggy](https://pluggy.readthedocs.io/en/latest/)
- [typing-extension](https://pypi.org/project/typing-extensions/) in case you are using python version <=3.9

## Execution

This plugin is started with [JuMonC - see execution](https://gitlab.jsc.fz-juelich.de/coec/jumonc#execution).
The paths returned can be set using `jumonc --llview="api-paths=example/path/"` when starting JuMonC


## Getting help

Open an [issue](https://gitlab.jsc.fz-juelich.de/coec/jumonc-nekrs/-/issues/new)


## Acknowledgments
[<img src="https://gitlab.jsc.fz-juelich.de/coec/jumonc-nekrs/-/blob/main/doc/Logo/EU_Horizon.png"  width="100" title="Horizon Europe: Research and innovation funding programme until 2027" alt="Horizon Europe">](https://ec.europa.eu/info/research-and-innovation/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en) JuMonC has been developed as part of the [CoEC](https://coec-project.eu/) project, the CoEC project has received funding from the European Union’s Horizon 2020 research and innovation programm under grant agreement No 952181.

[<img src="https://gitlab.jsc.fz-juelich.de/coec/jumonc-nekrs/-/raw/main/doc/Logo/COEC_LOGO.png"  height="100" title="The Center of Excellence in Combustion" alt="CoEC Logo">](https://coec-project.eu/) [<img src="https://gitlab.jsc.fz-juelich.de/coec/jumonc/-/raw/main/doc/Logo/EU_Horizon.png"  height="100" title="Horizon Europe: Research and innovation funding programme until 2027" alt="Horizon Europe">](https://ec.europa.eu/info/research-and-innovation/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en)

