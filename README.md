<img src="images/axolpy-logo-transparent.svg" width="50%" />

# axolpy-script, the Axolotl Library in Python
#### Release
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-script/releases">
    <img alt="Version" src="https://img.shields.io/github/v/release/tchiunam/axolpy-script?sort=semver" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-script/releases">
    <img alt="Release Date" src="https://img.shields.io/github/release-date/tchiunam/axolpy-script" />
  </a>
  <img alt="Language" src="https://img.shields.io/github/languages/count/tchiunam/axolpy-script" />
  <img alt="Lines of Code" src="https://img.shields.io/tokei/lines/github/tchiunam/axolpy-script" />
  <img alt="File Count" src="https://img.shields.io/github/directory-file-count/tchiunam/axolpy-script" />
  <img alt="Repository Size" src="https://img.shields.io/github/repo-size/tchiunam/axolpy-script.svg?label=Repo%20size" />
</div>

#### Code Quality
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-script/actions/workflows/python.yaml">
    <img alt="Python" src="https://github.com/tchiunam/axolpy-script/actions/workflows/python.yaml/badge.svg" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-script/actions/workflows/codeql-analysis.yaml">
    <img alt="CodeQL" src="https://github.com/tchiunam/axolpy-script/actions/workflows/codeql-analysis.yaml/badge.svg" />
  </a>
</div>

#### Activity
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-script/commits/main">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/tchiunam/axolpy-script" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-script/issues?q=is%3Aissue+is%3Aclosed">
    <img alt="Closed Issues" src="https://img.shields.io/github/issues-closed/tchiunam/axolpy-script" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-script/pulls?q=is%3Apr+is%3Aclosed">
    <img alt="Closed Pull Requests" src="https://img.shields.io/github/issues-pr-closed/tchiunam/axolpy-script" />
  </a>
</div>

#### License
<div align="left">
  <a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/github/license/tchiunam/axolpy-script" />
  </a>
</div>

#### Popularity
<div align="left">
  <img alt="Repo Stars" src="https://img.shields.io/github/stars/tchiunam/axolpy-script?style=social" />
  <img alt="Watchers" src="https://img.shields.io/github/watchers/tchiunam/axolpy-script?style=social" />
</div>

<br />
This is the script repository of the Axolotl series in Python. These
scripts are written for the common use cases for the life of an engineer.
You may configure **axolpy** through configuration file or command
line parameters.

## Usage
### Configure environment
Configure the follow environment variables:
```
AXOLPY_PATH=~/axolpy-script        # The path to axolpy-script directory
```

### Install dependencies
#### Recommended way
You are recommended to use [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv) to install the dependencies.
```
pipenv install
```

#### Alternative
You can install dependencies with the old way by using requirements.txt.
```
pip install -r requirements.txt
```

## Examples
### Encrypt or decrypt message
Run this to encrypt a message. Enter the key and message or provide them using `-k` for key file and `-m` for message.
```console
python bin/crypt-message.py
```
Similarly, run this to decrypt a message:
```console
python bin/crypt-message.py --decrypt
```

See the help for more details:
```console
python bin/crypt-message.py --help
```
You'll see output like this:
```console
usage: crypt-message.py [-h] [-g] [-k KEY_FILE] [-d] [-m MESSAGE]

Encrypt or decrypt a message. The output is written to stdout.

By default, encryption is executed. To decrypt, use the --decrypt.

options:
  -h, --help            show this help message and exit
  -g, --generate-key-file
                        Generate a key file. If this is specified, other arguments are ignored.
  -k KEY_FILE, --key-file KEY_FILE
                        The path to the key file.
  -d, --decrypt         Decrypt a message.
  -m MESSAGE, --message MESSAGE
                        Message to encrypt or decrypt. If not specified, read from stdin.
```

### Redis cluster load test
To run load test:
```console
locust -f bin/redis-cluster-load-test.py --headless -u 1000 -r 100 --run-time 5m --stop-timeout 5
```

---
#### See more  
1. [axolpy-lib](https://github.com/tchiunam/axolpy-lib) for the base library
