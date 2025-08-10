import os

def checkIfExists(filename, directory):
    '''Check if a video file already exists in the specified directory'''
    if not filename or not directory:
        return False

    filepath = os.path.join(directory, filename + ".mp4")
    
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return True
    
    return False

def getExistingEpisodes(directory):
    '''Get a list of all existing episode files in a directory'''
    if not os.path.exists(directory):
        return []
    
    existing_episodes = []
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            episode_name = filename[:-4]
            existing_episodes.append(episode_name)
    
    return existing_episodes