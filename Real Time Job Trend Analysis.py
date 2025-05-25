!pip install selenium
!apt-get update
!apt install chromium-chromedriver -y
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install pyngrok
!pip install streamlit
!pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_remoteok(keyword="data scientist"):
    url = f"https://remoteok.com/remote-{keyword.replace(' ', '-')}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find_all("tr", class_="job")

    print("🧠 Found", len(jobs), "job listings in HTML")

    data = []

    for job in jobs:
        try:
            title = job.find("h2").text.strip()
            company = job.find("h3").text.strip()
            location = job.find("div", class_="location").text.strip()
            date_posted = job.find("time")["datetime"]
            tags = [tag.text for tag in job.find_all("span", class_="tag")]
        except:
            continue

        data.append({
            "Portal": "RemoteOK",
            "Title": title,
            "Company": company,
            "Location": location,
            "DatePosted": date_posted,
            "Skills": ", ".join(tags)
        })

    return pd.DataFrame(data)


df = scrape_remoteok("developer")
print(f"✅ Scraped {len(df)} jobs")

df.to_csv("remoteok_jobs.csv", index=False)
df.head()


import pandas as pd

df_verify = pd.read_csv("remoteok_jobs.csv")

print(f"📦 Rows fetched: {df_verify.shape[0]} | Columns: {df_verify.shape[1]}")
df_verify.head()


import pandas as pd

df = pd.read_csv("remoteok_jobs.csv")

top_titles = df["Title"].value_counts().head(5)
print("🔥 Top 5 Job Titles:")
print(top_titles)

all_skills = df["Skills"].fillna("").astype(str).str.split(", ").explode()
top_skills = all_skills.value_counts().head(5)
print("\n🛠️ Top 5 Required Skills:")
print(top_skills)

top_cities = df["Location"].value_counts().head(5)
print("\n📍 Top 5 Hiring Cities:")
print(top_cities)

top_dates = df["DatePosted"].value_counts().sort_index()
print("\n📅 Job Posting Dates and Counts:")
print(top_dates)


app_code = '''
import streamlit as st
import pandas as pd

st.title("📊 Real-Time Job Trend Analyzer")
st.write("Candidate Name: Samie Tahir, Roll no: AI-375686, Course: AI Batch (7).")
st.write("Analyze trending tech jobs, required skills, and hiring hotspots in real-time.")

# Load data
df = pd.read_csv("remoteok_jobs.csv")

# Overview stats
st.subheader("📈 Overview Stats")
st.write(f"**Total Jobs:** {len(df)}")
st.write(f"**Columns:** {list(df.columns)}")

# Top Job Titles
st.subheader("🔥 Top 5 Job Titles")
top_titles = df["Title"].value_counts().head(5)
st.bar_chart(top_titles)

# Top Locations
st.subheader("📍 Top 5 Hiring Locations")
top_locations = df["Location"].value_counts().head(5)
st.bar_chart(top_locations)

# Posting Trends
st.subheader("🕒 Job Posting Trends Over Time")
if 'DatePosted' in df.columns:
    trend = df["DatePosted"].value_counts().sort_index()
    trend.index = pd.to_datetime(trend.index, errors='coerce')
    trend = trend.dropna()
    st.line_chart(trend)

# Keyword Filter
st.subheader("🔍 Filter by Keyword")
keyword = st.text_input("Enter keyword to search jobs (e.g., Python):")
if keyword:
    filtered = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    st.write(f"Found {len(filtered)} job(s) with keyword '{keyword}'")
    st.dataframe(filtered.head(10))
'''

with open("main_inline_app.py", "w") as f:
    f.write(app_code)

!ngrok authtoken 2xYfxJltximJ4lrEyq6XpZSPIhg_41pnU9EpFKhTj3wDWBLrK
from pyngrok import ngrok

ngrok.kill()

public_url = ngrok.connect(8501)
print("🔗 Streamlit App URL:", public_url)

!streamlit run main_inline_app.py &>/dev/null &
