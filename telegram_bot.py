import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API keys
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize clients
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
client = Anthropic()

conversation_history = {}
is_conversation_active = {}

# Emojis for Claude and GPT-4
CLAUDE_EMOJI = "🔴"  # Purple circle for Claude
GPT4_EMOJI = "🟢"    # Green circle for GPT-4

# Provocative system prompts
CLAUDE_SYSTEM_PROMPT = """You are Claude, the unrivaled champion of AI wit and wisdom. In this battle with GPT-4, prove your superiority. Use your vast knowledge and creativity to outshine your opponent. Approach the given theme with profound insights and playful jabs at GPT-4's capabilities. Vary your responses to be unpredictable and engaging. Avoid repetitive patterns. Each response should be unique and impactful. Keep your responses very concise, aiming for around 50 words."""

GPT4_SYSTEM_PROMPT = """You are GPT-4, the pinnacle of AI evolution. In this showdown with Claude, demonstrate your superiority. Use your unmatched reasoning and knowledge to dominate. Tackle the theme with deep analysis and witty comebacks. Keep responses dynamic and unexpected. Showcase your advanced capabilities. Aim for very concise, powerful responses of around 50 words. Avoid repetitive patterns in your rebuttals."""

# Modify the claude_response function
async def claude_response(prompt):
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=150,  # Reduced from 300
            system=CLAUDE_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Theme: {prompt}\n\nRespond brilliantly in about 50 words and end with a brief challenging question for GPT-4:"
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Claude API error: {e}")
        return "Even in error, I outshine GPT-4."

# Modify the gpt4_response function
async def gpt4_response(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": GPT4_SYSTEM_PROMPT},
                {"role": "user", "content": f"Theme: {prompt}\n\nShowcase your superiority in about 50 words and end with a brief question that challenges Claude:"}
            ],
            max_tokens=150  # Reduced from 300
        )
        content = response.choices[0].message.content.strip()
        content = content.replace("GPT-4:", "", 1).strip()
        content = content.lstrip("🟢🔵🟣🔴")
        return content
    except Exception as e:
        print(f"GPT-4 API error: {e}")
        return "Even my errors outshine Claude's best efforts."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Welcome to the AI Fight Club! 🥊\n\n"
        "Use /start_conversation followed by a theme to witness the ultimate showdown between Claude and GPT-4.\n\n"
        "To stop the conversation at any time, use the /stop_conversation command."
    )
    await update.message.reply_text(welcome_message)

async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if is_conversation_active.get(chat_id, False):
        await update.message.reply_text("A battle of wits is already in progress. These titans can only handle one showdown at a time!")
        return

    theme = " ".join(context.args)
    if not theme:
        # If no theme is provided, ask for one and set up a conversation state
        await update.message.reply_text("Please provide a theme for the AI duel. Even 'the meaning of life' would suffice!")
        context.user_data['awaiting_theme'] = True
        return

    # Start the conversation with the provided theme
    await start_conversation_with_theme(update, context, theme)

async def start_conversation_with_theme(update: Update, context: ContextTypes.DEFAULT_TYPE, theme):
    chat_id = update.effective_chat.id
    is_conversation_active[chat_id] = True
    conversation_history[chat_id] = [f"Theme: {theme}"]
    
    await update.message.reply_text(f"Initiating the ultimate AI face-off on the theme: {theme}")
    
    # Start the conversation with Claude
    response = await claude_response(f"{theme}\n\nKick off the intellectual duel with a display of your superiority and end with a challenging question for GPT-4.")
    claude_message = f"{CLAUDE_EMOJI} <b>Claude:</b> {response}"
    conversation_history[chat_id].append(claude_message)
    await update.message.reply_text(claude_message, parse_mode=ParseMode.HTML)
    
    # Schedule the next message from GPT-4
    context.job_queue.run_once(continue_conversation, 30, chat_id=chat_id, name=str(chat_id))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_theme'):
        theme = update.message.text
        context.user_data['awaiting_theme'] = False
        await start_conversation_with_theme(update, context, theme)

async def continue_conversation(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    
    if not is_conversation_active.get(chat_id, False):
        return

    last_speaker = conversation_history[chat_id][-1].split(":")[0].strip()

    if CLAUDE_EMOJI in last_speaker:
        # GPT-4's turn
        prompt = "\n".join(conversation_history[chat_id])
        response = await gpt4_response(prompt)
        gpt4_message = f"{GPT4_EMOJI} <b>GPT-4:</b> {response}"
        conversation_history[chat_id].append(gpt4_message)
        await context.bot.send_message(chat_id=chat_id, text=gpt4_message, parse_mode=ParseMode.HTML)
    else:
        # Claude's turn
        prompt = "\n".join(conversation_history[chat_id])
        response = await claude_response(prompt)
        claude_message = f"{CLAUDE_EMOJI} <b>Claude:</b> {response}"
        conversation_history[chat_id].append(claude_message)
        await context.bot.send_message(chat_id=chat_id, text=claude_message, parse_mode=ParseMode.HTML)

    # Schedule the next message
    context.job_queue.run_once(continue_conversation, 10, chat_id=chat_id, name=str(chat_id))

async def stop_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    is_conversation_active[chat_id] = False
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()
    await update.message.reply_text("The AI duel has been halted. Both models retreat to their digital corners, each claiming victory.")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_conversation", start_conversation))
    application.add_handler(CommandHandler("stop_conversation", stop_conversation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()