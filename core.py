from persona import PersonaEngine, Calculations
from utils.pdfcapture import pdfreadercapture
import pickle, hashlib, json, os
from pathlib import Path
from pydentmodel import profile_reformatter

RECORD = 'record.json'
OUTPUT = 'output'
SENIORITY_LEVEL_WITH_EXP = {"Internship": 1, "Entry level": 3, "Associate":5, "Mid-Senior level":10, "Director":20, "Executive":25}
class Core(PersonaEngine, pdfreadercapture, Calculations):
    
    def __init__(self, openai_key=None):
        super().__init__(openai_key)
    
    def save_pickle(self, full_persona, hash_filename):
        with open(hash_filename, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(full_persona, outp, pickle.HIGHEST_PROTOCOL)
    
    def load_pickle(self, hash_filename):
        with open(hash_filename, 'rb') as inp:
            full_persona = pickle.load(inp)
        return full_persona
    
    def load_json(self, file_path_linkapi):
        with open(file_path_linkapi, 'r') as fp:
            linkapi_json = json.load(fp)
        return linkapi_json
    
    def find_seniority_level(self, years_of_exp:int):
        for k,v in SENIORITY_LEVEL_WITH_EXP.items():
            if years_of_exp<=v:
                return k
            
    def get_all_career_paths(self, obj):
        career_paths = []
        for i in obj['career_paths']:
            career_paths.append(i['title'])
        return career_paths

    def run(self, file_path:str, file_path_linkapi:str=None) -> dict:
        try:
            text = self.read_pdf_reader(file_path)
            hash_object = hashlib.sha256()
            hash_object.update(file_path.encode())
            if file_path_linkapi: hash_object.update(file_path_linkapi.encode())
            hash_filename = hash_object.hexdigest() + '.pckl'
            if not os.path.exists(hash_filename):
                if file_path_linkapi:
                    linkapi_json = self.load_json(file_path_linkapi)
                    full_persona = self.analyze_resume_with_linkapi(text, linkapi_json)
                else:
                    full_persona = self.analyze_resume(text)
                # store full_persona in pickle file
                self.save_pickle(full_persona, hash_filename)
            full_persona = self.load_pickle(hash_filename)
            full_persona = profile_reformatter(json.loads(full_persona))
            questions_ask = self.questions_generator(str(full_persona))
            gns = self.analyze_specialist_or_generalist(str(full_persona))
            yearsofexp = self.calculate_experience(full_persona['experience_with_role'])
            feature1 = self.feature1(str(full_persona['experience_with_role']))
            feature2 = self.feature2(str(full_persona))
            feature3 = self.feature3(str(full_persona))
            feature4 = self.feature4(str(full_persona))
            full_persona = {**full_persona, **yearsofexp}
            skill_sets = full_persona['technical_skills'] + full_persona['domain_knowledges'] + full_persona['soft_skills'] + full_persona['behavioural_skills']
            skill_sets = skill_sets if skill_sets else ''
            years_of_exp = full_persona['total_years_of_experience']
            seniority_level = self.find_seniority_level(years_of_exp)
            current_role = full_persona['experience_with_role'][0]['role']
            industries_experience  = full_persona['industries_experience'] if full_persona['industries_experience'] else ''
            feature5 = self.feature5(str(years_of_exp), str(current_role), str(industries_experience), str(skill_sets), seniority_level)
            feature5 = json.loads(feature5)
            career_paths =  self.get_all_career_paths(feature5) # list of career paths
            feature6 = self.feature6(str(years_of_exp), str(current_role), str(industries_experience), str(skill_sets), seniority_level, career_paths)
            full_persona['candidate_type'] = json.loads(gns)
            return full_persona, json.loads(questions_ask), json.loads(feature1), json.loads(feature2), json.loads(feature3), json.loads(feature4), feature5, feature6
        except Exception as e:
            raise e
            return {"error": str(e)}
        