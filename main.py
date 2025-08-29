from helpers.dlVideo import dlVideo
from helpers.fetchCartoon import fetchCartoon
from helpers.fetchSeasons import fetchSeasons
from helpers.checkIfExists import checkIfExists, getExistingEpisodes
import os

cwd = os.getcwd()
os.makedirs(f"{cwd}/cartoons", exist_ok=True)
os.makedirs(f"{cwd}/cartoon_posters", exist_ok=True)

def get_season_range(total_seasons):
    '''Get season range from user input - supports mixed formats like "1-3,5,7-9"'''
    print(f"\n>> total seasons available: {total_seasons}")
    
    while True:
        try:
            range_input = input(f"> Enter season range to download (e.g., '1-3', '2,4,6', '1-3,5', or 'all'): ").strip().lower()
            
            if range_input == 'all':
                return list(range(1, total_seasons + 1))
            
            selected_seasons = []
            parts = range_input.split(',')
            
            for part in parts:
                part = part.strip()

                if '-' in part:
                    try:
                        start, end = part.split('-')
                        start, end = int(start.strip()), int(end.strip())
                        
                        if start < 1 or end > total_seasons or start > end:
                            print(f">> error: Invalid range '{part}'. Please enter ranges between 1 and {total_seasons}")
                            raise ValueError("Invalid range")
                            
                        selected_seasons.extend(range(start, end + 1))
                    except ValueError as e:
                        if "Invalid range" not in str(e):
                            print(f">> error: Invalid range format '{part}'. Use format like '1-3'")
                        raise
                
                else:
                    season = int(part)
                    if season < 1 or season > total_seasons:
                        print(f">> error: Invalid season number '{season}'. Please enter seasons between 1 and {total_seasons}")
                        raise ValueError("Invalid season")
                        
                    selected_seasons.append(season)
            
            selected_seasons = sorted(list(set(selected_seasons)))
            
            if not selected_seasons:
                print(">> error: No valid seasons specified. Please try again.")
                continue
                
            return selected_seasons
                
        except ValueError:
            print(">> error: Invalid input format. Please try again.")
            continue

cartoon_url = input("> Enter the cartoon url (e.g., https://www.wcoflix.tv/anime/batman-the-animated-series): ").strip()

cartoon_name, cartoon_path, links = fetchCartoon(cartoon_url)
if links:
    cartoon_path = os.path.join(f"{cwd}/cartoons", cartoon_path)
    
    print(f">> cartoon name: {cartoon_name}")
    print(f">> found {len(links)} episodes in total")

    seasons = fetchSeasons(links)
    total_seasons = len(seasons)
    
    print(f">> detected {total_seasons} season(s)")
    
    if total_seasons > 1:
        selected_seasons = get_season_range(total_seasons)
        print(f"\n>> selected seasons: {selected_seasons}\n")
    else:
        selected_seasons = [1]
        print(">> only 1 season available, downloading all episodes")

    missing_episodes = []
    total_episodes = 0
    skipped_episodes = 0

    for season_num in selected_seasons:
        if season_num in seasons:
            season_episodes = seasons[season_num]
            season_folder = f"S{season_num}"
            season_path = os.path.join(cartoon_path, season_folder)
            
            print(f">> processing season {season_num} with {len(season_episodes)} episodes")

            existing_episodes = getExistingEpisodes(season_path)
            if existing_episodes:
                print(f">> found {len(existing_episodes)} existing episodes in season {season_num}")
            
            for i, link in enumerate(season_episodes):
                episode_filename = f"S{season_num}E{i+1}"
                total_episodes += 1

                if checkIfExists(episode_filename, season_path):
                    print(f">> skipping {episode_filename} (already downloaded)")
                    skipped_episodes += 1
                    continue
                
                print(f">> downloading episode: {link}")
                success = dlVideo(link, episode_filename, season_path)
                
                if not success:
                    missing_episodes.append({
                        'url': link,
                        'filename': episode_filename,
                        'season_path': season_path,
                        'season': season_num,
                        'episode': i+1
                    })
        else:
            print(f">> warning: Season {season_num} not found in available seasons")

    if skipped_episodes > 0:
        print(f"\n>> skipped {skipped_episodes} already downloaded episodes")

    if missing_episodes:
        print(f"\n>> found {len(missing_episodes)} missing episodes, retrying downloads...")

        retry_missing = []
        for episode in missing_episodes:
            if checkIfExists(episode['filename'], episode['season_path']):
                print(f">> skipping retry for {episode['filename']} (now exists)")
                continue

            print(f">> retrying: S{episode['season']}E{episode['episode']}")
            success = dlVideo(episode['url'], episode['filename'], episode['season_path'])
            
            if not success:
                retry_missing.append(episode)

        if retry_missing:
            print(f"\n>> warning: {len(retry_missing)} episodes could not be downloaded:")
            for episode in retry_missing:
                print(f"   - S{episode['season']}E{episode['episode']}: {episode['url']}")
        else:
            print("\n>> all missing episodes successfully downloaded on retry!")
    else:
        if skipped_episodes == total_episodes:
            print("\n>> all episodes already downloaded!")
        else:
            print("\n>> all episodes downloaded successfully!")

else:
    print(">> error: cartoon not found or no episodes available.")