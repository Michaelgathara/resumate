from openai import OpenAI
client = OpenAI()

# MODEL = "gpt-3.5-turbo"
MODEL = "gpt-4"


def read_file_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Replace 'example.txt' with the path to your text file
SYSTEM = read_file_to_string('system.txt')



def call_gpt(system_prompt: str, prompt: str, model: str):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return completion


def main():
    job_description = """
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
    question = "This is sentence that you have to rephrase: "
    # to_rephrase = """Develop scripts for recurring tasks in Javascript and Python to facilitate employee productivity. Maintain and optimize scripts for increased speed through bug fixes, feature additions, and documentation updates.Prioritize and organize over 500 customer requests per semester according to deadlines and 3D print speeds to guarantee customer satisfaction"""
    to_rephrase = """Achieve a throughput of 4 documents a second while preserving accuracy and precision through the implementation of image preprocessing, Optical Character Recognition, and text preprocessing. Maintain a comprehensive grasp of the entire system, enabling me to provide informed assistance to team members."""
    print(call_gpt(SYSTEM, job_description+question +
          to_rephrase, MODEL).choices[0].message)


main()
