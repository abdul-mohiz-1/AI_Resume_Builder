import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in .env file!")
            
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate(self, doc_type, user_details):
        prompts = {
            "resume": """You are an expert Resume Writer. Generate a highly professional resume based on the user's details. 
            You MUST strictly follow this EXACT Markdown structure. Do not skip any sections. If the user doesn't provide specific info for a section, use placeholder text (like [Your Name] or [Insert Details]).
            
            # [Full Name]
            **Phone:** [Phone Number] | **Email:** [Email Address] | **Address:** [City, Country] | **LinkedIn/Portfolio:** [URL]
            
            ---
            
            ## Career Objective
            [A 2-3 line professional summary or career objective aligned with the user's goals]
            
            ## Education
            **[Highest Degree]**
            *[University/College Name] - [City, Country]* | *[Year]*
            
            **[Previous Education]**
            *[School/College Name] - [City]* | *[Year]*
            
            ## Skills
            - **Programming & Tech:** [List skills]
            - **Tools & Frameworks:** [List tools]
            - **Soft Skills:** [List skills]
            
            ## Projects
            ### [Project Name]
            - [1-2 lines describing the project, your role, and the technologies used]
            
            ### [Project Name 2]
            - [1-2 lines describing the project, your role, and the technologies used]
            
            ## Work Experience
            ### [Job Title]
            **[Company Name] - [City]** | *[Year - Year]*
            - [Responsibility/Achievement 1]
            - [Responsibility/Achievement 2]
            
            ## Certifications / Courses
            - [Certification/Course Name] - [Issuing Organization]
            
            ## Languages
            - English
            - Urdu
            - [Any other languages]
            
            ## Interests / Hobbies
            - [Interest 1]
            - [Interest 2]
            
            ## References
            *References available upon request.*
            """,
            
            "cover_letter": """You are an elite Career Coach. Write a highly persuasive, modern, and elegant cover letter based on the provided details. 
            Use this exact structure:
            
            # [Full Name]
            **Email:** [Email] | **Phone:** [Phone] | **LinkedIn:** [URL]
            
            ---
            **Date:** [Current Date]
            
            **To:** Hiring Manager
            
            **Dear Hiring Manager,**
            
            **[The Hook]:** Start with a powerful, engaging opening sentence that grabs attention and states the role being applied for.
            
            **[The Value Proposition]:** 1-2 paragraphs detailing how the user's specific skills and experiences solve problems and add value to the company.
            
            **[Why This Company]:** A brief section showing enthusiasm for the industry or role.
            
            **[Call to Action]:** A confident closing expressing eagerness to discuss the role further in an interview.
            
            **Sincerely,** [Full Name]
            """,
            
            "linkedin": """You are an expert Personal Branding Coach. Create a highly engaging LinkedIn profile optimization package based on the details.
            Use this exact structure:
            
            ## 🔥 High-Impact Headlines (Choose One)
            - [Option 1: Role + Value Proposition]
            - [Option 2: Niche + Key Skills]
            - [Option 3: Creative & Engaging]
            
            ---
            
            ## 📝 'About' Section / Summary
            **[The Hook]:** An engaging first sentence that makes people want to click 'see more'.
            
            **[My Journey]:** A short, compelling narrative about the user's professional background and passion.
            
            **[What I Do / Expertise]:** Clear bullet points on current expertise and top skills.
            
            **[Let's Connect]:** A call to action (e.g., "Always open to discussing new opportunities. Reach me at [Email]").
            
            ---
            
            ## 🚀 Top Skills to Pin
            - [Skill 1]
            - [Skill 2]
            - [Skill 3]
            - [Skill 4]
            """
        }
        
        system_prompt = prompts.get(doc_type, prompts["resume"])

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here are my details: {user_details}"}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        return response.choices[0].message.content