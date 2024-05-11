import os
import requests
from bs4 import BeautifulSoup
import json
import utility

def scrape_and_write_to_json(url, team_name):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables containing the match data
        tables = soup.find_all('table', class_='stats_table')

        # Initialize dictionary to store data
        team_data = {
            "team_name": team_name,
            "fixtures_scores": []
        }

        # Iterate over all tables
        for table in tables:
            # Extract table rows
            rows = table.find('tbody').find_all('tr')

            # Iterate over rows and append data to the list
            for row in rows:
                # Extract data from each row
                data = [td.text.strip() for td in row.find_all('td')]

                # Extract date from the first column
                date = row.find('th').text.strip() if row.find('th') else ""

                # Ensure there are enough values in the data list
                if len(data) >= 17:
                    # Add data to the dictionary
                    fixture_score = {
                        "Date": date,
                        "Time": data[0],
                        "Comp": data[1],
                        "Round": data[2],
                        "Day": data[3],
                        "Venue": data[4],
                        "Result": data[5],
                        "GF": data[6],
                        "GA": data[7],
                        "Opponent": data[8],
                        "xG": data[9],
                        "xGA": data[10],
                        "Poss": data[11],
                        "Attendance": data[12],
                        "Captain": data[13],
                        "Formation": data[14],
                        "Referee": data[15],
                        "Match Report": data[16],
                        "Notes": data[17] if len(data) >= 18 else ""
                    }
                    team_data["fixtures_scores"].append(fixture_score)

        # Create the directory if it doesn't exist
        os.makedirs("scoresFixtures", exist_ok=True)

        # Write data to JSON file
        filepath = f"scoresFixtures/{team_name}_scores_fixtures.json"
        with open(filepath, 'w') as json_file:
            json.dump(team_data, json_file, indent=4)

        print(f"Data from {url} has been written to '{filepath}' successfully.")
    except Exception as e:
        print(f"An error occurred while scraping data from {url}: {e}")




if __name__ == "__main__":
    team_mappings = utility.read_team_mappings("team_mappings.txt")

    team_urls = []
    for team_name, team_key in team_mappings.items():
        url = f"https://fbref.com/en/squads/{team_key}/2023-2024/matchlogs/all_comps/schedule/{team_name}-Scores-and-Fixtures-All-Competitions"
        team_urls.append((url, team_name))

    for url, team_name in team_urls:
        scrape_and_write_to_json(url, team_name)