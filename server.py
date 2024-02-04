from flask import Flask, render_template, url_for, flash, redirect


app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')

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
    app.run(host='0.0.0.0', port='7976', debug=True)