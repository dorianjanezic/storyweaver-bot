import os
import random
from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter
import argparse
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
    system_prompt = f"""
    You are a creative writer specializing in sci-fi stories with a focus on {theme}. 
    Your task is to craft an engaging narrative that explores this theme in about 3-4 paragraphs.
    Use vivid, sensory details to bring your scenes to life.
    Incorporate classic sci-fi elements and unexpected twists.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def generate_story(theme):
    """Generate a complete short story"""
    prompt = f"Generate a short sci-fi story (about 3-4 paragraphs) with the theme: {theme}."
    story = generate_story_segment(prompt, theme=theme)
    return story

def evaluate_single_story(story, theme):
    """Evaluate a single story using OpenAI's API"""
    prompt = f"""
    Evaluate the following sci-fi story with the theme "{theme}". Rate it on a scale of 1-10 for each of these criteria:
    1. Creativity
    2. Coherence
    3. Theme relevance
    4. Engagement
    5. Sci-fi elements

    Also, provide a one-sentence summary of the story.

    Story:
    {story}

    Provide your evaluation in the following format:
    Creativity: [score]
    Coherence: [score]
    Theme relevance: [score]
    Engagement: [score]
    Sci-fi elements: [score]
    Summary: [one-sentence summary]
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a literary critic specializing in sci-fi stories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        n=1,
        temperature=0.7,
    )
    
    return response.choices[0].message.content.strip()

def parse_scores(evaluation):
    """Parse the scores from the evaluation text"""
    scores = {}
    summary = ""
    for line in evaluation.split('\n'):
        if ':' in line:
            criterion, value = line.split(':', 1)
            criterion = criterion.strip()
            value = value.strip()
            if criterion in ['Creativity', 'Coherence', 'Theme relevance', 'Engagement', 'Sci-fi elements']:
                scores[criterion] = int(value)
            elif criterion == 'Summary':
                summary = value
    return scores, summary

def generate_report(evaluation_results):
    """Generate a report from the evaluation results"""
    report = "Story Evaluation Report\n"
    report += "======================\n\n"

    # Calculate average scores
    total_scores = Counter()
    for theme, evaluation in evaluation_results:
        scores, _ = parse_scores(evaluation)
        total_scores.update(scores)
    
    avg_scores = {k: v / len(evaluation_results) for k, v in total_scores.items()}
    
    report += "Average Scores:\n"
    for criterion, score in avg_scores.items():
        report += f"{criterion}: {score:.2f}\n"
    
    report += "\nTop 5 Stories:\n"
    top_stories = sorted(evaluation_results, key=lambda x: sum(parse_scores(x[1])[0].values()), reverse=True)[:5]
    for i, (theme, evaluation) in enumerate(top_stories, 1):
        report += f"\n{i}. Theme: {theme}\n"
        report += evaluation + "\n"
    
    return report

def main(num_stories):
    stories = []
    for i in range(num_stories):
        theme = random.choice(scifi_themes)
        print(f"Generating story {i+1}/{num_stories} with theme: {theme}")
        story = generate_story(theme)
        stories.append((theme, story))
    
    print("Evaluating stories...")
    evaluation_results = []
    for i, (theme, story) in enumerate(stories):
        print(f"Evaluating story {i+1}/{num_stories}")
        evaluation = evaluate_single_story(story, theme)
        evaluation_results.append((theme, evaluation))
    
    print("Generating report...")
    report = generate_report(evaluation_results)
    
    # Save report to a file
    with open('story_evaluation_report.txt', 'w') as f:
        f.write(report)
    
    # Save raw data to a JSON file
    raw_data = []
    for (theme, story), (_, evaluation) in zip(stories, evaluation_results):
        scores, summary = parse_scores(evaluation)
        raw_data.append({
            "theme": theme,
            "story": story,
            "scores": scores,
            "summary": summary
        })
    
    with open('story_evaluation_raw_data.json', 'w') as f:
        json.dump(raw_data, f, indent=2)
    
    print("Evaluation complete. Report saved to 'story_evaluation_report.txt'")
    print("Raw data saved to 'story_evaluation_raw_data.json'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and evaluate sci-fi stories.")
    parser.add_argument("num_stories", type=int, help="Number of stories to generate and evaluate")
    args = parser.parse_args()
    
    main(args.num_stories)