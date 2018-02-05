# ms mesh(multi scale mesh)
geo generator for gmsh for reduced order multiscale models and standard models.

# about:
msmesh was written on Python. It consists of 4 main parts:
* module for main geometrical objects,
* module for geometrical operations,
* main module for processing of input data and generating geometry,
* module for generating random input data. 

Module for main geometrical objects consists of following classes:
* Class Base — parent class for other classes
* Class Point — class point that includes the functions of work with a a point
* Class Line — class line
* Class Surface — surface class
* Class PhysicalLine — class physical line
* Class PhysicalSurface — class physical surface

Module for main geometrical operations includes operations of intersections and additions of objects and additional functions for them. 

Main module opens the input file and generates the geometry.

# running
The program works in console mode with the input file that should be set at the start. For making geometry start the program in the console using the command:
> python main.py input.txt

The output file as a geometry file is generated in temp.geo.

input.txt file is used as the input file and looks as follows:

mesh 1 5 5 10 10 1 2 3 4
line 13.3333 13.3333 39.3955 18.5295 5
line 23.3333 18.3333 20.3333 23.5295 5
ellipse 28 28 15 15 0 5 6

With specified input file we get this grid with a coarse scale and an ability to generate a grid with a smaller scale.
![alt text](https://github.com/Vay/msmesh/blob/master/example.png "example")

The picture below describes the parameters the we can specify.
![alt text](https://github.com/Vay/msmesh/blob/master/mesh-params.png "example")
for run random object generator use:

> python gen.py in output.txt


# library
It is also possible to use the program as a library for program calls using commands:
> addLine()
> addSurface()
> addCircle()

# install
The following programs are required to use the program:
* python 2.7
* matplotlib (sudo apt-get install python-matplotlib)
* pip (sudo apt-get install python-pip
* shapely (pip install shapely)

# to do
* refactoring
* adding holes
