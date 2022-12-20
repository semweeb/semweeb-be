from SPARQLWrapper import JSON, SPARQLWrapper
import json

sparql = SPARQLWrapper(
    "http://localhost:9999/blazegraph/namespace/kb/sparql"
)

sparql.setReturnFormat(JSON)

def search(query: str):
    sparql.setQuery("""
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix ex:    <http://example.org/data/>
        prefix exv:   <http://example.org/vocab#>
        prefix bds: <http://www.bigdata.com/rdf/search#>

        SELECT ?id ?title (GROUP_CONCAT(?genre_name;SEPARATOR=", ") AS ?genres) ?image WHERE {{
          BIND({} AS ?query)
          ?id a ex:AnimeID ;
            exv:title ?title ;
            exv:genres ?genre .

          OPTIONAL {{
            ?id exv:main_picture ?image .
          }}

          ?title bds:search ?query .
          ?genre rdfs:label ?genre_name .
        }} GROUP BY ?id ?title ?image
    """.format(json.dumps(query)))
    
    return sparql.queryAndConvert()["results"]["bindings"]

def get_suggestions(query: str):
    sparql.setQuery("""
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix ex:    <http://example.org/data/>
        prefix exv:   <http://example.org/vocab#>
        prefix bds: <http://www.bigdata.com/rdf/search#>

        SELECT ?id ?title (GROUP_CONCAT(?genre_name;SEPARATOR=", ") AS ?genres) ?image WHERE {{
          BIND({} AS ?query)
          ?id a ex:AnimeID ;
            exv:title ?title ;
            exv:genres ?genre .

          OPTIONAL {{
            ?id exv:main_picture ?image .
          }}

          ?title bds:search ?query .
          ?genre rdfs:label ?genre_name .
        }} GROUP BY ?id ?title ?image LIMIT 4
    """.format(json.dumps(query)))

    return sparql.queryAndConvert()["results"]["bindings"]


