from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetchCartoon(url):
    '''Fetches cartoon name and all episode links from the sidebar, returns them in correct order (first episode first)'''
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    print(">> fetching cartoon data")
    print(">> running selenium in headless mode")
    
    driver = webdriver.Firefox(options=options)
    episode_links = []
    cartoon_name = ""
    
    try:
        driver.get(url)        
        wait = WebDriverWait(driver, 10)
        
        try:
            cartoon_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/h1/div/a')))
            cartoon_name = cartoon_element.text.strip()

            unwanted_chars = ['\\', '/', ':', '"', '?', '<', '>', '|']
            cartoon_path = cartoon_name
            for char in unwanted_chars:
                cartoon_path = cartoon_path.replace(char, '')
            cartoon_path = cartoon_path.replace(' ', '_')

            print(f">> found cartoon: {cartoon_name}")
        except:
            print(">> warning: could not extract cartoon name")

        sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar_right3"]')))
        episode_divs = sidebar.find_elements(By.CLASS_NAME, "cat-eps")
        
        for div in episode_divs:
            try:
                link_element = div.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")
                if href:
                    episode_links.append(href)
            except:
                print(">> warning: could not extract link from div")

        episode_links.reverse()
        
        print(f">> found {len(episode_links)} episodes in total")
        return cartoon_name, cartoon_path, episode_links
        
    except:
        print(">> error fetching episode links")
        return False
   
    finally:
        driver.quit()
