Installation
============

This section describes the necessary steps for installing PyPDEVS.

Dependencies
------------

Basic single core functionality of PyPDEVS requires only cmake. For parallel and distributed simulation, mpi4py is required too.
Python 2.7 is always required, but this should be installed by default on most Linux distributions.

Installation
------------

Installation of PyPDEVS is done using cmake and can be achieved with the following commands, executed from the root of the project::

    mkdir build
    cd build
    cmake ..
    make
    make install

Afterwards, PyPDEVS should be installed. This can easily be checked with the command::

    python -c "import pypdevs"

If this returns without errors, PyPDEVS is sucessfully installed.

Parallel and distributed simulation
-----------------------------------

This requires the installation of mpi4py, which can be quite involved.

First of, an MPI middleware has to be installed, for which I recommend MPICH3.
Due to some non-standard configuration options, it is required to install MPICH manually instead of using the one from the repositories.

You can use either the official installation guide, or follow the steps below.
Just make sure that the correct configuration options are used.

The following commands should work on most systems, just replace the '/home/you' part with a location of your choosing::

    mkdir mpich-build
    mkdir mpich
    base=`pwd`
    cd mpich-build
    wget http://www.mpich.org/static/downloads/3.1.2/mpich-3.1.2.tar.gz
    tar -xvzf mpich-3.1.2.tar.gz
    cd mpich-3.1.2
    ./configure --prefix=$base/mpich --with-device=ch3:sock
    make
    make install
    export PATH=$base/mpich/bin:$PATH

You will probably want to put this final export of PATH to your .bashrc file, to make sure that mpi is found in new terminals too.
After that, make sure that the following command does not cause any errors and simply prints your hostname 4 times::

    mpirun -np 4 hostname

Now you just need to install mpi4py, which is easy if you have MPICH installed correctly::

    mkdir mpi4py
    cd mpi4py
    wget https://pypi.python.org/packages/source/m/mpi4py/mpi4py-1.3.1.tar.gz
    tar -xvzf mpi4py-1.3.1.tar.gz
    cd mpi4py-1.3.1
    python setup.py build
    python setup.py install --user

.. note:: Due to a bug in the mpi4py installation script, MPICH is sometimes not detected automatically. In this case, the 'build' command should be changed to: python setup.py build --mpicc=/location/of/mpich/bin/mpicc

Testing whether or not everything works can be done by making sure that the following command does not throw an error::

    python -c "import mpi4py"
