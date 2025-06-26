# ProjetoGrafico

This repository contains a simple 2D graphics application built with Python and Pygame. The program loads meshes from OBJ files and lets you apply basic geometric transformations through a small GUI.

## Requirements
- Python 3
- `numpy`
- `pygame`

## Setup
It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use "venv\\Scripts\\activate"
pip install numpy pygame
```

## Running
Start the application with:

```bash
python Display.py
```

A window will open showing panels for choosing shapes and applying transformations (translation, scaling, rotation, shearing, reflection). You can also import meshes from OBJ files such as the included `Site.obj`.

## Repository Contents
- `Display.py` – main entry point with the graphical interface.
- `DisplayFile.py` – helper class for managing a mesh and its transformations.
- `Mesh.py` – half-edge mesh implementation and OBJ parser.
- `Transformacao.py` – transformation utilities used by the application.
- `Site.obj` – example OBJ model loaded at startup.
