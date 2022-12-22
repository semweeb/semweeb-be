from SPARQLWrapper import JSON, SPARQLWrapper
import json

sparql = SPARQLWrapper(
    "http://localhost:9999/blazegraph/namespace/kb/sparql"
)

sparql.setReturnFormat(JSON)

def search(query: str, page: int, genre: list):
    if len(genre) > 0:
      filter = f"HAVING(regex(?genres, \"{genre[0].capitalize()}\")"
      for i in range(1, len(genre)):
        filter += f" || regex(?genres, \"{genre[i].capitalize()}\")"
      filter += ")"
    else:
      filter = ""

    print(filter)
    sparql.setQuery("""
      prefix xsd: <http://www.w3.org/2001/XMLSchema#>
      prefix skos: <http://www.w3.org/2004/02/skos/core#>
      prefix owl: <http://www.w3.org/2002/07/owl#>
      prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      prefix ex:    <http://example.org/data/>
      prefix exv:   <http://example.org/vocab#>
      prefix bds: <http://www.bigdata.com/rdf/search#>

      SELECT DISTINCT ?id (SAMPLE(?t) AS ?title) (GROUP_CONCAT(?genre_name; SEPARATOR=", ") as ?genres) (SAMPLE(?sc) AS ?score) (SAMPLE(?im) AS ?image) WHERE {{
        BIND({0} AS ?query)
        {{
          ?id a ex:AnimeID ;
                exv:title ?t ;
                exv:genres ?g ;
                exv:score ?sc .
          OPTIONAL {{
            ?id exv:main_picture ?im .
          }}  
          OPTIONAL {{
            ?id exv:title_english ?title_en ;
          }}
          ?g rdfs:label ?genre_name .
        }}
        {{
          ?t bds:search ?query .
        }}
        UNION
        {{
          OPTIONAL {{ 
            FILTER (strlen(?title_en) > 0)
            BIND(".#." AS ?title_en)
          }}
          ?title_en bds:search ?query .
        }}
      }} GROUP BY ?id 
      {1}
      ORDER BY DESC(?score) LIMIT 32 OFFSET {2}
    """.format(json.dumps(query), filter, json.dumps(page)))
    
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

      SELECT DISTINCT ?id (SAMPLE(?t) AS ?title) (GROUP_CONCAT(?genre_name; SEPARATOR=", ") as ?genres) (SAMPLE(?sc) AS ?score) (SAMPLE(?im) AS ?image) WHERE {{
        BIND({0} AS ?query)
        {{
          ?id a ex:AnimeID ;
                exv:title ?t ;
                exv:genres ?g ;
                exv:score ?sc .
          OPTIONAL {{
            ?id exv:main_picture ?im .
          }}  
          OPTIONAL {{
            ?id exv:title_english ?title_en ;
          }}
          ?g rdfs:label ?genre_name .
        }}
        {{
          ?t bds:search ?query .
        }}
        UNION
        {{
          OPTIONAL {{ 
            FILTER (strlen(?title_en) > 0)
            BIND(".#." AS ?title_en)
          }}
          ?title_en bds:search ?query .
        }}
      }} GROUP BY ?id ORDER BY DESC(?score) LIMIT 16
    """.format(json.dumps(query)))

    return sparql.queryAndConvert()["results"]["bindings"]

def get_anime_details(anime_id: str):
    sparql.setQuery(f"""
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix ex:    <http://example.org/data/>
        prefix exv:   <http://example.org/vocab#>
        prefix bds: <http://www.bigdata.com/rdf/search#>
        
        SELECT DISTINCT ?title ?scored_by ?members ?favorites ?status_name ?sfw ?approved ?type_name ?score ?episodes ?start_date ?end_date ?source_name ?synopsis ?background ?main_picture ?episode_duration ?total_duration ?rating_name ?start_year ?start_season ?broadcast_day ?broadcast_time ?trailer_url ?title_english ?title_japanese (GROUP_CONCAT(DISTINCT ?demographic_name;SEPARATOR=", ") AS ?demographics) (GROUP_CONCAT(DISTINCT ?theme_name;SEPARATOR=", ") AS ?themes) (GROUP_CONCAT(DISTINCT ?studio_name;SEPARATOR=", ") AS ?studios) (GROUP_CONCAT(DISTINCT ?producer_name;SEPARATOR=", ") AS ?producers) (GROUP_CONCAT(DISTINCT ?licensor_name;SEPARATOR=", ") AS ?licensors) (GROUP_CONCAT(DISTINCT ?genre_name;SEPARATOR=", ") AS ?genres) WHERE {{     
                                         
          ex:{anime_id} a ex:AnimeID ;
                exv:title ?title ;
                exv:scored_by ?scored_by ;
                exv:members ?members ;
                exv:favorites ?favorites ;
                exv:status ?status ;
                exv:sfw ?sfw ;
                exv:approved ?approved .

          ?status rdfs:label ?status_name .

          OPTIONAL {{
            ex:{anime_id} exv:type ?type .
            ?type rdfs:label ?type_name .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:score ?score .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:episodes ?episodes .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:start_date ?start_date .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:end_date ?end_date .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:source ?source .
            ?source rdfs:label ?source_name .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:demographics ?demographics.
            ?demographics rdfs:label ?demographic_name .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:studios ?studios .
            ?studios rdfs:label ?studio_name .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:producers ?producers .
            ?producers rdfs:label ?producer_name .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:licensors ?licensors .
            ?licensors rdfs:label ?licensor_name .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:synopsis ?synopsis .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:background ?background .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:main_picture ?main_picture.
          }}

          OPTIONAL {{
            ex:{anime_id} exv:episode_duration ?episode_duration.
          }}

          OPTIONAL {{
            ex:{anime_id} exv:total_duration ?total_duration .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:rating ?rating .
            ?rating rdfs:label ?rating_name .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:start_year ?start_year .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:start_season ?start_season .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:broadcast_day ?broadcast_day .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:broadcast_time ?broadcast_time .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:genres ?genres .
            ?genres rdfs:label ?genre_name .
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:themes ?themes .
            ?themes rdfs:label ?theme_name .
          }}

          OPTIONAL {{
            ex:{anime_id} exv:trailer_url ?trailer_url.
          }}

          OPTIONAL {{
            ex:{anime_id} exv:title_english ?title_english.
          }}
          
          OPTIONAL {{
            ex:{anime_id} exv:title_japanese ?title_japanese .
          }}

        }} GROUP BY ?title ?scored_by ?members ?favorites ?status_name ?sfw ?approved ?type_name ?score ?episodes ?start_date ?end_date ?source_name ?synopsis ?background ?main_picture ?episode_duration ?total_duration ?rating_name ?start_year ?start_season ?broadcast_day ?broadcast_time ?trailer_url ?title_english ?title_japanese
    """)

    return sparql.queryAndConvert()["results"]["bindings"][0]

def get_anime_voice_actor(anime_id: str):
    sparql.setQuery(f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wds: <http://www.wikidata.org/entity/statement/>
    PREFIX wdv: <http://www.wikidata.org/value/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>

    SELECT DISTINCT ?item ?itemLabel ?characters ?charactersLabel ?actor ?actorLabel WHERE {{
      SERVICE <https://query.wikidata.org/sparql> {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        {{
          SELECT DISTINCT ?actor ?actorLabel ?characters ?charactersLabel WHERE {{
            ?item p:P4086 ?statement0.
                ?statement0 ps:P4086 "{anime_id}".
                OPTIONAL {{
                  ?item p:P725 ?statement1.
                  ?statement1 ps:P725 ?actor.
                  ?statement1 pq:P453 ?characters.
                }}
          }} LIMIT 20
        }}
      }}
    }}               
    """)

    return sparql.queryAndConvert()["results"]["bindings"]

def get_random_anime_details():
  print("")
