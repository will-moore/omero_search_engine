import logging
import requests
import json
# url to send the query
image_ext = "/resources/image/searchannotation/"
# url to get the next page for a query, bookmark is needed
image_page_ext = "/resources/image/searchannotation_page/"
# search engine url
#base_url = "http://idr-testing.openmicroscopy.org/searchengineapi/api/v1/"
base_url = "http://127.0.0.1:5577/api/v1/"
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''
Find images of species and antibody in a specific tissue (mostly HPA) 
It is required to find the images that satisfy the following clauses: 
Organism ="Homo sapiens" and Antibody ="CAB034889" and (Organism Part = "Prostate" OR Organism Part Identifier = "T-77100")
TO send the query to the searchengine, it required creating two filters group, and filters and or filters;
And filters:
It has two clauses, 
Organism ="Homo sapiens", i.e. name ="Organism", value="Homo sapiens", and operator ="equals"
this can be translated to a d dict {"name" : "Organism", "value":"Homo sapiens", "operator" :"equals"}
each clause should have the same format so the scecond clause should be like that:
{"name" : "Antibody Identifier", "value":"CAB034889", "operator" :"equals"}
The and filters list should contais the two clauses:
'''
and_filters=[{"name": "Organism", "value":"Homo sapiens", "operator" :"equals"},{"name" : "Antibody Identifier", "value":"CAB034889", "operator" :"equals"}]
'''
The same should be done using the same approache for or filters as or filters also a list and has caluses has the same format as and filters clauses
'''

or_filters=[[{"name":"Organism Part", "value": "Prostate", "operator" :"equals"},{"name":"Organism Part Identifier", "value":"T-77100","operator" :"equals"}]]
'''
at this point, we could create a dict which should sent to the searchengine api
'''
query = {"and_filters": and_filters,"or_filters": or_filters}
query_data = {'query_details': query }

'''
The defaults search is case insestive for the values, if it is required to saearch using case sensitive, then anoter key should be added to the query data 
i.e. "case_sensitive"=True'''

#send the request
resp = requests.post(url="%s%s" % (base_url, image_ext), data=json.dumps(query_data))
# Extract the results form th response
try:
    returned_results = json.loads(resp.text)
    '''
    Check if the search returns results'''
    if returned_results.get("results"):
        if len(returned_results.get("results"))==0:
            logging.info("The search does not retuen results")
        #Get the otal number of images
        total_images=returned_results.get("results").get("size")

        logging.info("total_images: %s"%total_images)
        #if the number of pages is bigger than 1, then the bookmark is needed to get the next page
        bookmark=returned_results.get("results").get("bookmark")
        no_recieved_results = len(returned_results["results"]["results"])

    else:
        logging.info("No results.")
    '''
    the results is a dict which 
    
    ['notice', 'query_details', 'raw_elasticsearch_query', 'resource', 'results', 'server_query_time']'''
except Exception as e:
    logging.info("Error:  %s" % e)

