# Cold Email Generator for Job Applications

## Project Overview

This project is a web-based application built using Flask that automatically generates personalized cold outreach emails for job applications. By uploading a resume (in PDF format) and providing a job description, the application analyzes the input using the **Groq** API and **LangChain** to craft a targeted and professional cold email.

## Features

* Upload PDF resume and job description.
* Automated extraction of relevant information using NLP.
* Personalized cold email generation.
* Uses advanced language models for content analysis.
* Interactive and user-friendly web interface.

## Tech Stack

* **Python**: Core programming language.
* **Flask**: Backend web framework.
* **Groq API**: For natural language understanding and processing.
* **LangChain**: For document parsing and analysis.
* **HTML/CSS**: Frontend templates.
* **Werkzeug**: Secure file handling.
* **Jinja2**: Templating engine for dynamic content.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cold-email-generator.git
   cd cold-email-generator
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the API key:

   * Create a `.env` file in the project root:

     ```bash
     touch .env
     ```
   * Add your Groq API key:

     ```
     GROQ_API_KEY=your_api_key_here
     ```

## Running the App

Start the Flask development server:

```bash
flask run
```

Access the app at `http://127.0.0.1:5000/`.

## Usage

1. Open the app in your browser.
2. Upload your PDF resume.
3. Enter the job description.
4. Click "Generate Email" to receive a personalized cold outreach email.

## File Structure

```
project-root/
├── app.py                  # Flask application
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
├── instance/uploads/       # Uploaded files
├── requirements.txt        # Python dependencies
└── .env                    # API key (not included in the repo)
```

## Deployment

1. Use **Gunicorn** for production:

   ```bash
   gunicorn app:app
   ```
2. Deploy on platforms like **Heroku** or **AWS EC2**.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests to improve the project.

## Contact

For any questions, feel free to reach out to me at \[[your.email@example.com](mailto:your.email@example.com)].
