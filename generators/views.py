from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse  # Import JsonResponse to send JSON responses
import google.generativeai as genai
from datetime import datetime
from html import escape
from django import forms
import pandas as pd
from io import StringIO

def home(request):
    return render(request, 'generators/home.html')


#one

def bio_generator(request):
    if request.method == 'POST':  # Check if the form is submitted
        profession_description = request.POST.get('profession_description')  # Get the input from the form
        if profession_description:  # If profession description is provided
            # Configure the Gemini API (replace with your actual API key)
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Construct the prompt for Gemini API
            prompt = f"""
            Based on the following description of a profession, list the perfect professional bio's. 
            The bio should be concise, engaging, and highlight key skills, accomplishments, and areas of expertise relevant to the profession.

            Profession Description: {profession_description}

            Ensure the bio is written in a professional tone and suitable for use in resumes, LinkedIn profiles, or personal websites.
            Only provide the list of all professional bio's.
            """

            try:
                # Call the Gemini API to generate the professional bio
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content([prompt])

                # Send JSON response for the result section
                return JsonResponse({
                    'success': True,
                    'generated_bios': response.text,
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f"Error generating bio: {e}"
                })
        
        # If input is missing, return error message
        return JsonResponse({
            'success': False,
            'error': "Please provide a profession description."
        })
    
    return render(request, 'generators/bio_generator.html')  # Render the bio generation form for GET request

#two
def interview_answer(request):
    if request.method == 'POST':  # Check if the form is submitted
        job_title = request.POST.get('job_title')  # Get job title from the form input
        interview_question = request.POST.get('interview_question')  # Get interview question from the form input
        if job_title and interview_question:  # If both fields are provided
            # Configure the Gemini API (replace with your actual API key)
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")
            
            # Construct the prompt for Gemini API
            prompt = f"""
            You are applying for the role of {job_title}. Provide a professional, detailed, and thoughtful answer to the following interview question:

            Question: {interview_question}

            Ensure the answer demonstrates relevant skills, experience, and alignment with the job responsibilities.
            only list all the perfect and clear answers for the candidate to answer the interview question. Don't include subheadings. Only use bullet points.
            """
            
            try:
                # Call the Gemini API to generate the interview answer
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content([prompt])
                
                # Return the generated answer as plain text
                return HttpResponse(response.text, content_type="text/plain")
            except Exception as e:  # Catch any errors that occur during the API call
                return HttpResponse(f"Error generating answer: {e}", content_type="text/plain")
        
        return HttpResponse("Please provide both job title and interview question.", content_type="text/plain")
    
    return render(request, 'generators/interview_answer.html')  # Render the interview answer generation form if it's a GET request


#three
import google.generativeai as genai
from django.shortcuts import render

genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

def interview_question_generator(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '')
        job_description = request.POST.get('job_description', '')
        question_type = request.POST.get('question_type', 'Technical')
        num_questions = int(request.POST.get('num_questions', 10))

        # Ensure both job_title and job_description are provided
        if job_title and job_description:
            prompt = f"""
            Generate {num_questions} {question_type} interview questions for a {job_title} role.
            Use the following job description to tailor the questions:

            Job Description: {job_description}

            Ensure the questions are relevant and aligned with the specified role and its responsibilities.
            Only generate the questions based on the given information with a question mark. Don't use any parentheses.
            """
            try:
                # Use the correct model for generating content
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content(prompt)  # Pass the prompt directly as a string
                questions = response.text if response else "No questions generated."

                # Pass the questions to the template to display in the result section
                return render(request, 'generators/interview_question_generator.html', {'questions': questions})
            except Exception as e:
                # Catch any errors from the API or network issues
                return render(request, 'generators/interview_question_generator.html', {'error': f"Error fetching questions: {e}"})
        else:
            return render(request, 'generators/interview_question_generator.html', {'error': 'Please fill out all fields!'})
    
    return render(request, 'generators/interview_question_generator.html')

#four
import google.generativeai as genai
from django.shortcuts import render


