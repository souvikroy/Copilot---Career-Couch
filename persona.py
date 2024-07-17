from openai import OpenAI
from base import Base
from datetime import datetime
from dateutil.parser import *
from constant import *
from feature import PersonaFeature

# "total_years_of_experience_reason": [please provide details explanation for your calculation on total_years_of_experience],

class PersonaEngine(PersonaFeature):

    def __init__(self, openai_key=None):
        super().__init__()
        api_key = openai_key if openai_key else self.cfg.get('openai','key')
        self.client = OpenAI(
            api_key= api_key,
        )

    def analyze_resume(self, resume):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Given the text of a resume and json of response, combine the information from both responses, extract the key information of the candidate
                    Follow these instructions carefully:
                        1. To extract the experience_with_role, need to extract the role name, description, company name, start date, end date, and duration in months.
                        2. To extract the educations, need to extract the degree, major, university and completion_date.
                        3. To extract industries_experience need to extract the name of the industry.
                        4. To extract technical_skills need to extract the name of the technical skill.
                    
                    return in fixed JSON format:
                        {
                            "full_name": [full name of the candidate],
                            "email_id": [email id of the candidate],
                            "contact": [mobile no of the candidate],
                            "location": [current location of the candidate],
                            "date_of_birt": [date of birth of the candidate],
                            "currently_employed": [return true or false if the candidate is currently employed],
                            "gender": [gender of the candidate],
                            "experience_with_role": [
                                    {"company_name": [name of the company], "role":[role of the company], "description": "", "start_date": "", "end_date": "", "duration_months": [return only duration in months, do not add extra text before or after that, do not include symbols]}
                                ],
                            "industries_experience": [list of industry experience],
                            "educations": [
                                    {"degree": [degree of the education], "major": "", "university": "", "completion_date":""}
                                ],
                            "projects: [
                                    {"title": [name and title of the project], "start_date": "", "end_date": "", "description":""}
                                ],
                            "certifications": [
                                    {"name": [name of the certification], "start_date": "", "end_date": "", "license_number":"","display_source":"","authority":"", "url":""}
                                ],
                            "soft_skills": [list of soft skills],
                            "technical_skills": [list of technical skills],
                            "behavioural_skills": [list of behavioural skills],
                            "domain_knowledges": [list of domain knowledge],
                            "honors_and_awards: [list of honors and awards],
                            "linkedin": [link of linkedin],
                            "github": [link of github]

                        }
                    Ensure that the information is presented clearly and organized chronologically, starting with your most recent position. Fill in the details accordingly.
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": resume
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    def get_years_of_experince(self, resume):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Please calculate the total years of experience based on the information provided in the resume.
                    Follow these instructions carefully:
                        1. Assuming Current or Present date is May 2024.
                        2. Do not consider duration_in_months in provided text.
                        3. Calculate the duration of each role by subtracting the start date's month from the end date's month. 
                        4. If thers is only start date or end date ignore that position.
                        5. Calculate the total years of experience accurately.
                        6. Express the total experience in years and months.
                    return in fixed JSON format:
                        {   
                            "total_years_of_experience": [Convert months in years rounded to 1 decimal place]
                        }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": resume
            }
        ]
        # print(f"resume: {resume} candidate_profile: {linkapi_json}")
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip()
        # Return the parsed JSON response
        return result
    
    def analyze_resume_with_linkapi(self, resume, linkapi_json):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Given the text of a resume and json of response of candidate_profile, combine the information from both responses, extract the key information of the candidate
                    Follow these instructions carefully:
                        1.  To extract the experience_with_role, need to extract the role name, company name, description, start date (datetime), end date (datetime), and duration in months.
                        2.  To extract the educations, need to extract the degree, major, university and completion_date.
                        3.  To extract industries experience, look at the following sections and details to identify industries:
                                a. Professional Summary: Look for any direct mentions of industries or areas of expertise.
                                b. Work Experience: Examine the job roles, company names, and job descriptions for clues about the industries the candidate has worked in.
                                c. Keywords: Identify any industry-specific keywords, jargon, or technical terms that indicate the candidate’s industry background
                        4.  To extract technical skills using the following guidelines:
                                a. Review to identify technical skills by checking sections such as 'skills' or 'technical Skills' for specific tools, languages, or software. 
                                b. Examine job titles and descriptions for relevant technical responsibilities and projects. 
                                c. Look for certifications, education, and achievements related to technical expertise.
                        5.  To extract soft skill using the following guidelines:
                                a. look for keywords like 'teamwork,' 'leadership,' 'communication,' and 'problem-solving.' Look at job duties, achievements, and project examples to identify adaptability, creativity, and interpersonal skills.
                        6.  To extract domain knowledge using the following guidelines:
                                a. Look for domain knowledge by examining job titles and descriptions for industry-specific roles and responsibilities. 
                                b. Look for industry keywords, achievements, and projects relevant to the domain. Check education, certifications, and memberships in industry associations for specialized expertise.
                        7.  To extract projects need to extract the project title, start_date, end_date and description. 
                        8.  To extract certifications need to extract the certification name, start date (datetime), end date (datetime), license_number, display_source, authority and url.
                    
                    return in fixed JSON format:
                        {   
                            "full_name": [full name of the candidate],
                            "first_name": [first name of the candidate],
                            "last_name": [last name of the candidate],
                            "profile_pic_url" : [profile pic url of the candidate],
                            "headline" : [headliine of the cadidate profile],
                            "occupation": [occupation of the candidate],
                            "headline": [headline of the candidate],
                            "summary": [summary of the candidate profile],
                            "country": [country short name of the candidate where he/she is from],
                            "email_id": [email id of the candidate],
                            "contact": [mobile no of the candidate],
                            "location": [current location of the candidate]
                            "date_of_birt": [date of birth of the candidate],
                            "currently_employed": [return true or false if the candidate is currently employed],
                            "gender": [gender of the candidate],
                            "experience_with_role": [
                                    {"company_name": [name of the company], "role":[role of the company], "description": "", "start_date": "", "end_date": "", "duration_months":[return only duration in months, do not add extra text before or after that, do not include symbols]}
                                ],
                            "industries_experience": [list of industry experience],
                            "educations": [
                                    {"degree": [degree of the education], "major": "", "university": "", "completion_date":""}
                                ],
                            "projects: [
                                    {"title": [name and title of the project], "start_date": "", "end_date": "", "description":""}
                                ],
                            "certifications": [
                                    {"name": [name of the certification], "start_date": "", "end_date": "", "license_number":"","display_source":"","authority":"", "url":""}
                                ],
                            "soft_skills": [list of soft skill],
                            "technical_skills": [list of name of technical skill],
                            "behavioural_skills": [list of name behavioural skill],
                            "domain_knowledges": [list of domain knowledge],
                            "honors_and_awards: [list of honors and award],
                            "linkedin": [link of linkedin],
                            "github": [link of github]
                        }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": f"resume: {resume} candidate_profile: {linkapi_json}"
            }
        ]
        # print(f"resume: {resume} candidate_profile: {linkapi_json}")
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip()
        # Return the parsed JSON response
        return result
    

    def analyze_specialist_or_generalist(self, persona:dict):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Please analyze the following resume persona in json format and classify whether the candidate is a specialist or generalist in their career path. 
                    Evaluate the candidate's experience, skills, industries worked in, and the depth of their roles to make your determination. 
                    Return the analysis in the following FIXED JSON structure:
                    {
                        "type": ["specialist" or "generalist"],
                        "evidence": {
                            "depth_of_experience": [Provide a brief assessment of the depth of the candidate's experience in particular areas],
                            "breadth_of_experience": [Provide a brief assessment of the breadth of the candidate's experience across different areas]
                        }
                        "score": [assign a score in a range of 1-100, consider years of experience as paramater for calculate score],
                        "expain_score": [an explanation of score, do not use he/she, or candidate name; use term candidate instated],
                        "confidence": [How confident you are of this categorization. Use the options ['High','Medium','Low'] to decide]
                        
                    }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": persona
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip()
        # Return the parsed JSON response
        return result
    
    def questions_generator(self, persona):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    what are the top 10 questions can be asked for the candidate based on below resume in JSON. 
                    return in fixed JSON format:
                    Give only JSON, Do not give any note or text after JSON.
                        {
                            "questions": [questions and [Difficulty level: Hard, Medium, or Easy]]
                        }

                """
            },
            {
                "role": "user",
                "content": persona
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip()
        # Return the parsed JSON response
        return result
    

class Calculations:

    def __init__(self) -> None:
        pass
    
    def calculate_duration(self, start_date, end_date):
        if (start_date == '') or (start_date == 'Not Provided'):
            return 0
        if (end_date.lower() == "present") or (end_date.lower() == 'current')  or (end_date == ''):
            end_date = datetime.now()
        else:
            end_date = parse(end_date)
        if start_date.lower() == "currently employed" or start_date.lower() == "previous"  or start_date.lower()=='recent':
            start_date = end_date.replace(year=end_date.year - 1)
        else:
            start_date = parse(start_date)
        months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
        return months / 12
    
    def calculate_experience(self, resume):
        total_years = sum(self.calculate_duration(job["start_date"], job["end_date"]) for job in resume)
        total_years = round(total_years, 2)
        return {"total_years_of_experience": total_years}