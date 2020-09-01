# Eaton Remote Control
(Only tested on Eaton G3 ePDU Switched)

Eaton G3 Managed PDUs offer remote control via a webgui.
However, the lower end tiers do not offer a management API and their CLI is quite to use.
This project is a Python wrapper for the webgui, offering a CLI interface.
It can also be used in other Python projects.  

The Eaton configuration can be given via CLI or a `config.yaml` file (see `config.example.yaml`)

It relies on Node for the authentication script (`shark_gen.js`)

## Examples

Turn B1 off:`
`python3 -m eaton -c ./config.yaml outlet B1 off --yes-i-am-sure

# Under the hood
For the authentication subsystem, the `shark.js` library from Eaton is reverse engineered.
Most functions have been replaced by Python equivalents, implemented in `response_gen.py`
Only the MD5 hash function hasn't been reverse engineered (yet) as it doesn't give the same
results as Pythons hashlib md5.
