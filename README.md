kill_dots.py - utility for renaming files named with '.' in SerialEM to EMAN
============================================================

zbenmo@gmail.com (Oren)

The script translates 'tif' files with '.' in their name to the equivalent name with '_'. It also updates the relevant 'mdoc' file that references those files, and fixes the directory reference in the mdoc.

---

You are expected to have **Python 3** installed.

Try:

> python --version

Python 3.8.2

Or even better:

> which python3

To make sure 'python3' is available.

Or:

> module load ..

(to load python 3, if you are using the 'module' Linux framework)

---

Also a package or few are needed. Usually a virtual environment is used to install packages.
For example:

> python3 -m venv env  
> ./env/bin/activate  
> pip install -r requirements.txt

Or similar. Make sure the right python version is used above (if you can use python3 in the command above it will keep you safe).

The environment is now active and the requirements are available.

Remember that the next time you want to use the script, having closed the session above, you need to activate the environment first.

> ./env/bin/activate  

This will also make sure the the right python is used (and that the requirements are available).

---

You then use the utility and it should give you hints about the paramets.

> python kill_dots.py

Usage: kill_dots.py [OPTIONS] COMMAND [ARGS]...

Options:  
  --help  Show this message and exit.

Commands:  
apply  
examine

---

To test the water before doing anything, use for example:

> python kill_dots.py examine  .. ..\NA_001.st.mdoc

folder=..  
33 tif files in ..  
The mdoc file refers to 31 tif files

---

When you are ready, issue a command similar to the following:

> python kill_dots.py apply  .. ..\NA_001.st.mdoc here  

folder=..  
33 tif files in ..  
The mdoc file refers to 31 tif files  
Please verify, for example with 'ls here'