# Function to generate job description responsibilities based on job title
def get_job_description_from_title(job_title):
    genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")
    prompt = f"""
    Based on the job title '{job_title}', generate a detailed list of responsibilities needed for this job title, including:
    - Responsibilities

    The responsibilities should be clear, concise, and relevant to the given job title.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt])
    return response.text

# Django view for Job Responsibilities Generator
def job_responsibilities_generator(request):
    job_title = ''
    job_description = ''
    error = ''
    
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '')
        
        if job_title:
            try:
                # Generate the job description responsibilities
                job_description = get_job_description_from_title(job_title)
            except Exception as e:
                error = f"Error generating job description: {e}"
        else:
            error = 'Please enter a job title.'
    
    return render(request, 'generators/job_responsibilities_generator.html', {
        'job_title': job_title,
        'job_description': job_description,
        'error': error
    })


#five

import google.generativeai as genai
from django.shortcuts import render

# Function to generate job description based on job title


def get_job_description_from_title(job_title):
    prompt = f"""
    Based on the job title '{job_title}', generate a detailed job description including:
    - Responsibilities
    - Required Skills
    - Qualifications
    - Experience Required

    The job description should be clear, concise, and relevant to the given job title.
    """
    genai.configure(api_key="AIzaSyDbJIcsetgOpca1gupLXW1lZAwZDp649lY")

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt])
    return response.text

# Django view for Job Description Generator
def job_description_generator(request):
    job_title = ''
    job_description = ''
    error = ''
    
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '')
        
        if job_title:
            try:
                # Generate the job description
                job_description = get_job_description_from_title(job_title)
            except Exception as e:
                error = f"Error generating job description: {e}"
        else:
            error = 'Please enter a job title.'
    
    return render(request, 'generators/job_description_generator.html', {
        'job_title': job_title,
        'job_description': job_description,
        'error': error
    })



#six

from django.shortcuts import render
import google.generativeai as genai

# Function to get a suitable job title from the job description
def get_suitable_job_title_from_description(job_description):
    prompt = f"""
    Based on the following job description, analyze and generate the most suitable job title for the role:

    Job Description: '{job_description}'

    Please suggest all the most relevant job titles that perfectly fit the given job description.
    Only mention all the job titles in bullet points.
    """

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt])
    return response.text

# Django view function
def job_title_generator(request):
    job_title = None
    error = None

    if request.method == 'POST':
        job_description = request.POST.get('job_description', '')
        
        if job_description:
            try:
                # Configure the API key
                genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your valid API key
                
                # Fetch suitable job title from the Gemini API
                job_title = get_suitable_job_title_from_description(job_description)
            except Exception as e:
                error = f"Error generating job title: {e}"
        else:
            error = "Please enter a job description."

    return render(request, 'generators/job_title_generator.html', {'job_title': job_title, 'error': error})


#seven

# views.py
from django.shortcuts import render
import google.generativeai as genai

# Function to generate a letter of recommendation
def generate_recommendation(name, job_title, relationship, strengths, reason_for_fit):
    prompt = f"""
    Write a professional and compelling letter of recommendation for the following individual:

    - Name: {name}
    - Job Title: {job_title}
    - Relationship: {relationship}
    - Strengths, Skills, and Achievements: {strengths}
    - Why They Are a Good Fit: {reason_for_fit}

    The letter should be formal, well-structured, and emphasize their qualifications and suitability for the role they are applying for. Conclude with a positive and strong endorsement.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating letter: {e}"

def letter_of_recommendation(request):
    letter = ""
    error = ""
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        job_title = request.POST.get('job_title', '')
        relationship = request.POST.get('relationship', '')
        strengths = request.POST.get('strengths', '')
        reason_for_fit = request.POST.get('reason_for_fit', '')

        if name and job_title and relationship and strengths and reason_for_fit:
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your API key
            letter = generate_recommendation(name, job_title, relationship, strengths, reason_for_fit)
        else:
            error = "Please fill out all the fields!"

    return render(request, 'generators/letter_of_recommendation.html', {
        'letter': letter,
        'error': error
    })

#eight

from django.shortcuts import render
from django.http import HttpResponse
import google.generativeai as genai

# Function to generate mission statement based on company name and description
def get_mission_statement(company_name, company_description):
    prompt = f"""
    Based on the following company name and description, list the clear and impactful mission statements for the company:

    Company Name: {company_name}
    Description: {company_description}

    The mission statement should focus on the company's purpose, core values, and how it intends to serve its customers or stakeholders.
    don't include sub headings. only list it in the bulletin points.
    """

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt])
    return response.text

