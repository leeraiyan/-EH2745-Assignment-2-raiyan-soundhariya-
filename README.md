# EH2745 Assignment 2

A [web application](http://butterytoucan.eu.pythonanywhere.com/) that runs simulations on a PandaPower network, and performs Supervised and Unsupervised Machine Learning on the resulting time series dataset.

## Features
* Fully-functional and intuitive [web application](http://butterytoucan.eu.pythonanywhere.com/)
* Allows up to seven selectable cases for simulations
* Stores data in a sqlite database
* Displays time series data in a table
* Plots the results in several graphs
* Provides a dashboard for viewing the results
* Catches errors gracefully

## Installation Instructions
1. Clone this repository
2. Use Python 3.11 to run `pip install -r requirements.txt` (A virtual environment is highly recommended)
3. Use Python 3.11 to run `python run.py` (NOTE: for convenience, use the [web application](http://butterytoucan.eu.pythonanywhere.com/) instead!)

![Main UI](docs/images/ui.png)

![Results Page](docs/images/results.png)

## Python Files Included
Project is created with:
* `CIMXMLParser.py`: Contains the class `CIM_XML_parser`
* `PandaPowerManager.py`: Contains the class `PandaPowerWriter`
* `gui.py`: Contains GUI-related information

## Class Information
* AgentKMeans class represents an implementation of the K-means clustering algorithm.
  - Constructor: __init__(self) initializes the class instance.
  - Methods:
  -   `euclidean_distance(self, x1, x2)`: Calculates the Euclidean distance between two points x1 and x2.
  -   `calc_mean(self, data, types, k)`: Calculates the mean of the number of data points based on the provided data, types, and the number of centroids k.
  -   `calc_diff(self, x1, x2)`: Calculates the difference between the previous and new mean values x1 and x2.
  -   `calc_cost(self, data, means, types)`: Calculates the cost function based on the provided data, means, and types.
  -   `kmeans_clustering(self, data, init_guess=3)`: Performs K-means clustering on the given data using the specified number of initial guesses init_guess. Returns the number of means, the cost function for the best value, the mean values, and the final cluster assignments.

* `PandaPowerWriter` class is initialised by passing the outputs of the `CIM_XML_parser.run()` function. It handles the conversion of all equipment information into the creation format of a PandaPower network instance and its various equipment. It contains the following methods:
  - `__init__(self, dictEquipmentIDtoType, dictEquipment)`: The constructor method initializes the PandaPowerWriter object and sets the equipment ID-to-type dictionary and the equipment dictionary.
  - `initialiseNetwork(self)`: This method creates an empty pandapower network and calls other methods to initialize different components of the network, such as buses, lines, switches, loads, transformers, generators, shunts, and wards.
  - `getVoltageLevel(self, nodeID)`: Returns the voltage level associated with a node as a float.
  - `toHTML(self, htmlFileName)`: Outputs a HTML file that represents the pandapower network.
  - `getAssociatedSubstation(self, nodeID)`: Returns the name of the substation associated with a given equipment.
  - `getAssociatedBus(self, terminalID)`: Returns the ID of the connectivity node that corresponds to a particular terminal.
  - `getLineMaxCurrent(self, lineID)`: Returns the maximum current limit of a line as a float.
  - `initialiseBuses(self, newBusID)`: Creates the buses in the pandapower network. If newBusID is provided, it creates a new bus with the given ID.
  - `initialiseLines(self)`: Creates the lines in the pandapower network based on the equipment data.
  - `initialiseSwitches(self)`: Creates the switches in the pandapower network based on the equipment data.
  - `initialiseTransformer(self)`: Creates transformer objects in the pandapower network based on the equipment data.
  - `initialiseLoads(self)`: Creates load objects in the pandapower network based on the equipment data.
  - `initialiseStaticGen(self)`: Creates static generator objects in the pandapower network based on the equipment data.
  - `initialiseMachines(self)`: Creates generator objects in the pandapower network based on the equipment data.
  - `initialiseShunt(self)`: Creates linear shunt objects in the pandapower network based on the equipment data.
  - `initialiseWard(self)`: Creates ward objects in the pandapower network based on the equipment data.




