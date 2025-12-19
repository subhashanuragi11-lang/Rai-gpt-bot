"""
==============================================================================
PROJECT NAME: RAI GPT (ULTIMATE ENTERPRISE EDITION)
VERSION: 10.0 (Stable)
AUTHOR: @PixDev_Rai
OWNER ID: 6406769029
FRAMEWORK: Python-Telegram-Bot (v20+)
DESCRIPTION: 
    This is a high-level AI coding assistant bot designed for scalability.
    It includes a custom database engine, 24/7 web server, force subscription,
    admin dashboard, broadcast system, and memory management.
==============================================================================
"""

import os
import sys
import json
import time
import logging
import asyncio
import threading
import requests
import html
import re
import datetime
from typing import Union, List, Dict, Optional

# Flask for 24/7 Hosting
from flask import Flask

# Telegram API
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    BotCommand,
    User,
    Chat
)
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    ContextTypes, 
    Application, 
    filters,
    Defaults
)
from telegram.constants import ParseMode, ChatAction
from telegram.error import (
    BadRequest, 
    Forbidden, 
    NetworkError, 
    TelegramError
)

# ==============================================================================
#                           SECTION 1: CONFIGURATION
# ==============================================================================

class Config:
    """
    Central Configuration Class.
    Change settings here to affect the entire bot.
    """
    # ---------------- CREDENTIALS ----------------
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    
    # ---------------- BOT SETTINGS ----------------
    BOT_NAME = "Rai GPT Pro"
    VERSION = "10.5.2"
    DB_FILE = "rai_gpt_master_db.json"
    LOG_FILE = "bot_activity.log"
    
    # ---------------- FORCE SUBSCRIBE ----------------
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"  # Channel username with @
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    
    # ---------------- AI SETTINGS ----------------
    AI_PROVIDER_URL = "https://text.pollinations.ai/"
    MAX_HISTORY_DEPTH = 12  # How many previous messages to remember
    REQUEST_TIMEOUT = 180   # Seconds before AI gives up
    
    # ---------------- SYSTEM PROMPT ----------------
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Elite Coding AI developed by {OWNER_USERNAME}. "
        "Your purpose is to generate high-quality, production-ready code.\n"
        "GUIDELINES:\n"
        "1. Always provide full code. Never say 'rest is same'.\n"
        "2. If Python is used, provide a `requirements.txt` block.\n"
        "3. Explain your logic clearly using comments.\n"
        "4. Be professional and polite.\n"
        "5. If asked for hacking/illegal tools, decline politely but offer educational alternatives.\n"
        "6. Structure your response with proper Markdown formatting."
    )

# ==============================================================================
#                           SECTION 2: LOGGING SYSTEM
# ==============================================================================

# Setup Logger to track errors and info
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RaiGPT_Core")

# ==============================================================================
#                           SECTION 3: TEXT CONSTANTS
# ==============================================================================

class TextManager:
    """
    Holds all text messages used in the bot for easy editing.
    Uses HTML formatting.
    """
    WELCOME_MSG = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{Config.BOT_NAME} v{Config.VERSION}</b>    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Welcome, {{name}}!</b>

I am an <b>Enterprise-Grade AI Assistant</b> capable of writing complex code, debugging scripts, and answering technical queries.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>AVAILABLE MODULES:</b>

🟢 <b>AI Coding Engine</b>
   └ <code>/rai [query]</code> - Generate Code
   
🟡 <b>Memory Manager</b>
   └ <code>/new</code> - Clear Chat History
   
🔵 <b>User Profile</b>
   └ <code>/me</code> - View Account Stats

🟣 <b>Support System</b>
   └ <code>/help</code> - Documentation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Developer:</b> {Config.OWNER_USERNAME}
