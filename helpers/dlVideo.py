from helpers.fetchDLLink import fetchDLLink
import requests
import os
import time

def dlVideo(url, filename, directory):
    '''Downloads the video from the given URL and saves it to the specified filename and directory'''
    start_time = time.time()
    if not url or not filename or not directory:
        print(">> error: URL, filename, and directory must be provided.")
        return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
    }

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f">> created directory: {directory}")

    filepath = os.path.join(directory, filename + ".mp4")

    try:
        dl_link = fetchDLLink(url)
        if not dl_link:
            print(">> failed to fetch download link")
            return False

        clean_url = dl_link.replace('\\/', '/').replace('\\\\', '\\')
        response = requests.get(clean_url, headers=headers)

        if response.status_code == 200:
            with open(filepath, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=8192):
                    video_file.write(chunk)
            end_time = time.time()
            print(f">> video downloaded successfully to {filepath} ({round(end_time - start_time, 2)} seconds)")
            return True
        else:
            print(f">> failed to download video. Status code: {response.status_code}")
            return False

    except Exception as e:
        print(f">> an error occurred while downloading the video: {e}")
        return False
