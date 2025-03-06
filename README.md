This Python script scrapes job listings from the Cedars-Sinai Careers website, extracts job details (title, department, location, responsibilities, and qualifications), and stores them in a MongoDB database.

Prerequisites
To run this script, you need:

Python 3
MongoDB running locally or a remote MongoDB instance
Required Python packages: requests, beautifulsoup4, and pymongo
Setup
1. Clone the Repository
Clone this repository to your local machine.
git@github.com:Vishwanath232000/Job-Scrapper-Using-Python.git
cd cedars-sinai-job-scraping
2. Install Dependencies
You can install the required dependencies using pip.The dependencies used:
requests
beautifulsoup4
pymongo
3. Set Up MongoDB
Make sure you have MongoDB installed and running. If you're running MongoDB locally, the default connection is mongodb://localhost:27017/.

If you need a remote MongoDB instance, you can update the MongoClient URL in the script accordingly.

4. Configure Database
By default, the script connects to a MongoDB database named cedars_sinai_jobs and a collection named job_scrapping. You can modify these in the script if necessary.

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["cedars_sinai_jobs"]
table = db["job_scrapping"]

5. Run the Script
After setting up the dependencies and MongoDB, you can run the script using:
python job_scraper.py
The script will scrape the job listings from the Cedars-Sinai Careers website, extract details, and insert the data into the MongoDB collection.

Features:
Scrapes job listings (title, department, location).
Fetches job details (responsibilities and qualifications).
Stores the data in a MongoDB database.
How It Works:
The script first attempts to connect to the MongoDB instance.
It then fetches job listings from the Cedars-Sinai careers page.
For each job listing, the script extracts the title, department, location, job URL, responsibilities, and qualifications.
Finally, it inserts all the job details into the MongoDB collection and prints the information for review.
Handling Errors:
If MongoDB connection fails, the script will terminate with an error message.
If the request to the Cedars-Sinai website fails, the script will handle the exception and print an error message.
If the data extraction for any job listing fails, the script will skip that job and continue scraping the remaining listings.
