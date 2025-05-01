from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.ontology.creator import OntologyCreator
from app.ontology.queries import OntologyQueries
import os
import json
from rdflib import URIRef
from rdflib.namespace import RDF

main = Blueprint('main', __name__)


persistence_config = {
    "method": "file",  
    "graphdb_url": "http://localhost:7200/repositories/space"
}

@main.route('/')
def index():
    return render_template('index.html', persistence=persistence_config)

@main.route('/create-ontology', methods=['POST'])
def create_ontology():
    try:
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        creator = OntologyCreator(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        creator.create_ontology_structure()
        creator.fetch_solar_system_data()
        creator.fetch_spacex_data()
        creator.fetch_nasa_data()
        creator.fetch_exoplanet_data()
        success = creator.save_ontology()
        
        if success:
            return jsonify({"status": "success", "message": "Ontology created successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to create ontology"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main.route('/explore')
def explore():
    return render_template('explore.html', persistence=persistence_config)

@main.route('/sparql')
def sparql():
    return render_template('sparql.html', persistence=persistence_config)

@main.route('/graph')
def graph():
    return render_template('graph.html', persistence=persistence_config)

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    global persistence_config
    
    if request.method == 'POST':
        persistence_config["method"] = request.form.get('persistence_method', 'file')
        persistence_config["graphdb_url"] = request.form.get('graphdb_url', 'http://localhost:7200/repositories/space')
        
        return redirect(url_for('main.settings'))
    
    return render_template('settings.html', persistence=persistence_config)


@main.route('/api/classes')
def get_classes():
    try:
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        
        if not use_graphdb and not os.path.exists('ontology/space.ttl'):
            return jsonify({"error": "Ontology file not found. Please create the ontology first."}), 404
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        classes = queries.get_all_classes()
        return jsonify(classes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/instances')
def get_instances():
    try:
        class_uri = request.args.get('class')
        if not class_uri:
            return jsonify({"error": "Class URI parameter is required"}), 400
        
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        instances = queries.get_instances_of_class(class_uri)
        return jsonify(instances)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/entity')
def get_entity():
    try:
        uri = request.args.get('uri')
        if not uri:
            return jsonify({"error": "URI parameter is required"}), 400
        
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        
        entity_type = None
        uri_ref = URIRef(uri)
        for s, p, o in queries.g.triples((uri_ref, RDF.type, None)):  
            if "#" in str(o):
                entity_type = str(o).split("#")[-1]
                break
        
        
        label = queries.get_label(uri_ref)
        
        
        properties = queries.get_instance_properties(uri)
        
        
        relationships = queries.get_relationships(uri)
        
        return jsonify({
            "uri": uri,
            "label": label,
            "type": entity_type,
            "properties": properties,
            "relationships": relationships
        })
    except Exception as e:
        import traceback
        print(f"Error in get_entity: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@main.route('/api/search')
def search():
    try:
        term = request.args.get('term')
        if not term:
            return jsonify({"error": "Search term parameter is required"}), 400
        
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        results = queries.search_by_name(term)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/statistics')
def get_statistics():
    try:
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        stats = queries.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/sparql', methods=['POST'])
def execute_sparql():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({"error": "SPARQL query is required"}), 400
        
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        result = queries.execute_sparql_query(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/graph-data')
def get_graph_data():
    try:
        use_graphdb = persistence_config["method"] == "graphdb"
        graphdb_url = persistence_config["graphdb_url"] if use_graphdb else None
        
        queries = OntologyQueries(use_graphdb=use_graphdb, graphdb_url=graphdb_url)
        graph_data = queries.get_graph_data()
        return jsonify(graph_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500