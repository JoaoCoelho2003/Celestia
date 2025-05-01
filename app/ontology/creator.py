import os
import json
import requests
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD, OWL

class OntologyCreator:
    def __init__(self, output_path="ontology/space.ttl"):
        self.output_path = output_path
        self.g = Graph()
        
        
        self.SPACE = Namespace("http://www.semanticweb.org/ontologies/space")
        self.g.bind("space", self.SPACE)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    def create_ontology_structure(self):
        """Create the basic structure of the space ontology"""
        
        celestial_body = self.SPACE.CelestialBody
        planet = self.SPACE.Planet
        star = self.SPACE.Star
        moon = self.SPACE.Moon
        asteroid = self.SPACE.Asteroid
        comet = self.SPACE.Comet
        galaxy = self.SPACE.Galaxy
        
        space_mission = self.SPACE.SpaceMission
        astronaut = self.SPACE.Astronaut
        space_agency = self.SPACE.SpaceAgency
        spacecraft = self.SPACE.Spacecraft
        
        
        self.g.add((celestial_body, RDF.type, OWL.Class))
        self.g.add((celestial_body, RDFS.label, Literal("Celestial Body", lang="en")))
        
        
        for cls in [planet, star, moon, asteroid, comet, galaxy]:
            self.g.add((cls, RDF.type, OWL.Class))
            self.g.add((cls, RDFS.subClassOf, celestial_body))
        
        
        self.g.add((planet, RDFS.label, Literal("Planet", lang="en")))
        self.g.add((star, RDFS.label, Literal("Star", lang="en")))
        self.g.add((moon, RDFS.label, Literal("Moon", lang="en")))
        self.g.add((asteroid, RDFS.label, Literal("Asteroid", lang="en")))
        self.g.add((comet, RDFS.label, Literal("Comet", lang="en")))
        self.g.add((galaxy, RDFS.label, Literal("Galaxy", lang="en")))
        
        
        self.g.add((space_mission, RDF.type, OWL.Class))
        self.g.add((space_mission, RDFS.label, Literal("Space Mission", lang="en")))
        
        self.g.add((astronaut, RDF.type, OWL.Class))
        self.g.add((astronaut, RDFS.label, Literal("Astronaut", lang="en")))
        
        self.g.add((space_agency, RDF.type, OWL.Class))
        self.g.add((space_agency, RDFS.label, Literal("Space Agency", lang="en")))
        
        self.g.add((spacecraft, RDF.type, OWL.Class))
        self.g.add((spacecraft, RDFS.label, Literal("Spacecraft", lang="en")))
        
        
        orbits = self.SPACE.orbits
        has_moon = self.SPACE.hasMoon
        belongs_to = self.SPACE.belongsTo
        launched_by = self.SPACE.launchedBy
        participated_in = self.SPACE.participatedIn
        has_astronaut = self.SPACE.hasAstronaut
        uses_spacecraft = self.SPACE.usesSpacecraft
        
        
        self.g.add((orbits, RDF.type, OWL.ObjectProperty))
        self.g.add((orbits, RDFS.label, Literal("Orbits", lang="en")))
        self.g.add((orbits, RDFS.domain, celestial_body))
        self.g.add((orbits, RDFS.range, celestial_body))
        
        self.g.add((has_moon, RDF.type, OWL.ObjectProperty))
        self.g.add((has_moon, RDFS.label, Literal("Has Moon", lang="en")))
        self.g.add((has_moon, RDFS.domain, planet))
        self.g.add((has_moon, RDFS.range, moon))
        
        self.g.add((belongs_to, RDF.type, OWL.ObjectProperty))
        self.g.add((belongs_to, RDFS.label, Literal("Belongs To", lang="en")))
        self.g.add((belongs_to, RDFS.domain, celestial_body))
        self.g.add((belongs_to, RDFS.range, galaxy))
        
        self.g.add((launched_by, RDF.type, OWL.ObjectProperty))
        self.g.add((launched_by, RDFS.label, Literal("Launched By", lang="en")))
        self.g.add((launched_by, RDFS.domain, space_mission))
        self.g.add((launched_by, RDFS.range, space_agency))
        
        self.g.add((participated_in, RDF.type, OWL.ObjectProperty))
        self.g.add((participated_in, RDFS.label, Literal("Participated In", lang="en")))
        self.g.add((participated_in, RDFS.domain, astronaut))
        self.g.add((participated_in, RDFS.range, space_mission))
        
        self.g.add((has_astronaut, RDF.type, OWL.ObjectProperty))
        self.g.add((has_astronaut, RDFS.label, Literal("Has Astronaut", lang="en")))
        self.g.add((has_astronaut, RDFS.domain, space_mission))
        self.g.add((has_astronaut, RDFS.range, astronaut))
        
        self.g.add((uses_spacecraft, RDF.type, OWL.ObjectProperty))
        self.g.add((uses_spacecraft, RDFS.label, Literal("Uses Spacecraft", lang="en")))
        self.g.add((uses_spacecraft, RDFS.domain, space_mission))
        self.g.add((uses_spacecraft, RDFS.range, spacecraft))
        
        
        name = self.SPACE.name
        mass = self.SPACE.mass
        radius = self.SPACE.radius
        distance_from_sun = self.SPACE.distanceFromSun
        orbital_period = self.SPACE.orbitalPeriod
        launch_date = self.SPACE.launchDate
        end_date = self.SPACE.endDate
        description = self.SPACE.description
        
        
        self.g.add((name, RDF.type, OWL.DatatypeProperty))
        self.g.add((name, RDFS.label, Literal("Name", lang="en")))
        self.g.add((name, RDFS.range, XSD.string))
        
        self.g.add((mass, RDF.type, OWL.DatatypeProperty))
        self.g.add((mass, RDFS.label, Literal("Mass", lang="en")))
        self.g.add((mass, RDFS.domain, celestial_body))
        self.g.add((mass, RDFS.range, XSD.decimal))
        
        self.g.add((radius, RDF.type, OWL.DatatypeProperty))
        self.g.add((radius, RDFS.label, Literal("Radius", lang="en")))
        self.g.add((radius, RDFS.domain, celestial_body))
        self.g.add((radius, RDFS.range, XSD.decimal))
        
        self.g.add((distance_from_sun, RDF.type, OWL.DatatypeProperty))
        self.g.add((distance_from_sun, RDFS.label, Literal("Distance from Sun", lang="en")))
        self.g.add((distance_from_sun, RDFS.domain, celestial_body))
        self.g.add((distance_from_sun, RDFS.range, XSD.decimal))
        
        self.g.add((orbital_period, RDF.type, OWL.DatatypeProperty))
        self.g.add((orbital_period, RDFS.label, Literal("Orbital Period", lang="en")))
        self.g.add((orbital_period, RDFS.domain, celestial_body))
        self.g.add((orbital_period, RDFS.range, XSD.decimal))
        
        self.g.add((launch_date, RDF.type, OWL.DatatypeProperty))
        self.g.add((launch_date, RDFS.label, Literal("Launch Date", lang="en")))
        self.g.add((launch_date, RDFS.domain, space_mission))
        self.g.add((launch_date, RDFS.range, XSD.date))
        
        self.g.add((end_date, RDF.type, OWL.DatatypeProperty))
        self.g.add((end_date, RDFS.label, Literal("End Date", lang="en")))
        self.g.add((end_date, RDFS.domain, space_mission))
        self.g.add((end_date, RDFS.range, XSD.date))
        
        self.g.add((description, RDF.type, OWL.DatatypeProperty))
        self.g.add((description, RDFS.label, Literal("Description", lang="en")))
        self.g.add((description, RDFS.range, XSD.string))
    
    def fetch_solar_system_data(self):
        """Fetch data about the solar system from the Solar System OpenData API"""
        try:
            
            response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/")
            if response.status_code == 200:
                data = response.json()
                
                
                sun_uri = self.SPACE.Sun
                self.g.add((sun_uri, RDF.type, self.SPACE.Star))
                self.g.add((sun_uri, self.SPACE.name, Literal("Sun", datatype=XSD.string)))
                self.g.add((sun_uri, self.SPACE.mass, Literal(1.989e30, datatype=XSD.decimal)))
                self.g.add((sun_uri, self.SPACE.radius, Literal(696340, datatype=XSD.decimal)))
                self.g.add((sun_uri, self.SPACE.description, Literal("The Sun is the star at the center of the Solar System.", datatype=XSD.string)))
                
                
                milky_way_uri = self.SPACE.MilkyWay
                self.g.add((milky_way_uri, RDF.type, self.SPACE.Galaxy))
                self.g.add((milky_way_uri, self.SPACE.name, Literal("Milky Way", datatype=XSD.string)))
                self.g.add((milky_way_uri, self.SPACE.description, Literal("The Milky Way is the galaxy that contains our Solar System.", datatype=XSD.string)))
                
                
                self.g.add((sun_uri, self.SPACE.belongsTo, milky_way_uri))
                
                
                for body in data['bodies']:
                    if body['isPlanet']:
                        
                        planet_uri = self.SPACE[body['id'].capitalize()]
                        self.g.add((planet_uri, RDF.type, self.SPACE.Planet))
                        self.g.add((planet_uri, self.SPACE.name, Literal(body['englishName'], datatype=XSD.string)))
                        
                        
                        if body.get('mass'):
                            mass_value = body['mass'].get('massValue', 0)
                            mass_exp = body['mass'].get('massExponent', 0)
                            mass = mass_value * (10 ** mass_exp)
                            self.g.add((planet_uri, self.SPACE.mass, Literal(mass, datatype=XSD.decimal)))
                        
                        if body.get('meanRadius'):
                            self.g.add((planet_uri, self.SPACE.radius, Literal(body['meanRadius'], datatype=XSD.decimal)))
                        
                        if body.get('semimajorAxis'):
                            self.g.add((planet_uri, self.SPACE.distanceFromSun, Literal(body['semimajorAxis'], datatype=XSD.decimal)))
                        
                        if body.get('sideralOrbit'):
                            self.g.add((planet_uri, self.SPACE.orbitalPeriod, Literal(body['sideralOrbit'], datatype=XSD.decimal)))
                        
                        
                        self.g.add((planet_uri, self.SPACE.orbits, sun_uri))
                        self.g.add((planet_uri, self.SPACE.belongsTo, milky_way_uri))
                        
                        
                        description = f"{body['englishName']} is a planet in our Solar System."
                        self.g.add((planet_uri, self.SPACE.description, Literal(description, datatype=XSD.string)))
                
                
                for body in data['bodies']:
                    if body.get('aroundPlanet') and not body['isPlanet']:
                        
                        planet_id = body['aroundPlanet']['planet']
                        planet_uri = None
                        
                        
                        for s, p, o in self.g.triples((None, RDF.type, self.SPACE.Planet)):
                            planet_name = list(self.g.objects(s, self.SPACE.name))[0].value
                            if planet_name.lower() == body['aroundPlanet']['planet'].lower():
                                planet_uri = s
                                break
                        
                        if planet_uri:
                            
                            moon_uri = self.SPACE[body['id'].capitalize()]
                            self.g.add((moon_uri, RDF.type, self.SPACE.Moon))
                            self.g.add((moon_uri, self.SPACE.name, Literal(body['englishName'], datatype=XSD.string)))
                            
                            
                            if body.get('mass'):
                                mass_value = body['mass'].get('massValue', 0)
                                mass_exp = body['mass'].get('massExponent', 0)
                                mass = mass_value * (10 ** mass_exp)
                                self.g.add((moon_uri, self.SPACE.mass, Literal(mass, datatype=XSD.decimal)))
                            
                            if body.get('meanRadius'):
                                self.g.add((moon_uri, self.SPACE.radius, Literal(body['meanRadius'], datatype=XSD.decimal)))
                            
                            
                            self.g.add((moon_uri, self.SPACE.orbits, planet_uri))
                            self.g.add((planet_uri, self.SPACE.hasMoon, moon_uri))
                            self.g.add((moon_uri, self.SPACE.belongsTo, milky_way_uri))
                            
                            
                            description = f"{body['englishName']} is a moon of {list(self.g.objects(planet_uri, self.SPACE.name))[0].value}."
                            self.g.add((moon_uri, self.SPACE.description, Literal(description, datatype=XSD.string)))
                
                print(f"Added data for the Solar System with {len([s for s, p, o in self.g.triples((None, RDF.type, self.SPACE.Planet))])} planets and {len([s for s, p, o in self.g.triples((None, RDF.type, self.SPACE.Moon))])} moons.")
            else:
                print(f"Failed to fetch solar system data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching solar system data: {e}")
    
    def fetch_spacex_data(self):
        """Fetch data about SpaceX missions"""
        try:
            
            response = requests.get("https://api.spacexdata.com/v4/launches")
            if response.status_code == 200:
                launches = response.json()
                
                
                spacex_uri = self.SPACE.SpaceX
                self.g.add((spacex_uri, RDF.type, self.SPACE.SpaceAgency))
                self.g.add((spacex_uri, self.SPACE.name, Literal("SpaceX", datatype=XSD.string)))
                self.g.add((spacex_uri, self.SPACE.description, Literal("Space Exploration Technologies Corp. is an American spacecraft manufacturer, space launch provider, and satellite communications company.", datatype=XSD.string)))
                
                
                for launch in launches[:20]:
                    
                    mission_uri = self.SPACE[f"Mission_{launch['id']}"]
                    self.g.add((mission_uri, RDF.type, self.SPACE.SpaceMission))
                    self.g.add((mission_uri, self.SPACE.name, Literal(launch['name'], datatype=XSD.string)))
                    
                    
                    if launch.get('date_utc'):
                        launch_date = launch['date_utc'].split('T')[0]  
                        self.g.add((mission_uri, self.SPACE.launchDate, Literal(launch_date, datatype=XSD.date)))
                    
                    
                    description = launch.get('details', f"SpaceX mission {launch['name']}")
                    self.g.add((mission_uri, self.SPACE.description, Literal(description, datatype=XSD.string)))
                    
                    
                    self.g.add((mission_uri, self.SPACE.launchedBy, spacex_uri))
                    
                    
                    if launch.get('rocket'):
                        
                        rocket_response = requests.get(f"https://api.spacexdata.com/v4/rockets/{launch['rocket']}")
                        if rocket_response.status_code == 200:
                            rocket_data = rocket_response.json()
                            rocket_uri = self.SPACE[f"Spacecraft_{rocket_data['id']}"]
                            
                            
                            if (rocket_uri, RDF.type, self.SPACE.Spacecraft) not in self.g:
                                self.g.add((rocket_uri, RDF.type, self.SPACE.Spacecraft))
                                self.g.add((rocket_uri, self.SPACE.name, Literal(rocket_data['name'], datatype=XSD.string)))
                                self.g.add((rocket_uri, self.SPACE.description, Literal(rocket_data.get('description', f"SpaceX rocket {rocket_data['name']}"), datatype=XSD.string)))
                            
                            
                            self.g.add((mission_uri, self.SPACE.usesSpacecraft, rocket_uri))
                
                print(f"Added data for {len(launches[:20])} SpaceX missions.")
            else:
                print(f"Failed to fetch SpaceX data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching SpaceX data: {e}")
    
    def fetch_nasa_data(self):
        """Fetch data about NASA astronauts and missions"""
        try:
            
            nasa_uri = self.SPACE.NASA
            self.g.add((nasa_uri, RDF.type, self.SPACE.SpaceAgency))
            self.g.add((nasa_uri, self.SPACE.name, Literal("NASA", datatype=XSD.string)))
            self.g.add((nasa_uri, self.SPACE.description, Literal("The National Aeronautics and Space Administration is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research.", datatype=XSD.string)))
            
            
            missions = [
                {
                    "id": "Apollo11",
                    "name": "Apollo 11",
                    "launch_date": "1969-07-16",
                    "end_date": "1969-07-24",
                    "description": "The first crewed mission to land on the Moon.",
                    "spacecraft": "Saturn V",
                    "astronauts": ["Neil Armstrong", "Buzz Aldrin", "Michael Collins"]
                },
                {
                    "id": "Voyager1",
                    "name": "Voyager 1",
                    "launch_date": "1977-09-05",
                    "description": "An interstellar mission to study the outer Solar System and beyond.",
                    "spacecraft": "Voyager 1 Spacecraft"
                },
                {
                    "id": "Hubble",
                    "name": "Hubble Space Telescope",
                    "launch_date": "1990-04-24",
                    "description": "A space telescope that has made numerous important observations since its launch.",
                    "spacecraft": "Space Shuttle Discovery"
                },
                {
                    "id": "Curiosity",
                    "name": "Mars Science Laboratory (Curiosity)",
                    "launch_date": "2011-11-26",
                    "description": "A mission to land and operate a rover named Curiosity on the surface of Mars.",
                    "spacecraft": "Atlas V"
                },
                {
                    "id": "JamesWebb",
                    "name": "James Webb Space Telescope",
                    "launch_date": "2021-12-25",
                    "description": "An infrared space telescope designed to be the successor to the Hubble Space Telescope.",
                    "spacecraft": "Ariane 5"
                }
            ]
            
            for mission in missions:
                mission_uri = self.SPACE[mission["id"]]
                self.g.add((mission_uri, RDF.type, self.SPACE.SpaceMission))
                self.g.add((mission_uri, self.SPACE.name, Literal(mission["name"], datatype=XSD.string)))
                self.g.add((mission_uri, self.SPACE.launchDate, Literal(mission["launch_date"], datatype=XSD.date)))
                
                if mission.get("end_date"):
                    self.g.add((mission_uri, self.SPACE.endDate, Literal(mission["end_date"], datatype=XSD.date)))
                
                self.g.add((mission_uri, self.SPACE.description, Literal(mission["description"], datatype=XSD.string)))
                self.g.add((mission_uri, self.SPACE.launchedBy, nasa_uri))
                
                
                spacecraft_uri = self.SPACE[f"Spacecraft_{mission['id']}"]
                self.g.add((spacecraft_uri, RDF.type, self.SPACE.Spacecraft))
                self.g.add((spacecraft_uri, self.SPACE.name, Literal(mission["spacecraft"], datatype=XSD.string)))
                self.g.add((mission_uri, self.SPACE.usesSpacecraft, spacecraft_uri))
                
                
                if mission.get("astronauts"):
                    for astronaut_name in mission["astronauts"]:
                        astronaut_id = astronaut_name.replace(" ", "")
                        astronaut_uri = self.SPACE[astronaut_id]
                        
                        
                        if (astronaut_uri, RDF.type, self.SPACE.Astronaut) not in self.g:
                            self.g.add((astronaut_uri, RDF.type, self.SPACE.Astronaut))
                            self.g.add((astronaut_uri, self.SPACE.name, Literal(astronaut_name, datatype=XSD.string)))
                            self.g.add((astronaut_uri, self.SPACE.description, Literal(f"{astronaut_name} is a NASA astronaut.", datatype=XSD.string)))
                        
                        
                        self.g.add((astronaut_uri, self.SPACE.participatedIn, mission_uri))
                        self.g.add((mission_uri, self.SPACE.hasAstronaut, astronaut_uri))
            
            print(f"Added data for {len(missions)} NASA missions.")
        except Exception as e:
            print(f"Error adding NASA data: {e}")
    
    def save_ontology(self):
        """Save the ontology to a Turtle file"""
        try:
            self.g.serialize(destination=self.output_path, format="turtle")
            print(f"Ontology saved to {self.output_path}")
            return True
        except Exception as e:
            print(f"Error saving ontology: {e}")
            return False


if __name__ == "__main__":
    creator = OntologyCreator()
    creator.create_ontology_structure()
    creator.fetch_solar_system_data()
    creator.fetch_spacex_data()
    creator.fetch_nasa_data()
    creator.save_ontology()
    
    
    print(f"Total triples in the ontology: {len(creator.g)}")
    print(f"Number of classes: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.Class))])}")
    print(f"Number of object properties: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.ObjectProperty))])}")
    print(f"Number of data properties: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.DatatypeProperty))])}")