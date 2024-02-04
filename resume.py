import json

class Experience:
    def __init__(self, experience: dict):
        self.employer = experience["employer"].lower()
        self.job_title = experience["job_title"].lower()
        self.description = experience["description"]
        self.imp_description = []
    
    def __str__(self):
        return "_".join(self.job_title.split(" ")) + "_section\n" + ";".join(self.description) + ";\n"
      
class Project:
    def __init__(self, project: dict):
        self.activity_name = project["activity_name"].lower()
        self.description = project["description"]
        self.imp_description = []
        self.skills = project["skills"]
    
    def __str__(self):
        return "_".join(self.activity_name.split(" ")) + "_section\n" + ";".join(self.description) + ";\n"
        

class Skill:
    def __init__(self, skill: str):
        self.skills = skill
    
    def __str__(self):
        return ";".join(self.skills) + ";"

class Resume:
    def __init__(self, resume: str):
        resume_dict = json.loads(resume)
        self.projects = [Project(project) for project in resume_dict["projects"]]
        self.experience = [Experience(experience) for experience in resume_dict["experience"]]
        self.certifications = Skill(resume_dict["certifications"])
        self.skills = Skill(resume_dict["skills"])
    
    def import_improved(self, response: str):
    # Split the response by double newlines to separate sections
        sections = response.strip().split("\n\n")
        
        for section in sections:
            # Split each section by the first newline to separate the header from the description
            header, *description_lines = section.split("\n")
            # Rejoin the description lines into a single string
            description_text = " ".join(description_lines).strip(";")
            
            # Determine if the section is a project or experience by its header
            if "_section" in header:
                # Extract the name from the header
                name = header.replace("_section", "").replace("_", " ")
                # Try updating both projects and experiences
                updated = False
                for project in self.projects:
                    if project.activity_name.lower() == name.lower():
                        project.imp_description = description_text.split(";")
                        updated = True
                        break
                if not updated:  # If not found in projects, try experiences
                    for experience in self.experience:
                        if experience.job_title.lower() == name.lower():
                            experience.imp_description = description_text.split(";")
                            break


    def __str__(self):
        return "\n".join(str(x) for x in self.projects + self.experience)
