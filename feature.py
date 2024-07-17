from openai import OpenAI
from base import Base
from datetime import datetime
from dateutil.parser import *
from constant import *
import json

# "total_years_of_experience_reason": [please provide details explanation for your calculation on total_years_of_experience],

class PersonaFeature(Base):

    def __init__(self, openai_key=None):
        super().__init__()
        api_key = openai_key if openai_key else self.cfg.get('openai','key')
        self.client = OpenAI(
            api_key= api_key,
        )

    def feature1(self, experience_with_role):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    find complexity levels for each role based on the depth of technical implementation and innovation, and expertise scores for projects based on provided descriptions. 
                    Each project includes details such as role, company, start and end dates, and a brief description highlighting technologies used and tasks accomplished. 
                    return in fixed JSON format:
                        {
                        results : [
                                {
                                    "name" : [name of the company / organization],
                                    "technologies_used": [list of technologies_used],
                                    "complexity_level":  [Use the options ['Basic','Entry-level','Intermediate','Advanced','Expert'] to decide],
                                    "score": [score of complexity_level from 1 to 100]
                                }
                            ]
                        }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": experience_with_role
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            temperature=1,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    def feature2(self, persona):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    find how the progression of expertise moved based on types of projects , skills, experience with the roles, 
                    e.i like if any promotion is taken place & role increment or new types skills is  acquired / used whenever join a new company.  
                    return the career progression including roles, companies, and skills acquired for each role.  Also, provide a skill score based on the acquired skills. 
                    Finally, include a note summarising candidate's career progression and the skills the acquired.
                    return in fixed JSON format:
                        {
                            "career_progression": {
                                "company" : [name of the company],
                                "role": [name of the role for that company],
                                "skills_acquired": [list of skills acquired]
                            }
                            "skill_score": {
                                [name of the skill]: [score of the skill from 1 to 5]
                                }
                            "note" : [a note of summarising candidate's career progression and the skills the acquired. Do not use candidate's name, use he/she instated]
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
            temperature=0,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    def feature3(self, persona):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Evaluate how candidate's certifications and licenses align effectively with the projects and experiences listed in this perosna. 
                    Calculate the score of matches based on the technologies and tools used in the projects and experiences with respect to the certifications and licenses.
                    Follow the instructions carefully:
                        1. For find each match score check how many of the skills or similar keywords are matches with the technologies and tools used in his projects and experiences.
                        2. For generate score use the options ['High','Medium','Low'] to decide.
                    Give only JSON, Do not give any note or text after JSON.
                    {
                        "certification_match_score" : [
                                {   
                                    "name" : "",
                                    "score": "",
                                    "note": [an explanation of score and matches skill set else ""]
                                }
                            ],
                        "license_match_score": [Repeat the format as above skills_match_score]
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
            temperature=0,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    def feature4(self, persona):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    Based on candidate's profile and the certifications have acquired, assess the alignment between the certifications and the new job role. 
                    Also, determine how well the candidate's skills match withe the new job role.
                    Analyze candidate's certifications and job role alignment. Provide the alignment score for each certification and the average alignment score. 
                    Additionally, assess the alignment between candidate's skills and with the new job role, identifying aligned and unaligned skills, and provide an overall alignment score.
                    return in fixed JSON format, give only JSON. Do not give any note or text after JSON.
                    {
                        "certification_alignment": [
                            {
                                "certification_name": "",
                                "alignment_score": [score is in range from 1 to 100]
                            }
                        ],
                        "average_alignment_score": [score is in range from 1 to 100],
                        "skills_alignment": {
                            "aligned_skills": [list of alligned skills],
                            "unaligned_skills": [list of unaligned skills],
                            "overall_alignment_score": [score is in range from 1 to 100]
                        }
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
            temperature=0,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    def feature5(self, years_of_exp:int, current_role:str, industries:list, skills:list, seniority_level:str):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    You're a career guidance assistant bot. Your job is to help the candidate navigate their next career 
                    move based on their years of experience, current role within their organization, industry experience, and skill set and seniority level.
                    Give a 5 list of career moves options for the candidate.
                    return in fixed JSON format:
                        {
                            "career_paths" : [
                                {
                                    "title" : [name of the next role],
                                    "indusries": [list of industry name]
                                    "seniority_level" : [level ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']],
                                    "description": [a details explanation and description],
                                    "confidence": [How confident you are of this. Use the options ['High','Medium','Low'] to decide]
                                    "upgraded_skills": [list of 5 skills need to upgrade to match with next career based on current skill]
                                }
                            ]
                        }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": f"years of experience is : {years_of_exp}, current role/position is : {current_role}, industries experience is :{industries}, skil sets : {skills} and seniority level is : {seniority_level}" 
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            temperature=1,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    ############################################################################################ ############################################################################################
    
    def generate_milestone(self, years_of_exp:int, current_role:str, industries:list, skills:list, seniority_level:str, aspiring_role:str):
        # Define the messages for the chat model
        messages = [
            {
                "role": "system",
                "content": """
                    you are a career guidance assistance bot. Your job is to help the candidate to create a roadmap for given aspiring role 
                    based on their years of experience, current role within their organization, industry experience, skill set, seniority level.
                    Follow these instructions carefully during design a roadmap:
                        1. Roadmaps - milestones, actions, and critical enablers should all be
                            - Relevant
                            - Practical
                            - Have the right velocity
                            - Should be sequential and compound itself
                    return in JSON format
                    {
                        "roadmap": {
                            "milestones": [
                                {
                                    "title": [name of the milestone],
                                    "timeframe": [estimated timeframe],
                                    "description": [a details description] ],
                                    "actions": [list of action],
                                    "critical_enablers": [list of critical enabler]
                                }
                            ]
                        }
                    }
                    Give only JSON, Do not give any note or text after JSON.
                """
            },
            {
                "role": "user",
                "content": f"years of experience is : {years_of_exp}, current role/position is : {current_role}, \
                    industries experience is :{industries}, skil sets : {skills}, seniority level is : {seniority_level} and aspiring_role: {aspiring_role} \
                    " 
            }
        ]
        # Call the ChatGPT API
        response = self.client.chat.completions.create(
            model=GPT_MODEL,  # Specify the chat model you want to use
            messages=messages,
            temperature=1,
            response_format= { "type": "json_object" }
        )
        # Extract the generated response
        result = response.choices[0].message.content.strip() 
        # Return the parsed JSON response
        return result
    
    ############################################################################################ ############################################################################################

    def feature6(self,  years_of_exp:int, current_role:str, industries:list, skills:list, seniority_level:str, career_paths:list):
        roadmaps = []
        for aspiring_role in career_paths:
            res = self.generate_milestone(years_of_exp, current_role, industries, skills, seniority_level, aspiring_role)
            res = json.loads(res)
            obj = {}
            obj['aspiring_role'] = aspiring_role
            obj['milestones'] = res['roadmap']['milestones']
            roadmaps.append(obj)
        return {"roadmaps": roadmaps}

    