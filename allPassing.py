import os
import json
import requests
from bs4 import BeautifulSoup
import utility
import time

def scrape_passing_stats(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        tfoot = soup.find('tfoot')
        if tfoot:
            last_row = tfoot.find('tr')
            if last_row:
                passes_cell = last_row.find('td', {'data-stat': 'passes'})
                passes_pct_cell = last_row.find('td', {'data-stat': 'passes_pct'})
                if passes_cell and passes_pct_cell:
                    total_passes = passes_cell.text.strip()
                    passes_pct = passes_pct_cell.text.strip()

                    return total_passes, passes_pct

        return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request to {url}: {e}")
        return None, None

    except Exception as e:
        print(f"An error occurred while scraping data from {url}: {e}")
        return None, None

def scrape_corner_kick_stats(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'matchlogs_for'})

        if table:
            rows = table.find('tbody').find_all('tr')
            num_matches = 0
            total_corner_kicks = 0
            for row in rows:
                if row.find('th', {'data-stat': 'date'}) and row.find('td', {'data-stat': 'result'}):
                    num_matches += 1
                    corner_kick_elem = row.find('td', {'data-stat': 'corner_kicks'})
                    if corner_kick_elem and corner_kick_elem.text.strip().isdigit():
                        total_corner_kicks += int(corner_kick_elem.text.strip())

            corner_kick_per_match = total_corner_kicks / num_matches if num_matches > 0 else 0

            return num_matches, total_corner_kicks, corner_kick_per_match

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request to {url}: {e}")
        return None, None, None

    except Exception as e:
        print(f"An error occurred while scraping data from {url}: {e}")
        return None, None, None

def scrape_teams_allPassing_stats(team_urls):
    teams_data = []

    for url, team_name in team_urls:
        total_passes, passes_pct = scrape_passing_stats(url)

        corner_url = url.replace("/passing/", "/passing_types/")
        num_matches, total_corner_kicks, corner_kick_per_match = scrape_corner_kick_stats(corner_url)

        if total_passes is not None and passes_pct is not None and num_matches is not None:
            team_data = {
                "team_name": team_name,
                "passes": total_passes,
                "passes_pct": passes_pct,
                "played_matches": num_matches,
                "corner_kick_number": total_corner_kicks,
                "corner_kick_number_per_match": corner_kick_per_match
            }
            teams_data.append(team_data)
        else:
            print(f"Stats not found for {team_name}")

    return teams_data

def save_teams_allPassings_stats_json(teams_data, season):
    os.makedirs("allPassings", exist_ok=True)
    filepath = f"allPassings/{season}_allPassing_stats.json"

    with open(filepath, 'w') as json_file:
        json.dump(teams_data, json_file, indent=4)

    print(f"All teams' passing stats for {season} saved to '{filepath}'")

if __name__ == "__main__":
    team_mappings = utility.read_team_mappings("team_mappings.txt")

    # Define seasons to scrape
    seasons = utility.get_seasons()

    for season in seasons:
        team_urls = []

        for team_name, team_key in team_mappings.items():
            url = f"https://fbref.com/en/squads/{team_key}/{season}/matchlogs/all_comps/passing/{team_name}-Match-Logs-All-Competitions"
            team_urls.append((url, team_name))

        teams_data = scrape_teams_allPassing_stats(team_urls)
        save_teams_allPassings_stats_json(teams_data, season)

        # Introduce a delay of 30 seconds after scraping each season
        time.sleep(30)
