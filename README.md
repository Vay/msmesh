# ms mesh(multi scale mesh)
geo generator for gmsh, and used by math modeling for multi scale models and standard models.

# about:
* main.py - main file
* meshObjects.py - geometry objects class
* meshOperations - geometry operations class(adding lines, ellipse)

For making geometry:
python main.py input.txt
Mesh generating in temp.geo

for run random object generator use:

python gen.py in output.txt

# install
* python 2.7
* matplotlib (sudo apt-get install python-matplotlib)
* pip (sudo apt-get install python-pip
* shapely (pip install shapely)

# to do
* refactoring
* adding holes
