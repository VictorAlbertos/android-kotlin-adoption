import pandas as pd
from datetime import datetime
from dateutil.relativedelta import *
from network_utils import make_http_call


def fetch_repos_count(df, start_date, end_date, language, scope):
    """Fetch the repositories created between the supplied range of dates and filtered by their main language and the scope supplied

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame in which to add the data retrieved.
    start_date : datetime
        Repositories created after this date
    end_date : datetime
        Repositories created before this date
    language : str
        The main language of the repository.
    sccope : str
        `android` or `not android` repositories.
    """

    query = """s
        query fecthRepos($raw_query: String!) {
         search(query:$raw_query, type:REPOSITORY) {
          repositoryCount
         }
        }
        """

    variables = {
        "raw_query": f"{scope} language:{language} created:{start_date}..{end_date} is:public archived:false fork:false"
    }

    response = make_http_call(query, variables)
    repository_count = int(response['data']['search']['repositoryCount'])
    df.loc[len(df)] = [language, scope, start_date, repository_count]


df = pd.DataFrame(columns=['language', 'scope', 'created_at', 'count'])

date_format = '%Y-%m-%d'
start_date = datetime.strptime('2016-02-15', date_format)
end_date = datetime.strptime('2019-01-15', date_format)
current_start_date = start_date
current_end_date = start_date + relativedelta(months=+1)

while current_end_date < end_date:
    current_start_date_formatted = current_start_date.strftime(date_format)
    current_end_date_formatted = current_end_date.strftime(date_format)

    fetch_repos_count(df, current_start_date_formatted, current_end_date_formatted, 'kotlin', 'android')
    fetch_repos_count(df, current_start_date_formatted, current_end_date_formatted, 'java', 'android')
    fetch_repos_count(df, current_start_date_formatted, current_end_date_formatted, 'kotlin', 'NOT android')
    fetch_repos_count(df, current_start_date_formatted, current_end_date_formatted, 'java', 'NOT android')

    current_start_date += relativedelta(months=+1)
    current_end_date += relativedelta(months=+1)

    df.to_csv('creations.csv', index=False)

    print(current_start_date.strftime(date_format), '-', current_end_date.strftime(date_format))
