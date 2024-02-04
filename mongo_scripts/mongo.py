from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from os import getcwd
from hashlib import sha256

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

class MongoManager:
    def __init__(self):
        uri = f"mongodb+srv://arnet:{env.get('MONGO_PW')}@cluser0.i7wnmup.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        self.db = client.resumate
        self.resumes = self.db.resumes
        self.resume_pairs = self.db.resume_pairs
        
    def add_resume(self, email: str, prompt: str):
        prompt_hash = sha256((env.get('SALT') + prompt).encode()).hexdigest()
        resumesDocument = {
            "user" : f"{sha256((env.get('SALT') + email).encode()).hexdigest()}",
            "resume_prompt": f"{prompt_hash}",
        }
        self.resumes.insert_one(resumesDocument)
        with open(f"uploads/resumes/{prompt_hash}.txt", "w") as f:
            f.write(prompt)

    def get_all_resumes(self, email: str):
        entries = self.resumes.find({"user": f"{sha256((env.get('SALT') + email).encode()).hexdigest()}"})
        prevResumes = []
        while True:
            try:
                currentResume = entries.next()
                prevResumes.append(currentResume)
            except:
                break
        return prevResumes
    
        
    def add_resumeGPT_pair(self, resume: str, gpt: str):
        gpt_hash = sha256((env.get('SALT') + gpt).encode()).hexdigest()
        resumeGPTDocument = {
            "resume_prompt": f"{sha256((env.get('SALT') + resume).encode()).hexdigest()}",
            "gpt_prompt": f"{gpt_hash}"
        }
        self.resume_pairs.insert_one(resumeGPTDocument)
        with open(f"uploads/job_details/{gpt_hash}", "w") as f:
            f.write(gpt)


    def get_all_prompts(self, resume: str):
        entries = self.resumes.find({"user": f"{sha256((env.get('SALT') + resume).encode()).hexdigest()}"})
        prevPrompts = []
        while True:
            try:
                currentPrompts = entries.next()
                prevPrompts.append(currentPrompts)
            except:
                break
        return prevPrompts
    
    def get_resume(self, resume_hash: str):
        with open(f"uploads/resumes/{resume_hash}.txt") as f:
            return f.read()
        
    def get_job_details(self, gpt_hash: str):
        with open(f"uploads/job_details/{gpt_hash}.txt") as f:
            return f.read()

    


# Send a ping to confirm a successful connection
# try: 