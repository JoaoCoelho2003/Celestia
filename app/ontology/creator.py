import os
import requests
from datetime import datetime
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD, OWL

class OntologyCreator:
    def __init__(self, output_path="ontology/space.ttl", use_graphdb=False, graphdb_url="http://localhost:7200/repositories/space"):
        self.output_path = output_path
        self.use_graphdb = use_graphdb
        self.graphdb_url = graphdb_url
        self.g = Graph()
        
        
        self.SPACE = Namespace("http://www.semanticweb.org/ontologies/space#")
        self.g.bind("space", self.SPACE)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        
        
        if not use_graphdb:
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
                
                
                sun_response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/soleil")
                if sun_response.status_code == 200:
                    sun_data = sun_response.json()
                    if sun_data.get('mass'):
                        mass_value = sun_data['mass'].get('massValue', 0)
                        mass_exp = sun_data['mass'].get('massExponent', 0)
                        mass = mass_value * (10 ** mass_exp)
                        self.g.add((sun_uri, self.SPACE.mass, Literal(mass, datatype=XSD.decimal)))
                    
                    if sun_data.get('meanRadius'):
                        self.g.add((sun_uri, self.SPACE.radius, Literal(sun_data['meanRadius'], datatype=XSD.decimal)))
                    
                    
                    wiki_response = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/Sun")
                    if wiki_response.status_code == 200:
                        wiki_data = wiki_response.json()
                        self.g.add((sun_uri, self.SPACE.description, Literal(wiki_data.get('extract', "The Sun is the star at the center of the Solar System."), datatype=XSD.string)))
                
                
                milky_way_uri = self.SPACE.MilkyWay
                self.g.add((milky_way_uri, RDF.type, self.SPACE.Galaxy))
                self.g.add((milky_way_uri, self.SPACE.name, Literal("Milky Way", datatype=XSD.string)))
                
                wiki_response = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/Milky_Way")
                if wiki_response.status_code == 200:
                    wiki_data = wiki_response.json()
                    self.g.add((milky_way_uri, self.SPACE.description, Literal(wiki_data.get('extract', "The Milky Way is the galaxy that contains our Solar System."), datatype=XSD.string)))
                
                
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
                        
                        
                        wiki_response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{body['englishName']}")
                        if wiki_response.status_code == 200:
                            wiki_data = wiki_response.json()
                            self.g.add((planet_uri, self.SPACE.description, Literal(wiki_data.get('extract', f"{body['englishName']} is a planet in our Solar System."), datatype=XSD.string)))
                
                
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
                            
                            
                            try:
                                wiki_response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{body['englishName']}")
                                if wiki_response.status_code == 200:
                                    wiki_data = wiki_response.json()
                                    self.g.add((moon_uri, self.SPACE.description, Literal(wiki_data.get('extract', f"{body['englishName']} is a moon of {list(self.g.objects(planet_uri, self.SPACE.name))[0].value}."), datatype=XSD.string)))
                            except:
                                
                                self.g.add((moon_uri, self.SPACE.description, Literal(f"{body['englishName']} is a moon of {list(self.g.objects(planet_uri, self.SPACE.name))[0].value}.", datatype=XSD.string)))
                
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
                
                
                company_response = requests.get("https://api.spacexdata.com/v4/company")
                if company_response.status_code == 200:
                    company_data = company_response.json()
                    self.g.add((spacex_uri, self.SPACE.description, Literal(company_data.get('summary', "Space Exploration Technologies Corp. is an American spacecraft manufacturer, space launch provider, and satellite communications company."), datatype=XSD.string)))
                
                
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
                    
                    
                    if launch.get('crew') and len(launch['crew']) > 0:
                        for crew_id in launch['crew']:
                            
                            crew_response = requests.get(f"https://api.spacexdata.com/v4/crew/{crew_id}")
                            if crew_response.status_code == 200:
                                crew_data = crew_response.json()
                                astronaut_uri = self.SPACE[f"Astronaut_{crew_data['id']}"]
                                
                                
                                if (astronaut_uri, RDF.type, self.SPACE.Astronaut) not in self.g:
                                    self.g.add((astronaut_uri, RDF.type, self.SPACE.Astronaut))
                                    self.g.add((astronaut_uri, self.SPACE.name, Literal(crew_data['name'], datatype=XSD.string)))
                                    self.g.add((astronaut_uri, self.SPACE.description, Literal(f"{crew_data['name']} is an astronaut who has flown on SpaceX missions.", datatype=XSD.string)))
                                
                                
                                self.g.add((astronaut_uri, self.SPACE.participatedIn, mission_uri))
                                self.g.add((mission_uri, self.SPACE.hasAstronaut, astronaut_uri))
                
                print(f"Added data for {len(launches[:20])} SpaceX missions.")
            else:
                print(f"Failed to fetch SpaceX data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching SpaceX data: {e}")
    
    def fetch_nasa_data(self):
        """Fetch data about NASA from NASA APIs"""
        try:
            
            nasa_uri = self.SPACE.NASA
            self.g.add((nasa_uri, RDF.type, self.SPACE.SpaceAgency))
            self.g.add((nasa_uri, self.SPACE.name, Literal("NASA", datatype=XSD.string)))
            
            
            wiki_response = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/NASA")
            if wiki_response.status_code == 200:
                wiki_data = wiki_response.json()
                self.g.add((nasa_uri, self.SPACE.description, Literal(wiki_data.get('extract', "The National Aeronautics and Space Administration is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research."), datatype=XSD.string)))
            
            
            nasa_api_url = "https://images-api.nasa.gov/search?q=mission&media_type=image"
            response = requests.get(nasa_api_url)
            
            if response.status_code == 200:
                data = response.json()
                missions_added = 0
                
                
                for item in data.get('collection', {}).get('items', [])[:10]:
                    if 'data' in item and len(item['data']) > 0:
                        mission_data = item['data'][0]
                        
                        
                        if 'title' not in mission_data:
                            continue
                        
                        mission_id = mission_data['nasa_id'].replace(' ', '_')
                        mission_uri = self.SPACE[f"NASA_Mission_{mission_id}"]
                        
                        
                        self.g.add((mission_uri, RDF.type, self.SPACE.SpaceMission))
                        self.g.add((mission_uri, self.SPACE.name, Literal(mission_data['title'], datatype=XSD.string)))
                        
                        
                        if 'description' in mission_data:
                            self.g.add((mission_uri, self.SPACE.description, Literal(mission_data['description'], datatype=XSD.string)))
                        
                        
                        if 'date_created' in mission_data:
                            try:
                                date_obj = datetime.strptime(mission_data['date_created'], "%Y-%m-%dT%H:%M:%SZ")
                                date_str = date_obj.strftime("%Y-%m-%d")
                                self.g.add((mission_uri, self.SPACE.launchDate, Literal(date_str, datatype=XSD.date)))
                            except:
                                pass
                        
                        
                        self.g.add((mission_uri, self.SPACE.launchedBy, nasa_uri))
                        
                        missions_added += 1
                
                
                astronauts_url = "http://api.open-notify.org/astros.json"
                astro_response = requests.get(astronauts_url)
                
                if astro_response.status_code == 200:
                    astro_data = astro_response.json()
                    
                    for person in astro_data.get('people', []):
                        if person.get('craft') and person.get('name'):
                            
                            astronaut_id = person['name'].replace(' ', '_')
                            astronaut_uri = self.SPACE[f"Astronaut_{astronaut_id}"]
                            
                            
                            self.g.add((astronaut_uri, RDF.type, self.SPACE.Astronaut))
                            self.g.add((astronaut_uri, self.SPACE.name, Literal(person['name'], datatype=XSD.string)))
                            self.g.add((astronaut_uri, self.SPACE.description, Literal(f"{person['name']} is an astronaut currently in space on {person['craft']}.", datatype=XSD.string)))
                            
                            
                            craft_id = person['craft'].replace(' ', '_')
                            craft_uri = self.SPACE[f"Spacecraft_{craft_id}"]
                            
                            
                            if (craft_uri, RDF.type, self.SPACE.Spacecraft) not in self.g:
                                self.g.add((craft_uri, RDF.type, self.SPACE.Spacecraft))
                                self.g.add((craft_uri, self.SPACE.name, Literal(person['craft'], datatype=XSD.string)))
                                self.g.add((craft_uri, self.SPACE.description, Literal(f"{person['craft']} is a spacecraft currently in orbit.", datatype=XSD.string)))
                
                print(f"Added data for {missions_added} NASA missions and {len(astro_data.get('people', []))} astronauts currently in space.")
            else:
                print(f"Failed to fetch NASA data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching NASA data: {e}")
    
    def fetch_exoplanet_data(self):
        """Fetch data about exoplanets from the NASA Exoplanet Archive"""
        try:
            
            exoplanet_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,pl_orbper,pl_rade,pl_masse,pl_disc,pl_discmethod,pl_facility+from+ps+where+pl_controvflag=0+and+pl_masse+is+not+null+order+by+pl_masse+desc&format=json"
            response = requests.get(exoplanet_url)
            
            if response.status_code == 200:
                exoplanets = response.json()
                
                
                milky_way_uri = self.SPACE.MilkyWay
                
                
                for exoplanet in exoplanets[:20]:
                    planet_id = exoplanet['pl_name'].replace(' ', '_').replace('-', '_')
                    planet_uri = self.SPACE[f"Exoplanet_{planet_id}"]
                    
                    
                    self.g.add((planet_uri, RDF.type, self.SPACE.Planet))
                    self.g.add((planet_uri, self.SPACE.name, Literal(exoplanet['pl_name'], datatype=XSD.string)))
                    
                    
                    if exoplanet.get('pl_masse'):
                        
                        self.g.add((planet_uri, self.SPACE.mass, Literal(float(exoplanet['pl_masse']), datatype=XSD.decimal)))
                    
                    if exoplanet.get('pl_rade'):
                        
                        self.g.add((planet_uri, self.SPACE.radius, Literal(float(exoplanet['pl_rade']), datatype=XSD.decimal)))
                    
                    if exoplanet.get('pl_orbper'):
                        self.g.add((planet_uri, self.SPACE.orbitalPeriod, Literal(float(exoplanet['pl_orbper']), datatype=XSD.decimal)))
                    
                    
                    if exoplanet.get('hostname'):
                        star_id = exoplanet['hostname'].replace(' ', '_').replace('-', '_')
                        star_uri = self.SPACE[f"Star_{star_id}"]
                        
                        
                        if (star_uri, RDF.type, self.SPACE.Star) not in self.g:
                            self.g.add((star_uri, RDF.type, self.SPACE.Star))
                            self.g.add((star_uri, self.SPACE.name, Literal(exoplanet['hostname'], datatype=XSD.string)))
                            self.g.add((star_uri, self.SPACE.description, Literal(f"{exoplanet['hostname']} is a star with at least one known exoplanet.", datatype=XSD.string)))
                            self.g.add((star_uri, self.SPACE.belongsTo, milky_way_uri))
                        
                        
                        self.g.add((planet_uri, self.SPACE.orbits, star_uri))
                    
                    
                    self.g.add((planet_uri, self.SPACE.belongsTo, milky_way_uri))
                    
                    
                    discovery_method = exoplanet.get('pl_discmethod', 'Unknown method')
                    discovery_year = exoplanet.get('pl_disc', 'Unknown year')
                    discovery_facility = exoplanet.get('pl_facility', 'Unknown facility')
                    
                    description = f"{exoplanet['pl_name']} is an exoplanet orbiting the star {exoplanet.get('hostname', 'unknown')}. "
                    description += f"It was discovered in {discovery_year} using the {discovery_method} method by {discovery_facility}."
                    
                    self.g.add((planet_uri, self.SPACE.description, Literal(description, datatype=XSD.string)))
                
                print(f"Added data for {len(exoplanets[:20])} exoplanets.")
            else:
                print(f"Failed to fetch exoplanet data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching exoplanet data: {e}")
    
    def save_ontology(self):
        """Save the ontology to a Turtle file or GraphDB"""
        try:
            if self.use_graphdb:
                
                
                
                
                
                headers = {
                    'Content-Type': 'application/sparql-query',
                    'Accept': 'application/json'
                }
                
                clear_query = "CLEAR ALL"
                requests.post(self.graphdb_url + "/statements", headers=headers, data=clear_query)
                
                
                turtle_data = self.g.serialize(format="turtle")
                
                headers = {
                    'Content-Type': 'text/turtle',
                    'Accept': 'application/json'
                }
                
                response = requests.post(self.graphdb_url + "/statements", headers=headers, data=turtle_data)
                
                if response.status_code in [200, 201, 204]:
                    print(f"Ontology saved to GraphDB at {self.graphdb_url}")
                    return True
                else:
                    print(f"Error saving to GraphDB: {response.status_code} - {response.text}")
                    return False
            else:
                
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
    creator.fetch_exoplanet_data()
    creator.save_ontology()
    
    
    print(f"Total triples in the ontology: {len(creator.g)}")
    print(f"Number of classes: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.Class))])}")
    print(f"Number of object properties: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.ObjectProperty))])}")
    print(f"Number of data properties: {len([s for s, p, o in creator.g.triples((None, RDF.type, OWL.DatatypeProperty))])}")