📅 <b>Server Time:</b> {{time}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>Select an action below:</b>
"""

    FORCE_SUB_MSG = f"""
🛑 <b>ACCESS RESTRICTED</b>

⚠️ Dear <b>{{name}}</b>,

To use <b>{Config.BOT_NAME}</b>, you are required to join our official updates channel.
This helps us keep the servers running for free!

👇 <b>Join the channel and click 'Verify':</b>
"""

    HELP_MSG = f"""
📚 <b>DOCUMENTATION & HELP</b>

<b>1. How to generate code?</b>
   Type <code>/rai</code> followed by your question.
   <i>Ex:</i> <code>/rai Create a Flask Login System</code>

<b>2. The code is incomplete?</b>
   The AI tries to give full code, but Telegram has limits.
   Type <code>/rai continue</code> to get the rest.

<b>3. Bot isn't replying?</b>
   Complex code takes 1-2 minutes. Please be patient.

<b>4. How to reset context?</b>
   If the AI gets confused, type <code>/new</code> to restart memory.

👨‍💻 <b>Support:</b> {Config.OWNER_USERNAME}
"""

    MAINTENANCE_MSG = """
🚧 <b>SYSTEM MAINTENANCE</b> 🚧

The bot is currently undergoing upgrades.
Please try again in 30 minutes.

<i>We apologize for the inconvenience.</i>
"""

    BAN_MSG = "🚫 <b>ACCOUNT SUSPENDED</b>\n\nYou have been banned from using this bot due to policy violations."

# ==============================================================================
#                           SECTION 4: DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    Handles JSON-based data persistence.
    Thread-safe and robust.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = threading.Lock()
        self.db = self._load_initial()

    def _load_initial(self):
        """Loads DB from disk or creates default."""
        if not os.path.exists(self.filepath):
            logger.warning("Database file missing. Creating new DB.")
            return {
                "users": {},
                "banned_ids": [],
                "settings": {"maintenance_mode": False},
                "stats": {"total_queries": 0, "start_time": str(datetime.datetime.now())}
            }
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"DB Corruption: {e}. Backup restored (simulated).")
            return {"users": {}, "banned_ids": [], "settings": {"maintenance_mode": False}}

    def save(self):
        """Writes data to disk safely."""
        with self.lock:
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.db, f, indent=4)
            except Exception as e:
                logger.error(f"DB Save Failed: {e}")

    # --- User Management ---
    def register_user(self, user: User):
        uid = str(user.id)
        if uid not in self.db["users"]:
            self.db["users"][uid] = {
                "first_name": user.first_name,
                "username": user.username,
                "joined_at": str(datetime.datetime.now()),
                "query_count": 0,
                "history": []
            }
            self.save()
            return True
        return False

    def get_user_data(self, user_id):
        return self.db["users"].get(str(user_id))

    def get_all_user_ids(self):
        return list(self.db["users"].keys())

    # --- History Management ---
    def add_history_entry(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.db["users"]:
            history = self.db["users"][uid].get("history", [])
            history.append({"role": role, "content": content})
            
            # Prune history to keep JSON size manageable
            if len(history) > Config.MAX_HISTORY_DEPTH:
                history = history[-Config.MAX_HISTORY_DEPTH:]
            
            self.db["users"][uid]["history"] = history
            
            # Update stats
            if role == "user":
                self.db["users"][uid]["query_count"] += 1
                self.db["stats"]["total_queries"] = self.db.get("stats", {}).get("total_queries", 0) + 1
            
            self.save()

    def get_user_history(self, user_id):
        uid = str(user_id)
        return self.db["users"].get(uid, {}).get("history", [])

    def clear_user_history(self, user_id):
        uid = str(user_id)
        if uid in self.db["users"]:
            self.db["users"][uid]["history"] = []
            self.save()

    # --- Ban System ---
    def is_banned(self, user_id):
        return int(user_id) in self.db["banned_ids"]

    def set_ban_status(self, user_id, banned: bool):
        uid = int(user_id)
        if banned:
            if uid not in self.db["banned_ids"]:
                self.db["banned_ids"].append(uid)
        else:
            if uid in self.db["banned_ids"]:
                self.db["banned_ids"].remove(uid)
        self.save()

    # --- System Settings ---
    def is_maintenance(self):
        return self.db.get("settings", {}).get("maintenance_mode", False)

    def set_maintenance(self, status: bool):
        if "settings" not in self.db: self.db["settings"] = {}
        self.db["settings"]["maintenance_mode"] = status
        self.save()

# Instantiate Database
db = DatabaseEngine(Config.DB_FILE)

# ==============================================================================
#                           SECTION 5: 24/7 WEB SERVER
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def home():
    """Health check endpoint for Render/UptimeRobot."""
    stats = db.db.get("stats", {})
    return f"""
    <h1>Rai GPT Server is Running</h1>
    <p>Status: Online</p>
    <p>Total Queries Processed: {stats.get('total_queries', 0)}</p>
    <p>Owner: {Config.OWNER_USERNAME}</p>
    """

def run_flask():
    """Runs Flask in a separate thread."""
    port = int(os.environ.get('PORT', 8080))
    # Disable flask banners
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.run(host='0.0.0.0', port=port)

# ==============================================================================
#                           SECTION 6: AI PROCESSING CORE
# ==============================================================================

class AIEngine:
    """
    Handles communication with Pollinations AI API.
    Includes Retry Logic and formatting.
    """
    def __init__(self):
        self.api_endpoint = Config.AI_PROVIDER_URL

    def generate_response(self, user_input: str, history: List[Dict]) -> str:
        """Generates AI response based on prompt and history."""
        
        # 1. Context Construction
        context_string = ""
        for msg in history:
            role = "User" if msg['role'] == 'user' else "AI"
            context_string += f"{role}: {msg['content']}\n"

        # 2. Payload Construction
        full_prompt = (
            f"{Config.SYSTEM_INSTRUCTION}\n\n"
            f"--- HISTORY ---\n{context_string}\n"
            f"--- NEW REQUEST ---\nUser: {user_input}\nAI:"
        )

        # 3. Request Execution with Retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Encode the prompt for URL
                encoded_prompt = requests.utils.quote(full_prompt)
                request_url = f"{self.api_endpoint}{encoded_prompt}"
                
                response = requests.get(request_url, timeout=Config.REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    result = response.text
                    if len(result) < 5: 
                        continue # Invalid response
                    return result
                
                time.sleep(1) # Wait before retry
                
            except requests.exceptions.Timeout:
                logger.warning(f"AI Timeout (Attempt {attempt+1})")
            except Exception as e:
                logger.error(f"AI Error: {e}")
                
        return "❌ <b>Connection Failed.</b> The AI brain is currently unreachable. Please try again in 1 minute."

ai_core = AIEngine()

# ==============================================================================
#                           SECTION 7: HELPER UTILITIES
# ==============================================================================

class Utils:
    @staticmethod
    def split_message(text: str, limit=4000) -> List[str]:
        """
        Splits long messages intelligently to avoid breaking code blocks.
        """
        if len(text) <= limit:
            return [text]
        
        parts = []
        while len(text) > 0:
            if len(text) > limit:
                # Priority 1: Split at Code Block End
                split_at = text.rfind('```', 0, limit)
                # Priority 2: Split at Double Newline
                if split_at == -1: split_at = text.rfind('\n\n', 0, limit)
                # Priority 3: Split at Single Newline
                if split_at == -1: split_at = text.rfind('\n', 0, limit)
                # Fallback: Hard Limit
                if split_at == -1: split_at = limit
                
                chunk = text[:split_at]
                parts.append(chunk)
                text = text[split_at:]
            else:
                parts.append(text)
                text = ""
        return parts

    @staticmethod
    async def check_membership(user_id: int, bot) -> bool:
        """
        Verifies if the user has joined the required channel.
        """
        if not Config.FORCE_SUB_ENABLED:
            return True
            
        try:
            member = await bot.get_chat_member(Config.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked', 'restricted']:
                return False
            return True
        except BadRequest:
            # If bot is not admin, logic fails gracefully (allows user)
            logger.error("Bot is not admin in Force Sub channel!")
            return True
        except Exception as e:
            logger.error(f"Membership Check Error: {e}")
            return True

# ==============================================================================
#                           SECTION 8: COMMAND HANDLERS
# ==============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Register User
    db.register_user(user)
    
    # 1. Check Maintenance
    if db.is_maintenance() and user.id != Config.OWNER_ID:
        await update.message.reply_text(TextManager.MAINTENANCE_MSG, parse_mode=ParseMode.HTML)
        return

    # 2. Check Ban
    if db.is_banned(user.id):
        await update.message.reply_text(TextManager.BAN_MSG, parse_mode=ParseMode.HTML)
        return

    # 3. Check Force Subscribe
    is_joined = await Utils.check_membership(user.id, context.bot)
    if not is_joined:
        txt = TextManager.FORCE_SUB_MSG.format(name=html.escape(user.first_name))
        kb = [
            [InlineKeyboardButton("🚀 JOIN CHANNEL", url=Config.CHANNEL_LINK)],
            [InlineKeyboardButton("✅ I HAVE JOINED", callback_data="verify_join")]
        ]
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    # 4. Welcome Message
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    txt = TextManager.WELCOME_MSG.format(name=html.escape(user.first_name), time=time_str)
    
    kb = [
        [InlineKeyboardButton("🤖 Ask AI Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("💎 My Profile", callback_data="profile"), InlineKeyboardButton("🆘 Support", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{Config.OWNER_USERNAME.replace('@','')}")]
    ]
    
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TextManager.HELP_MSG, parse_mode=ParseMode.HTML)

async def new_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.clear_user_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Conversation History Cleared!</b>\nI am ready for a new topic.", parse_mode=ParseMode.HTML)

async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User Profile Command"""
    user = update.effective_user
    data = db.get_user_data(user.id)
    
    if not data:
        await update.message.reply_text("User data not found.")
        return
        
    txt = f"""
👤 <b>USER PROFILE</b>

🆔 <b>ID:</b> <code>{user.id}</code>
📛 <b>Name:</b> {html.escape(user.first_name)}
📅 <b>Joined:</b> {data['joined_at'][:10]}
💬 <b>Total Queries:</b> {data['query_count']}
"""
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 9: AI HANDLER (/rai)
# ==============================================================================

async def rai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # --- PRE-CHECKS ---
    if db.is_maintenance() and user.id != Config.OWNER_ID:
        await update.message.reply_text(TextManager.MAINTENANCE_MSG, parse_mode=ParseMode.HTML)
        return
        
    if db.is_banned(user.id):
        return

    if not await Utils.check_membership(user.id, context.bot):
        await update.message.reply_text(f"❌ <b>Access Denied!</b>\nPlease join {Config.CHANNEL_USERNAME} to use this command.", parse_mode=ParseMode.HTML)
        return

    if not context.args:
        await update.message.reply_text("⚠️ <b>Missing Input!</b>\nExample: <code>/rai python calculator code</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    
    # --- UI FEEDBACK ---
    status_msg = await update.message.reply_text(
        f"🧠 <b>Processing Request...</b>\n\n📝 <i>Topic: {html.escape(prompt[:40])}...</i>\n⏳ <i>Writing Code...</i>",
        parse_mode=ParseMode.HTML
    )
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # --- AI GENERATION ---
        history = db.get_user_history(user.id)
        
        # Run blocking IO in executor
        loop = asyncio.get_running_loop()
        ai_reply = await loop.run_in_executor(None, ai_core.generate_response, prompt, history)
        
        # Update History
        db.add_history_entry(user.id, "user", prompt)
        db.add_history_entry(user.id, "ai", ai_reply)
        
        # --- SEND RESPONSE ---
        await status_msg.delete()
        
        # Split logic for long messages
        messages = Utils.split_message(ai_reply)
        
        for i, msg in enumerate(messages):
            try:
                # Attempt Markdown
                await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            except:
                # Fallback to HTML if Markdown breaks
                try:
                    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
                except:
                    await update.message.reply_text(msg) # Raw text fallback
            
            # Tiny delay to keep order
            if len(messages) > 1:
                time.sleep(0.5)

    except Exception as e:
        logger.error(f"Handler Error: {e}")
        await status_msg.edit_text("❌ <b>Internal Error.</b> Please try again later.", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 10: ADMIN DASHBOARD
# ==============================================================================

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    
    stats = db.db.get("stats", {})
    users_count = len(db.db.get("users", {}))
    banned_count = len(db.db.get("banned_ids", []))
    
    txt = f"""
📊 <b>ADMIN DASHBOARD</b>

👥 <b>Total Users:</b> {users_count}
🚫 <b>Banned:</b> {banned_count}
💬 <b>Total Interactions:</b> {stats.get('total_queries', 0)}
🚀 <b>Uptime Since:</b> {stats.get('start_time', 'Unknown')}
    """
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
        
    msg = " ".join(context.args)
    users = db.get_all_user_ids()
    
    progress_msg = await update.message.reply_text(f"🚀 <b>Starting Broadcast...</b>\nTarget: {len(users)} users", parse_mode=ParseMode.HTML)
    
    success = 0
    blocked = 0
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}", parse_mode=ParseMode.HTML)
            success += 1
        except (Forbidden, BadRequest):
            blocked += 1
        except Exception:
            pass
            
    await progress_msg.edit_text(
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"🟢 Sent: {success}\n"
        f"🔴 Blocked/Failed: {blocked}",
        parse_mode=ParseMode.HTML
    )

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    try:
        target = int(context.args[0])
        db.set_ban_status(target, True)
        await update.message.reply_text(f"🚫 User {target} Banned.")
    except: await update.message.reply_text("Usage: /ban user_id")

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    try:
        target = int(context.args[0])
        db.set_ban_status(target, False)
        await update.message.reply_text(f"✅ User {target} Unbanned.")
    except: await update.message.reply_text("Usage: /unban user_id")

async def admin_maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    try:
        state = context.args[0].lower()
        if state == "on":
            db.set_maintenance(True)
            await update.message.reply_text("🚧 Maintenance Mode ENABLED.")
        elif state == "off":
            db.set_maintenance(False)
            await update.message.reply_text("✅ Maintenance Mode DISABLED.")
        else:
            await update.message.reply_text("Usage: /maintenance [on/off]")
    except: await update.message.reply_text("Usage: /maintenance [on/off]")

# ==============================================================================
#                           SECTION 11: CALLBACK HANDLERS
# ==============================================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "verify_join":
        is_sub = await Utils.check_membership(query.from_user.id, context.bot)
        if is_sub:
            await query.delete_message()
            await start_command(update, context)
        else:
            await query.answer("❌ You haven't joined yet!", show_alert=True)
            
    elif data == "help_menu":
        await query.edit_message_text(TextManager.HELP_MSG, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start_menu")]]))
        
    elif data == "profile":
        user_data = db.get_user_data(query.from_user.id)
        if user_data:
            txt = f"👤 <b>PROFILE</b>\n\nName: {html.escape(user_data['first_name'])}\nJoined: {user_data['joined_at'][:10]}\nQueries: {user_data['query_count']}"
            await query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start_menu")]]))
            
    elif data == "start_menu":
        # Simplified start for back button
        await start_command(update, context)

# ==============================================================================
#                           SECTION 12: INITIALIZATION
# ==============================================================================

async def post_init(app: Application):
    """Sets bot menu commands on startup."""
    commands = [
        BotCommand("start", "🏠 Main Menu"),
        BotCommand("rai", "🤖 Ask AI"),
        BotCommand("new", "🧹 Reset Memory"),
        BotCommand("me", "👤 My Profile"),
        BotCommand("help", "🆘 Support")
    ]
    await app.bot.set_my_commands(commands)

def main():
    print("🚀 INITIALIZING RAI GPT PRO...")
    
    # 1. Start Flask Server (Threaded)
    threading.Thread(target=run_flask, daemon=True).start()
    print("✅ Web Server Started (24/7 Mode)")
    
    # 2. Build Bot
    app = ApplicationBuilder().token(Config.TOKEN).post_init(post_init).build()
    
    # 3. Register Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("rai", rai_handler))
    app.add_handler(CommandHandler("new", new_chat_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("me", me_command))
    
    # Admin
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("maintenance", admin_maintenance))
    
    # Callback
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Bot is Live & Polling!")
    app.run_polling()

if __name__ == "__main__":
    main()
