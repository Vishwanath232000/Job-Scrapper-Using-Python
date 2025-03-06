import requests
from bs4 import BeautifulSoup
import pymongo
import re


#Setting up MongoDB connection
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["cedars_sinai_jobs"]
    table = db["job_scrapping"]
    print("Connected to MongoDB successfully.")
except pymongo.errors.PyMongoError as e:
    print(f"MongoDB Connection Error: {e}")
    exit(1)  # Exit if database connection fails


#   Search URL and headers
search_url = "https://careers.cshs.org/search-jobs?utm_source=google.com&utm_medium=paid_search&utm_campaign=Healthcare_Jobs&utm_content=search_engine&utm_term=343201292&ss=paid&gad_source=1&gclid=CjwKCAiAk8G9BhA0EiwAOQxmfr-pO26RLmIiTENJCSCal6S-R11SBlss1_ZwbWcX1ks8FQlj-dX9jBoCSAwQAvD_BwE"
# Use below url if given above does not work
# search_url = "https://careers.cshs.org/search-jobs"

base_url = "https://careers.cshs.org"
headers = {"User-Agent": "Mozilla/5.0"}

# Attempting to fetch the job listings page
try:
    response = requests.get(search_url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise error for non-200 responses
    soup = BeautifulSoup(response.text, "html.parser")
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch job listings: {e}")
    exit(1)  # Exit if the request fails

# Extract job from each job in that page
jobs = []
for job_card in soup.select("#search-results-list ul li"):
    try:
        job_link = job_card.find("a")
        title = job_link.find("h2").text.strip() if job_link and job_link.find("h2") else "N/A"
        department = job_card.select_one(".job-info .cat2").text.strip() if job_card.select_one(".job-info .cat2") else "N/A"
        location = job_card.select_one(".job-location").text.strip() if job_card.select_one(".job-location") else "N/A"
        job_url = base_url + job_link["href"] if job_link and "href" in job_link.attrs else ""

        if not job_url:
            continue
        # Fetching job details
        try:
            job_response = requests.get(job_url, headers=headers, timeout=10)
            job_response.raise_for_status()
            job_soup = BeautifulSoup(job_response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch job details for {title}: {e}")
            continue

        # Extracting responsibilities
        responsibilities_section = job_soup.find("div", class_="job-details__description-content",
                                                 attrs={"data-bind": "html: pageData().job.description"})
        responsibilities = ""
        if responsibilities_section:
            text = responsibilities_section.get_text("\n").strip()
            match = re.search(r'What will you be doing in this role\?\n(.*?)(?:\n[A-Z]|$)', text, re.DOTALL)
            responsibilities = match.group(1).strip() if match else text  # Fallback to full text

        # Extracting qualifications
        qualifications_section = job_soup.find("div", class_="job-details__description-content",
                                               attrs={"data-bind": "html: pageData().job.qualifications"})
        qualifications = qualifications_section.get_text("\n").strip() if qualifications_section else "N/A"

        # Creating a job JSON object
        job = {
            "title": title,
            "department": department,
            "location": location,
            "url": job_url,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
        }

        jobs.append(job)

    except Exception as e:
        print(f"Error processing a job card: {e}")
        continue

#Inserting into MongoDB
if jobs:
    try:
        # Inserting into MongoDb
        table.insert_many(jobs)

        #printing all the jobs found
        for job_info in jobs:
            print(job_info)
        print(f"Inserted {len(jobs)} job listings into MongoDB.")
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB Insertion Error: {e}")
else:
    print("No jobs found or extracted.")
