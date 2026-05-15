


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

```powershell
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

Enabling language server and type checking is highly recommended.
See Default mesh definition in `data/mesh.py`
The `'geo'` field defines the elements of the cylinder.
See `make_mesh.py:make_mesh` which creates and exported the mesh based on the definition.

### Running problems

See `data/problems.py` for example problems definitions.
`main.py` imports the default problems set and runs through all of them.
`make_vtu.py` post processes and makes all vtus. 

Any forward problem needs to be ran before inverse problems.

You may run `n` simulations with mpi in parallel, e.g.,

```bash
python main.py -n 8 --parallel 2
```

You may generate the pfiles without running the problem by

```bash
python main.py --dry-run
```


dfsgresg
  resg

  feaf