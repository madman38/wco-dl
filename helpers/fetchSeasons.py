import re
from collections import defaultdict

def fetchSeasons(links):
    '''Organizes episode links by season number, returns a dictionary with seasons as keys.
    Excludes links that don't contain season or episode indicators (like extras/shorts).'''
    seasons = defaultdict(list)
    
    for link in links:
        has_season = re.search(r'season-(\d+)', link, re.IGNORECASE)
        has_episode = re.search(r'episode', link, re.IGNORECASE)
        
        if not has_season and not has_episode:
            continue
            
        if has_season:
            season_num = int(has_season.group(1))
        else:
            season_num = 1
        
        seasons[season_num].append(link)

    sorted_seasons = {}
    for season_num in sorted(seasons.keys()):
        sorted_seasons[season_num] = seasons[season_num]
    
    return sorted_seasons