import pandas as pd
from network_utils import make_http_call


def fetch_repos_migrations(df, language, cursor):
    """Fetch the repositories created before 2016-02-15 and having a commit after 2019-01-01, then save them in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame in which to add the data retrieved.
    language : str
        The main language of the repository.
    cursor : str
        The current cursor (page).
    """

    query = """
        query($raw_query: String!, $cursor:String) {
         search(query:$raw_query, type:REPOSITORY, first:50, after:$cursor) {
          pageInfo {
              hasNextPage
              endCursor
          }
          repositoryCount
          edges {
           node {
            ... on Repository {
              id
              name
              diskUsage
              createdAt
              forkCount
              watchers {
                totalCount
              }
              issues {
                totalCount
              }
              pullRequests {
                totalCount
              }
              stargazers {
                totalCount
              }
            }
           }
          }
         }
        }
        """

    variables = {
        "raw_query": f"android language:{language} created:<2016-02-15 pushed:>2019-01-01 is:public archived:false fork:false",
        "cursor": cursor
    }

    response = make_http_call(query, variables)['data']['search']

    for edge in response['edges']:
        node = edge['node']

        migrated = True if language == 'kotlin' else False

        df.loc[len(df)] = [node['id'], node['name'], migrated, node['diskUsage'], node['createdAt'], node['forkCount'],
                           node['watchers']['totalCount'], node['issues']['totalCount'],
                           node['pullRequests']['totalCount'], node['stargazers']['totalCount']]

    return response['pageInfo']['hasNextPage'], response['pageInfo']['endCursor']


df = pd.DataFrame(columns=['id', 'name', 'migrated', 'disk_usage', 'created_at', 'fork_count', 'watchers_count',
                           'issues_count', 'pull_requests_count', 'starts_count'])

has_next_page = True
cursor = None
page = 1

while has_next_page:
    has_next_page, cursor = fetch_repos_migrations(df, 'kotlin', cursor)

    print(f'Fetched Kotlin page: {page}')
    page += 1

    df.to_csv('migrations.csv', index=False)

has_next_page = True
cursor = None
page = 1

while has_next_page:
    has_next_page, cursor = fetch_repos_migrations(df, 'java', cursor)

    print(f'Fetched Java page: {page}')
    page += 1

    df.to_csv('migrations.csv', index=False)
