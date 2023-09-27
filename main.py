import openai
import gradio as gr
import ast
from dotenv import load_dotenv
import os

# Load in the API key from the .env file or ask the user to input it
try:
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    openai.api_key = OPENAI_API_KEY
    if not OPENAI_API_KEY:
        raise ValueError("API key not found in .env file.")

except ValueError as e:
    print(e)
    OPENAI_API_KEY = input("Please enter your OpenAI API key: ")


def generate_output(input_text):
    """
    Obtain the model's response based on the input text, system message, and optional model parameters.
    
    Parameters:
    - input_text (str): Text input from the user.
    - system_message (str): System's instruction or context for the model.
    - model (str, optional): The model to be used. Defaults to "gpt-3.5-turbo".
    - temperature (float, optional): Sampling temperature. Defaults to 0.
    - max_tokens (int, optional): Maximum tokens to be generated by the model. Defaults to 500.

    Returns:
    - str: Model's completion based on input.
    """
    
    system_message = """You will take on the role of a researcher trying to write MyChart messages to recruit participants for clinical trials. You will get two examples of good MyChart messages as well as a list of information about a research study.

Using the information about the research study, craft a short, concise and captivating mychart message that follows the style and information content of the examples.

The following are example mychart messages:
Example 1:
"If you have type 2 diabetes, are at least 40 years old, and have a smartphone, you may be eligible to participate in a free and confidential research study investigating risk factors associated with blood glucose fluctuations. If you meet study criteria and decide to enroll, you will be asked to: · Complete an in-person questionnaire and interview · Wear a continuous glucose monitoring sensor for 14 days · Respond to short surveys on your smartphone, and wear an accelerometer on your wrist to measure your physical activity and sleep for 14 days · Complete two phone or ZOOM interviews to report your dietary intake You may receive up to $200, upon study completion. To learn more or to see if you are eligible to participate, click on “I’m interested” or call the ‘Help us Discover’ recruitment call center at 1-877-978-8343. This message is automated and is sent in an electronic manner based on your health record; no one has been inside or viewed your medical chart. No action by you is required. You may ignore this message or click “No, thank you.” Thank you very much for considering being a part of research at Yale. To learn about future research opportunities, you may also create a volunteer profile through the Research Tab in MyChart. To opt-out of all future research communications, please call the ‘Help us Discover’ recruitment call center at 1-877-978-8343 and select #3."

Example 2:
"If you are currently pregnant, own a smartphone, and are at least 18 years old, you may be eligible to participate in a free and confidential research study investigating better ways of identifying pregnant individuals who may need extra support during the perinatal period by analyzing patterns of smartphone use. If you meet study criteria and decide to enroll, you will be asked to give us some demographic information, information about your pregnancy (and birth of your child) and contact information so we will be able to be in touch with you during your participation in the study. We will also ask you to answer online surveys once a month and to temporarily install a passive data collection phone app called EARS. Additionally, we will request temporary access to some of your health records. You will be compensated up to $190 for participating. To learn more or to see if you are eligible to participate, click on “I’m interested” or call the ‘Help us Discover’ recruitment call center at 1-877-978-8343. This message is automated and is sent in an electronic manner based on your health record; no one has been inside or viewed your medical chart. No action by you is required. You may ignore this message or click “No, thank you”. Thank you very much for considering being a part of research at Yale. To learn about future research opportunities, you may also create a volunteer profile through the Research Tab in MyChart. To opt-out of all future research communications, please call the ‘Help us Discover’ recruitment call center at 1-877-978-8343 and select #3."

Output only the final mychart message, do not include any additional text.
"""

    user_message = f"{input_text}"

    messages = [
        {'role':'system', 
         'content': system_message},
        {'role':'user', 
         'content': user_message},
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0, 
        max_tokens=750,
    )
    return response.choices[0].message["content"]

  

# UI starts here
app = gr.Interface(
    fn = generate_output,
    inputs = gr.Textbox(lines=25, placeholder = "Please paste study summary here"),
    outputs = gr.Textbox(lines=25).style(show_copy_button=True)
)


app.launch()