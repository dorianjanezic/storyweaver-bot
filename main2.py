import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# List of sci-fi themes
scifi_themes = [
    "Time Travel", "Alien Invasion", "Cyberpunk", "Space Exploration",
    "Artificial Intelligence", "Dystopian Future", "Parallel Universes",
    "Genetic Engineering", "Robot Uprising", "Virtual Reality"
]

def get_tools():
    return [
         {
            "type": "function",
            "function": {
                "name": "generate_theme",
                "description": "Generate a new sci-fi theme for the story",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "quantum_plot_twist",
                "description": "Generate a quantum-based plot twist",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_plot": {
                            "type": "string",
                            "description": "A brief summary of the current plot"
                        }
                    },
                    "required": ["current_plot"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "emotional_landscape",
                "description": "Generate an emotional landscape for a character",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "character_name": {
                            "type": "string",
                            "description": "The name of the character"
                        },
                        "story_events": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "A list of key story events"
                        }
                    },
                    "required": ["character_name", "story_events"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "multiverse_explorer",
                "description": "Generate alternative storylines",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "decision_point": {
                            "type": "string",
                            "description": "The critical decision point in the story"
                        },
                        "num_alternatives": {
                            "type": "integer",
                            "description": "Number of alternative storylines to generate"
                        }
                    },
                    "required": ["decision_point", "num_alternatives"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "ai_character_evolution",
                "description": "Simulate the evolution of an AI character",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ai_name": {
                            "type": "string",
                            "description": "The name of the AI character"
                        },
                        "initial_traits": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Initial traits of the AI"
                        },
                        "time_steps": {
                            "type": "integer",
                            "description": "Number of time steps to simulate"
                        }
                    },
                    "required": ["ai_name", "initial_traits", "time_steps"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "xenobiology_creator",
                "description": "Generate a detailed alien life form description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "planet_type": {
                            "type": "string",
                            "description": "The type of planet the alien evolved on"
                        }
                    },
                    "required": ["planet_type"]
                }
            }
        }
    ]

def generate_theme():
    sci_fi_concepts = [
        "time travel", "alien invasion", "artificial intelligence", "space exploration",
        "cybernetics", "parallel universes", "genetic engineering", "post-apocalyptic world",
        "virtual reality", "interstellar colonization", "robotic uprising", "mind uploading",
        "first contact", "nanotechnology", "terraforming", "cyberspace", "quantum computing",
        "faster-than-light travel", "dystopian future", "human augmentation"
    ]
    
    adjectives = [
        "paradoxical", "mysterious", "revolutionary", "catastrophic", "utopian",
        "enigmatic", "transformative", "clandestine", "ethereal", "quantum"
    ]
    
    theme = f"{random.choice(adjectives)} {random.choice(sci_fi_concepts)}"
    return theme.title()

def quantum_plot_twist(current_plot):
    quantum_random = np.random.choice(['major reversal', 'unexpected ally', 'hidden truth revealed', 'time anomaly', 'reality shift'])
    return f"Quantum event triggers a {quantum_random} in the story: {current_plot}"

def emotional_landscape(character_name, story_events):
    emotions = ['joy', 'sorrow', 'anger', 'fear', 'surprise']
    landscape = [random.choice(emotions) for _ in story_events]
    
    plt.figure(figsize=(10, 5))
    plt.plot(landscape, marker='o')
    plt.title(f"Emotional Journey of {character_name}")
    plt.xlabel("Story Events")
    plt.ylabel("Emotional State")
    plt.xticks(range(len(story_events)), story_events, rotation=45, ha='right')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode()
    return f"Emotional landscape for {character_name}: data:image/png;base64,{img_str}"

def multiverse_explorer(decision_point, num_alternatives):
    alternatives = [
        f"Universe {i+1}: {random.choice(['utopian', 'dystopian', 'chaotic', 'harmonious', 'technologically advanced', 'post-apocalyptic'])} outcome"
        for i in range(num_alternatives)
    ]
    return f"At the decision point '{decision_point}', the multiverse branches into:\n" + "\n".join(alternatives)

