# !pip install pymupdf

import fitz
import re
import json

def build_json(rnum):
    fpath = f"../resumes/resume_{rnum}/resume_{rnum}.pdf"
    doc = fitz.open(fpath)

    #REGEXES
    re_edu_award = r"education|school|award|achievement|leadership|extracurric"
    re_experiences = r"experience"
    re_projects = r"project"
    re_skills = r"Skill|Certificat(e|ion)|SKILL"
    re_dates = r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec|20\d\d|19\d\d|present|_"
    re_bullets = r"●|‑|•|▪"


    def rem_dates(toks):
        if len(toks) == 0:
            return
        while re.search(re_dates, toks[0]):
            print("REMOVINGGG", toks[0])
            toks.pop(0)

    def find_bullet(toks):
        if len(toks) == 0:
            return
        while not re.search(re_bullets, toks[0]):
            toks.pop(0)


    def peek_sections(toks, opt):
        if re.search(re_edu_award, toks[0], re.IGNORECASE):
            return True
        match opt:
            case "exp":
                return re.search(re_projects, toks[0], re.IGNORECASE) or re.search(re_skills, toks[0], re.IGNORECASE)
            case "proj":
                return re.search(re_experiences, toks[0], re.IGNORECASE) or re.search(re_skills, toks[0], re.IGNORECASE)
            case "skill":
                return re.search(re_experiences, toks[0], re.IGNORECASE) or re.search(re_projects, toks[0], re.IGNORECASE)

    def peek_dates(toks):
        if len(toks) > 1:
            for i in range(2):
                if  re.search(re_dates, toks[i], re.IGNORECASE):
                    return True
            return False
        else:
            for i in range(len(toks)):
                if  re.search(re_dates, toks[i], re.IGNORECASE):
                    return True
            return False
        
    def peek_bullets(toks):
        if not re.search(re_bullets, toks[0]) and re.search(re_bullets, toks[1]):
            return True

    text = ""
    for page in doc:
        next = re.sub(r"●( |\n)|▪( |\n)|•( |\n)|‑( |\n)", "●", page.get_text())
        text += next.replace("_", "")

    resume = {"experiences": [],
            "projects": [],
            "skills": []}


    toks = text.splitlines()
    toks = [i for i in toks if i]
    print(toks)
    while toks:
        if re.search(re_experiences, toks[0], re.IGNORECASE):
            toks.pop(0)
            while not peek_sections(toks, "exp"):
                job = {}
                rem_dates(toks)
                if not toks:
                    break
                if "|" in toks[0] or "," in toks[0] or re.search(re_bullets, toks[1]):
                    job["job_title"] = toks.pop(0)
                else:
                    title = toks.pop(0)
                    rem_dates(toks)
                    job["job_title"] = toks.pop(0) + " | " + title
                    rem_dates(toks)  
                find_bullet(toks)
                job["description"] = []
                while re.search(re_bullets, toks[0]):
                    desc = re.sub(re_bullets, "", toks.pop(0))
                    while not re.search(re_bullets, toks[0]) and not peek_sections(toks, "exp") and not peek_dates(toks):
                        desc += " " + toks.pop(0)
                    job["description"].append(desc)
                resume["experiences"].append(job)
                if len(toks) == 0:
                    break                                                                                                                                                                                                                                                                                                                                                                                                               
        elif re.search(re_projects, toks[0], re.IGNORECASE):
            toks.pop(0)
            if len(toks) == 0:
                    break
            while not peek_sections(toks, "proj"):
                project = {}
                # rem_dates(toks)
                if not toks:
                    break
                project["project_title"] = toks.pop(0)
                rem_dates(toks) 
                find_bullet(toks)                                                                                                                                                                                                               
                project["description"] = []
                while re.search(re_bullets, toks[0]):
                    desc = re.sub(re_bullets, "", toks.pop(0))
                    while not re.search(re_bullets, toks[0]) and not peek_sections(toks, "proj") and not peek_dates(toks) and not peek_bullets(toks):
                        desc += " " + toks.pop(0)
                    project["description"].append(desc)
                resume["projects"].append(project)
                if len(toks) == 0:
                    break
        elif re.search(re_skills, toks[0]):
            toks.pop(0)
            while not peek_sections(toks, "skill"):
                resume["skills"].append(toks.pop(0))
                if len(toks) == 0:
                    break
        else:
            toks.pop(0)
    print("\n\n\n")
    print(resume["experiences"])
    print("\n\n\n")
    print(resume["projects"])
    print("\n\n\n")
    print(resume["skills"])
    with open(f"resume_{rnum}.json", "w") as out:
        json.dump(resume, out)


for i in range(7):
    build_json(i)