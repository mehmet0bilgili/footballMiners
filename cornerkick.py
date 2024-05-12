import os
import json
import requests
import utility
from bs4 import BeautifulSoup


def corner_kick_percentage_for_teams(team_urls):
    teams_data = []

    for url, team_name in team_urls:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'matchlogs_for'})

            if table:
                rows = table.find('tbody').find_all('tr')
                num_matches = 0
                total_Corner_Kick = 0
                for row in rows:
                    if row.find('th', {'data-stat': 'date'}) and row.find('td', {'data-stat': 'result'}):
                        num_matches += 1
                        corner_kick_elem = row.find('td', {'data-stat': 'corner_kicks'})
                        if corner_kick_elem and corner_kick_elem.text.strip().isdigit():
                            total_Corner_Kick += int(corner_kick_elem.text.strip())

                # Calculate derived statistics
                corner_kick_per_match = total_Corner_Kick / num_matches if num_matches > 0 else 0

                # Prepare team data
                team_stats = {
                    'team_name': team_name,
                    'played_matches': num_matches,
                    'corner_kick_number': total_Corner_Kick,
                    'corner_kick_number_per_match': corner_kick_per_match,

                }

                teams_data.append(team_stats)

    return teams_data


def save_teams_corner_stats_json(teams_data):
    os.makedirs("corner", exist_ok=True)
    filepath = "corner/team_corner_stats.json"

    with open(filepath, 'w') as json_file:
        json.dump(teams_data, json_file, indent=4)

    print(f"Teams match statistics saved to '{filepath}'")


if __name__ == "__main__":
    team_mappings = utility.read_team_mappings("team_mappings.txt")

    team_urls = []

    for team_name, team_key in team_mappings.items():
        corner_url = f"https://fbref.com/en/squads/{team_key}/2023-2024/matchlogs/all_comps/passing_types/{team_name}-Match-Logs-All-Competitions"
        team_urls.append((corner_url, team_name))

        # Scrape teams statistics
    teams_data = corner_kick_percentage_for_teams(team_urls)

    # Save teams statistics to JSON file
    save_teams_corner_stats_json(teams_data)