'''
TODO:
- Load csv
- Add new data
- log into github
- select repo
- select file (should be the same every time)

'''

from typing import Dict, Text

from loguru import logger
from github import Github
from github.Repository import Repository

from secret import USERNAME, PASSWORD
from nhl_api import results



def format_results(results: Dict) -> Text:

    # Turn results into string that can be appended to csv. Format should be:
    # game_id, Date,game_goals,is_playoff,reg_goals,playoff_goals,reg_games_played,
    # playoff_games_played,reg_goals_total,playoff_goals_total,total_goals,
    # reg_games_total,playoff_games_total

    # Add '\n' to end


    return []


def main():

    g = Github(USERNAME, PASSWORD)

    # mock_data = "100000,2050-10-05,2,False,2,0,1,0,2,0,2,1,0"

    repo = g.get_repo("josephofiowa/dekegeek") # type: Repository
    contents = repo.get_contents("gretzky-ovechkin/data/ovi_goals.csv")

    formatted_results = format_results(results)

    new_contents = contents + formatted_results
    commit_message = "Updating ovi data"
    repo.update_file(contents.path, commit_message, new_contents, contents.sha, branch="master")


if __name__ == "__main__":
    main()





