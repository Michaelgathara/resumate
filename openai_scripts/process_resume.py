import typing
import json
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

def call_gpt(prompt: str, model: str=MODEL, system_prompt: str=SYSTEM):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return completion



def main():
    resume_str = """{
    "experience": [
        {
        "employer": "University of South Florida IT",
        "job_title": "3D Print Lab Technician",
        "description": [
            "Develop scripts for recurring tasks in Javascript and Python to facilitate employee productivity.",
            "Maintain and optimize scripts for increased speed through bug fixes, feature additions, and documentation updates.",
            "Prioritize and organize over 500 customer requests per semester according to deadlines and 3D print speeds to guarantee customer satisfaction."
        ]
        },
        {
        "employer": "Center For Advanced Medical Learning And Simulation (CAMLS)",
        "job_title": "Student Researcher",
        "description": [
            "Authored a proceedings paper alongside esteemed doctors, addressing the use cases and essential precautions in AI integration within healthcare training.",
            "Aforementioned paper was accepted for presentation at the upcoming IMSH conference in January.",
            "Collaboratively analyzed the technical aspects of Dr. Shannon Bailey’s research question, offering insights into potential bottlenecks by acknowledging constraints posed by technological limitations"
        ]
        }
    ],
    "certifications": [],
    "skills": [
        "Python",
        "C",
        "C#",
        "JavaScript",
        "HTML",
        "CSS",
        "git",
        "vscode",
        "unity",
        "openai"
    ],
    "projects": [
        {
        "activity_name": "Machine Learning Document Sorter",
        "description": [
            "Achieve a throughput of 4 documents a second while preserving accuracy and precision through the implementation of image preprocessing, Optical Character Recognition, and text preprocessing.",
            "Maintain a comprehensive grasp of the entire system, enabling me to provide informed assistance to team members."
        ],
        "skills": ["python", "google colaboratory", "github"]
        },
        {
        "activity_name": "DIminished Java Compiler",
        "description": [
            "Incrementally developed a compiler through the comprehensive implementation of a lexical analyzer, parser,abstract syntax tree builder, type checker, and code generator for Diminished Java programs",
            "Deepened knowledge of compiler architecture, with a particular focus on semantic analysis, memory management (stack/heap), and the transformation of high-level code into machine-level instructions"
        ],
        "skills": ["C", "github"]
        },
        {
        "activity_name": "CollegeIn Website",
        "description": [
            "Collaborated with a team of three to develop an efficient software workflow using Agile methodology and project management tools such as Jira and Github to ensure on-time project delivery.",
            "Utilized Python to communicate with the backend and implemented FastAPI for efficient data storage in databases.",
            "Created dynamic user pages using the retrieved data from the database, enhancing the user experience with unique user pages"
        ],
        "skills": ["Python", "JavaScript", "HTML", "CSS", "Jira", "github"]
        },
        {
        "activity_name": "Customer Emailing Service",
        "description": ["Enhanced the automated emailing service to increase transparency and deliver complete and accurate order details, resulting in a significant reduction in email-related customer complaints"],
        "skills": ["JavaScript", "google apps script", "github"]
        }
    ]
    }"""


    job_desc = """
        Position Overview

    As a Data Engineer intern, you’ll be at the forefront of the Management Reporting Team’s mission to improve important data processing and analytics pipelines for our Subscription Models. You'll delve into research, find ways to transform data into relevant insights, while building pipelines to create the master data sets. You’ll also use Machine Learning techniques, to build and deploy AI models needed for our projects, working with our data engineers to ensure that our AI solutions are accurate, efficient, and scalable.

    Responsibilities

    • Collaborate with data engineers and data scientists to ensure that data is available and accessible for model development and deployment 
    • Improve machine learning models for accuracy, efficiency, and scalability 
    • Develop and document software solutions to address complex data collection, processing, transformation, and reporting issues 
    • Develop Integration processes and data processing workflows using tools like Snowflake, Fivetran, dbt, Apache Spark, and more 
    • Perform analysis on large datasets and produce qualitative visualizations based on reporting requirements


    Minimum Qualifications

    • Must be currently enrolled in a full-time, degree seeking program with an expected graduation date in 2024 
    • Strong CS Fundamentals using Python & SQL 
    • Exposure to Datawarehouse and Data Lake concepts


    Preferred Qualifications

    • Prior software engineering experience from internships, hackathons, or other side projects
    • Knowledge of Machine Learning Concepts like NLP, ranking, recommendations, or classification algorithms 
    • Familiarity with the AWS Environment (EC2, S3, Lambda, Glue, Canvas, etc.) 
    • Experience with Py Torch or TensorFlow


    About The US Intern Program

    The 2024 U.S. program runs for 12 weeks (May 20 – August 9 or June 17 – September 6). All internships are paid. As an intern, you will contribute to meaningful projects, be mentored by industry leaders, and participate in tech talks and other activities designed to support your personal and professional development. Our internships align with Autodesk’s Flexible Workplace approach, which is designed to meet the needs of our business while providing flexibility in support of office, remote and hybrid work preferences.

    Learn More

    About Autodesk

    Welcome to Autodesk! Amazing things are created every day with our software – from the greenest buildings and cleanest cars to the smartest factories and biggest hit movies. We help innovators turn their ideas into reality, transforming not only how things are made, but what can be made.

    We take great pride in our culture here at Autodesk – our Culture Code is at the core of everything we do. Our values and ways of working help our people thrive and realize their potential, which leads to even better outcomes for our customers.

    When you’re an Autodesker, you can be your whole, authentic self and do meaningful work that helps build a better future for all. Ready to shape the world and your future? Join us!
    """
    resume_obj = resume.Resume(resume_str)


    prompt = job_desc + "\n" + str(resume_obj)

    completion_object = call_gpt(prompt)

    response_text = str(completion_object.choices[0].message.content)
    print(response_text)

    resume_obj.import_improved(response_text)
    print(resume_obj.experience[0].imp_description)

if __name__ == "__main__":
    main()
