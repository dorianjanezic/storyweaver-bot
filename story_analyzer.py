import json
import re
from collections import Counter, defaultdict
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer

def download_nltk_resources():
    resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)

# Download necessary NLTK data
download_nltk_resources()

def load_json_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def extract_years(text):
    year_pattern = r'\b(1\d{3}|2\d{3})\b'
    return re.findall(year_pattern, text)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]

def find_repetitive_words(text, threshold=3):
    words = preprocess_text(text)
    word_counts = Counter(words)
    return {word: count for word, count in word_counts.items() if count >= threshold}

def group_similar_words(word_dict):
    grouped = defaultdict(list)
    for word, count in word_dict.items():
        root = word[:4]  # Use first 4 letters as a simple way to group similar words
        grouped[root].append((word, count))
    return {key: sorted(value, key=lambda x: x[1], reverse=True) for key, value in grouped.items()}

def analyze_stories(data):
    all_text = " ".join(item.get('content', '') for item in data)
    all_years = []
    word_frequencies = Counter()
    repetitive_words_per_story = []
    all_repetitive_words = Counter()

    for item in data:
        story = item.get('content', '')
        all_years.extend(extract_years(story))
        word_frequencies.update(preprocess_text(story))
        
        repetitive_words = find_repetitive_words(story)
        repetitive_words_per_story.append({
            'theme': item.get('theme', 'Unknown'),
            'repetitive_words': repetitive_words
        })
        all_repetitive_words.update(repetitive_words)

    return all_years, word_frequencies, repetitive_words_per_story, all_repetitive_words

def plot_word_frequencies(word_freq, top_n=20, filename='word_frequencies.png'):
    words, counts = zip(*word_freq.most_common(top_n))
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_year_distribution(years):
    year_counts = Counter(years)
    plt.figure(figsize=(12, 6))
    plt.bar(year_counts.keys(), year_counts.values())
    plt.title('Distribution of Years Mentioned in Stories')
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('year_distribution.png')
    plt.close()

def main():
    data = load_json_data('generated_stories.json')
    if not data:
        print("No data to analyze. Exiting.")
        return

    years, word_frequencies, repetitive_words_per_story, all_repetitive_words = analyze_stories(data)

    print("Most common years mentioned:")
    for year, count in Counter(years).most_common(10):
        print(f"{year}: {count} times")

    print("\nMost common words across all stories:")
    for word, count in word_frequencies.most_common(20):
        print(f"{word}: {count} times")

    print("\nMost repetitive words across all stories:")
    grouped_repetitive = group_similar_words(all_repetitive_words)
    for root, words in sorted(grouped_repetitive.items(), key=lambda x: sum(count for _, count in x[1]), reverse=True)[:10]:
        print(f"{root}:")
        for word, count in words:
            print(f"  {word}: {count} times")

    print("\nRepetitive words in individual stories:")
    for item in repetitive_words_per_story:
        print(f"\nTheme: {item['theme']}")
        grouped = group_similar_words(item['repetitive_words'])
        for root, words in sorted(grouped.items(), key=lambda x: sum(count for _, count in x[1]), reverse=True)[:5]:
            print(f"  {root}:")
            for word, count in words:
                print(f"    {word}: {count} times")

    plot_word_frequencies(word_frequencies)
    plot_year_distribution(years)
    plot_word_frequencies(all_repetitive_words, filename='repetitive_words.png')

    print("\nAnalysis complete. Check 'word_frequencies.png', 'year_distribution.png', and 'repetitive_words.png' for visualizations.")

if __name__ == "__main__":
    main()