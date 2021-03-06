<img id="eGov-logo-text-CZ" width="400" src="assets/Logo-text-en.png">

# eGovernment index dashboard: An eGov benchmarks data viewer
![eGovernment index dashboard deploy and test](https://github.com/Plavit/eGovernment-index-dashboard/workflows/eGovernment%20index%20dashboard%20deploy%20and%20test/badge.svg?branch=master)
![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_message=online&url=http%3A%2F%2Fegov-t1.herokuapp.com%2F)
\
A simple Python and Dash Plotly app that visualizes hard-to-process data from eGov indexes by the European Union and the United Nations. This project started off as a part of a semestral assignment at FIT, Czech Technical University and later used during further research at the Charles University in Prague and at the Univeristy of Cambridge

## Mutations
This project has been split into several variations over time. Different repositories contain different versions based on the same original idea. There are currently two repositories:
-  [`eGovernment-index-dashboard`](https://github.com/Plavit/eGovernment-index-dashboard),  the original main working version, currently containing a czech mutation used for my diploma thesis
-  [`eGovernment-index-dashboard-international`](https://github.com/Plavit/eGovernment-index-dashboard-international), the version adapted for some English publications

### This version (`eGovernment-index-dashboard-international`)
The English version submitted as supporting material to the Cambridge Journal of Science and Policy. It contains data updated in early 2021, the EU benchmark up to 2019 and the UN benchmark up to 2020. Compared to the original version, the individual country spotlight was removed

## Live example
Check the app here:
https://egov-dashboard-cambridge.herokuapp.com/

## Deployment
To run locally:

1) Get requirements in requirements.txt through
`npm install`
2) Run the app with:
`$ python app.py`

