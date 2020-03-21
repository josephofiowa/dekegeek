from datetime import datetime as dt
from datetime import timedelta as td
from typing import Dict, List, Text
import re

from loguru import logger
import requests
from github import Github
from github.Repository import Repository

from .secret import USERNAME, PASSWORD
from .constants import BASE_URL, TEAMS_ENDPOINT


def find_last_game():
    # Finds last game in our dataset

    g = Github(USERNAME, PASSWORD)
    repo = g.get_repo("josephofiowa/dekegeek")  # type: Repository
    contents = repo.get_contents("gretzky-ovechkin/data/ovi_goals.csv")

    last_entry = str(contents.decoded_content.split(b"\n")[-2])

    logger.info(type(last_entry))
    last_date = re.findall(r"\d{4}-\d{2}-\d{2}", last_entry)[0]
    logger.info(f"Last date: {last_date}")
    return last_date


def find_caps_id(teams: List[Dict]) -> int:
    for i in teams:
        if i["name"] == "Washington Capitals":
            return i["id"]


def get_start_date(last_recorded_date: Text) -> Text:

    last_date = dt.strptime(last_recorded_date, "%Y-%m-%d")
    start_date = last_date + td(days=1)
    return str(start_date.date())  # convert back to string


def pull_dates(response: requests.models.Response) -> List:
    # Extract dates from NHL API response

    json_ = response.json()

    return [i["date"] for i in json_["dates"]]


def get_player_id(player_name: Text, teamId: int) -> int:
    """Get player ID given player name and teamId.
    
    Arguments:
        player_name {Text} -- Full name, as written in NHL database
        teamId {int} -- Team ID name, per NHL database
    
    Returns:
        int -- player ID in NHL database
    """

    params = {"expand": "team.roster", "teamId": teamId}

    res = requests.get(BASE_URL + TEAMS_ENDPOINT, params=params)
    roster = res.json()["teams"][0]["roster"]["roster"]
    player_to_id = {player["person"]["fullName"]:player["person"]["id"] for player in roster}

    return player_to_id[player_name]


def get_games():

    # Get all games after a certain date (last date in our csv)
    # Needs to be split out into smaller functions

    base_url = "https://statsapi.web.nhl.com/api/v1"
    teams = requests.get(f"{base_url}/teams").json()["teams"]

    caps_id = find_caps_id(teams)
    last_recorded_date = find_last_game()
    start_date = get_start_date(last_recorded_date)
    end_date = str(dt.now().date())

    params = {
        "startDate": start_date,
        "endDate": end_date,
        "teamId": caps_id,
        "gameType": ["R", "P"],
    }

    request_url = base_url + "/schedule"

    response = requests.get(request_url, params=params)

    return response


def get_game_stats(game_id: Text, player: Text):

    # TODO: set default player to ovechkin
    pass


# schedule

# test_request = requests.get()

results = {"results": {"stat_a": 1}}
