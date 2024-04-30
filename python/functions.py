# -------------------------------------------------------------------
# Libraries
# -------------------------------------------------------------------

import os
import json
import pandas as pd

import openai
from openai import OpenAI

import google.generativeai as genai

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# -------------------------------------------------------------------
# User-Defined Functions
# -------------------------------------------------------------------
# ---------------------------
# API Functions
# ---------------------------

def google_api_test(googleai_api_key):
    
    genai.configure(api_key=googleai_api_key)
    
    genai_model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
    )

    try:
        response = genai_model.generate_content("Return: 'Ok'")
        return response.candidates[0].content.parts[0].text.replace(" \n", "")
        
    except Exception as e:
        return e    
    
def openai_api_test(openai_api_key):

    os.environ["OPENAI_API_KEY"] = openai_api_key
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    try:    
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Return 'Ok'",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.to_dict()["choices"][0]["message"]["content"]
        
    except Exception as e:
        return e    
    
# ---------------------------
# GoogleAI Responses
# ---------------------------
    
### > Text-to-text    
def t2t(text):
    response = genai_model.generate_content(text)
    
    return response.text    

### > Image-to-text
def i2t(img):
    """
    image to text
    """
    response = genai_model.generate_content(img)
    
    return response.text

### > Text & Image-to-text
def ti2t(text, img):
    """
    The generate_content method can handle a wide variety of use cases depending on what the underlying model supports, including:
    * multi-turn chat
    * multimodal input. 
    
    The available models only support text and images as input, and text as output.
    """
    response = genai_model.generate_content([text, img])
    
    return response.text

# ---------------------------
# ■ OpenAI (Dall-E) responses
# ---------------------------
### > Text-to-image

def get_image_from_DALL_E_3_API(user_prompt,
                               image_dimension="1024x1024",
                               image_quality="hd", #"standard"
                               model="dall-e-3",
                               nb_final_image=1):
   response = client.images.generate(
     model = model,
     prompt = user_prompt,
     size = image_dimension,
     quality = image_quality,
     n=nb_final_image,
   )


   image_url = response.data[0].url
  
   display(Image(url=image_url))
   
