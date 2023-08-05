# py-unicode-linebreak

Python bindings for the Rust crate [unicode-linebreak](https://crates.io/crates/unicode-linebreak).

## Installation

```bash
pip install unicode-linebreak
```

## Usage

```python
from unicode_linebreak import linebreaks

string = 'a b\nc\r\nd e\rf end'
expected_result = [
    (2, False), (4, True), (7, True), (9, False),
    (11, True), (13, False), (16, True)
]
assert linebreaks(string) == expected_result
```

Returns a list of tuples with the index of the linebreak and a boolean indicating whether the linebreak is a mandatory break.

## Contribute

```bash
python -m virtualenv venv
source venv/bin/activate
pip install -r dev-requirements.txt
maturin develop && python -m unittest
```
