import os
import json
import requests
import utility
import time
from bs4 import BeautifulSoup

def scrape_misc_stats(team_urls):
    teams_data = []

    for url, team_name in team_urls:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'matchlogs_for'})

            if table:
                rows = table.find('tbody').find_all('tr')
                
                num_matches = 0
                total_red_cards = 0
                total_yellow_cards = 0
                total_offsides = 0

                for row in rows:
                    if row.find('th', {'data-stat': 'date'}) and row.find('td', {'data-stat': 'result'}):
                        num_matches += 1

                        red_cards_elem = row.find('td', {'data-stat': 'cards_red'})
                        yellow_cards_elem = row.find('td', {'data-stat': 'cards_yellow'})
                        offsides_elem = row.find('td', {'data-stat': 'offsides'})

                        if red_cards_elem and red_cards_elem.text.strip().isdigit():
                            total_red_cards += int(red_cards_elem.text.strip())

                        if yellow_cards_elem and yellow_cards_elem.text.strip().isdigit():
                            total_yellow_cards += int(yellow_cards_elem.text.strip())

                        if offsides_elem and offsides_elem.text.strip().isdigit():
                            total_offsides += int(offsides_elem.text.strip())

                # Calculate derived statistics
                red_cards_per_match = total_red_cards / num_matches if num_matches > 0 else 0
                yellow_cards_per_match = total_yellow_cards / num_matches if num_matches > 0 else 0
                offsides_per_match = total_offsides / num_matches if num_matches > 0 else 0

                # Prepare team data
                team_stats = {
                    'team_name': team_name,
                    'played_matches': num_matches,
                    'red_card_number': total_red_cards,
                    'red_card_per_match': red_cards_per_match,
                    'yellow_card_number': total_yellow_cards,
                    'yellow_card_per_match': yellow_cards_per_match,
                    'offsides_number': total_offsides,
                    'offsides_per_match': offsides_per_match
                }

                teams_data.append(team_stats)

    return teams_data

def save_teams_misc_stats_json(teams_data, season):
    os.makedirs("misc", exist_ok=True)
    filepath = f"misc/{season}_misc_stats.json"

    with open(filepath, 'w') as json_file:
        json.dump(teams_data, json_file, indent=4)

    print(f"Teams match statistics for {season} saved to '{filepath}'")

if __name__ == "__main__":
    team_mappings = utility.read_team_mappings("team_mappings.txt")

    seasons = utility.get_seasons()

    for season in seasons:
        team_urls = []

        for team_name, team_key in team_mappings.items():
            misc_url = f"https://fbref.com/en/squads/{team_key}/{season}/matchlogs/all_comps/misc/{team_name}-Match-Logs-All-Competitions"
            team_urls.append((misc_url, team_name))  

        teams_data = scrape_misc_stats(team_urls)
        save_teams_misc_stats_json(teams_data, season)

        time.sleep(30)
