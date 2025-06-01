# RPCW_TP

This project is part of the RPCW (Representation and Processing of Knowledge on the Web) course. It focuses on creating and managing an ontology-based system for representing and querying data related to space exploration. The system uses RDF and OWL standards to define and query relationships between entities such as astronauts, space missions, celestial bodies, and more.

---

## Table of Contents

1. [Tools Used](#tools-used)
2. [Development Strategy](#development-strategy)
3. [Features](#features)
4. [Pages Overview](#pages-overview)
5. [Dependencies](#dependencies)
6. [How to Run](#how-to-run)
7. [Start Guide](#start-guide)
8. [Authors](#authors)

---

## Tools Used

* **Python 3.10+** — Main language for scripting, data processing, and ontology population.
* **RDFlib** — Python library for manipulating RDF graphs and serializing in Turtle format.
* **Requests** — Python library for making HTTP calls to external APIs (NASA, SpaceX, Wikipedia, etc).
* **Flask** — Web framework for the application's interface.
* **GraphDB** — Triplestore for storing and querying the ontology using SPARQL.
* **HTML/CSS/JavaScript** — For the application’s frontend, with Bootstrap Icons and CodeMirror for query editing.
* **External APIs** — NASA, SpaceX, Wikipedia, JPL Small-Body Database, Solar System OpenData.

## Development Strategy

1. **Ontology Modeling**

   * Analysis of the problem domain (space exploration) and identification of key entities: celestial bodies, space missions, astronauts, agencies, spacecraft, etc.
   * Definition of relevant classes, properties, and relationships, following best modeling practices in OWL/RDF.
   * Implementation of the ontology's base structure in Python, using the RDFlib library to ensure flexibility and easy maintenance.

2. **Automatic Ontology Population**

   * Collection of real data from public APIs (NASA, SpaceX, Wikipedia, JPL Small-Body Database, Solar System OpenData).
   * Conversion of the collected data into ontology instances, automatically creating entities and relationships among them.

3. **Persistence and Querying**

   * Serialization of the ontology into a Turtle (`.ttl`) file to facilitate sharing and reuse.
   * Integration with GraphDB for persistent storage and efficient execution of SPARQL queries.
   * Implementation of SPARQL queries for exploration, validation, and knowledge extraction from the ontology.

4. **Web Application Development**

   * Creation of an intuitive web interface using Flask, allowing users to explore, search, and query the ontology.
   * Implementation of features for importing/exporting ontologies, executing custom SPARQL queries, and visualizing relationships through interactive graphical formats.
   * Use of HTML, CSS, and JavaScript to deliver a modern and responsive user experience.

5. **Testing and Validation**

   * Execution of manual and automated tests to ensure data integrity and the correct functioning of queries.
   * Iterative adjustments to ontology modeling and population scripts based on test results and user feedback.
   * Continuous validation of GraphDB integration and the web interface.

This approach ensures a robust, scalable, and user-friendly solution for representing and exploring knowledge in the space domain.

## Features

- **Ontology Management**:

  - Create and manage an ontology structure for space exploration.
  - Define classes, properties, and relationships between entities.

- **SPARQL Query Execution**:

  - Execute SPARQL queries to retrieve data from the ontology.

- **Graph Visualization**:

  - Generate graph data for visualizing relationships between entities.

- **Entity Search**:

  - Search for entities (e.g., astronauts, missions) by name.

- **Statistics**:
  - Retrieve statistics about the ontology, such as the number of classes, properties, and triples.

### Pages Overview

Below are brief descriptions of each page developed together with a screenshot:

1. **Home Page**  
   Overview of the application and its features.
   ![Home Page](public/home_page.png)

2. **Explore Page**  
   Explore the ontology visually, navigating through classes, properties, and relationships between entities. Not only that but see statistics about the ontology like how many triples it has, etc.
   ![Explore Page](public/explore_page.png)

3. **Entity Page**  
   View detailed information about a specific entity, including its properties, relationships, and associated data within the ontology.
   ![Entity Page](public/entity_page.png)

4. **SPARQL Query Page**  
   Execute SPARQL queries and view results.
   ![SPARQL Query Page](public/sparql_page.png)

5. **Graph Page**  
   Visualize the ontology as an interactive graph, showcasing entities and their relationships.
   ![Graph Page 1](public/graph_page_1.png)
   ![Graph Page 2](public/graph_page_2.png)

6. **Settings Page**  
   Allows users to configure the application's persistence settings. Users can select the ontology file path and choose between using a local file or a GraphDB repository for storing the ontology.
   ![Settings Page](public/settings_page.png)

---

## Dependencies

The project dependencies are listed in the `requirements.txt` file. To install them, run the following command:

```bash
pip install -r requirements.txt
```

## How to Run

To start the application, simply run the `run.py` script using Python:

```bash
python3 run.py
```


## Start Guide

This guide provides a quick sequence of steps to begin configuring and using the application.

1. **Setup**  
   Set up the connection to GraphDB and create the necessary repositories.

2. **Import**  
   Import existing ontologies or create base ontologies to structure the data.

3. **Query**  
   Use SPARQL queries to extract, modify, and manage the stored data.

4. **Visualize**  
   Explore the data and its relationships through interactive graphs to facilitate analysis.

It is essential to strictly follow steps 1 and 2 to ensure proper and effective setup of the application's working environment.


## Authors

- [**João Coelho: PG55954**](https://github.com/JoaoCoelho2003)
- [**Mariana Silva: PG55980**](https://github.com/MarianaSilva659)
- [**José Rodrigues: PG55969**](https://github.com/FilipeR13)
