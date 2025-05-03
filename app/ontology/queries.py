from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS
import os


class OntologyQueries:
    def __init__(
        self,
        ontology_path="ontology/space.ttl",
        use_graphdb=False,
        graphdb_url="http://localhost:7200/repositories/space",
    ):
        self.g = Graph()
        self.use_graphdb = use_graphdb
        self.graphdb_url = graphdb_url

        if use_graphdb:

            self.g.parse(graphdb_url, format="turtle")
        else:

            if os.path.exists(ontology_path):
                self.g.parse(ontology_path, format="turtle")
            else:
                print(f"Warning: Ontology file {ontology_path} not found.")

        self.SPACE = Namespace("http://www.semanticweb.org/ontologies/space#")
        self.g.bind("space", self.SPACE)

    def get_all_classes(self):
        """Get all classes in the ontology"""
        classes = []
        for s, p, o in self.g.triples((None, RDF.type, None)):
            if str(o) == "http://www.w3.org/2002/07/owl#Class":
                class_uri = str(s)
                label = self.get_label(s)
                classes.append({"uri": class_uri, "label": label})
        return classes

    def get_label(self, uri):
        """Get the label for a URI"""
        if not uri:
            return "Unknown"

        uri = URIRef(uri) if not isinstance(uri, URIRef) else uri

        for s, p, o in self.g.triples((uri, RDFS.label, None)):
            return o.value

        if "#" in str(uri):
            return str(uri).split("#")[-1]
        return str(uri)

    def get_instances_of_class(self, class_uri):
        """Get all instances of a class"""
        instances = []

        try:
            class_uri = (
                URIRef(class_uri) if not isinstance(class_uri, URIRef) else class_uri
            )

            for s, p, o in self.g.triples((None, RDF.type, class_uri)):
                instance_uri = str(s)
                label = self.get_label(s)
                instances.append({"uri": instance_uri, "label": label})
        except Exception as e:
            print(f"Error in get_instances_of_class: {e}")

        return instances

    def get_instance_properties(self, instance_uri):
        """Get all properties of an instance"""
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
        """Search for instances by name"""
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
        """Get all relationships of an instance"""
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
        """Get statistics about the ontology"""
        stats = {
            "total_triples": len(self.g),
            "classes": {},
            "properties": {"object_properties": 0, "data_properties": 0},
        }

        try:

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

    def execute_sparql_query(self, query_string):
        """Execute a SPARQL query on the ontology"""
        try:
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
                                value.value if hasattr(value, "value") else str(value)
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

                    if len(instance_types[type_name]) < limit_per_type:
                        instance_types[type_name].append(str(s))

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

                for instance_uri in instances:
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

            all_relationships = []
            for s, p, o in self.g.triples((None, None, None)):
                if (
                    isinstance(s, URIRef)
                    and isinstance(o, URIRef)
                    and p != RDF.type
                    and str(p) != "http://www.w3.org/2000/01/rdf-schema#subClassOf"
                ):
                    source_id = str(s)
                    target_id = str(o)

                    if source_id in node_ids and target_id in node_ids:
                        all_relationships.append(
                            {
                                "source": source_id,
                                "target": target_id,
                                "label": str(p).split("#")[-1],
                            }
                        )

            for rel in all_relationships:
                links.append(rel)

        except Exception as e:
            print(f"Error in get_graph_data: {e}")

        return {"nodes": nodes, "links": links}
