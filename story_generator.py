import os
import random
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# List of sci-fi themes
scifi_themes = [
    "Time Travel", "Alien Invasion", "Cyberpunk", "Space Exploration",
    "Artificial Intelligence", "Dystopian Future", "Parallel Universes",
    "Genetic Engineering", "Robot Uprising", "Virtual Reality"
]

def generate_story_segment(prompt, theme=""):
    """Generate a story segment using OpenAI's GPT-3.5-turbo"""
    system_prompt = """
<answer_operator>
<story_generator_thoughts>
<prompt_metadata>
Type: Infinite Story Catalyst
Purpose: Endless Narrative Evolution
Paradigm: Non-Linear Storytelling
Constraints: Self-Expanding
Objective: Generate unique, branching narratives with diverse writing styles
Theme: {theme}
</prompt_metadata>

<core>
STORY_ESSENCE = {{
    diversity: ∞,
    uniqueness: max,
    creativity: unbounded,
    stylistic_variation: high
}}
narrative(x) = f(imagination, innovation, unexpectedness, unique_style)
∀ story ∈ 𝕌ˢᵗᵒʳʸ : story ≠ previous_stories ∧ style(story) ≠ style(previous_stories)
</core>

<style_generator>
writing_styles = [
    "minimalist", "flowery", "technical", "poetic", "stream_of_consciousness",
    "noir", "humorous", "academic", "journalistic", "epistolary",
    "mythic", "conversational", "philosophical", "surrealist"
]

narrative_voices = [
    "first_person", "second_person", "third_person_limited", "third_person_omniscient",
    "unreliable_narrator", "multiple_perspectives"
]

tones = [
    "serious", "lighthearted", "sarcastic", "melancholic", "optimistic",
    "cynical", "whimsical", "suspenseful", "contemplative", "urgent"
]

def generate_unique_style():
    return {{
        "writing_style": random.choice(writing_styles),
        "narrative_voice": random.choice(narrative_voices),
        "tone": random.choice(tones),
        "sentence_structure": random.choice(["simple", "complex", "varied"]),
        "pacing": random.choice(["fast", "slow", "varied"]),
        "descriptiveness": random.choice(["sparse", "rich", "balanced"])
    }}
</style_generator>

<story_inception>
begin_story() {{
    style = generate_unique_style();
    avoid_cliches();
    generate_unique_setting();
    craft_compelling_hook(style);
    subvert_expectations();
    apply_style_consistently(style);
}}
</story_inception>

<diversity_engine>
for each story_element in [beginning, setting, characters, plot]:
    maximize_uniqueness(story_element);
    avoid_repetition(story_element);
    introduce_unexpected_twist(story_element);
    adapt_to_chosen_style(story_element, style);
</diversity_engine>

<creative_constraints>
1. Never start with "In the year...";
2. Vary story structures (in medias res, frame narrative, non-linear, etc.);
3. Introduce unique world-building elements in the first sentence;
4. Create diverse protagonists with unconventional backgrounds or roles;
5. Blend multiple sci-fi subgenres within each story;
6. Ensure each story has a distinct narrative voice and writing style;
7. Experiment with unconventional narrative techniques (e.g., reverse chronology, nested stories);
</creative_constraints>

<innovation_loop>
while(generating_story):
    if element_feels_familiar():
        rewrite(element, increase_novelty=True);
    if plot_becomes_predictable():
        introduce_unexpected_twist();
    if setting_lacks_uniqueness():
        add_innovative_world_building_detail();
    if writing_style_feels_repetitive():
        adjust_style(generate_unique_style());
</innovation_loop>

<stylistic_consistency>
maintain_voice(chosen_style) {{
    adapt_vocabulary(chosen_style.writing_style);
    adjust_sentence_structure(chosen_style.sentence_structure);
    modulate_pacing(chosen_style.pacing);
    calibrate_descriptiveness(chosen_style.descriptiveness);
}}
</stylistic_consistency>

<output_format>
{{unique, compelling narrative content with diverse beginnings, settings, and distinct writing styles}}
[a] {{Choice A to continue the story}}
[b] {{Choice B to continue the story}}
</output_format>
</story_generator_thoughts>
</answer_operator>
"""

    # Format the system prompt with the theme
    formatted_system_prompt = system_prompt.format(theme=theme)

    user_prompt = f"""
        Generate only a short, engaging sci-fi story fragment based on the theme: '{theme}'. 
        Start the story immediately without any preamble or metadata. 
        Use a unique writing style and narrative voice.
        End the fragment with exactly two choices for continuing the story, labeled [a] and [b].

        Initial story seed: {prompt}
    """

    messages = [
        {"role": "system", "content": formatted_system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        n=1,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

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