from telegram import Update
from telegram.ext import ContextTypes
from market_data import get_market_snapshot
from etf_rules import choose_etfs
from prompts import build_brief_prompt
from gemini_client import generate_market_brief

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I summarize market trends and suggest ETFs to watch.\n"
        "Try /brief"
    )

async def brief_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching market snapshot...")

    try:
        snapshot = get_market_snapshot()
        etfs = choose_etfs(snapshot)
        prompt = build_brief_prompt(snapshot, etfs)
        text = generate_market_brief(prompt)
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Something went wrong: {e}")