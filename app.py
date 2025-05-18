import os 
from crewai import Task , Crew , Agent
from langchain_community import document_loaders
from langchain.document_loaders import PyPDFLoader
from flask import Flask , render_template, request , redirect, url_for , flash
from werkzeug.utils import secure_filename

os.environ['GROQ_API_KEY'] =  "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"


app = Flask(__name__)

UPLOAD_FOLDER = 'instance/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_upload', methods=['GET','POST'])
def process_upload():

    job_description = request.form.get('job_desc')
    if not job_description:
        flash('No job description provided')
        return redirect(url_for(''))

    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('upload'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('upload'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process PDF and generate questions
        loader = PyPDFLoader(filepath)
        text = loader.load()
        os.remove(filepath) 
        resume_content = "".join([t.page_content for t in text])

        cold_email_template_analyzer = Agent(
    role="Cold Email Template Data Analyzer",
    goal="Extract key information from job descriptions and resumes to populate cold outreach email templates",
    backstory="""You are a specialized data analyst who extracts targeted information 
    from job postings and candidate resumes to fill in cold email templates. You identify 
    the most relevant details that will make outreach emails personalized and impactful,
    focusing specifically on the fields needed for standard templates.""",
    verbose=True,
    allow_delegation=False,
    llm="groq/llama3-70b-8192"
)

        template_data_analysis_task = Task(
            description="""Analyze the job posting '{job_description}' and candidate 
            resume '{resume_content}' to extract information for the following template fields:
            
            1. [job_title]: Extract the specific job title from the posting
            2. [job description provided by hiring team]: Extract a concise summary of what the company is looking for
            3. [little internship and project descriptions of the applicant]: Identify 2-3 most relevant past experiences or projects from the resume that align with the job requirements
            4. [name]: Candidate's name from resume
            5. [college_name]: Educational institution from resume
            6. [Portfolio Link]: If available in resume
            
            Provide this information formatted for direct insertion into the template.""",
            agent=cold_email_template_analyzer,
            expected_output="""A structured JSON document containing:
            {
                "name": "Candidate's full name",
                "college_name": "University or college name",
                "job_title": "Position title from job posting",
                "job_description_summary": "Brief summary of key responsibilities/requirements",
                "relevant_experiences": "2-3 concise bullet points of most relevant work experiences/projects",
                "portfolio_link": "URL from resume if available"
            }"""
        )

        cold_email_writer = Agent(
            role="Cold Email Composer",
            goal="Create personalized cold outreach emails using a template and job-resume analysis",
            backstory="""You are a skilled email copywriter specializing in cold outreach for job 
            applications. You transform raw job and resume data into compelling, personalized emails 
            that catch hiring managers' attention. You understand how to maintain the template structure 
            while adding personalized elements that make each email feel custom-crafted.""",
            verbose=True,
            allow_delegation=False,
            llm="groq/llama3-70b-8192"
        )

        email_composition_task = Task(
    description="""Using the analyzed data from the job posting and resume, 
    compose a personalized cold outreach email following this exact template structure:
    
    "Hello Hiring Team,
    
    Hope you're doing well!
    
    I'm a [name] from [college_name] and I'm reaching out to express my interest in [job_title] internship with your team.
    
    I'm currently exploring internship opportunities in [job_title] and I noticed your team is [smoothly paraphrase the job description, focusing on the company's objectives, 
    technologies, and unique aspects of the role]. Over the past,
    [little work experience and project descriptions of the applicant related to job description], I realized how much
    I love building things people actually want to use. I've attached my resume and a couple of project
    samples to give you a quick look at what I've been up to.
    
    I would greatly appreciate the opportunity to discuss how I can contribute to your team. Could we schedule a brief chat at your convenience?
    
    Looking forward to connecting!"
    
    When filling in the placeholders, follow these guidelines:
    
    1. Names ([name]): Use proper name capitalization (e.g., "Sarthak" NOT "SARTHAK")
    2. Institution names ([college_name]): Use official capitalization (e.g., "Maharaja Agrasen Institute of Technology")
    3. Job titles ([job_title]): Use standard capitalization (e.g., "AI/ML Intern" NOT "AI/ML INTERN")
    4. Project names: Use title case for project names (e.g., "Customer Churn Prediction Using ANN" NOT "CUSTOMER CHURN PREDICTION USING ANN")
    5. Technologies: Maintain correct technical capitalization (e.g., "TensorFlow", "MySQL", "CNN")
    
    For the job description section:
    - Do NOT directly copy-paste from the original job posting
    - Rewrite and paraphrase the job description in a conversational way
    - Focus on what the company is trying to achieve rather than just listing requirements
    - Make it sound natural, as if you genuinely understand their needs
    - Limit to 1-2 sentences that flow naturally in the email
    - Connect it to your background in the following sentence
    
    For the work experience section:
    - Connect your experiences directly to the company's specific needs
    - Be specific about relevant skills rather than generic descriptions
    - Focus on outcomes and results where possible
    
    DO NOT use all caps for names, project titles, or other elements unless they are acronyms or initialisms (like "AI", "ML", "CNN").
    
    Format the work experience and project descriptions with proper punctuation and sentence structure while maintaining a professional tone.""",
    agent=cold_email_writer,
    expected_output="""A complete, ready-to-send cold outreach email with all template placeholders
    filled in with appropriate information and proper capitalization. The job description should be
    naturally paraphrased and integrated, NOT directly copied from the original posting. The email
    should demonstrate understanding of the company's needs while highlighting relevant candidate
    experience. The email must maintain the exact structure of the provided template while ensuring 
    the inserted information flows naturally within the content and follows standard professional 
    writing conventions."""
)


        crew = Crew(
            agents=[cold_email_template_analyzer, cold_email_writer],
            tasks=[template_data_analysis_task, email_composition_task],
            verbose=True,
            share_crew=True
        )


        result = crew.kickoff(inputs = {"job_description": job_description , 'resume_content':resume_content})
        
        return render_template('index.html' , result=result)
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)