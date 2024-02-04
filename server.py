from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session

import json
import time
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from mongo_scripts.mongo import MongoManager

import resume
from dotenv import load_dotenv
from openai import OpenAI
MODEL = "gpt-4"
# MODEL = "gpt-3.5-turbo"
load_dotenv()
SYSTEM = """
You are an expert resume rewriting system,

you will be given different parts of the resume, each with multiple semicolon separated sentences to rephrase based on a job description I will give you.
I want you to make minimal changes to the sentence to match the job description, but if you think a sentence is okay,
then do not rephrase it at all and simply return it.

This task requires you to take a deep breath before changing a sentence.
You are to be accurate, do not be over-confident. Precision is what you will be judged on.
Also, think about how each change contributes to sentence being better suited to the job description.

Here is the input format,
Job description
section name
sentences to be rephrased
"""

client = OpenAI()
mongo  = MongoManager()


def call_gpt(prompt: str, model: str=MODEL, system_prompt: str=SYSTEM):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return completion

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__, static_folder="static")
app.secret_key = 'We in this code'

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@app.route('/')
@app.route('/index')
def home():
    print(app.debug)
    return render_template("home.html", session=session.get('user'), title="Home")

@app.route('/submission')
def submission():
    if not app.debug: 
        # print(session)
        try:
            expiry = session["user"]["userinfo"]["exp"]
            if session.get("user", "NOACCESS") == "NOACCESS" or time.time() > expiry:
                session = None
                return redirect("/")
        except:
            return redirect("/")

    return render_template('index.html', title='Submission')

@app.route('/submit_resume', methods=['POST'])
def submit_resume():
    if request.method == 'POST':
        job_desc = request.form.get('job_desc', '')
        resume_data = {
            "experience": [],
            "certifications": [], 
            "skills": request.form.getlist('skills'), 
            "projects": []
        }

        experiences = request.form.getlist('company')
        titles = request.form.getlist('title')
        descriptions = request.form.getlist('description')
        experience_count = len(experiences)
        print(f"Exp len: {experience_count}")
        for i in range(1, int(experience_count) + 1):
            experience = {
                "job_type": 'full_time',
                "employer": experiences[i-1],
                "job_title": titles[i-1],
                "description": descriptions[i-1]
            }
            resume_data["experience"].append(experience)

        projects = request.form.getlist('project_name')
        skills = request.form.getlist('technologies_used')
        del descriptions
        project_descriptions = request.form.getlist('project_description')
        project_count = len(projects)
        for i in range(1, int(project_count) + 1):
            project = {
                "activity_name": projects[i-1],
                "description": project_descriptions[i-1],
                "skills": skills[i-1] 
            }
            resume_data["projects"].append(project)

        # print(jsonify(resume_data))
        resume_obj = resume.Resume(json.dumps(resume_data))

        # print(f"Resume {json.dumps(resume_data)} - {str(resume_data)}")
        prompt = job_desc + "\n" + str(resume_obj)

        # print(f"Prompt: {prompt}")        
        mongo.add_resume(session["user"]["userinfo"]["email"] if not app.debug else "ajnettles@gmail.com", prompt)

        completion_object = call_gpt(prompt)

        response_text = str(completion_object.choices[0].message.content)

        mongo.add_resumeGPT_pair(prompt, response_text)

        return response_text
    

# def submit_resume():
#     if request.method == 'POST':
#         universities = request.form.getlist('university')
#         degrees = request.form.getlist('degree')
#         companies = request.form.getlist('company')
#         titles = request.form.getlist('title')
#         skills = request.form.get('skills', '')

#         job_desc = request.form.get('job_desc', '')

#         print(f"Universities: {universities}")
#         print(f"Degrees: {degrees}")
#         print(f"Companies: {companies}")
#         print(f"Titles: {titles}")
#         print(f"Skills: {skills}")
#         print(f"Job Desc: {job_desc}")

#         return "Form submitted"
        
        # filename = request.files['resume'].filename
        # return render_template("submit_resume.html", title="Resumate", fileName = filename)



@app.route("/login")
def login():
    if not app.debug:
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )
    else:
        return render_template('index.html')
        # return redirect("/submission")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/submission")


# @app.route('/submit_resume', methods=['GET', 'POST'])
# def submit_resume():
#     form = ResumeForm()
#     if form.validate_on_submit():
#         resume = Resume(content=form.content.data, user_id=form.user_id.data)
#         db.session.add(resume)
#         db.session.commit()
#         flash('Your resume has been submitted!', 'success')
#         return redirect(url_for('index'))
#     return render_template('submit_resume.html', title='Submit Resume', form=form)

# @app.route('/submit_job', methods=['GET', 'POST'])
# def submit_job():
#     form = JobPostingForm()
#     if form.validate_on_submit():
#         job_posting = JobPosting(title=form.title.data, description=form.description.data)
#         db.session.add(job_posting)
#         db.session.commit()
#         flash('Job posting has been created!', 'success')
#         return redirect(url_for('index'))
#     return render_template('submit_job.html', title='Submit Job', form=form)

# @app.route('/job_listings')
# def job_listings():
#     jobs = JobPosting.query.all()
#     return render_template('job_listings.html', jobs=jobs, title='Job Listings')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get("PORT", 7976 if app.debug else 443), debug=True)