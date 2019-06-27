from urllib.request import Request, urlopen
from requests import Session
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from faker import Faker 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.select import Select
from random import randint
import random 
import string
import time

ua = UserAgent()  
proxies = []  

# Main function
def main():
  # Retrieve latest proxies
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 100):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 1 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      print("/-----------/")
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    fake = Faker(locale='en_GB') 
    firstname = fake.name().split( )[0]
    while "." in firstname:
      firstname = fake.name().split( )[0]
    lastname = fake.name().split( )[1]
    city = fake.city()
    postcode = fake.postcode()
  
    if randint(0, 1) == 1:
      name = firstname + lastname
      word_list = list(string.ascii_letters+string.digits) 
      random_string= "".join([random.choice(word_list) for i in range(4)]) 
      email = name+random_string
    else:
      name = firstname
      word_list = list(string.ascii_letters+string.digits) 
      number_list = list(string.digits) 
      random_string= "".join([random.choice(number_list) for i in range(1)]) 
      random_string_two= "".join([random.choice(word_list) for i in range(1)]) 
      email = random_string + name + random_string_two + city.replace(" ", "")
    
    if randint(0, 1) == 1:
      email = email+'@gmail.com'
    else:
      email = email+'@hotmail.com'

    chrome_options = Options()  
    #chrome_options.add_argument("--headless")  
    sel_proxy = proxy['ip'] + ':' + proxy['port']
    chrome_options.add_argument('--proxy-server=http://%s' % sel_proxy)

    driver = webdriver.Chrome(options=chrome_options)
    webpage = #test url 
    driver.get(webpage)  
    driver.implicitly_wait(10)

    if driver.find_elements_by_name("first_name"):
      print (driver.title)
      print ("Name: " + firstname + " " + lastname)
      print ("Email: " + email)

      elem = driver.find_element_by_name("first_name");
      elem.clear()
      elem.send_keys(firstname)
      elem.send_keys(Keys.RETURN)

      elem = driver.find_element_by_name("last_name");
      elem.clear()
      elem.send_keys(lastname)
      elem.send_keys(Keys.RETURN)

      if driver.find_element_by_class_name("js-email-signup"):
        elem = driver.find_element_by_class_name("js-email-signup");
        elem.clear()
        elem.send_keys(email)
        elem.send_keys(Keys.RETURN)
        
      if driver.find_element_by_name("city"): 
        elem = driver.find_element_by_name("city");
        elem.clear()
        elem.send_keys(city)
        elem.send_keys(Keys.RETURN)

      if driver.find_element_by_name("post_code"): 
        driver.find_element_by_name("post_code")
        elem = driver.find_element_by_name("post_code");
        elem.clear()
        elem.send_keys(postcode)
        elem.send_keys(Keys.RETURN)

      if driver.find_elements_by_name("box_consent"):
        elem = driver.find_elements_by_name("box_consent");
        elem[0].click();

      captcha = driver.findElement(By.xpath('//*[@id="left_content"]/div/div[4]/div[2]/div[2]/div/div//div[2]/div/div[4]/div/div/div[1]/div/div[2]/div[2]/div/div/iframe'));
      captcha.click();
      builder.moveToElement(captcha, 150, 130).click().build().perform();

      elem = driver.find_element_by_name("sign_form")
      elem.click();
      time.sleep(2);
      driver.close()

      print("/-----------/")

    else:
      driver.close()
    
# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
  main()