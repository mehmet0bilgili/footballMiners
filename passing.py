import os
import requests
from bs4 import BeautifulSoup
import json
import utility

def scrape_passing_stats(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the last row in the tfoot element
        tfoot = soup.find('tfoot')
        if tfoot:
            last_row = tfoot.find('tr')
            if last_row:
                # Find the cells with passes and passes_pct
                passes_cell = last_row.find('td', {'data-stat': 'passes'})
                passes_pct_cell = last_row.find('td', {'data-stat': 'passes_pct'})
                if passes_cell and passes_pct_cell:
                    # Extract the text content of the cells
                    total_passes = passes_cell.text.strip()
                    passes_pct = passes_pct_cell.text.strip()

                    return total_passes, passes_pct

        # If we couldn't find the required values
        return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request to {url}: {e}")
        return None, None

    except Exception as e:
        print(f"An error occurred while scraping data from {url}: {e}")
        return None, None

def scrape_teams_passing_stats(team_urls):
    teams_data = []

    for url, team_name in team_urls:
        total_passes, passes_pct = scrape_passing_stats(url)
        if total_passes is not None and passes_pct is not None:
            team_data = {
                "team_name": team_name,
                "passes": total_passes,
                "passes_pct": passes_pct
            }
            teams_data.append(team_data)
        else:
            print(f"Passing stats not found for {team_name}")

    return teams_data

def save_teams_passing_stats_json(teams_data):
    os.makedirs("passing", exist_ok=True)

    filepath = "passing/teams_passing_stats.json"
    with open(filepath, 'w') as json_file:
        json.dump(teams_data, json_file, indent=4)

    print(f"All teams' passing stats saved to '{filepath}'")


if __name__ == "__main__":
    team_mappings = utility.read_team_mappings("team_mappings.txt")

    team_urls = []

    for team_name, team_key in team_mappings.items():
        passing_url = f"https://fbref.com/en/squads/{team_key}/2023-2024/matchlogs/all_comps/passing/{team_name}-Match-Logs-All-Competitions"
        team_urls.append((passing_url, team_name))

    teams_data = scrape_teams_passing_stats(team_urls)
    save_teams_passing_stats_json(teams_data)
