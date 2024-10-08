# recueil

API to type words ("Paris" -> "city")

Copyright zefrenchwan, 2024
MIT license

## TLDR

1. Webapp to get and put data you ask for. Not just a cache, there is type inheritance and type inference
2. Put data in bootstrap folder, change my config if necessary
3. Create an env file and put values for `DBUSER`, `DBPASS` and `DBNAME`
4. Launch `deploy.sh`
5. Use it, for instance: `curl http://localhost:8000/check/value/paris/as/city/`  


## What would be the typical use case for this project ? 

1. Data recognition for some specific values. You may want precise, hard coded results sometimes because your model is not always sufficient 
2. Looking for typed values, because usually you know the type of a data. 

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
It sounds like a better option to look for `/check/value/Paris/as/CITY/` than `/check/value/Paris/` and then filter on the client side. 
Still, we may do better. 
Paris is a capital city, then a city, then a location, then a physical entity. 
When asking for locations, you do not want to request `location`, and `city` and `capital` and ... 
You want to receive cities when asked for locations because cities are a sort of location. 

## How do I run it ? 

1. create a `.env` file at the same level as the Dockerfile
2. Set in there `DBUSER` and `DBPASS` for auth, `DBNAME` for database name
3. Run script `./deploy.sh`

### Available endpoints

1. `/check/value/{value}/` will return information for that value, no matter the type 
2. `/check/value/{value}/as/{tag}/` will return information for that value, filtered as instances of `tag` or its subclasses
3. `/add/value/{value}/as/{tag}/` will add `value` as `tag`. It changes values, not the inheritance tree. Tag may be stored if not already here
4. `/link/child/{child}/to/parent/{parent}/` will add the link child -> parent, may add child or parent if not already inserted

### I want custom data, not an empty database

Sure ! 
Simple, there is a `bootstrap` folder that contains csv files and json files. 
Put your data in it:
* in `json` files, follow the example structure to add your own data, note that `content` is an object
* in `csv` files, put your own inheritance tree. Structure is parent then child, left blanks mean 'same as the upper line' 


## FAQ / Comments

### Is it prod ready ? 

Nope, because rebooting means losing all pg data. 
It is useful for me to test my code, not useful at all for you.
So, that would be the first change you want to make. 
Then, security audit. 
So far, there is no auth at all. 
You may want to secure this data

### I want to export data once registered in the database

Probably not. 
You want to change the docker file to keep the stored data. 
My project is a POC, yours may not be. 


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


### Dude, come on, use a graph database ! 

So far, the one I used was slower than my beloved postgresql. 


### Dude, come on, use a cache ! 

Might be an idea, but you would need to store the tree as is. 
Interesting, maybe on a next project ! 