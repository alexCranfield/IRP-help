# 📝 Getting Started

This repo aims to help you get started with setting up a suitable project space for your project. If you're able to see this file, you're off to a good start!

## Recommendations

Note: If you prefer to work another way, feel free to do so! This is just a guide to help if you're unsure how to get going.
- **Install Python.**
  - *I would recommend either 3.9 or 3.10 due to their fairly recent release date and available support.*
  - *If you prefer to work in another language (Rust, R, whatever) feel free to do so! I may struggle to help you with some of them.*
- **Set up and use a dependency manager.**
  - *I'm going to use `miniconda` here, but feel free to use others (`pip`, `poetry`, `mamba`, etc...)*
- **Get required packages installed.**
  - *I'm hoping i can help here by providing my packages, but some will depend on the system you're using.*


## Installing Python


## Installing `miniconda`
`miniconda` (or the full `anaconda` if you'd like) can be installed from [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Follow the instructions provided by the link. This should set-up everything you need for getting a virtual environment (`venv`) created. You may need to restart your system for changes to take effect.

### Getting set-up (Creating a `venv`)
I'm going to use a virtual environment (`venv`) here to develop my code. I'd recommended using a `venv` in development because it provides a self-contained environment for your project with its own Python interpreter and installed packages. This means that any changes you make to the Python environment in one project will not affect other projects or the system-level Python installation. Using a virtual environment can help ensure that your project is isolated, reproducible, portable, secure, and easy to manage.

Once you've installed `conda` (through `miniconda` or `anaconda`) - you can create a `venv` by running:

```bash
conda create --name IRP-env python=3.10
```

This will create a new `conda` virtual environment using Python 3.10. There'll be a lot of packages installed following a confirmation from the user (done so by typing `y` for yes). Feel free to tweak the name and version as necessary.

With the virutal environment (`venv`) created, we now need to activate it before we go any further.
```bash
conda activate IRP-env
```

You should see this change reflected in your terminal by having the `venv` title shown in brackets to the left of your shell.

```bash
(base) alex@spire test % conda activate IRP-env
(IRP-env) alex@spire test % 
```

For more information regarding `conda`, check out [this cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).


### Installing Packages
To make our lives easier, we can make use of existing code in the project by installing packages. There's a few I'd recommend for data processing.

To simplify matters, I've created a `requirements.txt` file that contains packages and versions I've installed for these examples.

To set up your `venv` with these packages, run:
```bash
(IRP-env) alex@spire test % conda install --file requirements.txt
```
☕️ Note that this may take a little while (5-10mins), go grab a coffee or something whilst it runs!

If you want to install some new packages, say `pandas` or `polars`, run:
```bash
(IRP-env) alex@spire test % conda install <package_name>
```
Most packages will have installation instructions available online, for an example see [`pandas` on PyPI](https://pypi.org/project/pandas/). You may need to specify a specific channel to install from, for instance, or even a specific version number. [An example of this](https://pypi.org/project/cfgrib/) is `cfgrib` - which is a package containing an engine used to read weather (GRIB) files.

When you run an install command, `conda` will automatically resolve dependencies. It will provide a list of packages that need changing, installing, or removing in order for the `venv` to operate. It's not a perfect system, but it will work most of the time. For instance, installing `pandas`, which relies on a lot of other packages, such as `numpy`, will automatically install these required packages for us - very handy!

## Setting up for ML
Some AI/ML packages require a little more effort to get working, especially if you want to make use of hardware acceleration through things like GPUs or TPUs.

This is going to depend on the system you're using. I've linked some resources below for each operating system:

## Setting up for using jupyter
I've used Jupyter notebooks quite a bit here. They're really not good for production code, but for development they're fantastic! (At least I think so). To get set-up for this, we'll need to set up an iPython kernel (`ipykernel`) within our `venv`.

The `ipykernel` specifically is the kernel used for running Python code in Jupyter notebooks. It provides a communication protocol between the Jupyter notebook and the kernel, which allows the notebook to send code to the kernel for execution, and receive output from the kernel. This enables users to interactively work with Python code, visualize data, and produce rich, interactive output in a web-based environment. 

To set-up an `ipykernel` in our `venv`, we can run the following (assuming you've installed the packages from the `requirements.txt` file):

```bash
python -m ipykernel install --user --name IRP-env
```
This should give you a ipython kernel that you can use in your notebooks, allowing you to execute code through the `venv` created earlier.

