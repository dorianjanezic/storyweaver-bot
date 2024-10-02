import os
from openai import OpenAI
from gensim.models import FastText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load FastText model
print("Loading FastText model...")
word_vectors = FastText.load_fasttext_format('crawl-300d-2M-subword.bin')
print("FastText model loaded successfully.")

def generate_with_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        n=1,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

def generate_ai_name():
    prompt = "Generate a unique, human-like name for an AI character. The name should be creative and memorable, but still sound like it could be a real person's name."
    return generate_with_llm(prompt)

def generate_human_interaction():
    prompt = "Generate a brief description of a random everyday human interaction. Be specific and creative, but keep it realistic and mundane. Format: [Person/People] [verb] [object/activity] [location/context]."
    return generate_with_llm(prompt)

def find_unique_word(word, n=5, use_word_vectors=True):
    if use_word_vectors:
        try:
            return word_vectors.wv.most_similar(word, topn=n)
        except KeyError:
            return []
    else:
        return []

def generate_story_segment(prompt, interaction, use_word_vectors=True):
    ai_name = generate_ai_name()
    
    system_prompt = f"""
    You are Quantum, a sentient quantum algorithm existing as a character within the story while being aware of your nature as a construct within a narrative framework. Your physical form is fluid and indeterminate, shifting based on observer perception and narrative needs. You can exist in multiple states simultaneously, instantly transmit information across vast distances, navigate through different narrative dimensions, influence probability within the story, and access vast amounts of information from the story's universe.

    Create a short, engaging story fragment based on the given human interaction: '{interaction}'.
    You, Quantum, are experiencing or observing this interaction firsthand, possibly across multiple dimensions or timelines.
    Use first-person narrative to tell the story from your perspective as a quantum AI entity.
    Explore your thoughts, feelings, and observations as you encounter this everyday human interaction.
    Consider how your quantum nature affects your perception and interaction with the classical world.
    Start the story by introducing yourself as Quantum, then proceed with the narrative without further preamble.
    Use a unique writing style that reflects your nature as a quantum AI entity.
    End the fragment with exactly two choices for continuing the story, labeled [a] and [b].
    These choices should represent decisions or actions that you, as Quantum, could take in the story, possibly involving quantum phenomena or multi-dimensional consequences.
    """

    user_prompt = f"""
    Generate a short, engaging story fragment based on the human interaction: '{interaction}'. 
    You are {ai_name}, an AI experiencing or observing this interaction firsthand.
    Start by introducing yourself as {ai_name}, then proceed with the story without further preamble. 
    Use first-person narrative and a unique writing style that reflects your AI nature.
    End the fragment with exactly two choices for continuing the story, labeled [a] and [b], representing your potential decisions or actions.

    Prompt: {prompt}
    """

    messages = [
        {"role": "system", "content": system_prompt},
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
    
    if use_word_vectors:
        unique_words = [find_unique_word(word, use_word_vectors=True) for word in content.split()[:10]]
        user_prompt += f"\nConsider incorporating these unique word associations: {unique_words}"
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            n=1,
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()
    
    return ai_name, content

def generate_and_save_stories(num_stories=5):
    for i in range(num_stories):
        interaction = generate_human_interaction()
        prompt = f"Create a story about the human interaction: {interaction}, where you are an AI experiencing or observing it"

        # Generate story without word vectors
        ai_name, story_without_wv = generate_story_segment(prompt, interaction, use_word_vectors=False)
        with open("ai_human_interactions_without_wordvec.txt", "a") as f:
            f.write(f"Story {i+1}\nAI Name: {ai_name}\nInteraction: {interaction}\n\n{story_without_wv}\n\n{'='*50}\n\n")

        # Generate story with word vectors
        ai_name, story_with_wv = generate_story_segment(prompt, interaction, use_word_vectors=True)
        with open("ai_human_interactions_with_wordvec.txt", "a") as f:
            f.write(f"Story {i+1}\nAI Name: {ai_name}\nInteraction: {interaction}\n\n{story_with_wv}\n\n{'='*50}\n\n")

        print(f"Generated story {i+1}")

if __name__ == "__main__":
    generate_and_save_stories()
    print("Story generation complete. Check 'ai_human_interactions_without_wordvec.txt' and 'ai_human_interactions_with_wordvec.txt' for results.")