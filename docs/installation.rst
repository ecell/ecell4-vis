==================
installation
==================

To run ecell4-vis, you have to install these dependencies.

dependencies (Ubuntu Linux)
==================================

- Python
- wxPython
- h5py
- numpy
- vtk

::

   # apt-get update
   # apt-get install python-wxgtk2.8
   # apt-get install python-numpy
   # apt-get install python-h5py
   # apt-get install python-vtk

dependencies (Mac OSX) 
============================

- homebrew

  - wxmac
  - numpy
  - h5py
  - vtk(you need to tap homebrew science)

::

   $ brew install wxmac
   $ brew tap homebrew/science
   $ brew install vtk
   $ sudo easy_install pip
   $ pip install numpy --user
   $ pip install h5py --user
