<!-- markdownlint-disable MD026 MD036-->

# `.pypirc` File Management Client

**"This is hopefully a temporary fork, as the official project looks dead."**
said [Chappers](https://github.com/charliec443), who originally forked this project. Unfortunately, that fork is also dead.
So here I am. Forking it again, making it work with Python 3.10+ (no backwards compatibility).

If you want to have it work in older versions of Python, please go download the [original](https://github.com/ampledata/pypirc), or [Chapper's fork](https://github.com/charliec443/pypirc).

## Installation

Install from [pypi](https://pypi.org) via the following:

```bash
pip install pypirc-voidei
```

## Usage Example

Display current pypi configuration:

```bash
pypirc
```

Add a pypi server:

```bash
pypirc -s mypypi -u foo -p bar -r https://mypypi.example.com/
```

### Credits:

#### Source

Official: <https://github.com/ampledata/pypirc>
Chappers: <https://github.com/chappers/pypirc>
voidei: <https://github.com/voidei/pypirc>

#### Author

Greg Albrecht <gba@splunk.com>
<http://ampledata.org/>

#### Copyright

```plaintext
Copyright 2012 Splunk, Inc.
```

#### License

**Apache License 2.0**
