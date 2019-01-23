from credentials import token
import requests
import time


def make_http_call(query, variables, retry=0):
    """Perform an http call to Github api graph

    Parameters
    ----------
    query : str
        Query of the call
    variables : str
        Arguments to populate the query template
    retry: int, optional
        This param is not meant to use for consumers. It's a workaround to retry calls track avoiding and endless loop.
        Github v4 api is not 100% reliable and sometimes responds with internal errors.

    Returns
    -------
    the response if it's successful otherwise it throws
    """

    try:
        time.sleep(5)
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables},
                                headers={"Authorization": f"Bearer {token}"}, timeout=10)
    except requests.exceptions.Timeout:
        print(f"Retrying http call times {retry}")
        return make_http_call(query, variables, retry + 1)

    if request.status_code == 200:
        return request.json()
    if request.status_code == 502 and retry < 10:
        print("Retrying http call")
        return make_http_call(query, variables, retry + 1)
    else:
        raise Exception(
            "Query failed to run by returning code of {}. Error message: {}. Query: {}".format(request.status_code,
                                                                                               request.content, query))
