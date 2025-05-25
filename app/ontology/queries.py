import requests
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS
from SPARQLWrapper import SPARQLWrapper, JSON, POST


class OntologyQueries:
    def __init__(
        self,
        use_graphdb=True,
        graphdb_url="http://localhost:7200/repositories/space-ontology",
    ):
        self.use_graphdb = use_graphdb
        self.graphdb_url = graphdb_url

        if use_graphdb:
            self.sparql = SPARQLWrapper(f"{graphdb_url}")
            self.sparql.setReturnFormat(JSON)

            self.g = Graph()
            try:
                response = requests.get(
                    f"{graphdb_url}/statements",
                    headers={"Accept": "text/turtle"},
                    timeout=30,
                )
                if response.status_code == 200:
                    self.g.parse(data=response.text, format="turtle")
            except Exception as e:
                print(f"Warning: Could not load GraphDB data: {e}")
                self.g = Graph()
        else:
            self.g = Graph()

        self.SPACE = Namespace("http://www.semanticweb.org/ontologies/space#")
        self.g.bind("space", self.SPACE)

    def execute_sparql_query(self, query_string):
        try:
            if self.use_graphdb:
                query_upper = query_string.upper().strip()

                if any(
                    query_upper.startswith(op)
                    for op in ["INSERT", "DELETE", "CLEAR", "DROP", "CREATE"]
                ):
                    self.sparql.setMethod(POST)
                    self.sparql.setQuery(query_string)
                    self.sparql.setReturnFormat(JSON)

                    try:
                        result = self.sparql.query()
                        self._reload_local_graph()
                        return {
                            "success": True,
                            "message": "Update executed successfully",
                        }
                    except Exception as e:
                        return {"success": False, "error": str(e)}
                else:
                    self.sparql.setQuery(query_string)
                    results = self.sparql.query().convert()

                    formatted_results = []
                    if "results" in results and "bindings" in results["results"]:
                        for binding in results["results"]["bindings"]:
                            result = {}
                            for var, value in binding.items():
                                if value["type"] == "uri":
                                    label = self.get_label(URIRef(value["value"]))
                                    result[var] = {
                                        "uri": value["value"],
                                        "label": label,
                                    }
                                else:
                                    result[var] = value["value"]
                            formatted_results.append(result)

                    return {
                        "success": True,
                        "results": formatted_results,
                        "variables": results.get("head", {}).get("vars", []),
                    }
            else:
                results = []
                qres = self.g.query(query_string)

                for row in qres:
                    result = {}
                    for var in qres.vars:
                        value = row[var]
                        if value:
                            if isinstance(value, URIRef):
                                label = self.get_label(value)
                                result[var] = {"uri": str(value), "label": label}
                            else:
                                result[var] = (
                                    value.value
                                    if hasattr(value, "value")
                                    else str(value)
                                )
                        else:
                            result[var] = None
                    results.append(result)

                return {
                    "success": True,
                    "results": results,
                    "variables": [str(var) for var in qres.vars],
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _reload_local_graph(self):
        try:
            if self.use_graphdb:
                response = requests.get(
                    f"{self.graphdb_url}/statements",
                    headers={"Accept": "text/turtle"},
                    timeout=30,
                )
                if response.status_code == 200:
                    self.g = Graph()
                    self.g.parse(data=response.text, format="turtle")
                    self.g.bind("space", self.SPACE)
        except Exception as e:
            print(f"Warning: Could not reload graph from GraphDB: {e}")

    def get_all_classes(self):
        if self.use_graphdb:
            query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?class ?label WHERE {
                ?class a owl:Class .
                OPTIONAL { ?class rdfs:label ?label }
            }
            """

            try:
                self.sparql.setQuery(query)
                results = self.sparql.query().convert()

                classes = []
                if "results" in results and "bindings" in results["results"]:
                    for binding in results["results"]["bindings"]:
                        class_uri = binding["class"]["value"]
                        label = binding.get("label", {}).get(
                            "value", class_uri.split("#")[-1]
                        )
                        classes.append({"uri": class_uri, "label": label})

                return classes
            except Exception as e:
                print(f"Error in get_all_classes: {e}")
                return []
        else:
            classes = []
            for s, p, o in self.g.triples((None, RDF.type, None)):
                if str(o) == "http://www.w3.org/2002/07/owl#Class":
                    class_uri = str(s)
                    label = self.get_label(s)
                    classes.append({"uri": class_uri, "label": label})
            return classes

    def get_label(self, uri):
        if not uri:
            return "Unknown"

        uri = URIRef(uri) if not isinstance(uri, URIRef) else uri

        for s, p, o in self.g.triples((uri, RDFS.label, None)):
            return o.value

        if self.use_graphdb:
            try:
                query = f"""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?label WHERE {{
                    <{uri}> rdfs:label ?label .
                }}
                """
                self.sparql.setQuery(query)
                results = self.sparql.query().convert()

                if "results" in results and "bindings" in results["results"]:
                    bindings = results["results"]["bindings"]
                    if bindings:
                        return bindings[0]["label"]["value"]
            except Exception as e:
                print(f"Error getting label for {uri}: {e}")

        if "#" in str(uri):
            return str(uri).split("#")[-1]
        return str(uri)

    def get_instances_of_class(self, class_uri):
        if self.use_graphdb:
            query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX space: <http://www.semanticweb.org/ontologies/space#>
            
            SELECT ?instance ?label WHERE {{
                ?instance a <{class_uri}> .
                OPTIONAL {{ ?instance rdfs:label ?label }}
                OPTIONAL {{ ?instance space:name ?label }}
            }}
            """

            try:
                self.sparql.setQuery(query)
                results = self.sparql.query().convert()

                instances = []
                if "results" in results and "bindings" in results["results"]:
                    for binding in results["results"]["bindings"]:
                        instance_uri = binding["instance"]["value"]
                        label = binding.get("label", {}).get(
                            "value", instance_uri.split("#")[-1]
                        )
                        instances.append({"uri": instance_uri, "label": label})

                return instances
            except Exception as e:
                print(f"Error in get_instances_of_class: {e}")
                return []
        else:
            instances = []
            try:
                class_uri = (
                    URIRef(class_uri)
                    if not isinstance(class_uri, URIRef)
                    else class_uri
                )

                for s, p, o in self.g.triples((None, RDF.type, class_uri)):
                    instance_uri = str(s)
                    label = self.get_label(s)
                    instances.append({"uri": instance_uri, "label": label})
            except Exception as e:
                print(f"Error in get_instances_of_class: {e}")

            return instances

    def get_instance_properties(self, instance_uri):
        properties = []

        try:
            instance_uri = (
                URIRef(instance_uri)
                if not isinstance(instance_uri, URIRef)
                else instance_uri
            )

            for s, p, o in self.g.triples((instance_uri, None, None)):
                if p != RDF.type and p != RDFS.label:
                    prop_name = str(p).split("#")[-1]

                    obj_value = o.value if hasattr(o, "value") else str(o)
                    if isinstance(o, URIRef):
                        obj_label = self.get_label(o)
                        if obj_label:
                            obj_value = obj_label

                    properties.append({"property": prop_name, "value": obj_value})
        except Exception as e:
            print(f"Error in get_instance_properties: {e}")

        return properties

    def search_by_name(self, search_term):
        if self.use_graphdb:
            query = f"""
            PREFIX space: <http://www.semanticweb.org/ontologies/space#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?instance ?name ?type WHERE {{
                ?instance space:name ?name .
                ?instance a ?type .
                FILTER(CONTAINS(LCASE(?name), LCASE("{search_term}")))
                FILTER(?type != <http://www.w3.org/2002/07/owl#Class>)
            }}
            """

            try:
                self.sparql.setQuery(query)
                results = self.sparql.query().convert()

                search_results = []
                if "results" in results and "bindings" in results["results"]:
                    for binding in results["results"]["bindings"]:
                        instance_uri = binding["instance"]["value"]
                        name = binding["name"]["value"]
                        type_uri = binding["type"]["value"]
                        type_name = (
                            type_uri.split("#")[-1] if "#" in type_uri else type_uri
                        )

                        search_results.append(
                            {
                                "uri": instance_uri,
                                "name": name,
                                "type": type_name,
                            }
                        )

                return search_results
            except Exception as e:
                print(f"Error in search_by_name: {e}")
                return []
        else:
            results = []
            try:
                for s, p, o in self.g.triples((None, self.SPACE.name, None)):
                    if search_term.lower() in str(o).lower():
                        instance_uri = str(s)
                        instance_name = o.value

                        instance_type = None
                        for _, _, type_uri in self.g.triples((s, RDF.type, None)):
                            if "#" in str(type_uri):
                                instance_type = str(type_uri).split("#")[-1]
                                break

                        results.append(
                            {
                                "uri": instance_uri,
                                "name": instance_name,
                                "type": instance_type,
                            }
                        )
            except Exception as e:
                print(f"Error in search_by_name: {e}")

            return results

    def get_relationships(self, instance_uri):
        relationships = []

        try:
            instance_uri = (
                URIRef(instance_uri)
                if not isinstance(instance_uri, URIRef)
                else instance_uri
            )

            for s, p, o in self.g.triples((instance_uri, None, None)):
                if isinstance(o, URIRef) and p != RDF.type:
                    rel_type = str(p).split("#")[-1]
                    target_label = self.get_label(o)
                    target_type = None

                    for _, _, type_uri in self.g.triples((o, RDF.type, None)):
                        if "#" in str(type_uri):
                            target_type = str(type_uri).split("#")[-1]
                            break

                    relationships.append(
                        {
                            "direction": "outgoing",
                            "type": rel_type,
                            "target_uri": str(o),
                            "target_label": target_label,
                            "target_type": target_type,
                        }
                    )

            for s, p, o in self.g.triples((None, None, instance_uri)):
                if p != RDF.type:
                    rel_type = str(p).split("#")[-1]
                    source_label = self.get_label(s)
                    source_type = None

                    for _, _, type_uri in self.g.triples((s, RDF.type, None)):
                        if "#" in str(type_uri):
                            source_type = str(type_uri).split("#")[-1]
                            break

                    relationships.append(
                        {
                            "direction": "incoming",
                            "type": rel_type,
                            "source_uri": str(s),
                            "source_label": source_label,
                            "source_type": source_type,
                        }
                    )
        except Exception as e:
            print(f"Error in get_relationships: {e}")

        return relationships

    def get_statistics(self):
        stats = {
            "total_triples": 0,
            "classes": {},
            "properties": {"object_properties": 0, "data_properties": 0},
        }

        try:
            if self.use_graphdb:
                count_query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
                self.sparql.setQuery(count_query)
                results = self.sparql.query().convert()

                if "results" in results and "bindings" in results["results"]:
                    bindings = results["results"]["bindings"]
                    if bindings:
                        stats["total_triples"] = int(bindings[0]["count"]["value"])

                class_query = """
                SELECT ?type (COUNT(?instance) as ?count) WHERE {
                    ?instance a ?type .
                    FILTER(?type != <http://www.w3.org/2002/07/owl#Class>)
                    FILTER(?type != <http://www.w3.org/2002/07/owl#ObjectProperty>)
                    FILTER(?type != <http://www.w3.org/2002/07/owl#DatatypeProperty>)
                } GROUP BY ?type
                """

                self.sparql.setQuery(class_query)
                results = self.sparql.query().convert()

                if "results" in results and "bindings" in results["results"]:
                    for binding in results["results"]["bindings"]:
                        type_uri = binding["type"]["value"]
                        count = int(binding["count"]["value"])
                        class_name = (
                            type_uri.split("#")[-1] if "#" in type_uri else type_uri
                        )
                        stats["classes"][class_name] = count
            else:
                stats["total_triples"] = len(self.g)

                for s, p, o in self.g.triples((None, RDF.type, None)):
                    if "#" in str(o):
                        class_name = str(o).split("#")[-1]
                        if class_name not in stats["classes"]:
                            stats["classes"][class_name] = 0
                        stats["classes"][class_name] += 1

                for s, p, o in self.g.triples((None, RDF.type, None)):
                    if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty":
                        stats["properties"]["object_properties"] += 1
                    elif str(o) == "http://www.w3.org/2002/07/owl#DatatypeProperty":
                        stats["properties"]["data_properties"] += 1

        except Exception as e:
            print(f"Error in get_statistics: {e}")

        return stats

    def get_graph_data(self, limit_per_type=25, class_filter=None):
        nodes = []
        links = []
        node_ids = set()

        try:
            for s, p, o in self.g.triples((None, RDF.type, None)):
                if str(o) == "http://www.w3.org/2002/07/owl#Class":
                    node_id = str(s)
                    if node_id not in node_ids:
                        nodes.append(
                            {"id": node_id, "label": self.get_label(s), "type": "class"}
                        )
                        node_ids.add(node_id)

            instance_types = {}
            for s, p, o in self.g.triples((None, RDF.type, None)):
                if (
                    str(o) != "http://www.w3.org/2002/07/owl#Class"
                    and str(o) != "http://www.w3.org/2002/07/owl#ObjectProperty"
                    and str(o) != "http://www.w3.org/2002/07/owl#DatatypeProperty"
                ):

                    type_name = str(o).split("#")[-1]
                    if type_name not in instance_types:
                        instance_types[type_name] = []

                    instance_uri = str(s)
                    instance_types[type_name].append(instance_uri)

            if class_filter:
                filtered_types = {}
                for type_name, instances in instance_types.items():
                    if type_name == class_filter:
                        filtered_types[type_name] = instances
                instance_types = filtered_types

            for type_name, instances in instance_types.items():
                type_uri = None
                for s, p, o in self.g.triples((None, RDF.type, None)):
                    if str(o) == "http://www.w3.org/2002/07/owl#Class" and str(
                        s
                    ).endswith("#" + type_name):
                        type_uri = str(s)
                        break

                for instance_uri in instances[:limit_per_type]:
                    if instance_uri not in node_ids:
                        s = URIRef(instance_uri)
                        nodes.append(
                            {
                                "id": instance_uri,
                                "label": self.get_label(s),
                                "type": type_name,
                            }
                        )
                        node_ids.add(instance_uri)

                        if type_uri:
                            links.append(
                                {
                                    "source": instance_uri,
                                    "target": type_uri,
                                    "label": "type",
                                }
                            )

            for s, p, o in self.g.triples((None, None, None)):
                if (
                    isinstance(s, URIRef)
                    and isinstance(o, URIRef)
                    and p != RDF.type
                    and p != RDFS.subClassOf
                ):

                    source_id = str(s)
                    target_id = str(o)

                    if source_id in node_ids and target_id in node_ids:
                        rel_type = str(p).split("#")[-1]
                        links.append(
                            {
                                "source": source_id,
                                "target": target_id,
                                "label": rel_type,
                            }
                        )

        except Exception as e:
            print(f"Error in get_graph_data: {e}")

        return {"nodes": nodes, "links": links}
