# from flask_sqlalchemy import SQLAlchemy



class Resume():
    class Education:
        '''
        '''
        def __init__(self, level, major, minor, school, begin_date, end_date, gpa):
            self.level = level # Level could also be referenced as degree level
            self.major = major
            self.minor = minor
            self.school = school
            self.begin_date = begin_date
            self.end_date = end_date
            self.gpa = gpa

    class Experience:
        '''
        '''
        def __init__(self, job_type, employer, description):
            self.job_type = job_type
            self.employer = employer
            self.description = description

    class Project:
        '''
        '''
        def __init__(self, activity_name, description):
            self.activity_name = activity_name
            self.description = description

    class Award:
        '''
        '''
        def __init__(self, name, date, description):
            self.name = name
            self.date = date
            self.description = description


    def __init__(self, first_name: str, middle_name: str, last_name: str, email: str, phone_number: str, education: list[Education], experience: list[Experience], certifications: list[str], skills: list[str], projects: list[Project], awards: list[Award]):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.education = education
        self.experience = experience
        self.certifications = certifications
        self.skills = skills
        self.projects = projects
        self.awards = awards

    def add_education(self, new_education: Education):
        self.education.append(new_education)
    
    def add_experience(self, new_experience: Experience):
        self.experience.append(new_experience)

    def add_certification(self, new_certification: str):
        self.certifications.append(new_certification)

    def add_skill(self, new_skill: str):
        self.skills.append(new_skill)

    def add_project(self, new_project: Project):
        self.projects.append(new_project)

    def add_award(self, new_award: Award):
        self.awards.append(new_award)

class JobPosting():
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    # description = db.Column(db.Text, nullable=False)
    # posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   
    # def __repr__(self):
    #     return f'<JobPosting {self.title}>'
    
    def __init__(self):
        raise NotImplementedError
