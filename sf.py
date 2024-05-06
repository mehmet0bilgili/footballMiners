import os
import requests
from bs4 import BeautifulSoup
import json

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
    urls = [
        (
        "https://fbref.com/en/squads/822bd0ba/2023-2024/matchlogs/all_comps/schedule/Liverpool-Scores-and-Fixtures-All-Competitions",
        "Liverpool"),
        (
        "https://fbref.com/en/squads/18bb7c10/2023-2024/matchlogs/all_comps/schedule/Arsenal-Scores-and-Fixtures-All-Competitions",
        "Arsenal"),
        (
        "https://fbref.com/en/squads/8602292d/2023-2024/matchlogs/all_comps/schedule/Aston-Villa-Scores-and-Fixtures-All-Competitions",
        "Aston Villa"),
        (
        "https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/all_comps/schedule/Manchester-City-Scores-and-Fixtures-All-Competitions",
        "Manchester City"),
        (
        "https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/all_comps/schedule/Tottenham-Hotspur-Scores-and-Fixtures-All-Competitions",
        "Tottenham Hotspur"),
        (
        "https://fbref.com/en/squads/19538871/2023-2024/matchlogs/all_comps/schedule/Manchester-United-Scores-and-Fixtures-All-Competitions",
        "Manchester United"),
        (
        "https://fbref.com/en/squads/7c21e445/2023-2024/matchlogs/all_comps/schedule/West-Ham-United-Scores-and-Fixtures-All-Competitions",
        "West Ham United"),
        (
        "https://fbref.com/en/squads/d07537b9/2023-2024/matchlogs/all_comps/schedule/Brighton-and-Hove-Albion-Scores-and-Fixtures-All-Competitions",
        "Brighton and Hove Albion"),
        (
        "https://fbref.com/en/squads/8cec06e1/2023-2024/matchlogs/all_comps/schedule/Wolverhampton-Wanderers-Scores-and-Fixtures-All-Competitions",
        "Wolverhampton Wanderers"),
        (
        "https://fbref.com/en/squads/b2b47a98/2023-2024/matchlogs/all_comps/schedule/Newcastle-United-Scores-and-Fixtures-All-Competitions",
        "Newcastle United"),
        (
        "https://fbref.com/en/squads/cff3d9bb/2023-2024/matchlogs/all_comps/schedule/Chelsea-Scores-and-Fixtures-All-Competitions",
        "Chelsea"),
        (
        "https://fbref.com/en/squads/fd962109/2023-2024/matchlogs/all_comps/schedule/Fulham-Scores-and-Fixtures-All-Competitions",
        "Fulham"),
        (
        "https://fbref.com/en/squads/4ba7cbea/2023-2024/matchlogs/all_comps/schedule/Bournemouth-Scores-and-Fixtures-All-Competitions",
        "Bournemouth"),
        (
        "https://fbref.com/en/squads/47c64c55/2023-2024/matchlogs/all_comps/schedule/Crystal-Palace-Scores-and-Fixtures-All-Competitions",
        "Crystal Palace"),
        (
        "https://fbref.com/en/squads/cd051869/2023-2024/matchlogs/all_comps/schedule/Brentford-Scores-and-Fixtures-All-Competitions",
        "Brentford"),
        (
        "https://fbref.com/en/squads/d3fd31cc/2023-2024/matchlogs/all_comps/schedule/Everton-Scores-and-Fixtures-All-Competitions",
        "Everton"),
        (
        "https://fbref.com/en/squads/e297cd13/2023-2024/matchlogs/all_comps/schedule/Luton-Town-Scores-and-Fixtures-All-Competitions",
        "Luton Town"),
        (
        "https://fbref.com/en/squads/e4a775cb/2023-2024/matchlogs/all_comps/schedule/Nottingham-Forest-Scores-and-Fixtures-All-Competitions",
        "Nottingham Forest"),
        (
        "https://fbref.com/en/squads/943e8050/2023-2024/matchlogs/all_comps/schedule/Burnley-Scores-and-Fixtures-All-Competitions",
        "Burnley"),
        (
        "https://fbref.com/en/squads/1df6b87e/2023-2024/matchlogs/all_comps/schedule/Sheffield-United-Scores-and-Fixtures-All-Competitions",
        "Sheffield United")
    ]

    for url, team_name in urls:
        scrape_and_write_to_json(url, team_name)