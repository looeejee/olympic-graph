# olympic-graph
A graph containing info from Paris 2024 Olympic Games.


## Steps to recreate the DB

Create a Free-Tier instance on Neo4j Aura https://neo4j.com/cloud/aura-free/


Once Connected to the DB the commands to load the data and create the graph are the following

### Step-1: Create Constrain for Athletes:

```
CREATE CONSTRAINT Athelte_code IF NOT EXISTS
FOR (a:Athlete)
REQUIRE a.code IS UNIQUE;
```

### Step-2: Create Movie Nodes

We will start by creating the Movie Nodes using the movies.csv file in this repository

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/rotten_tomatoes_movies/main/movies.csv' AS row
MERGE (a:Athlete {code: row.code})
SET
a.name = row.name,
a.gender = row.gender,
a.height = toInteger(rrow.height),
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

### Step-3: Create Critics Nodes

We will then create the Critics Nodes using the file critic_reviews.csv

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/rotten_tomatoes_movies/main/critic_reviews.csv' AS row
MERGE (c:Critic {name: row.criticName}) RETURN c
```

### Step-4: Create Relationship

As a final step we weill create the Relationship (c:Critic)-[r:HAS_REVIEWED]->(m:Movie) using the file critic_review.csv

```
LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/looeejee/rotten_tomatoes_movies/main/critic_reviews.csv' AS row
MATCH (c:Critic) WHERE c.name=row.criticName
MATCH (m:Movie) WHERE m.movieId= row.movieId
MERGE (c)-[r:HAS_REVIEWED]->(m)
SET r.reviewId=row.reviewId,
r.creationDate= date(row.creationDate),
r.reviewUrl = row.reviewUrl,
r.isFresh = toBoolean(row.isFresh),
r.originalScore= row.originalScore,
r.quote = row.quote,
r.scoreSentiment = row.scoreSentiment
RETURN c,m,r LIMIT 100