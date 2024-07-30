# olympic-graph
A graph containing some data from Paris 2024 Olympic Games. Please note that the content from repository is for education purpose only to explore Neo4j Aura DB and Cypher Query language.

The dataset used for this exercise is avalaible on Kaggle at the page: https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games/discussion?sort=hotness


## Steps to recreate the DB

Create a Free-Tier instance on Neo4j Aura https://neo4j.com/cloud/aura-free/


Once Connected to the DB the commands to load the data and create the graph are the following

### Step-1: Create Constrain for Athletes:

```
CREATE CONSTRAINT Athelte_code IF NOT EXISTS
FOR (a:Athlete)
REQUIRE a.code IS UNIQUE;
```

### Step-2: Create Athletes Nodes

We will start by creating the Movie Nodes using the atheletes.csv file in this repository

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/athletes.csv' AS row
MERGE (a:Athlete {code: row.code})
SET
a.name = row.name,
a.gender = row.gender,
a.height = toInteger(row.height),
a.weight = toInteger(row.weight),
a.birth_date = date(row.birth_date),
a.birth_place = row.birth_place,
a.birth_place = row.birth_place,
a.nickname = row.nickname,
a.hobbies= split(row.hobbies, ','),
a.occupation = split(row.occupation,','),
a.education = a.education,
a.reason = a.reason
```

### Step-3: Create Countries Nodes

We will then create the Country Nodes using the athletes.csv file

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/athletes.csv' AS row
MERGE (c:Country {name: row.country}) 
SET c.country_code= row.country_code
RETURN c
```


### Step-3: Create Sport Nodes

We will then create the Sport Nodes using the athletes.csv file

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/events.csv' AS row
MERGE (s:Sport {name: row.sport}) 
SET s.sport_code = row.sport_code,
s.sport_tag = row.sport_tag,
s.sport_url = row.sport_url
RETURN s
```

### Step-4: Create Event Nodes
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/events.csv' AS row
MERGE (e:Event {name: row.event})
RETURN e 



### Step-4: Create Relationship **Event-Sport**

In step we will create the Relationship (e:Event)-[r:BELONGS_TO]->(s:Sport) using the file events.csv

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/events.csv' AS row
MATCH (e:Event) WHERE e.name=row.event
MATCH (s:Sport) WHERE s.name= row.sport
MERGE (e)-[r:BELONGS_TO]->(s)
RETURN e,s,r LIMIT 100
```

### Step-5: Create Relationship **Athlete-Event**

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/medallists.csv' AS row
MATCH (a:Athlete) WHERE a.name=row.name
MATCH (e:Event) WHERE e.name=row.event
CALL apoc.merge.relationship(a,
  'HAS_WON_IN_PLACE_' + (row.medal_code),
  {medal_date:date(row.medal_date)},
  {},
  e ,
  {}
) 
YIELD rel
RETURN a,rel,e
```

### Step-6: Create Relationship **Athlete-Country**

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/olympic-graph/main/data/athletes.csv' AS row
MATCH (a:Athlete) WHERE a.name=row.name
MATCH (c:Country) WHERE c.name=row.country
MERGE (a)-[r:HAS_COUNTRY]->(c)
RETURN a,r,c
```

### EXAMPLE QUERIES

```
MATCH ()-[r:HAS_COUNTRY]->(c) WITH count(r) as Athletes, c.name AS Country WHERE Athletes > 200 RETURN Country, Athletes
```

```
MATCH (c)<-[:HAS_COUNTRY]-(a:Athlete)-[r:HAS_WON_IN_PLACE_1]->(e:Event)-[:BELONGS_TO]->(s) RETURN c.name, count(r)
```

