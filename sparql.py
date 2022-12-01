from SPARQLWrapper import JSON, SPARQLWrapper

sparql = SPARQLWrapper(
    "http://vocabs.ardc.edu.au/repository/api/sparql/"
    "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
)

sparql.setReturnFormat(JSON)

def search(query: str):
    sparql.setQuery("""
        PREFIX gts: <http://resource.geosciml.org/ontology/timescale/gts#>

        SELECT *
        WHERE {
            ?a a gts:Age .
        }
        ORDER BY ?a
        LIMIT 3
        """
    )

    return sparql.queryAndConvert()
