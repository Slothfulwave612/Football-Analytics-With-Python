from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# ready the chrome-drivers
driver = webdriver.Chrome("C:/Chrome_Drivers/chromedriver", options=options)

for i in range(1, 20000):
    link = f"https://understat.com/match/{str(i)}"
    
    try:
        driver.get(link)

        # get the match data
        content = driver.execute_script("return shotsData;")
        
        xg_file = open(f"{str(i)}.json", "w")
        json.dump(content, xg_file, indent=2)
        xg_file.close()
        
    except Exception as e:
        print(f"Match ID {i} not present")

# close the driver
driver.close()