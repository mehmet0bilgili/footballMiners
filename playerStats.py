import os
import requests
from bs4 import BeautifulSoup
import json
import utility  # Import your utility module containing read_team_mappings function

def scrape_team_player_stats(team_url, team_name):
    # Send a GET request to the team URL
    response = requests.get(team_url)
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Initialize an empty list to store player data
    player_data = []
    
    # Find the table containing standard player statistics
    standardStatTable = soup.find("table", {"id": "stats_standard_9"})
    
    # Find the table containing shooting statistics
    shootingStatTable = soup.find("table", {"id": "stats_shooting_9"})
    
    # Find the table containing goal and shot creating actions (GCA) statistics
    gcaStatTable = soup.find("table", {"id": "stats_gca_9"})
    
    # Find the table containing passing statistics
    passingStatTable = soup.find("table", {"id": "stats_passing_9"})

    #defense statitics
    defenseStatTable = soup.find("table", {"id": "stats_defense_9"})
    
    # Loop through each row in the standard statistics table
    for row in standardStatTable.find("tbody").find_all("tr"):
        # Extract player data elements
        name = row.find("th", {"data-stat": "player"}).text.strip()
        position = row.find("td", {"data-stat": "position"}).text.strip()
        age = row.find("td", {"data-stat": "age"}).text.strip()
        games = int(row.find("td", {"data-stat": "games"}).text.strip())
        games_starts = int(row.find("td", {"data-stat": "games_starts"}).text.strip())
        minutes_text = row.find("td", {"data-stat": "minutes"}).text.strip().replace(",", "")
        minutes_played = int(minutes_text) if minutes_text else 0
        
        # Handle goals data
        goals_text = row.find("td", {"data-stat": "goals"}).text.strip()
        goals = int(goals_text) if goals_text else 0
        
        # Handle assists data
        assists_text = row.find("td", {"data-stat": "assists"}).text.strip()
        assists = int(assists_text) if assists_text else 0

        xG_text = row.find("td", {"data-stat": "xg"}).text.strip()
        xG = float(xG_text) if xG_text else 0

        xGA_text = row.find("td", {"data-stat": "xg_assist"}).text.strip()
        xGA = float(xGA_text) if xGA_text else 0
        
        # Handle yellow cards data
        yellow_cards_text = row.find("td", {"data-stat": "cards_yellow"}).text.strip()
        yellow_cards = int(yellow_cards_text) if yellow_cards_text else 0
        
        # Handle red cards data
        red_cards_text = row.find("td", {"data-stat": "cards_red"}).text.strip()
        red_cards = int(red_cards_text) if red_cards_text else 0
        
        # Initialize shooting statistics
        shots = 0
        shots_on_target = 0
        shots_on_target_pct = 0.0
        
        # Find corresponding shooting statistics for the player in the shooting table
        for shooting_row in shootingStatTable.find("tbody").find_all("tr"):
            if shooting_row.find("th", {"data-stat": "player"}).text.strip() == name:
                shots = int(shooting_row.find("td", {"data-stat": "shots"}).text.strip())
                shots_on_target = int(shooting_row.find("td", {"data-stat": "shots_on_target"}).text.strip())
                shots_on_target_pct_text = shooting_row.find("td", {"data-stat": "shots_on_target_pct"}).text.strip()
                if shots_on_target_pct_text:
                    shots_on_target_pct = float(shots_on_target_pct_text)
                break
        
        # Initialize GCA statistics
        sca = 0
        sca_per90 = 0.0
        gca = 0
        gca_per90 = 0.0
        
        # Find corresponding GCA statistics for the player in the GCA table
        for gca_row in gcaStatTable.find("tbody").find_all("tr"):
            if gca_row.find("th", {"data-stat": "player"}).text.strip() == name:
                sca_text = gca_row.find("td", {"data-stat": "sca"}).text.strip()
                if sca_text:
                    sca = int(sca_text)
                
                sca_per90_text = gca_row.find("td", {"data-stat": "sca_per90"}).text.strip()
                if sca_per90_text:
                    sca_per90 = float(sca_per90_text)
                
                gca_text = gca_row.find("td", {"data-stat": "gca"}).text.strip()
                if gca_text:
                    gca = int(gca_text)
                
                gca_per90_text = gca_row.find("td", {"data-stat": "gca_per90"}).text.strip()
                if gca_per90_text:
                    gca_per90 = float(gca_per90_text)
                
                break
        
        # Initialize passing statistics
        passes = 0
        passes_pct = 0.0
        
        # Find corresponding passing statistics for the player in the passing table
        for passing_row in passingStatTable.find("tbody").find_all("tr"):
            if passing_row.find("th", {"data-stat": "player"}).text.strip() == name:
                passes_text = passing_row.find("td", {"data-stat": "passes"}).text.strip()
                if passes_text:
                    passes = int(passes_text)
                passes_pct_text = passing_row.find("td", {"data-stat": "passes_pct"}).text.strip()
                if passes_pct_text:
                    passes_pct = float(passes_pct_text)
                break

        tackles_won = 0
        interceptions = 0

        for defense_row in defenseStatTable.find("tbody").find_all("tr"):
            if defense_row.find("th", {"data-stat": "player"}).text.strip() == name:
                tackles_won_text = defense_row.find("td", {"data-stat": "tackles_won"}).text.strip()
                if tackles_won_text:
                    tackles_won = int(tackles_won_text)
                interceptions_text = defense_row.find("td", {"data-stat": "interceptions"}).text.strip()
                if interceptions_text:
                    interceptions = int(interceptions_text)
                break
        
        # Create a dictionary representing the player's data
        player_info = {
            "name": name,
            "position": position,
            "age": age,
            "games": games,
            "games_starts": games_starts,
            "minutes_played": minutes_played,
            "goals": goals,
            "assists": assists,
            "xG": xG,
            "XGA": xGA,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
            "shots": shots,
            "shots_on_target": shots_on_target,
            "shots_on_target_pct": shots_on_target_pct,
            "sca": sca,
            "sca_per90": sca_per90,
            "gca": gca,
            "gca_per90": gca_per90,
            "passes": passes,
            "passes_pct": passes_pct,
            "tackles_won": tackles_won,
            "interceptions": interceptions
        }
        
        # Append the player's data to the list
        player_data.append(player_info)
    
    # Ensure the 'playerStats' directory exists
    os.makedirs("playerStats", exist_ok=True)
    
    # Save player data as JSON file with proper formatting
    filename = f"playerStats/{team_name}_player_stats.json"
    with open(filename, "w") as outfile:
        json.dump(player_data, outfile, indent=4)
    
    print(f"Player data with stats for {team_name} saved to {filename}")

if __name__ == "__main__":
    # Read team mappings from the utility module
    team_mappings = utility.read_team_mappings("team_mappings.txt")
    
    # Iterate through each team and scrape player statistics
    for team_name, team_key in team_mappings.items():
        # Generate team URL using team_key and team_name
        team_url = f"https://fbref.com/en/squads/{team_key}/{team_name}-Stats"
        # Scrape player statistics (standard, shooting, and GCA) for the current team
        scrape_team_player_stats(team_url, team_name)
