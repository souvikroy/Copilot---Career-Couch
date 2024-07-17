from typing import List, Optional, Any
from pydantic import BaseModel
import json

# Example usage
dummy_json_data = {
    "first_name": "Ananya",
    "last_name": "Rakesh",
    "profile_pic_url": "https://media.licdn.com/dms/image/D4D03AQFTDXun4FbSnA/profile-displayphoto-shrink_400_400/0/1688970759089?e=1720051200&v=beta&t=vMqjDF2ZsMRXMPsZw5A1eMJcWxjMUHGNF-3p5rJsx6A",
    "headline": "Data Analyst || Business Analyst || Advance SQL || Advance Excel || Python || Tableau|| Power Bi || Machine Learning || Keep learning Keep growing",
    "occupation": "Implementation Engineer at Umbrella Protection Systems",
    "summary": "⭐As a  data analyst, I possess a diverse set of skills that enable me to provide valuable insights to organizations. With a strong foundation in data analysis tools such as SQL, Excel, Tableau, and Python, I am able to clean, transform, and visualize data in meaningful ways. I also have experience in data modeling, statistical analysis, and predictive modeling techniques. I'm excited to apply my skills and knowledge to help organizations achieve their data-driven goals.\nconnect with me \n✉️Email - rakeshananya943@gmail.com\n📱Mobile -  7017545048",
    "country": "IN",
    "email_id": "rakeshananya943@gmail.com",
    "contact": "7017545048",
    "location": "Noida, Uttar Pradesh, India",
    "experience_with_role": [
        {
            "role": "Implementation Engineer",
            "company_name": "Umbrella Protection Systems",
            "description": None,
            "start_date": "2023-10-01",
            "end_date": None,
            "duration_months": "8"
        },
        {
            "role": "Site Civil Engineer",
            "company_name": "OP Chains Housings",
            "description": None,
            "start_date": "2021-06-01",
            "end_date": "2022-07-31",
            "duration_months": "14"
        }
    ],
    "educations": [
        {
            "degree": "Diploma",
            "major": "Data analytics",
            "university": "Masai",
            "completion_date": "2023-03-31"
        },
        {
            "degree": "Bachelor of Technology",
            "major": "Civil Engineering",
            "university": "SACHDEVA INSTITUTE OF TECHNOLOGY, MATHURA",
            "completion_date": "2019-12-31"
        }
    ],
    "industries_experience": [
        "Data Analysis",
        "Civil Engineering"
    ],
    "projects": [
        {
            "title": "Exploratory Data Analysis on Indian Premier League Data",
            "start_date": "2023-04-01",
            "end_date": "2023-04-30",
            "description": "Conducted EDA using Python on IPL data to provide valuable insights for cricket teams, sponsors, and broadcasters to make informed decisions regarding player recruitment, team strategy, and marketing initiatives..."
        },
        {
            "title": "Financial Analysis of Various Indian States",
            "start_date": "2023-04-01",
            "end_date": "2023-04-30",
            "description": "Driven by my passion for data-driven insights and economic evaluation, I embarked on a project to conduct a thorough financial analysis of multiple Indian states. By exploring a diverse range of financial indicators, socio-economic factors, and government policies, I aimed to provide valuable insights into the financial health and performance of these states..."
        }
    ],
    "certifications": [
        {
            "name": "Advance SQL",
            "start_date": "2023-06-01",
            "end_date": None,
            "license_number": "E7062AA1D5SEF",
            "display_source": "www.hackerrank.com",
            "authority": "HackerRank",
            "url": "https://www.hackerrank.com/certificates/e7d62aa1d5ef"
        },
        {
            "name": "Microsoft Power BI Desktop for Business Intelligence",
            "start_date": "2023-02-01",
            "end_date": None,
            "license_number": None,
            "display_source": "drive.google.com",
            "authority": "Udemy",
            "url": "https://drive.google.com/file/d/1HSEwqLaoUbI_qEwGHf-zXsAQ-ze-jlwG/view?usp=share_link"
        }
    ],
    "soft_skills": ["Team Leadership", "Team Management", "Client Relations"],
    "technical_skills": ["SQL (Intermediate)", "SQL (Basic)", "Python for Data Analysis", "Microsoft Power BI Desktop for Business Intelligence", "Autodesk Auto CAD"],
    "behavioural_skills": [],
    "domain_knowledges": ["Data Analysis", "Civil Engineering"],
    "honors_and_awards": [],
    "linkedin": "www.linkedin.com/in/ananya-rakesh",
    "github": None
}

class ExperienceWithRole(BaseModel):
    role: str
    company_name: str
    description: Optional[str] = ''
    start_date: str
    end_date: Optional[str] = ''
    duration_months: Optional[Any] = ''

class Education(BaseModel):
    degree: str
    major: str
    university: str
    completion_date: str

class Project(BaseModel):
    title: str
    start_date: str
    end_date: Optional[str] = ''
    description: str

class Certification(BaseModel):
    name: str
    start_date: str
    end_date: Optional[str] = ''
    license_number: Optional[str] = ''
    display_source: str
    authority: str
    url: str

class Profile(BaseModel):
    full_name : Optional[str] = ''
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    profile_pic_url: Optional[str] = ''
    headline: Optional[str] = ''
    occupation: Optional[str] = ''
    summary: Optional[str] = ''
    country: Optional[str] = ''
    email_id: Optional[str] = ''
    contact: Optional[str] = ''
    location: Optional[str] = ''
    experience_with_role: Optional[List[ExperienceWithRole]] = []
    educations: Optional[List[Education]] = []
    industries_experience: Optional[List[str]] = []
    projects: Optional[List[Project]] = []
    certifications: Optional[List[Certification]] = []
    soft_skills: Optional[List[str]] = []
    technical_skills: Optional[List[str]] = []
    behavioural_skills: Optional[List[str]] = []
    domain_knowledges: Optional[List[str]] = []
    honors_and_awards: Optional[List[str]] = []
    linkedin: Optional[str] = ''
    github: Optional[str] = ''

# Function to replace None with ""
def replace_none_with_empty_string(data):
    if isinstance(data, dict):
        return {k: replace_none_with_empty_string(v) if v is not None else "" for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_none_with_empty_string(v) if v is not None else "" for v in data]
    else:
        return data

def profile_reformatter(json_data):
    profile = Profile(**json_data)
    profile = json.loads(profile.model_dump_json())
    # Replace None with ""
    cleaned_json = replace_none_with_empty_string(profile)
    return cleaned_json