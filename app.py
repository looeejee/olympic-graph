from flask import Flask, jsonify
from neo4j import GraphDatabase
import random

app = Flask(__name__)

# Load Neo4j DB credentials from Kubernetes secret
neo4j_uri = os.environ['NEO4J_URI']
neo4j_user = os.environ['NEO4J_USER']
neo4j_password = os.environ['NEO4J_PASSWORD']

# Create a Neo4j DB driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

@app.route('/create-data', methods=['GET'])
def create_data():
    with driver.session() as session:
        # Create 100 nodes
        nodes = []
        for i in range(100):
            node = session.run('CREATE (n:Node {id: $id}) RETURN n', id=i)
            nodes.append(node.single()['n'])

        # Create relationships between nodes
        relationships = []
        for i in range(100):
            for j in range(100):
                if i != j:
                    relationship = session.run('MATCH (a:Node {id: $id1}), (b:Node {id: $id2}) CREATE (a)-[:RELATES_TO]->(b)', id1=i, id2=j)
                    relationships.append(relationship.single())

        # Return the data
        data = {'nodes': nodes, 'relationships': relationships}
        return jsonify(data)

@app.route('/visualize-data', methods=['GET'])
def visualize_data():
    with driver.session() as session:
        # Get all nodes and relationships
        nodes = session.run('MATCH (n) RETURN n')
        relationships = session.run('MATCH (a)-[r]->(b) RETURN a, r, b')

        # Visualize the data using a library like NetworkX and Matplotlib
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        for node in nodes:
            G.add_node(node['n']['id'])
        for relationship in relationships:
            G.add_edge(relationship['a']['id'], relationship['b']['id'])

        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.show()

        return 'Data visualized!'

@app.route('/delete-data', methods=['GET'])
def delete_data():
    with driver.session() as session:
        # Delete all nodes and relationships
        session.run('MATCH (n) DETACH DELETE n')
        return 'Data deleted!'

if __name__ == '__main__':
    app.run(debug=True)
