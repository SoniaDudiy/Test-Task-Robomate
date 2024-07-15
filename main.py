import requests
from bs4 import BeautifulSoup

def parse_work_ua_resumes(soup):
    resumes = []
    job_links = soup.find_all('div', class_='job-link')
    for job_link in job_links:
        title = job_link.find('a').text.strip() if job_link.find('a') else "Unknown"
        company_div = job_link.find('div', class_='add-top-sm')
        company = company_div.find('span').text.strip() if company_div and company_div.find('span') else "Unknown"
        description = job_link.find('p', class_='overflow').text.strip() if job_link.find('p', class_='overflow') else "Unknown"
        resumes.append({
            'title': title,
            'company': company,
            'description': description
        })
    return resumes

def parse_robota_ua_resumes(soup):
    resumes = []
    job_links = soup.find_all('div', class_='card')
    for job_link in job_links:
        title = job_link.find('a', class_='ga_listing').text.strip() if job_link.find('a', class_='ga_listing') else "Unknown"
        company = job_link.find('div', class_='job-list-company-title').text.strip() if job_link.find('div', class_='job-list-company-title') else "Unknown"
        description = job_link.find('div', class_='job-list-item-preview').text.strip() if job_link.find('div', class_='job-list-item-preview') else "Unknown"
        resumes.append({
            'title': title,
            'company': company,
            'description': description
        })
    return resumes

def fetch_resumes(job_position, years_of_experience, skills, location, salary_expectation):
    # URL для пошуку на work.ua
    work_ua_url = f"https://www.work.ua/jobs-{job_position.replace(' ', '+')}+{location.replace(' ', '+')}?experience={years_of_experience}&skills={skills.replace(' ', '+')}&salary={salary_expectation}"
    
    # URL для пошуку на robota.ua
    robota_ua_url = f"https://robota.ua/jobsearch?keywords={job_position.replace(' ', '+')}&location={location.replace(' ', '+')}&experience={years_of_experience}&skills={skills.replace(' ', '+')}&salary={salary_expectation}"
    
    # Отримання HTML-коду сторінок
    try:
        work_ua_response = requests.get(work_ua_url)
        work_ua_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch resumes from work.ua: {e}")
        return
    
    try:
        robota_ua_response = requests.get(robota_ua_url)
        robota_ua_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch resumes from robota.ua: {e}")
        return
    
    # Парсинг резюме
    work_ua_soup = BeautifulSoup(work_ua_response.content, 'html.parser')
    work_ua_resumes = parse_work_ua_resumes(work_ua_soup)
    print("Work.ua resumes fetched successfully")
    for resume in work_ua_resumes:
        print(resume)
    
    robota_ua_soup = BeautifulSoup(robota_ua_response.content, 'html.parser')
    robota_ua_resumes = parse_robota_ua_resumes(robota_ua_soup)
    print("Robota.ua resumes fetched successfully")
    for resume in robota_ua_resumes:
        print(resume)

# Приклад виклику функції
fetch_resumes("Data Scientist", "1-3", "Python, Machine Learning", "Kyiv", "50000")