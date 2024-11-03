from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
user = "neo4j"
password = "passwd"

# Initialize the driver
driver = GraphDatabase.driver(uri, auth=("neo4j", "passwd"))

# Function to create a person node
def create_person(tx, name):
    query = """
    CREATE (p:Person {name: $name})
    RETURN p
    """
    tx.run(query, name=name)

# Function to create a relationship between two persons
def create_friendship(tx, name1, name2):
    query = """
    MATCH (p1:Person {name: $name1}), (p2:Person {name: $name2})
    CREATE (p1)-[:FRIENDS_WITH]->(p2)
    """
    tx.run(query, name1=name1, name2=name2)

# Function to query persons and their friends
def get_persons_and_friends(tx):
    query = """
    MATCH (p:Person)-[:FRIENDS_WITH]->(friend)
    RETURN p.name AS Person, friend.name AS Friend
    """
    result = tx.run(query)
    for record in result:
        print(f"{record['Person']} is friends with {record['Friend']}")

# Connect and run the functions
with driver.session() as session:
    # Create two person nodes
    session.write_transaction(create_person, "Iikku")
    session.write_transaction(create_person, "Petsku")

    # Create a friendship relationship
    session.write_transaction(create_friendship, "Iikku", "Petsku")

    # Query and print persons and their friendships
    session.read_transaction(get_persons_and_friends)

# Close the driver connection
driver.close()
