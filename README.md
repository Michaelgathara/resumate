# resumate
1. Create a python env, `python3 -m venv env/`
2. Pip install requirements.txt, `pip install -r requirements.txt`

resume-feedback-project/
│
├── app/
│   ├── __init__.py        # Initializes your Flask app as a package
│   ├── models.py          # Defines your data models (e.g., User, Resume, JobPosting)
│   ├── forms.py           # Contains WTForms for resume and job posting submissions
│   ├── routes.py          # Handles routing and view functions for your application
│   └── templates/         # Contains HTML templates
│       ├── base.html      # Base template
│       ├── index.html     # Home page template
│       ├── submit_resume.html  # Form template for resume submission
│       └── submit_job.html     # Form template for job posting submission
│
├── tests/                 # Contains your test cases
│   └── test_basic.py
│
├── run.py                 # Entry point to run the Flask application
│
├── requirements.txt       # Lists the project dependencies
│
└── README.md              # Project overview and setup instructions