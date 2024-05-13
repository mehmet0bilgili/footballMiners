def read_team_mappings(mapping_file):
    team_mappings = {}
    with open(mapping_file, 'r') as file:
        for line in file:
            if line.strip():
                team_name, team_key = line.strip().split(',')
                team_mappings[team_name] = team_key
    return team_mappings


def get_seasons():
    return ["2023-2024", "2022-2023", "2021-2022", "2020-2021", "2019-2020"]