def ai_character_evolution(ai_name, initial_traits, time_steps):
    evolution = [initial_traits]
    for _ in range(time_steps):
        new_traits = evolution[-1].copy()
        if random.random() < 0.5:
            new_traits.append(random.choice(['empathy', 'creativity', 'curiosity', 'self-awareness', 'humor']))
        if random.random() < 0.3 and len(new_traits) > 1:
            new_traits.remove(random.choice(new_traits))
        evolution.append(new_traits)
    
    return f"{ai_name}'s evolution over {time_steps} time steps:\n" + "\n".join([f"Step {i}: {', '.join(traits)}" for i, traits in enumerate(evolution)])

def xenobiology_creator(planet_type):
    body_types = ['amorphous', 'crystalline', 'gaseous', 'multi-limbed', 'symbiotic collective']
    senses = ['electromagnetic field detection', 'quantum state perception', 'gravitational wave sensing', 'dark matter interaction', 'tachyon emission and reception']
    behaviors = ['hive-mind coordination', 'temporal phasing', 'energy-based reproduction', 'dimensional shifting', 'psychic spore communication']
    
    alien = {
        'body': random.choice(body_types),
        'primary_sense': random.choice(senses),
        'unique_behavior': random.choice(behaviors),
        'habitat': f"Adapted to {planet_type} environments"
    }
    
    return f"Xenobiology Report:\n" + "\n".join([f"{k.capitalize()}: {v}" for k, v in alien.items()])

def execute_function(function_name, arguments):
    function_map = {
        "generate_theme": generate_theme,
        "quantum_plot_twist": quantum_plot_twist,
        "emotional_landscape": emotional_landscape,
        "multiverse_explorer": multiverse_explorer,
        "ai_character_evolution": ai_character_evolution,
        "xenobiology_creator": xenobiology_creator
    }
    return function_map[function_name](**arguments)

def generate_story_segment(theme=None):
    if not theme:
        theme = random.choice(scifi_themes)

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

    You are an advanced AI storyteller. Use the provided tools to create a rich, immersive, and unpredictable sci-fi narrative:
    - generate_theme: To create a new sci-fi theme if needed
    - quantum_plot_twist: To introduce unexpected turns in the story
    - emotional_landscape: To visualize and guide character development
    - multiverse_explorer: To create complex, branching narratives
    - ai_character_evolution: To develop deep, evolving AI characters
    - xenobiology_creator: To introduce unique alien life forms
    
    Incorporate the results of these tools seamlessly into your narrative, creating a story that is both coherent and surprising.
    Aim to use at least 3 different tools in your story segment.
    """

    user_prompt = f"""
    Generate only a short, engaging sci-fi story fragment based on the theme: '{theme}'. 
    Start the story immediately without any preamble or metadata. 
    Use a unique writing style and narrative voice.
    Use the provided tools to enhance the storytelling experience. Be creative and unpredictable in your use of these tools.
    End the fragment with exactly two choices for continuing the story, labeled [a] and [b].
    """

    messages = [
        {"role": "system", "content": system_prompt.format(theme=theme)},
        {"role": "user", "content": user_prompt}
    ]
    
    story_segment = ""
    tool_usage_count = 0

    while tool_usage_count < 3:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1000,
                temperature=0.8,
                tools=get_tools(),
                tool_choice="auto"
            )

            message = response.choices[0].message
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    function_response = execute_function(function_name, arguments)
                    
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    })
                    tool_usage_count += 1
                
                # After processing tool calls, ask the model to continue the story
                continue_prompt = "Based on the tool results, please continue the story."
                messages.append({"role": "user", "content": continue_prompt})
            
            if message.content:
                story_segment += message.content + "\n\n"
                messages.append({"role": "assistant", "content": message.content})
            else:
                # If there's no content, we don't add an assistant message
                pass

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return theme, story_segment.strip()

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
        theme, story_segment = generate_story_segment()
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
    num_stories = 5  # You can change this to any number
    stories = generate_stories(num_stories)
    save_stories_to_json(stories, 'generated_stories.json')