# View for Mission Statement Generator
def mission_statement_generator(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name', '')
        company_description = request.POST.get('company_description', '')

        if company_name and company_description:
            # Configure the API key
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Generate mission statement
            mission_statement = get_mission_statement(company_name, company_description)

            return render(request, 'generators/mission_statement_generator.html', {
                'company_name': company_name,
                'company_description': company_description,
                'mission_statement': mission_statement
            })
        else:
            return render(request, 'generators/mission_statement_generator.html', {
                'error': 'Please enter both company name and description.'
            })

    return render(request, 'generators/mission_statement_generator.html')


#nine

from django.shortcuts import render
import google.generativeai as genai

# Function to generate the offer letter based on user input
def generate_offer_letter(candidate_name, position_title, responsibilities, compensation, benefits):
    prompt = f"""
    Write a formal and professional offer letter for the following candidate:

    - Candidate Name: {candidate_name}
    - Position Title: {position_title}
    - Responsibilities: {responsibilities}
    - Compensation Package: {compensation}
    - Benefits: {benefits}

    The letter should be polite, clear, and professional. It should outline the position, responsibilities, compensation, and benefits in a positive tone while maintaining a formal structure. The offer should conclude with an invitation to accept the offer and join the company.
    The letter should be formal, polite, and professional. It should outline the following:

    1. A warm introduction to the candidate.
    2. A clear statement of the position title and compensation package.
    3. A description of the candidate's responsibilities and expectations.
    4. A list of the benefits offered.
    5. Proposed start date and response deadline.
    6. Instructions on how to respond, including signing and returning the letter.
    7. A polite conclusion, expressing excitement for the candidate to join the team.

    Be sure to include the company header, formal tone, and include placeholders where necessary.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating letter: {e}"

# View for Offer Letter Generator
def offer_letter_generator(request):
    if request.method == 'POST':
        candidate_name = request.POST.get('candidate_name', '')
        position_title = request.POST.get('position_title', '')
        responsibilities = request.POST.get('responsibilities', '')
        compensation = request.POST.get('compensation', '')
        benefits = request.POST.get('benefits', '')

        if candidate_name and position_title and responsibilities and compensation and benefits:
            # Configure the Gemini API key
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Generate the offer letter
            offer_letter = generate_offer_letter(candidate_name, position_title, responsibilities, compensation, benefits)

            return render(request, 'generators/offer_letter_generator.html', {
                'offer_letter': offer_letter,
                'candidate_name': candidate_name,
                'position_title': position_title,
                'responsibilities': responsibilities,
                'compensation': compensation,
                'benefits': benefits
            })
        else:
            return render(request, 'generators/offer_letter_generator.html', {
                'error': 'Please fill out all fields!'
            })

    return render(request, 'generators/offer_letter_generator.html')


#ten

from django.shortcuts import render
import google.generativeai as genai

# Function to generate job qualifications based on job title
def get_job_qualification_from_title(job_title):
    prompt = f"""
    Based on the job title '{job_title}', generate a detailed qualifications needed for this job title including:
    - Qualifications
    
    The qualifications should be clear, concise, and relevant to the given job title.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating qualifications: {e}"

# View for Job Qualification Generator
def job_qualification_generator(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '')

        if job_title:
            # Configure the Gemini API key
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Generate the job qualifications
            job_qualification = get_job_qualification_from_title(job_title)

            return render(request, 'generators/job_qualification_generator.html', {
                'job_qualification': job_qualification,
                'job_title': job_title
            })
        else:
            return render(request, 'generators/job_qualification_generator.html', {
                'error': 'Please enter a job title!'
            })

    return render(request, 'generators/job_qualification_generator.html')


#Eleven

from django.shortcuts import render
import google.generativeai as genai

# Function to get skills from Gemini API based on job title
def get_skills_from_gemini(job_title):
    prompt = f"""
    Based on the job title '{job_title}', generate a comprehensive list of skills required for the role. 
    The skills should be categorized into:
    1. Technical Skills
    2. Soft Skills
    Make sure to include relevant skills based on the job title and provide a brief explanation where necessary.
    If the title is not having the Technical Skills or Soft Skills remove that.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating skills: {e}"

# View for Skills Generator
def skills_generator(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '')

        if job_title:
            # Configure the Gemini API key
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Generate the skills based on the job title
            skills = get_skills_from_gemini(job_title)

            return render(request, 'generators/skills_generator.html', {
                'skills': skills,
                'job_title': job_title
            })
        else:
            return render(request, 'generators/skills_generator.html', {
                'error': 'Please enter a job title!'
            })

    return render(request, 'generators/skills_generator.html')


#twelve

from django.shortcuts import render
import google.generativeai as genai

# Function to generate vision statement from company name and description
def get_vision_statement(company_name, company_description):
    prompt = f"""
    Based on the following company name and description, list the clear and impactful vision statements for the company:

    Company Name: {company_name}
    Description: {company_description}

    The vision statement should be professional, inspiring, future-oriented, and reflective of the company's goals and values.
    Don't include subheadings. Only list it in bullet points.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating vision statement: {e}"

# View for Vision Statement Generator
def vision_statement_generator(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name', '')
        company_description = request.POST.get('company_description', '')

        if company_name and company_description:
            # Configure the Gemini API key
            genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

            # Generate the vision statement
            vision_statement = get_vision_statement(company_name, company_description)

            return render(request, 'generators/vision_statement_generator.html', {
                'vision_statement': vision_statement,
                'company_name': company_name,
                'company_description': company_description
            })
        else:
            return render(request, 'generators/vision_statement_generator.html', {
                'error': 'Please enter both company name and description!'
            })

    return render(request, 'generators/vision_statement_generator.html')

#thirteen


# Configure the API key for Google Gemini (PaLM)
genai.configure(api_key="AIzaSyBIlGPeWx1RBBUJYaqTqyEchB0UxLKcOrw")  # Replace with your actual API key

# Function to generate the speech
# Function to generate the speech
def generate_speech(occasion, audience, speech_length, message, tone_of_voice):
    prompt = f"""
    Generate a {speech_length} speech for a {occasion}. The audience will be {audience}. 
    The speech should convey the following message: '{message}'.
    The speech should be formal, appropriate for the occasion, and use a {tone_of_voice} tone of voice.
    """

    # Create a generative model instance
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    try:
        # Generate the speech using the provided prompt
        response = model.generate_content([prompt])
        return response.text  # Return the generated speech text
    except Exception as e:
        # Return error message in case of an exception
        return None, str(e)  # Return None if there's an error

# View to handle the speech generation form
def speech_writer(request):
    if request.method == 'POST':
        # Get input data from the form submission
        occasion = request.POST.get('occasion')
        audience = request.POST.get('audience')
        speech_length = request.POST.get('speech_length')
        message = request.POST.get('message')
        tone_of_voice = request.POST.get('tone_of_voice')
        
        # Debugging: print the form data to the console
        print(f"Occasion: {occasion}, Audience: {audience}, Speech Length: {speech_length}, Message: {message}, Tone: {tone_of_voice}")

        # Check if all fields are provided
        if all([occasion, audience, speech_length, message, tone_of_voice]):
            # Generate the speech
            speech, error = generate_speech(occasion, audience, speech_length, message, tone_of_voice)
            
            if speech:
                # Return the generated speech in JSON response
                return JsonResponse({'speech': speech})
            else:
                # Return an error message if speech generation failed
                return JsonResponse({'error': f"Speech generation failed: {error}"}, status=500)
        else:
            # Return an error if any field is missing
            return JsonResponse({'error': 'All fields are required'}, status=400)

    # If it's a GET request, simply render the form page
    return render(request, 'generators/speech_writter.html')


#fourteen

# Configure the Gemini API key (ensure this is secured in environment variables)
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

def generate_character_reference(request):
    if request.method == "POST":
        recipient_name = request.POST.get("recipient_name")
        relationship = request.POST.get("relationship")
        strengths = request.POST.get("strengths")
        weaknesses = request.POST.get("weaknesses", "")  # Optional field
        job_description = request.POST.get("job_description")

        if not all([recipient_name, relationship, strengths, job_description]):
            return JsonResponse({"error": "Please fill out all required fields!"}, status=400)

        prompt = f"""
        Write a formal and personalized character reference letter for the following individual:

        - Recipient's Name: {recipient_name}
        - Relationship to the Writer: {relationship}
        - Strengths: {strengths}
        - Weaknesses: {weaknesses}
        - Job/Position Applied For: {job_description}

        The letter should emphasize the subject's character, strengths, and potential while providing a balanced, professional tone. Conclude with a strong endorsement of their qualifications and suitability for the position.
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content([prompt])
            return JsonResponse({"letter": response.text})
        except Exception as e:
            return JsonResponse({"error": f"Error generating letter: {e}"}, status=500)

    return render(request, "generators/reference_letter.html")

#fiveteen

# Configure the Gemini API
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate LinkedIn bio
def generate_linkedin_bio(personal_info):
    """
    Generate a LinkedIn bio based on the provided personal information.
    """
    prompt = f"""
    Create a professional LinkedIn bio based on the following personal information:

    {personal_info}

    The LinkedIn bio should be:
    - Concise, professional, and written in the first person.
    - Summarize the key points of the person's experience, skills, and achievements.
    - Include key skills and strengths that make the person stand out professionally.
    - Include relevant accomplishments and background in a structured way.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating LinkedIn bio: {e}"

# View to render the LinkedIn bio generator form
def linkedin_bio_generator(request):
    if request.method == "POST":
        personal_info = request.POST.get("personal_info", "")
        if personal_info.strip():
            bio = generate_linkedin_bio(personal_info)
            if bio.startswith("Error"):
                return JsonResponse({"error": bio}, status=400)
            return JsonResponse({"bio": bio})
        return JsonResponse({"error": "Please provide valid personal information."}, status=400)

    return render(request, "generators/linkedin_bio.html")

#sixteen

# Configure GenAI API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate performance review
def generate_performance_review(employee_name, job_title, key_achievements):
    """
    Generate a performance review based on the employee's name, job title, and key achievements.
    """
    prompt = f"""
    Generate a detailed and personalized performance review for an employee with the following details:

    Employee Name: {employee_name}
    Job Title: {job_title}
    Key Achievements: {key_achievements}

    The performance review should include:
    1. A positive introduction acknowledging the employee’s contributions.
    2. A focus on key achievements, highlighting what the employee has done well.
    3. Recognition of the employee’s strengths in skills such as teamwork, leadership, communication, and technical abilities.
    4. Specific areas of improvement or focus for the next quarter or year, with suggestions for professional development.
    5. SMART objectives for future goals.
    6. A rating (1 to 5).
    7. Recommendations for future growth.
    Dont include headings.
    Use a friendly and professional tone, and make sure the review is constructive and motivating.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating performance review: {e}"

# Django view for the performance review generator
def performance_review_view(request):
    if request.method == "POST":
        employee_name = request.POST.get("employee_name")
        job_title = request.POST.get("job_title")
        key_achievements = request.POST.get("key_achievements")

        if employee_name and job_title and key_achievements:
            # Generate the performance review
            review = generate_performance_review(employee_name, job_title, key_achievements)
            return JsonResponse({"review": review})
        else:
            return JsonResponse({"error": "All fields are required!"}, status=400)
    return render(request, "generators/generate_per_re.html")

#seventeen


# Configure the GenAI API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your actual API key

# Function to generate interview feedback
def generate_feedback(job_title, feedback_notes, candidate_name, interviewer_name, interview_date):
    prompt = f"""
    Generate a detailed and professional interview feedback report:

    Candidate Name: {candidate_name}
    Interviewer: {interviewer_name}
    Date of Interview: {interview_date}
    Job Title: {job_title}
    Feedback Notes: {feedback_notes}

    The feedback should include:
    - Overall Impression
    - Technical Skills (with specific examples if applicable)
    - Soft Skills (such as communication, teamwork, adaptability)
    - Areas for Improvement
    - Final Recommendation for hiring suitability

    Ensure the tone is formal, encouraging, and professional. Format the feedback using markdown for better readability.
    """
    try:
        # Generate the content using GenAI
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating feedback: {e}"

# Django view for the form
def interview_feedback_view(request):
    if request.method == 'POST':
        # Get data from the form
        candidate_name = request.POST.get('candidate_name', '').strip()
        interviewer_name = request.POST.get('interviewer_name', '').strip()
        interview_date = request.POST.get('interview_date', '').strip()
        job_title = request.POST.get('job_title', '').strip()
        feedback_notes = request.POST.get('feedback_notes', '').strip()

        # Validate form inputs
        if all([candidate_name, interviewer_name, interview_date, job_title, feedback_notes]):
            # Generate the feedback
            feedback = generate_feedback(job_title, feedback_notes, candidate_name, interviewer_name, interview_date)
            return JsonResponse({'success': True, 'feedback': feedback})
        else:
            return JsonResponse({'success': False, 'error': 'Please fill in all the fields.'})
    return render(request, 'generators/interview_feedback.html')


#eighteen

# Configure Gemini API
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your actual API key

# Function to generate LinkedIn connection request
def generate_connection_message(your_name, your_goals, person_name, how_you_know_them, specific_action):
    prompt = f"""
    Create a personalized LinkedIn connection request message based on the following details:

    - Your Name: {your_name}
    - Your Goals: {your_goals}
    - Person's Name: {person_name}
    - How You Know Them: {how_you_know_them}
    - Specific Action Requested: {specific_action}

    Ensure the message is:
    - Polite and professional
    - Personalized to the person and the context
    - Concise and clear about the purpose of connecting

    Format the output as a professional LinkedIn connection message.
    """
    try:
        # Use the Gemini model to generate content
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating message: {e}"

# Main view for LinkedIn Connection Request Generator
def linkedin_request_view(request):
    if request.method == "POST":
        your_name = request.POST.get("your_name")
        your_goals = request.POST.get("your_goals")
        person_name = request.POST.get("person_name")
        how_you_know_them = request.POST.get("how_you_know_them")
        specific_action = request.POST.get("specific_action")

        if all([your_name, your_goals, person_name, how_you_know_them, specific_action]):
            message = generate_connection_message(
                your_name, your_goals, person_name, how_you_know_them, specific_action
            )

            if message.startswith("Error"):
                return JsonResponse({"success": False, "error": message})
            else:
                return JsonResponse({"success": True, "message": escape(message)})
        else:
            return JsonResponse({"success": False, "error": "All fields are required."})

    return render(request, "generators/linkedin_request.html")

#nineteen


# Configure the Gemini API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your actual API key

# Form definition
class ResumeBulletPointForm(forms.Form):
    job_title = forms.CharField(label="Job Title", max_length=100, required=True)
    skills = forms.CharField(label="Relevant Skills", widget=forms.Textarea, required=True)
    key_responsibilities = forms.CharField(label="Key Responsibilities", widget=forms.Textarea, required=True)
    key_achievements = forms.CharField(label="Key Achievements", widget=forms.Textarea, required=True)

# Function to generate resume bullet points
def generate_resume_bullets(job_title, skills, key_responsibilities, key_achievements):
    prompt = f"""
    Write professional and concise resume bullet points based on the following inputs:

    - Job Title: {job_title}
    - Skills: {skills}
    - Key Responsibilities: {key_responsibilities}
    - Key Achievements: {key_achievements}

    The bullet points should:
    1. Use action verbs and quantify achievements where possible.
    2. Be specific to the job title provided.
    3. Highlight key accomplishments and contributions.
    4. Be formatted as bullet points.

    Ensure the tone is professional and impactful, and the content is formatted using markdown bullet points for easy readability.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating bullet points: {e}"

# Main view to handle the form
def resume_bullet_generator(request):
    if request.method == "POST":
        form = ResumeBulletPointForm(request.POST)
        if form.is_valid():
            # Extract form data
            job_title = form.cleaned_data["job_title"]
            skills = form.cleaned_data["skills"]
            key_responsibilities = form.cleaned_data["key_responsibilities"]
            key_achievements = form.cleaned_data["key_achievements"]

            # Generate bullet points
            result = generate_resume_bullets(job_title, skills, key_responsibilities, key_achievements)

            # Check for errors
            if result.startswith("Error"):
                return JsonResponse({"success": False, "error": result})
            
            return JsonResponse({"success": True, "bullet_points": result})
    else:
        form = ResumeBulletPointForm()

    return render(request, "generators/resume_bullet_points.html", {"form": form})

#tweenty


# Configure the Gemini API key (replace with your actual API key)
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate peer review
def generate_peer_review(name, overall_feedback, key_strengths, areas_for_improvement):
    """
    Generate a professional peer review based on the inputs.
    """
    prompt = f"""
    Generate a constructive and professional peer review for the following colleague:

    - Name: {name}
    - Overall Feedback: {overall_feedback}
    - Key Strengths: {key_strengths}
    - Areas for Improvement: {areas_for_improvement}

    The review should:
    1. Highlight the key strengths and contributions of the individual.
    2. Provide specific suggestions for improvement in the identified areas.
    3. Maintain a positive and constructive tone.
    4. Be formatted as a professional review.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating peer review: {e}"

# Main view for the peer review generator
def peer_review_generator(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        overall_feedback = request.POST.get("overall_feedback", "").strip()
        key_strengths = request.POST.get("key_strengths", "").strip()
        areas_for_improvement = request.POST.get("areas_for_improvement", "").strip()

        if not (name and overall_feedback and key_strengths and areas_for_improvement):
            return JsonResponse({"success": False, "error": "All fields are required."})

        # Generate the peer review
        review = generate_peer_review(name, overall_feedback, key_strengths, areas_for_improvement)

        if review.startswith("Error"):
            return JsonResponse({"success": False, "error": review})

        return JsonResponse({"success": True, "review": review})

    return render(request, "generators/peer_review.html")

#twentyone
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse

# Function to generate SOP based on the user inputs
def generate_sop(procedure, steps, additional_details):
    """
    Generate a professional Standard Operating Procedure (SOP) based on the inputs.
    """
    # Set the API key within the function to ensure it is configured properly.
    genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")
    
    # Construct the prompt for the generative model
    prompt = f"""
    Generate a detailed and professional Standard Operating Procedure (SOP) for the following:

    - Procedure: {procedure}
    - Steps/Details: {steps}
    - Additional Context: {additional_details}

    The SOP should:
    1. Be structured with a clear title, introduction, and step-by-step instructions.
    2. Include any important considerations or notes based on the context provided.
    3. Be formatted professionally with numbered steps and sections.
    """
    
    try:
        # Create the generative model object
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Make the API call to generate the content
        response = model.generate_content([prompt])
        
        # Return the generated content (SOP)
        return response.text
    
    except Exception as e:
        # Return error message if something goes wrong
        return f"Error generating SOP: {str(e)}"


# View to handle SOP generation
def sop_generator(request):
    if request.method == 'POST':
        # Get data from the form submission
        procedure = request.POST.get('procedure')
        steps = request.POST.get('steps')
        additional_details = request.POST.get('additional_details')
        
        # Ensure all fields are filled out
        if not (procedure and steps and additional_details):
            return JsonResponse({"error": "Please fill in all fields!"}, status=400)

        # Generate SOP by calling the function
        sop = generate_sop(procedure, steps, additional_details)
        
        # Check if SOP generation failed
        if sop.startswith("Error"):
            return JsonResponse({"error": sop}, status=500)

        # Return SOP as JSON for the front-end to display
        return JsonResponse({"success": True, "sop": sop})

    # If not a POST request, render the SOP form page
    return render(request, 'generators/sop_generator.html')

#twentytwo


# Configure the API key globally (set in settings.py or directly in the function)
def configure_genai_api():
    """
    Ensure the Generative AI API is configured properly.
    """
    try:
        genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")
    except Exception as e:
        raise RuntimeError(f"Error configuring GenAI API: {str(e)}")

# Function to generate LinkedIn post
def generate_linkedin_post(post_details, tone, length):
    """
    Generate a LinkedIn post based on user inputs.
    """
    # Ensure API configuration
    configure_genai_api()

    prompt = f"""
    Create a LinkedIn post with the following details:
    
    - Post content: {post_details}
    - Tone of voice: {tone}
    - Output length: {length}
    
    The post should be engaging, professional, and formatted appropriately for LinkedIn.
    """

    try:
        # Create generative model object
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        # Generate the content
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating LinkedIn post: {str(e)}"

# View for LinkedIn post generator
def linkedin_post_generator(request):
    if request.method == "POST":
        post_details = request.POST.get("post_details")
        tone = request.POST.get("tone")
        length = request.POST.get("length")

        # Validate input
        if not post_details or not tone or not length:
            return JsonResponse({"error": "Please fill in all the fields!"}, status=400)

        # Generate LinkedIn post
        linkedin_post = generate_linkedin_post(post_details, tone, length)

        # Check for errors in the generation process
        if linkedin_post.startswith("Error"):
            return JsonResponse({"error": linkedin_post}, status=500)

        # Return the generated post
        return JsonResponse({"success": True, "linkedin_post": linkedin_post})

    # Render the HTML form if it's a GET request
    return render(request, "generators/linkedin_post_generator.html")


#twentythree


# Configure the Gemini API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your actual API key

# Function to generate a job summary based on user inputs
def generate_job_summary(job_title, company_details):
    """
    Generate a professional job summary based on the inputs.
    """
    prompt = f"""
    Generate a professional and attention-grabbing job summary for the following:

    - Job Title: {job_title}
    - Company Overview and Expectations: {company_details}

    The job summary should:
    1. Be clear, concise, and engaging.
    2. Highlight the key responsibilities, company culture, and unique aspects of the position.
    3. Use professional language suitable for job postings.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating job summary: {e}"

# Django view to handle the job summary generation
def job_summary_generator(request):
    if request.method == "POST":
        job_title = request.POST.get("job_title")
        company_details = request.POST.get("company_details", "")

        if not job_title:
            return JsonResponse({"error": "Please enter a Job Title!"}, status=400)

        # Generate job summary
        job_summary = generate_job_summary(job_title, company_details)

        if job_summary.startswith("Error"):
            return JsonResponse({"error": job_summary}, status=500)

        return JsonResponse({"success": True, "job_summary": job_summary})

    # Render the HTML form if it's a GET request
    return render(request, "generators/job_summary_generator.html")

#twentyfour


# Configure the API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")  # Replace with your actual API key

# Function to generate Key Results based on the Objective
def generate_key_results(objective):
    """
    Generate actionable Key Results based on the provided Objective.
    """
    prompt = f"""
    Generate 3-5 actionable Key Results for the following Objective:
    
    - Objective: {objective}
    
    The Key Results should:
    1. Be specific, measurable, and relevant to the objective.
    2. Include achievable targets with a timeline where applicable.
    3. Use a professional and clear format suitable for OKRs.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating Key Results: {e}"

# Django view for OKR Generator
def okr_generator(request):
    if request.method == "POST":
        objective = request.POST.get("objective")
        if not objective:
            return JsonResponse({"error": "Please enter an Objective!"}, status=400)

        # Generate Key Results
        key_results = generate_key_results(objective)

        if key_results.startswith("Error"):
            return JsonResponse({"error": key_results}, status=500)

        return JsonResponse({"success": True, "key_results": key_results})

    # Render the HTML form for GET requests
    return render(request, "generators/okr_generator.html")

#twentyfive


# Configure the Gemini API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate KPIs
def generate_kpis(business_name, goals, metrics, time_frame):
    prompt = f"""
    Generate Key Performance Indicators (KPIs) for the following inputs:

    - Business or Project Name: {business_name}
    - Goals: {goals}
    - Key Metrics: {metrics if metrics else "N/A"}
    - Time Frame: {time_frame if time_frame else "Not specified"}

    The KPIs should be clear, measurable, and relevant to the input details. Provide actionable and professional suggestions.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating KPIs: {e}"

# KPI Generator View
def kpi_generator(request):
    if request.method == "POST":
        business_name = request.POST.get("business_name")
        goals = request.POST.get("goals")
        metrics = request.POST.get("metrics")
        time_frame = request.POST.get("time_frame")

        if business_name and goals:
            kpis = generate_kpis(business_name, goals, metrics, time_frame)
            if kpis.startswith("Error"):
                return JsonResponse({"success": False, "error": kpis})
            return JsonResponse({"success": True, "kpis": kpis})
        return JsonResponse({"success": False, "error": "Please provide the Business Name and Goals!"})
    return render(request, "generators/kpi_generator.html")

#twentysix


# Configure the Gemini API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate staff schedule
def generate_schedule(team_name, team_members, roles, availability, time_frame):
    prompt = f"""
    Create a professional and detailed staff schedule for the following:

    - Team/Organization Name: {team_name}
    - Team Members and Roles: {team_members} with corresponding roles: {roles if roles else "N/A"}
    - Availability: {availability if availability else "Assume all members are fully available during working hours."}
    - Time Frame: {time_frame if time_frame else "Weekly"}

    The schedule should ensure:
    1. Fair distribution of tasks.
    2. Overlapping availability for team collaboration.
    3. Clear role assignments and task descriptions.

    Present the schedule in a structured and easy-to-read format.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating schedule: {e}"

# Function to convert schedule to CSV
def convert_schedule_to_csv(schedule_text):
    try:
        schedule_lines = schedule_text.strip().split("\n")
        schedule_data = []
        for line in schedule_lines:
            if ":" in line:
                parts = line.split(":", 1)
                schedule_data.append([parts[0].strip(), parts[1].strip()])
            elif "|" in line:
                columns = [col.strip() for col in line.split("|") if col.strip()]
                schedule_data.append(columns)
        max_columns = max(len(row) for row in schedule_data)
        formatted_data = pd.DataFrame(schedule_data, columns=[f"Column {i+1}" for i in range(max_columns)])
        return formatted_data.to_csv(index=False)
    except Exception as e:
        return f"Error converting to CSV: {e}"

# Django view to handle schedule generation
def schedule_view(request):
    if request.method == "POST":
        team_name = request.POST.get("team_name")
        team_members = request.POST.get("team_members")
        roles = request.POST.get("roles", "")
        availability = request.POST.get("availability", "")
        time_frame = request.POST.get("time_frame", "Weekly")

        if team_name and team_members:
            schedule = generate_schedule(team_name, team_members, roles, availability, time_frame)
            if schedule.startswith("Error"):
                return JsonResponse({"success": False, "error": schedule})
            else:
                csv_data = convert_schedule_to_csv(schedule)
                return JsonResponse({"success": True, "schedule": schedule, "csv": csv_data})
        else:
            return JsonResponse({"success": False, "error": "Team Name and Team Members are required!"})
    return render(request, "generators/schedule.html")

#twentyseavan


# Configure the Gemini API key
genai.configure(api_key="AIzaSyB46sAin3C4rTXYCmXkmfQho4fzNUMH6Rw")

# Function to generate HR policy
def generate_policy(company_name, country, policy_name, policy_details, job_title, company_size):
    """
    Generate a professional HR policy based on the user inputs.
    """
    prompt = f"""
    Generate a detailed and professional HR policy for the following:

    - Company Name: {company_name}
    - Country/Region: {country}
    - Policy Name: {policy_name}
    - Policy Details: {policy_details}
    - Job Title: {job_title}
    - Company Size: {company_size}

    The policy should:
    1. Be structured with a clear title and introduction.
    2. Include all the provided details in a professional manner.
    3. Be formatted with sections and proper HR language.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating policy: {e}"

# View for the Policy Generator
def policy_generator(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        country = request.POST.get("country", "")
        policy_name = request.POST.get("policy_name")
        policy_details = request.POST.get("policy_details")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name", "")
        job_title = request.POST.get("job_title", "")
        company_size = request.POST.get("company_size")

        if not company_name or not policy_name or not policy_details:
            return JsonResponse({"success": False, "error": "Please fill in all required fields!"})

        # Generate the policy
        policy = generate_policy(company_name, country, policy_name, policy_details, job_title, company_size)
        if policy.startswith("Error"):
            return JsonResponse({"success": False, "error": policy})
        
        return JsonResponse({"success": True, "policy": policy})
    
    return render(request, "generators/policy_generator.html")
