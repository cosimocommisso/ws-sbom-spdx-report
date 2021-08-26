![Logo](https://whitesource-resources.s3.amazonaws.com/ws-sig-images/Whitesource_Logo_178x44.png)  
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI](https://github.com/whitesource-ps/ws-sbom-report/actions/workflows/ci-master.yml/badge.svg)](https://github.com/whitesource-ps/ws-sbom-report/actions/workflows/ci-master.yml)
[![Python 3.6](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Blue_Python_3.6%2B_Shield_Badge.svg/86px-Blue_Python_3.6%2B_Shield_Badge.svg.png)](https://www.python.org/downloads/release/python-360/)
[![GitHub release](https://img.shields.io/github/v/release/whitesource-ps/ws-sbom-spdx-report)](https://github.com/whitesource-ps/ws-sbom-spdx-report/releases/latest)
# WhiteSource SPDX Suite
Suite of utilities to handle SPDX.

The suite contains:
1. Software Bill of Materials (SBOM) Report Generator in SPDX format (JSON, XML, RDF and Tag-Value file types)
1. Import SPDX SBOM Report file Utility into WhiteSource.
### Supported Operating Systems
- **Linux (Bash):**	CentOS, Debian, Ubuntu, RedHat
- **Windows (PowerShell):**	10, 2012, 2016
### Prerequisites
- **Python 3.7+**
### Installation
- Download and unzip the package.
## 1. SBOM Report Generator in SPDX format
CLI Tool to generate SBOM report on chosen scope in [SPDX format](https://spdx.org).
* The tool utilizes [spdx-tools](https://github.com/spdx/tools).
* The tool can be executed on WS Product or Project scope.
* The tool accepts additional values which are unknown to WS via `sbom_extra.json`.
* If not stated, the tool will access SAAS.
* If not stated, the tool will produce report in JSON format.

2. Edit the file **sbom_extra.json** with the appropriate values to complete the report:
### Usage
```shell
sbom_report.py [-h] -u WS_USER_KEY -k WS_TOKEN [-s SCOPE_TOKEN]
                      [-a WS_URL] [-t {tv,json,xml,rdf,yaml}] [-e EXTRA]
                      [-o OUT_DIR]

Utility to create SBOM from WhiteSource data

optional arguments:
  -h, --help            show this help message and exit
  -u WS_USER_KEY, --userKey WS_USER_KEY
                        WS User Key
  -k WS_TOKEN, --token WS_TOKEN
                        WS Organization Key
  -s SCOPE_TOKEN, --scope SCOPE_TOKEN
                        Scope token of SBOM report to generate
  -a WS_URL, --wsUrl WS_URL
                        WS URL
  -t {tv,json,xml,rdf,yaml}, --type {tv,json,xml,rdf,yaml}
                        Output type
  -e EXTRA, --extra EXTRA
                        Extra configuration of SBOM
  -o OUT_DIR, --out OUT_DIR
                        Output directory
```
### Execution
Execution instructions:  
```shell
python sbom_report.py -u <USER_KEY> -k <TOKEN> -s <SCOPE_TOKEN>
```
## 2. Import SPDX SBOM Report file Utility
Utility that generate update request and upload it into WhiteSource Application.
### Usage
```shell
spdx2ws.py [-h] -u WS_USER_KEY -k WS_TOKEN [-a WS_URL] [-l SPDX_FILE]
                  [-o OUTPUT_DIR] [-pj PROJECT_TOKEN] [-pd PRODUCT_TOKEN]
                  [-pdn PRODUCT_NAME]

Utility to import SPDX document into WS

optional arguments:
  -h, --help            show this help message and exit
  -u WS_USER_KEY, --userKey WS_USER_KEY
                        WS User Key
  -k WS_TOKEN, --token WS_TOKEN
                        WS Organization Token
  -a WS_URL, --wsUrl WS_URL
                        WS URL
  -l SPDX_FILE, --spdxFile SPDX_FILE
                        Location of imported file
  -o OUTPUT_DIR, --outputDir OUTPUT_DIR
                        Output Directory to save update request
  -pj PROJECT_TOKEN, --projectToken PROJECT_TOKEN
                        Project token to import data to
  -pd PRODUCT_TOKEN, --productToken PRODUCT_TOKEN
                        Product token to import data to
  -pdn PRODUCT_NAME, --productName PRODUCT_NAME
                        Product name to import data to
```
### Execution
Execution instructions:
```shell
python spdx2ws.py -u <USER_KEY> -k <TOKEN> -s <SCOPE_TOKEN> -l <SPDX_REPORT> -pj <PROJECT_TOKEN>
python spdx2ws.py -u <USER_KEY> -k <TOKEN> -s <SCOPE_TOKEN> -l <SPDX_REPORT> -pd <PRODUCT_TOKEN>
python spdx2ws.py -u <USER_KEY> -k <TOKEN> -s <SCOPE_TOKEN> -l <SPDX_REPORT> -pdn <PRODUCT_NAME>
```