# Project Description: Course Module Filtering System

This project aims to develop a filtering system for course modules, addressing the current limitations in course selection. The existing system lacks the ability to filter courses based on specific criteria, such as campus location, the semester (Fall/Spring) in which the courses are offered, the credit level (ranging from 3 to 7, indicating the course's difficulty and the typical stage at which students take it), and the number of credits each course awards. By implementing these filters, students will be able to efficiently narrow down their course options, ensuring they can select modules that align with their academic needs and preferences.


- Currently only works for specific course lists (could integrate an AI API for this?)

# Challenges/Problems I researched solutions for

1) **Connecting to Module Web Server**
   - When I first tried scraping the page, I would get an error that said connection was being blocked. 
     - [This is because web servers can be set up to detect bots and automated scripts based on information in default HTTP headers, such as User-Agent, Referer, and Accept-Language](https://brightdata.com/blog/web-data/http-headers-for-web-scraping#:~:text=This%20is%20because%20web%20servers,reliability%20of%20your%20scraping%20operations.)
    - Solved this by incorporating headers to my request in the beautifulsoup4 response.get() function.
     ```python
      headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
  
      response = requests.get(url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
     ```
2) **Beautifulsoup4 only supports scraping static HTML Pages and not pages that dynamically load information using JavaScript**
   - After fixing the network connection error, I successfully scraped the HTML from the page. However I quickly realized that not all the page elements were being saved and when I printed out the HTML, it was very small and didn't contain everything.
   - I then researched what was going on and realized it was due to HTML being dynamically loaded JavaScript in the backend. From here I knew I had to somehow simulate having all the HTML be loaded.
   - I found a python tool called **Selenium** that was a solution to my problem. I learned that Selenium simulates running a webpage and after a certain timeout period, it will bring the response content. After trying this, all the HTML elements were able to be scraped from the Course Module Page since all the elements loaded into my data structure.

