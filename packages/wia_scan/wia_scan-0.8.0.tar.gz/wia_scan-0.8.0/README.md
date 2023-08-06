
<h1 align="center">
  <br>
  <a href="https://github.com/JonasZehn/python_wia_scan"><img src="https://raw.githubusercontent.com/JonasZehn/python_wia_scan/main/res/teaser.png" alt="wia_scan" width="600"></a>
  <br>
  wia_scan
  <br>
</h1>

<p align="center">
  <a href="https://pypi.python.org/pypi/wia_scan"> <img src="https://img.shields.io/pypi/v/wia_scan.svg" alt="wia_scan on PyPI"> </a>
  <a href="./LICENSE"> <img src="https://img.shields.io/badge/license-MIT-blue" alt="wia_scan PyPI License"> </a>
  <a href="https://coveralls.io/github/JonasZehn/python_wia_scan?branch=main"> <img src="https://coveralls.io/repos/github/JonasZehn/python_wia_scan/badge.svg?branch=main" alt="Coverage Status"> </a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>


## Introduction

A simple utility for using document scanners that support
[Windows Image Acquisition (WIA)](https://learn.microsoft.com/en-us/windows/win32/wia/-wia-startpage)
and is easy to install. If your scanner works using `Windows Fax and Scan`, there is a good chance it will work with this python script.
This package allows you to create your own efficient scanning loop or use the one the one already provided.

Use cases:
* You have a flatbed scanner, and you need to scan a lot of documents, thus you don't want to
  use Windows Fax and Scan tool as it can introduce quite some overhead. This utility allows
  you to only press a few keystrokes in between scans, while you may need to turn the page or
  change the paper since you don't have an automatic feeding scanner like I don't.
* Support scanners in your own application on Windows using a simple Python dependency

The utility supports a simple calibration process which is fully visual. The reason for this process is that my scanner's default
brightness (corresponding to brightness=0) is too bright.

Alternatives: Existing WIA libraries, but to my surprise the ones I found required quite old
versions of Python, which I didn't want since I wanted to combine the scanning process with some modern Python packages.

## Installation

Requirements:
* Windows
* Python ≥ 3.7

`wia_scan` can be installed from the package repository by running
```
pip install wia_scan
```

### Alternative: From Source
Download the source code in this repository and install flit using `pip install flit` and run the following command from the source folder
```
flit install
```

## Usage

### Scan Many Documents
The main use case of this utility is to scan many documents using a few key presses, this can be achieved by running
```
wia_scan many
```
During the process, the utility will ask you beforehand which quality profile should be used for the next scan, and 
multiple sides can be combined into a single picture.

### Command Line Interface

```
  wia_scan list_devices [-v]
  wia_scan single [--file=<output_file>] [--dpi=<dpi>] [--brightness=<brightness>]
                  [--contrast=<contrast>] [--mode=<mode>] [-v] [--uid=<uid>] [-q]
  wia_scan many [--out=<output_folder>] [--brightness=<brightness>] [--contrast=<contrast>] [-v]
  wia_scan calibrate brightness [--start=<start_range>] [--end=<end_range>]
                [--num_runs=<num_runs>] [--out=<output_folder>] [--uid=<uid>] [-q]
  wia_scan --help
  wia_scan --version

Options:
  -h --help                    Show this screen.
  --version                    Show version.
  -v --verbose                 Verbose output
  -q --quiet                   Quiet=no output
  --dpi=<dpi>                  Dots per inch; the higher this setting the higher the
                               output resolution [default: 200]
  --brightness=<brightness>    Brightness setting for the scanner, goes from -1000 to
                               1000 [default: 0]
  --contrast=<contrast>        Contrast setting for the scanner, goes from -1000
                               to 1000 [default: 0]
  --mode=<mode>                RGB for colored, L for grayscale [default: RGB]
  --file=<output_file>         Image output file
  --out=<output_folder>        Scanned images output folder [default: .]
  --start=<start_range>        Lowest value of brightness scanned [default: -200]
  --end=<end_range>            Highest value of brightness scanned [default: 200]
  --num_runs=<num_runs>        Number of scans for the "calibration" process [default: 9]
```

### Library Usage - Custom Loop
Example: Create your own python file `custom_loop.py` and scan many single sided documents from the same scanner while waiting for a single key press between scans:
```
from wia_scan import *

device = prompt_choose_device_and_connect()
for i in range(1000000):
    press_any_key_to_continue()
    pillow_image = scan_side(device=device)
    filename = f'{i}.jpeg'
    pillow_image.save(filename, subsampling=0, optimize=True,
             progressive=True, quality=80)
```


## License
`wia_scan` is distributed under the terms of the MIT license.
