# StoryWeaver Bot

StoryWeaver Bot is a Discord bot that generates interactive sci-fi stories using OpenAI's GPT models. Users can start new stories, choose themes, and make choices to continue the narrative.

## Features

- Start new interactive sci-fi stories
- Choose from various sci-fi themes
- Make choices to progress the story
- End active stories
- List available themes

## Commands

- `!newstory`: Start a new interactive sci-fi story and choose a theme
- `!endstory`: End your current active story
- `!themes`: List available sci-fi themes
- `!help`: Display help information

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following content:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Replace `your_discord_bot_token` and `your_openai_api_key` with your actual Discord bot token and OpenAI API key.

## Running the Bot

Run the bot using the following command:

```
python main.py
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

