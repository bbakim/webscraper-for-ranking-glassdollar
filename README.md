# webscraper-for-ranking-glassdollar
The code that retrieves the information of the most startup-friendly companies using web scraping.

To execute the code, please run "pip install requirements.txt" command. Then run "python main.py". To get the results, open the given "http://localhost:8000/fetch-and-save-data" URL from any browser. In a few minutes the results will be saved as json file to the same directory with main.py.

To execute the code with docker, please run "docker build -t your-image-name:tag ." on the same directory with main.py. After building the package, run "docker run -d -p 8000:8000 your-image-name:tag". To see results run "docker run -d -p 8000:8000 -v /path/on/host:/path/in/container enterprise_ranking_scraper:tag" instead. Replace /path/on/host with the directory on your host machine where you want to save the CSV file, and /path/in/container with the corresponding directory inside the container where your application writes the file. To copy files from container, run "docker cp container_id:/path/in/container/filename.csv /path/on/host". Run "docker stop <container_id>" to stop the container. Run "docker rm <container_id>" to remove the container.
