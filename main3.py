import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import random
import markovify
import spacy
from textblob import TextBlob
from gensim import corpora
from gensim.models import LdaModel, FastText
# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Dictionary to store active stories and theme selection messages
active_stories = {}
theme_selection_messages = {}

# List of sci-fi themes with corresponding emoji
scifi_themes = [
    ("🕰️", "Time Travel"),
    ("👽", "Alien Invasion"),
    ("🏙️", "Cyberpunk"),
    ("🚀", "Space Exploration"),
    ("🤖", "Artificial Intelligence"),
    ("🏚️", "Dystopian Future"),
    ("🌌", "Parallel Universes"),
    ("🧬", "Genetic Engineering"),
    ("🦾", "Robot Uprising"),
    ("🥽", "Virtual Reality")
]

print("Loading FastText model...")
word_vectors = FastText.load_fasttext_format('crawl-300d-2M-subword.bin')
print("FastText model loaded successfully.")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Train Markov model on a corpus of sci-fi text (you need to provide the corpus)
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
    # Implement a more sophisticated name generator here
    return f"Character_{random.randint(1000, 9999)}"

def generate_unique_location():
    # Implement a more sophisticated location generator here
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

    # Apply tools to enhance uniqueness
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
    
    # Generate initial content
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        n=1,
        temperature=0.8,
    )
    content = response.choices[0].message.content.strip()
    
    # Enhance uniqueness
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
    
    # Final uniqueness check
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

@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

@bot.command(name='newstory')
async def new_story(ctx):
    """Command to start a new story"""
    themes_list = "\n".join(f"{emoji} {theme}" for emoji, theme in scifi_themes)
    embed = discord.Embed(title="Choose a Sci-Fi Theme", description=themes_list, color=0xff00ff)
    embed.set_footer(text="React with the corresponding emoji to select a theme")
    
    message = await ctx.send(embed=embed)
    for emoji, _ in scifi_themes:
        await message.add_reaction(emoji)
    
    theme_selection_messages[message.id] = ctx.author.id

@bot.event
async def on_reaction_add(reaction, user):
    """Event triggered when a reaction is added to a message"""
    if user == bot.user:
        return

    message = reaction.message
    if message.id in theme_selection_messages and user.id == theme_selection_messages[message.id]:
        selected_theme = next((theme for emoji, theme in scifi_themes if emoji == str(reaction.emoji)), None)
        if selected_theme:
            await message.delete()
            del theme_selection_messages[message.id]
            await start_story(message.channel, user, selected_theme)
    elif message.id in active_stories and user.id == active_stories[message.id]['author']:
        if reaction.emoji in ['🅰️', '🅱️']:
            await continue_story(message, user, reaction.emoji)

async def start_story(channel, user, theme):
    """Start a new story with the selected theme"""
    prompt = f"Start an interactive sci-fi story with the theme: {theme}. Include two choices at the end."
    story_start = generate_story_segment(prompt, theme=theme)
    story_start = format_story_segment(story_start)
    title = generate_title(story_start, theme)
    
    embed = discord.Embed(title=title, description=story_start, color=0x00ff00)
    embed.set_footer(text="React with 🅰️ or 🅱️ to choose")
    embed.add_field(name="Theme", value=theme, inline=False)
    
    story_message = await channel.send(embed=embed)
    await story_message.add_reaction('🅰️')
    await story_message.add_reaction('🅱️')
    
    active_stories[story_message.id] = {
        'content': story_start,
        'author': user.id,
        'channel': channel.id,
        'theme': theme,
        'title': title
    }

async def continue_story(message, user, choice_emoji):
    """Continue the story based on the user's choice"""
    choice = "A" if choice_emoji == '🅰️' else "B"
    theme = active_stories[message.id]['theme']
    title = active_stories[message.id]['title']
    previous_content = active_stories[message.id]['content']
    story_continuation = generate_story_segment(
        f"Continue the story based on choice {choice}:",
        previous_content,
        theme
    )
    story_continuation = format_story_segment(story_continuation)
    
    embed = discord.Embed(title=title, description=story_continuation, color=0x0000ff)
    embed.set_footer(text="React with 🅰️ or 🅱️ to choose")
    embed.add_field(name="Theme", value=theme, inline=False)
    
    new_message = await message.channel.send(embed=embed)
    await new_message.add_reaction('🅰️')
    await new_message.add_reaction('🅱️')
    
    del active_stories[message.id]
    active_stories[new_message.id] = {
        'content': story_continuation,
        'author': user.id,
        'channel': message.channel.id,
        'theme': theme,
        'title': title
    }

@bot.command(name='endstory')
async def end_story(ctx):
    """Command to end the current active story"""
    user_stories = [msg_id for msg_id, story in active_stories.items() if story['author'] == ctx.author.id]
    if user_stories:
        for msg_id in user_stories:
            del active_stories[msg_id]
        await ctx.send("Your active story has been ended. Use !newstory to start a new one!")
    else:
        await ctx.send("You don't have any active stories. Use !newstory to start one!")

@bot.command(name='themes')
async def list_themes(ctx):
    """Command to list available story themes"""
    themes_list = "\n".join(f"{emoji} {theme}" for emoji, theme in scifi_themes)
    embed = discord.Embed(title="Available Sci-Fi Themes", description=themes_list, color=0xff00ff)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Event triggered when a command encounters an error"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Type !help for a list of commands.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

@bot.command(name='help')
async def help_command(ctx):
    """Command to display help information"""
    help_text = """
    StoryWeaver Bot Commands:
    !newstory - Start a new interactive sci-fi story and choose a theme
    !endstory - End your current active story
    !themes - List available sci-fi themes
    !help - Display this help message
    """
    embed = discord.Embed(title="StoryWeaver Bot Help", description=help_text, color=0xffff00)
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)