### > Massive Image Generation   
def AI_image_generation(main_script, i):
    response = client.images.generate(
     model = "dall-e-3",
     prompt = main_script["panels"][i]["ai_image_prompt"],
     size = "1024x1024",
     quality = "hd",
     n=1,
    )
    
    image_url = response.data[0].url
    
    response = requests.get(image_url)
    image_data = response.content
    original_image = Image.open(BytesIO(image_data))
    
    width, height = original_image.size 
    
    top_margin = 40
    bottom_margin = 0
    
    new_width = width
    new_height = height + top_margin + bottom_margin
    
    # Create a new image with added top and bottom margins
    new_width = original_image.width
    new_height = original_image.height + top_margin + bottom_margin
    new_image = Image.new("RGB", (new_width, new_height), color="white")
    new_image.paste(original_image, (0, top_margin))
    
    # Add text to the bottom margin
    draw = ImageDraw.Draw(new_image)
    font = ImageFont.load_default(30)
    
    draw.text((10, 0), f"Title: {main_script['title']}", fill =(0, 0, 0),font=font)
    draw.text((width * 3 //4 + 100 , 0), f"Panel: {main_script['panels'][i]['panel_number']}", fill =(0, 0, 0),font=font)
    
    new_image.save(f"images/{i+1}_{main_script['title'].replace(' ', '_')}.jpg")
    
# ---------------------------
# Script Generation
# ---------------------------
def s0_meta_userprompt_info(user_input):
    """
    Meta information from user Input.
    The user starts with a simple story idea. This function will compile different metadata from it.
    """
    
    prompt_ui = f"""This tool analyzes and organizes elements of a statement into a JSON object. You'll provide the statement within triple ticks after the following instructions.
    
    The JSON response will categorize the statement based on these key-value pairs:
    
    main_characters: Who are the people involved? Infer the character's job and refer to them by gender and job position. ("User" if the implicit author of the statement is active during the statement, "None" if directed at "you", or unclear, or the implicit author of the statement just gives an instruction). Separate by commas every explicitly mentioned character. 
    place: Where does the statement take place? Separate by commas all mentioned locations (return a single "None" if unclear).
    object: Separate by commas physical, real-world objects (not places, digital media). Ignore if similar to "place". (return a single "None" if unclear). (return a single "None" if unclear).
    goal: Provide a detailed overall objective of the statement. If it's about creating content (video, short, TikTok, commercial), restate it as a "short story" for clarity.
    genre: Infer the movie genre of the story. (Return 'Slice of life' if unclear)
    action: What's happening? Does the object or main character have an action? Provide a JSON object with "object_action" and "character_action" keys with their respective evaluations. (Rewrite the answer for 'character_action' as 'None' when the action is related, similar, or equal to the overall objective of the statement)
    weather: Does the statement mention any weather conditions? Separate by commas all mentioned elements (None if unclear).
    category: The statement's category: 'Business' (transactions/solutions/business or merchandise promotion), 'Educational' (teaching), or 'Entertainment' (default). 
    restrictions: Separate by commas anything the statement says shouldn't be included. (return a a single "None" if unclear).
    Now, please provide the statement for analysis within triple ticks ```{user_input}```
    """    

    p0  = dummy_json_parser(t2t, prompt_ui)
    
    return p0
    
def s1_scene_treatment(p0):
    """
    Scene treatment
    The metadata compiled from the previous step will be extended into a full scene.
    """
    
    vague_idea = f"State a single graphic narration of a plot idea. The original concept development for this story has the goal of a `{p0['goal']}` in the genre `{p0['genre']}` and with the purpose of `{p0['category']}`.  I want your input to provide a more thorough description of the concept, and to construct a narrative chain order. I want the story plot to be composed of simple places, objects, and people to facilitate the understanding. Don't propose fantasy lands, space, or unreachable places to humans like the bottom of the ocean; unless explicitly asked. No fantastical elements like talking animals or dragons."
    
    str = "" 
    
    if "None" in [val for val in p0.values()]:    
        
        str = "Be mindful about incorporating the following elements into the plot: \n "
        
        if p0["main_characters"] == "None":
            str += "* main_characters: Define the main characters involved in the development of the story. Describe them with gender, job position, and personality traits that would move the plot forward. Give them a human name. Contain each description within a sentence. \n "
        
        if p0["place"] == "None":
            str += "* place: Define a physical location where the story would make the most sense to take place. Consider any place accessible to the public, even businesses or a home. No fantastical settings. No space settings. No bottom of the sea. \n "
        
        if p0["object"] == "None":
            str += "* object: Define an object that is relevant to the plot of the story. An object that facilitates reaching the goal of the story. Consider the symbolism of the object to represent an idea or quality in benefit of the evolution of the story. \n "
            
        if p0["weather"] == "None":
            str += "* weather: Define the best weather conditions in tune to the mood of the story. \n "
            
        if p0["action"]["object_action"] == "None":
            str += "* object_action: What's happening with the object? Is the object involved in any action(s)? \n "
                
        if p0["action"]["character_action"] == "None":
            str += "* character_action: What's happening with the characters? In what actions are the characters involved? \n "
            
        if p0["restrictions"] == "None":
            str += "\n Additionally, keep the story according to PG-13 movie guidelines. \n "
        
    str += "Remember, don't format your answer with the previous list of element. I just a straight narration with the plot for the story."
    
    main_plotline = t2t(vague_idea + str)    

    return main_plotline        

def s2_script_prompt(p0, main_plotline):
    
    scene_treatment_prompt = f"""Task: You are a comic book writer tasked with creating a script for graphic narration. This script will guide your artist collaborator in drawing each panel of the comic book. You consider the following plotline as main guideline: `{main_plotline}`.
    
    Starting Point: Choose a story premise that aligns with the goal of a `{p0['goal']}` in the genre `{p0['genre']}` and with the purpose of `{p0['category']}`. Here are your options:
    
    * "What if?": Explores reality-based issues and fabrications, focusing on fundamental human concerns like fear and curiosity. Teaches the audience how to handle threats.
    * "Let me tell you what happened to": Relates a private event involving a relatable character, sharing intimate experiences with the audience.
    * "Our protagonist is thrown into this new adventure": Features a well-defined character facing a straightforward, challenging adventure. This premise involves simple problems and one-dimensional characters.
    * "Have you heard about...?": Centers around a joke that leads to an unexpected conclusion, utilizing humor techniques like irony, wordplay, and misdirection. Starts with a prologue.
    
    Script Framework: Structure your script as a JSON object with the following keys:
    
    * "title": Place only once an appropriate title for the story at the beginning of the JSON object.
    * "characters": List characters using upper case for character names. Describe them on detail and include some background that would serve the storyline.
    * "settings": Describe the settings where and when the storyline takes place. If historical context isn't provided, assume a current day setting. Characters are free to roam through multiple settings if the storyline is large. 
    * "panels": Array of objects, each object representing a panel in the comic. The panels should contain:
      - "panel_number": Mandatory. Numeric identifier for each panel.
      - "panel_description": Mandatory. Provide a detailed graphic narration of the scene, including character appearances and actions.
      - "characters_involved": Make a list of the characters that are mentioned during the scene. If unclear return an empty list.
      - "setting_involved": Generate a dictionary outlining the setting featured in the panel. . Each dictionary should contain three key-value pairs: "setting" for the setting itself, "perspective" for whether it's observed from an "interior" or "exterior" perspective, and "location" for whether it's located within a "building" or "outdoor space". Ensure to only include one of the settings that have been previously specified. 
      - "captions": Optional. Use "CAPTION:" followed by the text to add context such as time, location, or background information.
      - "dialogue": Optional. Use the format 'CHARACTER NAME: dialogue text' for speaking characters. Use "NO POINTER:" for speaking characters not yet introduced.
    vague_idea
    
    Detailed Guidelines:
    * Panels: 
      - Visual Description: Provide detailed descriptions for the artist, covering the development of the scene, character appearances, and actions.
      - Segmented Panels: Break the script into numbered panels, each depicting a specific action or moment.
      - Character Development: Include detailed character descriptions such as physical appearance, attire, and personality traits. Describe character gestures that are easy to watch and understand. Utilize pantomime to vividly depict the character's actions and expressions, enhancing the narrative through silent, expressive motions.
      - Captions Usage: Use captions to add context, such as time, location, and background information.
      - Genre and Historical Context: Maintain consistency with the chosen genre and historical context.
      - Emotional Engagement: Craft scenes that evoke emotions aligned with the genre, enhancing character interactions and visual storytelling.
      - Storytelling Structure: Ensure the script follows a linear progression, integrating flashbacks or past references seamlessly when necessary.
      - Main Storyline: Develop a compelling main storyline to guide the narrative.
      - Character Design and Imagery: Focus on creating visually memorable characters and scenes.
      - Dialogue and Interaction: Use dialogue to advance the plot, develop characters, and reveal relationships and motivations.
      - Purpose: Your script should aim to meet the project’s goal, fit within the specified genre, and fulfill the intended category.
    
    """
    
    main_script = dummy_json_parser(t2t, scene_treatment_prompt)

    return main_script

def s3_internal_setting_update(main_script):
    """
    This function will augment with visual details about the location where the story takes place.
    This facilitates consistent AI image prompting
    """
    
    for s in main_script["settings"]:
        setting_update = t2t(f"Revise and elaborate on the physical description of the location `{s}` described as `{main_script['settings'][s]}`. Incorporate details such as colors, style, and historically accurate background items, including any furniture or decor present. Concentrate solely on the visual aspects without introducing any emotional elements associated with the location.")
        main_script["settings"][s] = setting_update

    return main_script

def s3_internal_character_update(main_script):
    """
    This function will augment with visual details about the characters that take place in the story.
    This facilitates consistent AI image prompting
    """
    
    for k in main_script['characters']:
        character_update = t2t(f"Rewrite and expand on the character description from {main_script['characters'][k]} to create a detailed physical description for an AI image prompt. Include details about the character's age, height, gender, any unique physical features, and hair (including color, style, and length) for consistent art generation. Describe their clothing style, focusing on the type and style of garments. Focus exclusively on the physical aspects without adding any background information irrelevant to the AI image prompt. Don't use any words that may trigger safety settings. Don't add accessories carried by hand.")
        main_script['characters'][k] = character_update

    return main_script

def s4_AIimage_generation(main_script):
    """
    Add new section `ai_image_prompt` with the visual descriptions defined in s3.
    """
    
    for p in main_script["panels"]:
        augment_prompt = "Generate a hyper-realistic image based on this panel description: `" + p["panel_description"] + "` \n "
        
        if len(p["characters_involved"]) > 0:
            augment_prompt += "Use the character descriptions provided below as a blueprint to accurately shape and define the characters: \n "
            for c in p["characters_involved"]:
                augment_prompt += "* " + c + ": " + main_script["characters"][c] + "\n"
        
        if p["setting_involved"]["perspective"] == 'interior' and p["setting_involved"]["location"] == 'building':
            augment_prompt += " The panel is set in the following setting: \n " + "`" + main_script["settings"][p["setting_involved"]["setting"]] + "` \n"
    
        p["ai_image_prompt"] = augment_prompt

    return main_script

def AI_image_generation2(main_script, i):
    response = client.images.generate(
     model = "dall-e-3",
     prompt = main_script["panels"][i]["ai_image_prompt"],
     size = "1024x1024",
     quality = "hd",
     n=1,
    )
    
    image_url = response.data[0].url
    
    response = requests.get(image_url)
    image_data = response.content
    original_image = Image.open(BytesIO(image_data))
    
    width, height = original_image.size 
    
    text_to_add = "PANEL DESCRIPTION: " + main_script['panels'][i]['panel_description']
    
    # Use textwrap to break text into lines based on available width
    lines = textwrap.wrap(text_to_add, width=150)
    
    captions_text = main_script.get("panels", [{}])[i].get("captions")
    
    if captions_text:
        lines += " "
        lines += textwrap.wrap(captions_text, width=150)
    
    dialogue_text = main_script.get("panels", [{}])[i].get("dialogue")
    
    if dialogue_text:
        lines += " "
        lines += textwrap.wrap(dialogue_text, width=150)
    
    top_margin = 40
    bottom_margin = 15 * (len(lines) + 3)
    
    new_width = width
    new_height = height + top_margin + bottom_margin
    
    # Create a new image with added top and bottom margins
    new_width = original_image.width
    new_height = original_image.height + top_margin + bottom_margin
    new_image = Image.new("RGB", (new_width, new_height), color="white")
    new_image.paste(original_image, (0, top_margin))
    
    # Add text to the top margin
    draw = ImageDraw.Draw(new_image)
    font = ImageFont.load_default(30)
    
    draw.text((10, 0), f"Title: {main_script['title']}", fill =(0, 0, 0),font=font)
    draw.text((width * 3 //4 + 100 , 0), f"Panel: {main_script['panels'][i]['panel_number']}", fill =(0, 0, 0),font=font)
    
    bottom_font_size = 15
    font = ImageFont.load_default(bottom_font_size)
    
    # Calculate starting position for the first line
    current_y = height + top_margin + bottom_font_size  # Adjust for margin and spacing
    
    for line in lines:
        # Get text width using textlength
        text_width = draw.textlength(line, font=font)
    
        # Calculate approximate text height based on font size
        text_height = font.size  # Assuming single-line text
    
        # Draw the text on the image
        draw.text((10, current_y), line, fill=(0, 0, 0), font=font)
    
        # Update current position for next line
        current_y += text_height + 5  # Adjust for line spacing
    
    new_image.save(f"images/{i+1}_{main_script['title'].replace(' ', '_')}.jpg")