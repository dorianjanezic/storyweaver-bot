import os
from dotenv import load_dotenv
from openai import OpenAI
import random
import markovify
import spacy
from textblob import TextBlob
from gensim import corpora
from gensim.models import LdaModel, FastText

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# List of sci-fi themes
scifi_themes = [
    "Time Travel",
    "Alien Invasion",
    "Cyberpunk",
    "Space Exploration",
    "Artificial Intelligence",
    "Dystopian Future",
    "Parallel Universes",
    "Genetic Engineering",
    "Robot Uprising",
    "Virtual Reality"
]

print("Loading FastText model...")
word_vectors = FastText.load_fasttext_format('crawl-300d-2M-subword.bin')
print("FastText model loaded successfully.")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Train Markov model on a corpus of sci-fi text
with open("scifi_corpus.txt", "r") as f:
    text = f.read()
text_model = markovify.Text(text)

# Sci-fi concept generator components
scientific_terms = ["quantum", "nano", "bio", "cyber", "fusion", "neural", "cosmic"]
futuristic_ideas = ["teleportation", "mind-uploading", "terraforming", "time-dilation"]
random_elements = ["crystal", "vortex", "nexus", "pulse", "nova"]

# Story structures
story_structures = [
    "linear",
    "non_linear",
    "frame_narrative",
    "parallel_narratives",
    "circular",
    "reverse_chronology"
]

def find_unique_word(word, n=5):
    """Find n unique words related to the input word"""
    try:
        return word_vectors.wv.most_similar(word, topn=n)
    except KeyError:
        return []

def generate_unique_sentence():
    return text_model.make_sentence()

def replace_entities(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, generate_unique_name())
        elif ent.label_ == "LOC":
            text = text.replace(ent.text, generate_unique_location())
    return text

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def extract_topics(text, num_topics=5):
    tokens = text.lower().split()
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    return lda_model.print_topics()

def generate_scifi_concept():
    return f"{random.choice(scientific_terms)}-{random.choice(futuristic_ideas)} {random.choice(random_elements)}"

def choose_story_structure():
    return random.choice(story_structures)

def generate_unique_name():
    return f"Character_{random.randint(1000, 9999)}"

def generate_unique_location():
    return f"Location_{random.randint(1000, 9999)}"

def generate_story_segment(prompt, previous_content="", theme=""):
    """Generate a story segment using OpenAI's GPT-3.5-turbo with enhanced uniqueness"""
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
    </story_generator_thoughts>
    </answer_operator>
    """

    formatted_system_prompt = system_prompt.format(theme=theme)

    story_structure = choose_story_structure()
    unique_concept = generate_scifi_concept()
    
    user_prompt = f"""
        Generate only a short, engaging sci-fi story fragment based on the theme: '{theme}'. 
        Start the story immediately without any preamble or metadata. 
        Use a unique writing style and narrative voice.
        End the fragment with exactly two choices for continuing the story, labeled [a] and [b].
        Incorporate the unique concept: {unique_concept}
        Use the {story_structure} story structure.

        Previous story content: {previous_content}
        Continue from: {prompt}
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
    content = response.choices[0].message.content.strip()
    
    content = replace_entities(content)
    sentiment = analyze_sentiment(content)
    if sentiment > 0.5 or sentiment < -0.5:
        user_prompt += "\nAdjust the emotional tone to be more neutral."
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            n=1,
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()
    
    topics = extract_topics(content)
    if len(set(topics)) < 3:
        user_prompt += "\nIncorporate more diverse topics and themes."
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            n=1,
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()
    
    unique_words = [find_unique_word(word) for word in content.split()[:10]]
    user_prompt += f"\nConsider incorporating these unique word associations: {unique_words}"
    messages.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        n=1,
        temperature=0.8,
    )
    final_content = response.choices[0].message.content.strip()
    
    return final_content

def format_story_segment(segment):
    """Format the story segment to ensure options are on new lines"""
    parts = segment.split('[A]')
    if len(parts) == 2:
        main_text, options = parts
        options = '[A]' + options
        options = options.replace('[B]', '\n[B]')
        return f"{main_text.strip()}\n\n{options.strip()}"
    return segment

def generate_title(story_start, theme):
    """Generate a title for the story"""
    prompt = f"Generate a short, catchy title for a sci-fi story with the theme '{theme}' and this beginning: {story_start[:100]}..."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative title generator for sci-fi stories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def main():
    """Function to run local tests"""
    print("Running local tests...")

    # Test story generation
    theme = random.choice(scifi_themes)
    print(f"Starting a new story with theme: {theme}")
    
    prompt = f"Start an interactive sci-fi story with the theme: {theme}. Include two choices at the end."
    story_start = generate_story_segment(prompt, theme=theme)
    story_start = format_story_segment(story_start)
    title = generate_title(story_start, theme)

    print(f"Title: {title}")
    print(f"Story start:\n{story_start}")

    # Show the effect of word_vectors
    # print("\nUnique word associations:")
    # unique_words = [find_unique_word(word) for word in story_start.split()[:10]]
    # for word, associations in zip(story_start.split()[:10], unique_words):
    #     print(f"{word}: {associations}")

    # Show the effect of the sci-fi corpus
    # print("\nGenerated unique sentences from the sci-fi corpus:")
    # for _ in range(3):
    #     print(generate_unique_sentence())

    # Test story continuation
    print("\nContinuing the story with choice A:")
    generate_title(story_start, theme)
    continuation = generate_story_segment("Continue the story based on choice A:", story_start, theme)
    continuation = format_story_segment(continuation)
    print(continuation)

if __name__ == "__main__":
    main()