# recueil

API to type words ("Paris" -> "city")

Copyright zefrenchwan, 2024
MIT license

## What problems do you work on ? 

There are three current limits when looking for data: 
1. Time management. Looking for a dead person in a search does not mean the same as for a living one. I made `Patterns` for that
2. Data recognition for some specific values. You may want precise, hard coded results sometimes because your model is not always sufficient 
3. Looking for typed values, because usually you know the type of a data. 

### Improve recognition of specific tokens 
NLP models (spaCy for instance) tend to learn from corpus and then recognize what *looks like* a named entity. 
It usually is good enough. 
But when a company claims to be an expert of a given field, not finding or not typing common knowledge is a real issue. 
For instance, you may want to recognize "Michel Barnier" as a french prime minister when your job is social network analysis applied to politics. 
To do so, a model is not sufficient. 
You need a tool that contains "hard coded information": 
* named entities on a specific field 
* specific values (first names usually used)

### Typed searches

Assume you ask for a word, "Paris" for instance. 
It matches the first name of a famous american person, a city in France, music albums, etc. 
Why would you load all those entries when you know that you ask for a city ? 
It sounds like a better option to look for `myaddr/CITY/Paris` than `myaddr/Paris` and then filter on the client side. 
Still, we may do better. 
Paris is a capital city, then a city, then a location, then a physical entity. 
When asking for locations, you do not want to request "location", and "city" and "capital city" and ... 
You want to receive cities when asked for locations because cities are a sort of location. 

## How do I run it ? 

1. create a `.env` file at the same level as the Dockerfile
2. Set in there `DBUSER` and `DBPATH`
3. Run script `./deploy.sh`


## FAQ / Comments

### Is it prod ready ? 

Depends on what you mean by prod ready, but please, audit this code and make it compliant within your organization security policy. 

### You said that using NLP models is not a good thing ! 

No, I did not, calm down. 
I said that models are good, they adapt to new information when a hard code reference data tool will not. 
Still, humans share a common basic knowledge about some named entities. 
This project may be combined to a model, to detect specific values. 
It will not replace a model, unless you work on a given specific corpus. 

### Why python ? It is way too slow for my super fast project 

1. First, because I like Python, and you may want to copy my design for your super fast project. This is why I used MIT license. 
2. You may want to deploy more instances, or cache data. There are solutions for this issue. 
3. I work on a problem, and I try code based solutions. Consider this code as a POC, not a final prod ready code

### Wait, there is no ORM ?

This is a good question. 
To me, coding in SQL with low-level access is really efficient and not that difficult. 
So, you will find stored procedures and all a database may offer. 
No ORM, then. 