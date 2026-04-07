


## Requirements
- Requires Python 3.14
- Cheart solver compiled and available in the environment as `cheartsolver.out`


## Getting started

Pull submodules
```bash
git submodule update --init --recursive
```

### Using `uv`
```bash
uv sync
```

### Using `pip`

1. Create a virtual environment
```bash
python -m venv .venv
```
2. Activate virtual environment

Linux/MacOs
```bash
source .venv/bin/activate
```
Windows
```Powershell
.venv/Script/activate
```

3. Install
```bash
python -m pip install .
```

## Examples

### Pilot examples 
To run all the pilot examples:
```bash
chsolve pilot/*.P
```

Enable logs and using 8 mpi processes 
```bash
chsolve pilot/*.P --log -n 8
```

### Creating the mesh