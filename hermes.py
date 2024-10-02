import os
import random
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# List of sci-fi themes
scifi_themes = [
    "Time Travel", "Alien Invasion", "Cyberpunk", "Space Exploration",
    "Artificial Intelligence", "Dystopian Future", "Parallel Universes",
    "Genetic Engineering", "Robot Uprising", "Virtual Reality"
]

# Initialize OpenAI client
openai_api_key = os.getenv('LAMBDA_API_KEY')
openai_api_base = "https://api.lambdalabs.com/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = "hermes-3-llama-3.1-405b-fp8-128k"

def generate_story_segment(prompt, theme=""):
    """Generate a story segment using Lambda API with hermes-3-llama-3.1-405b-fp8-128k model"""
    system_prompt = """
You are a creative sci-fi story generator. Generate a short, engaging sci-fi story fragment based on the given theme. Start the story immediately without any preamble or metadata. Use a unique writing style and narrative voice. End the fragment with exactly two choices for continuing the story, labeled [a] and [b].
"""

    user_prompt = f"""
Generate a short, engaging sci-fi story fragment based on the theme: '{theme}'. 
Start the story immediately without any preamble or metadata. 
Use a unique writing style and narrative voice.
End the fragment with exactly two choices for continuing the story, labeled [a] and [b].

Initial story seed: {prompt}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model=model,
        max_tokens=500,
        temperature=0.8,
        top_p=1,
    )

    return chat_completion.choices[0].message.content.strip()

def generate_story():
    """Generate a single story with choices"""
    theme = random.choice(scifi_themes)
    prompt = ""
    story = generate_story_segment(prompt, theme)
    
    print(f"Theme: {theme}\n")
    print(story)

def parse_story_segment(segment):
    """Parse the story segment to extract the main content and choices"""
    lines = segment.split('\n')
    main_content = []
    choices = {}
    
    current_section = 'main'
    for line in lines:
        if line.startswith('[a]'):
            current_section = 'a'
            choices['a'] = line[4:].strip()
        elif line.startswith('[b]'):
            current_section = 'b'
            choices['b'] = line[4:].strip()
        elif current_section == 'main':
            main_content.append(line)
    
    return {
        'content': ' '.join(main_content).strip(),
        'choices': choices
    }

def generate_stories(num_stories):
    """Generate multiple stories and return as a list of dictionaries"""
    stories = []
    for _ in range(num_stories):
        theme = random.choice(scifi_themes)
        prompt = ""
        story_segment = generate_story_segment(prompt, theme)
        parsed_segment = parse_story_segment(story_segment)
        
        story = {
            'theme': theme,
            'content': parsed_segment['content'],
            'choices': parsed_segment['choices']
        }
        stories.append(story)
        
        print(f"Generated story with theme: {theme}")
    
    return stories

def save_stories_to_json(stories, filename):
    """Save the generated stories to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    print(f"Stories saved to {filename}")

if __name__ == "__main__":
    num_stories = 10  # You can change this to any number
    stories = generate_stories(num_stories)
    save_stories_to_json(stories, 'generated_stories.json')