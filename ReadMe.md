## About
Users may require inspiration to record content for their social media that follows a structured storytelling. By prompting a vague idea for a story, this project will provide a script along with visual storyboards that serve as inspiration for the user to record more narrative video content with the purpose of education, entertainment, or business.

## What it does
* Prompt instructions with guidelines to create a rich and structured script starting from a vague story idea or narrative goal.
* These guidelines are non-restrictive for creative output, meaning that they take advantage of the creative outputs from Google's AI LLM to create a new coherent script each time.
* Business owners may record content that with an engaging narrative for their products; social media influencers may record new narratives that entertain their audiences; educators may design a narrative that explains a new concept to a wide audience.

## How we built it
* Structured prompts for specific genres following different story structure designs.
* Added restrictions to avoid showing fantastical elements that can't be recorded

## Challenges we ran into
- Despite filling out the application form to use Google Imagen's model but I didn't get a response, so I had to opt to use OpenAI's image model. No API Documentation publicly available to incorporate potential Imagen functions for image generation.
- During AI image generation, character design showed inconsistent elements. AI image models would include new or reinterpret established visual elements (hair-do's, new clothes) . It is difficult to control AI image outputs, but they may serve as inspiration nonetheless. 
- Prompt responses are by default non-deterministic, but the inclusion of a dummy JSON parser with Python would allow their control.
- Reached token limit multiple times. ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).
- Reached AI image prompt token limit.

## Accomplishments that we're proud of
A GenAI product with No-Code tools from the user.

## What we learned
- Prompt Engineering
- JSON parsers for stuctured and reusable prompt responses.
- Basic website Design

## What's next for Lights! Camera! Prompt!
- New Website Design
- Incorporate Google's Imagen Text-to-Image Diffusion Model.
- Incorporate multi-modal input. The user may use an image as a story inspiration along with a description.
- Incorporate Voice narration
- Incorporate video clips with duration that takes into consideration the voice narration length.
- Incorporate concepts about cinematic shots for AI Image prompts.

# Instructions:
0. Create an environment to run, and install the /python/requirements.txt
1. Open the file /python/LPA-Main.ipynb
2. Go to the end of the notebook in the "Test" section
3. Insert values for `openai_api_key` and `googleai_api_key` for AI Image generation and Text Generation respectively
4. Start with a vague idea for a story with the goal of entertainment, business, or education.
5. Run all the cells below.
6. There are two types of outputs:
    * A Script located in python/main_script.json 
    * Multiple Storyboards in static/*.jpg
7. Returning to the root folder where this project is, run in terminal "python main.py" to execute a simple webpage displaying the results of the LPA project.
8. Use these script and storyboards generated by this process as inspiration to record content.