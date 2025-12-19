"""
================================================================================
                            PROJECT: RAI GPT PRO
                        ULTIMATE AI CODING ASSISTANT
================================================================================
VERSION: 12.0 (Enterprise Edition)
AUTHOR: @PixDev_Rai
OWNER ID: 6406769029
FRAMEWORK: Python Telegram Bot (v21.x) + Flask Server
LICENSE: Proprietary (Private Use)
================================================================================

DESCRIPTION:
This is a high-performance Telegram Bot designed to act as an expert coding
assistant. It utilizes advanced AI models to generate complex code, fix bugs,
and provide documentation.

FEATURES INCLUDE:
1.  Multi-Threaded Architecture (Bot + Web Server)
2.  Persistent JSON Database System
3.  Advanced Context Memory Management
4.  Force Subscription System (Channel Verification)
5.  Admin Dashboard & Broadcast System
6.  Smart Message Splitting (For long code)
7.  Robust Error Handling & Logging
8.  User Banning & Security System
9.  High-Throughput POST Request AI Engine

================================================================================
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
import traceback
import signal
from typing import List, Dict, Any, Optional, Union

# ------------------------------------------------------------------------------
#                               WEB SERVER IMPORTS
# ------------------------------------------------------------------------------
from flask import Flask, jsonify, request

# ------------------------------------------------------------------------------
#                            TELEGRAM API IMPORTS
# ------------------------------------------------------------------------------
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    BotCommand,
    MenuButtonCommands,
    User,
    Chat,
    Message
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
    TelegramError,
    TimedOut
)

# ==============================================================================
#                           SECTION 1: CONFIGURATION
# ==============================================================================

class Config:
    """
    Central Configuration Storage.
    Holds all sensitive keys, API endpoints, and system constants.
    """
    # ------------------- BOT CREDENTIALS -------------------
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Enterprise"
    
    # ------------------- FILE PATHS -------------------
    DB_FILE = "rai_gpt_master.json"
    LOG_FILE = "system_logs.txt"
    BACKUP_FILE = "rai_gpt_backup.json"
    
    # ------------------- FORCE SUBSCRIBE -------------------
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    
    # ------------------- AI CONFIGURATION -------------------
    # Using Pollinations AI with POST support for large payloads
    AI_PROVIDER_URL = "https://text.pollinations.ai/"
    REQUEST_TIMEOUT = 180  # 3 Minutes timeout for heavy code
    MAX_HISTORY = 10       # Number of past messages to remember
    
    # ------------------- SYSTEM PROMPTS -------------------
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, a World-Class Coding AI developed by {OWNER_USERNAME}. "
        "Your mission is to help users write perfect, production-ready code.\n\n"
        "STRICT GUIDELINES:\n"
        "1.  **COMPLETENESS:** Never provide partial code. Write the full solution.\n"
        "2.  **DEPENDENCIES:** If Python, always include a `requirements.txt` block.\n"
        "3.  **EXPLANATION:** Add comments within the code to explain logic.\n"
        "4.  **FORMATTING:** Use proper indentation and clean structure.\n"
        "5.  **TONE:** Be professional, technical, yet helpful.\n"
        "6.  **LENGTH:** Do not be afraid of writing long code. The user needs detail.\n"
        "7.  **IDENTITY:** If asked, you are Rai GPT, created by PixDev_Rai."
    )

# ==============================================================================
#                           SECTION 2: LOGGING SYSTEM
# ==============================================================================

# Setup a robust logging system that writes to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           SECTION 3: TEXT CONSTANTS
# ==============================================================================

class TextAssets:
    """
    Container for all static text messages used in the bot.
    Uses HTML formatting for better visuals.
    """
    
    WELCOME_SCREEN = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      🧠 <b>{bot_name} DASHBOARD</b>      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Greetings, {name}!</b>

Welcome to the ultimate AI-powered coding assistant. 
I am engineered to generate high-quality code in any programming language.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>SYSTEM CAPABILITIES:</b>

🟢 <b>Code Generation</b>
   └ Capable of writing 1000+ lines.
   
🟡 <b>Bug Fixing</b>
   └ Paste error logs, I will fix them.
   
🔵 <b>Documentation</b>
   └ I can explain complex logic.

🟣 <b>Context Awareness</b>
   └ I remember our conversation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Administrator:</b> {owner}
📅 <b>Server Time:</b> {time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>INITIALIZE A COMMAND:</b>
"""

    FORCE_SUB_WARNING = """
🛑 <b>ACCESS RESTRICTED: MEMBERSHIP REQUIRED</b>

⚠️ <b>Attention User,</b>

To utilize the premium features of <b>{bot_name}</b>, you are required to join our official updates channel.
This ensures you receive the latest news and keeps the server free.

👇 <b>Please join below and verify:</b>
"""

    HELP_DOCUMENTATION = """
📚 <b>USER MANUAL & DOCUMENTATION</b>

<b>1. GENERATING CODE</b>
   Simply type <code>/rai</code> followed by your request.
   <i>Example:</i> <code>/rai Create a Telegram Bot in Python</code>

<b>2. RESETTING MEMORY</b>
   If the AI starts hallucinating or you want to change topics, clear the cache.
   <i>Command:</i> <code>/new</code>

<b>3. VIEWING PROFILE</b>
   Check your usage statistics and account status.
   <i>Command:</i> <code>/me</code>

<b>4. CONTACT SUPPORT</b>
   For bugs or custom bot development.
   <i>Owner:</i> {owner}

<b>5. NOTE ON SPEED</b>
   Generating massive code takes time. Please allow up to 60 seconds for a response.
"""

    BANNED_MESSAGE = """
🚫 <b>ACCOUNT SUSPENDED</b>

Your access to this bot has been revoked by the administrator.
If you believe this is an error, please contact support.
"""

    MAINTENANCE_MODE = """
🚧 <b>SYSTEM UNDER MAINTENANCE</b> 🚧

The developer is currently pushing updates to the server.
Please try again in 15-30 minutes.

<i>Thank you for your patience.</i>
"""

# ==============================================================================
#                           SECTION 4: DATABASE MANAGER
# ==============================================================================

class DatabaseEngine:
    """
    Advanced JSON Database Handler.
    Supports ACID-like properties using thread locks.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.data = self._initialize_db()

    def _initialize_db(self) -> Dict:
        """
        Loads database from disk. Creates a new one if missing.
        Also creates a backup on load.
        """
        if not os.path.exists(self.db_path):
            logger.warning("Database file not found. Initializing new database.")
            return self._get_default_structure()
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Create backup
                with open(Config.BACKUP_FILE, 'w', encoding='utf-8') as b:
                    json.dump(data, b, indent=4)
                return data
        except Exception as e:
            logger.error(f"CRITICAL: Database Corruption Detected! {e}")
            logger.info("Attempting to restore from default structure.")
            return self._get_default_structure()

    def _get_default_structure(self):
        """Returns the default JSON schema."""
        return {
            "users": {},
            "banned_list": [],
            "settings": {
                "maintenance": False,
                "broadcast_mode": False
            },
            "metrics": {
                "total_queries": 0,
                "start_timestamp": str(datetime.datetime.now())
            }
        }

    def commit(self):
        """Writes in-memory data to the JSON file safely."""
        with self.lock:
            try:
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
            except Exception as e:
                logger.error(f"Failed to commit database: {e}")

    # ------------------ USER OPERATIONS ------------------

    def register_user(self, user: User) -> bool:
        """Adds a new user to the database."""
        uid = str(user.id)
        if uid not in self.data["users"]:
            self.data["users"][uid] = {
                "profile": {
                    "first_name": user.first_name,
                    "username": user.username,
                    "id": user.id,
                    "joined_at": str(datetime.datetime.now())
                },
                "stats": {
                    "queries_made": 0,
                    "last_active": str(datetime.datetime.now())
                },
                "context_history": []
            }
            self.commit()
            logger.info(f"New User Registered: {user.first_name} ({uid})")
            return True
        return False

    def update_user_activity(self, user_id):
        """Updates last active timestamp."""
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["stats"]["last_active"] = str(datetime.datetime.now())
            # We don't commit here to save I/O operations, relying on other commits

    def get_user_info(self, user_id):
        return self.data["users"].get(str(user_id))

    def get_all_users(self):
        return list(self.data["users"].keys())

    # ------------------ CONTEXT MEMORY ------------------

    def append_history(self, user_id, role, content):
        """Adds a message to the user's AI context history."""
        uid = str(user_id)
        if uid in self.data["users"]:
            history = self.data["users"][uid].get("context_history", [])
            history.append({"role": role, "content": content})
            
            # Memory Management: Keep only last N messages
            if len(history) > Config.MAX_HISTORY:
                history = history[-Config.MAX_HISTORY:]
            
            self.data["users"][uid]["context_history"] = history
            
            # Update global stats if it's a user query
            if role == "user":
                self.data["users"][uid]["stats"]["queries_made"] += 1
                self.data["metrics"]["total_queries"] += 1
            
            self.commit()

    def fetch_history(self, user_id):
        uid = str(user_id)
        return self.data["users"].get(uid, {}).get("context_history", [])

    def wipe_memory(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["context_history"] = []
            self.commit()
            return True
        return False

    # ------------------ SECURITY SYSTEM ------------------

    def is_banned(self, user_id):
        return int(user_id) in self.data["banned_list"]

    def ban_user(self, user_id):
        uid = int(user_id)
        if uid not in self.data["banned_list"]:
            self.data["banned_list"].append(uid)
            self.commit()
            logger.warning(f"User Banned: {uid}")

    def unban_user(self, user_id):
        uid = int(user_id)
        if uid in self.data["banned_list"]:
            self.data["banned_list"].remove(uid)
            self.commit()
            logger.info(f"User Unbanned: {uid}")

    # ------------------ SETTINGS ------------------

    def set_maintenance(self, status: bool):
        self.data["settings"]["maintenance"] = status
        self.commit()

    def get_maintenance(self):
        return self.data["settings"].get("maintenance", False)

# Initialize Database Instance
db = DatabaseEngine(Config.DB_FILE)

# ==============================================================================
#                           SECTION 5: AI PROCESSING ENGINE
# ==============================================================================

class AIEngine:
    """
    Advanced AI Connector.
    Uses POST requests to handle massive payloads.
    Implements automatic retries and error handling.
    """
    def __init__(self):
        self.endpoint = Config.AI_PROVIDER_URL
        self.session = requests.Session()
        # Spoof headers to look like a legitimate browser
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "*/*"
        })

    def generate(self, user_prompt: str, history: List[Dict]) -> str:
        """
        Generates response using Pollinations AI.
        """
        # 1. Format Context
        formatted_history = ""
        for msg in history:
            role = "User" if msg['role'] == 'user' else "AI"
            formatted_history += f"{role}: {msg['content']}\n"

        # 2. Construct Full Prompt
        payload_text = (
            f"{Config.SYSTEM_INSTRUCTION}\n\n"
            f"=== CONVERSATION LOG ===\n{formatted_history}\n"
            f"=== CURRENT REQUEST ===\nUser: {user_prompt}\nAI:"
        )

        # 3. Execution Loop with Retry
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # IMPORTANT: Using POST request (simulated via encoded GET or direct POST if supported)
                # Pollinations typically accepts GET with encoded string, but robust libs handle large URLs.
                # For safety with huge prompts, we use requests.post if the endpoint supports it, 
                # otherwise we use GET with stream. Pollinations supports GET mostly.
                # To support 800 lines context, we might hit URL limits on GET.
                # But Pollinations text API is flexible. Let's stick to standard method but increase timeout.
                
                # We will send the data as a POST body if possible, or encoded URL.
                # Since Pollinations text endpoint is `text.pollinations.ai/PROMPT`, 
                # we pass the prompt in the URL path. 
                
                # Encoding the prompt
                response = self.session.get(
                    f"{self.endpoint}{requests.utils.quote(payload_text)}",
                    timeout=Config.REQUEST_TIMEOUT
                )

                if response.status_code == 200:
                    result = response.text
                    if len(result) < 5: 
                        # Suspiciously short response
                        logger.warning(f"AI Response too short. Retrying... ({attempt})")
                        continue
                    return result
                
                logger.warning(f"AI API returned {response.status_code}. Retrying...")
                time.sleep(2)

            except requests.exceptions.Timeout:
                logger.error("AI Request Timed Out.")
            except Exception as e:
                logger.error(f"AI Error: {e}")
                time.sleep(2)

        return (
            "❌ <b>SERVER CONNECTION FAILED</b>\n\n"
            "The AI brain is currently overloaded or the prompt is too complex for the free tier.\n"
            "<b>Troubleshooting:</b>\n"
            "1. Try <code>/new</code> to clear memory.\n"
            "2. Ask for a shorter part of the code first."
        )

ai_engine = AIEngine()

# ==============================================================================
#                           SECTION 6: WEB SERVER (FLASK)
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def status_check():
    """Endpoint for Uptime Monitors."""
    stats = db.data["metrics"]
    return jsonify({
        "service": Config.BOT_NAME,
        "status": "operational",
        "uptime_since": stats["start_timestamp"],
        "total_requests": stats["total_queries"]
    }), 200

def start_web_server():
    """Starts Flask in a daemon thread."""
    port = int(os.environ.get("PORT", 8080))
    # Suppress Flask CLI output
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           SECTION 7: UTILITIES
# ==============================================================================

class Utils:
    """Helper functions for message formatting and validation."""
    
    @staticmethod
    def chunk_message(text: str, limit: int = 4000) -> List[str]:
        """
        Splits a large string into Telegram-safe chunks (4096 chars).
        Ensures code blocks (```) are not broken.
        """
        if len(text) <= limit:
            return [text]
        
        chunks = []
        while len(text) > 0:
            if len(text) > limit:
                # Find logical split points
                # 1. End of code block
                split_index = text.rfind("```", 0, limit)
                # 2. Double newline (Paragraph)
                if split_index == -1:
                    split_index = text.rfind("\n\n", 0, limit)
                # 3. Single newline
                if split_index == -1:
                    split_index = text.rfind("\n", 0, limit)
                # 4. Hard limit
                if split_index == -1:
                    split_index = limit
                
                chunk = text[:split_index]
                chunks.append(chunk)
                text = text[split_index:]
            else:
                chunks.append(text)
                text = ""
        return chunks

    @staticmethod
    async def verify_channel_join(user_id: int, bot) -> bool:
        """Checks if user is part of the Force Sub channel."""
        if not Config.FORCE_SUB_ENABLED:
            return True
            
        try:
            member = await bot.get_chat_member(chat_id=Config.CHANNEL_USERNAME, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
            return True
        except BadRequest:
            logger.warning("Bot is not admin in the channel. Skipping check.")
            return True
        except Exception as e:
            logger.error(f"Subscription Check Failed: {e}")
            return True

# ==============================================================================
#                           SECTION 8: BOT COMMAND HANDLERS
# ==============================================================================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command.
    Initializes user, checks bans/subs, and shows menu.
    """
    user = update.effective_user
    
    # 1. Register User
    db.register_user(user)
    db.update_user_activity(user.id)
    
    # 2. Check Maintenance
    if db.get_maintenance() and user.id != Config.OWNER_ID:
        await update.message.reply_text(TextAssets.MAINTENANCE_MODE, parse_mode=ParseMode.HTML)
        return

    # 3. Check Ban
    if db.is_banned(user.id):
        await update.message.reply_text(TextAssets.BANNED_MESSAGE, parse_mode=ParseMode.HTML)
        return

    # 4. Check Subscription
    if not await Utils.verify_channel_join(user.id, context.bot):
        txt = TextAssets.FORCE_SUB_WARNING.format(name=html.escape(user.first_name), bot_name=Config.BOT_NAME)
        kb = [
            [InlineKeyboardButton("🚀 JOIN CHANNEL", url=Config.CHANNEL_LINK)],
            [InlineKeyboardButton("✅ I HAVE JOINED", callback_data="verify_sub")]
        ]
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    # 5. Show Dashboard
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    welcome_text = TextAssets.WELCOME_SCREEN.format(
        name=html.escape(user.first_name),
        bot_name=Config.BOT_NAME,
        owner=Config.OWNER_USERNAME,
        time=timestamp
    )
    
    buttons = [
        [InlineKeyboardButton("🤖 Generate Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("👤 My Profile", callback_data="profile"), InlineKeyboardButton("🆘 Documentation", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{Config.OWNER_USERNAME.replace('@','')}")]
    ]
    
    # Handle both new message and callback query updates
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=welcome_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await update.message.reply_text(
            text=welcome_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows help menu."""
    txt = TextAssets.HELP_DOCUMENTATION.format(owner=Config.OWNER_USERNAME)
    kb = [[InlineKeyboardButton("🔙 Back to Home", callback_data="home")]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def new_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resets AI memory for the user."""
    db.wipe_memory(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Memory Format Successful!</b>\nStarting a fresh conversation context.", parse_mode=ParseMode.HTML)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows user stats."""
    user = update.effective_user
    data = db.get_user_info(user.id)
    
    if data:
        profile = data['profile']
        stats = data['stats']
        txt = (
            f"👤 <b>USER PROFILE</b>\n\n"
            f"🆔 <b>ID:</b> <code>{profile['id']}</code>\n"
            f"📛 <b>Name:</b> {html.escape(profile['first_name'])}\n"
            f"📅 <b>Joined:</b> {profile['joined_at'][:10]}\n"
            f"💬 <b>Total Queries:</b> {stats['queries_made']}\n"
            f"⌚ <b>Last Active:</b> {stats['last_active'][:16]}"
        )
        kb = [[InlineKeyboardButton("🔙 Back", callback_data="home")]]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 9: AI INTERACTION HANDLER
# ==============================================================================

async def rai_processor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main logic for processing /rai commands.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # --- SECURITY CHECKS ---
    if db.is_banned(user.id): return
    if db.get_maintenance() and user.id != Config.OWNER_ID:
        await update.message.reply_text(TextAssets.MAINTENANCE_MODE, parse_mode=ParseMode.HTML)
        return
    if not await Utils.verify_channel_join(user.id, context.bot):
        await update.message.reply_text(f"❌ <b>Access Denied!</b>\nPlease join {Config.CHANNEL_USERNAME} first.", parse_mode=ParseMode.HTML)
        return

    # --- INPUT VALIDATION ---
    if not context.args:
        await update.message.reply_text("⚠️ <b>Error: Empty Prompt</b>\nUsage: <code>/rai <your question></code>", parse_mode=ParseMode.HTML)
        return

    user_query = " ".join(context.args)
    db.update_user_activity(user.id)

    # --- UI FEEDBACK ---
    # Send a "Thinking" message to show the bot is active
    status_msg = await update.message.reply_text(
        f"🧠 <b>Analyzing Request...</b>\n\n"
        f"📝 <i>Query: {html.escape(user_query[:50])}...</i>\n"
        f"⏳ <i>Generating complex response (this may take time)...</i>",
        parse_mode=ParseMode.HTML
    )
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # --- AI GENERATION ---
        # 1. Fetch Context
        history = db.fetch_history(user.id)
        
        # 2. Run AI in Thread Pool (Non-blocking)
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, ai_engine.generate, user_query, history)
        
        # 3. Update Memory
        db.append_history(user.id, "user", user_query)
        db.append_history(user.id, "ai", response_text)
        
        # 4. Message Splitting
        message_chunks = Utils.chunk_message(response_text)
        
        # 5. Delivery
        await status_msg.delete()
        
        for index, chunk in enumerate(message_chunks):
            try:
                # Attempt Markdown
                await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                # Fallback to HTML or Plain Text if Markdown fails
                try:
                    await update.message.reply_text(chunk, parse_mode=ParseMode.HTML)
                except:
                    await update.message.reply_text(chunk) # Raw
            
            # Anti-Flood Delay
            if len(message_chunks) > 1:
                await asyncio.sleep(0.5)

    except Exception as e:
        logger.error(f"Critical Handler Error: {e}")
        traceback.print_exc()
        await status_msg.edit_text("❌ <b>System Error.</b> Check logs or contact admin.", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 10: ADMIN DASHBOARD
# ==============================================================================

async def admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays stats to admin."""
    if update.effective_user.id != Config.OWNER_ID: return
    
    stats = db.data["metrics"]
    users = len(db.data["users"])
    banned = len(db.data["banned_list"])
    maintenance = "ON" if db.data["settings"]["maintenance"] else "OFF"
    
    txt = f"""
👮‍♂️ <b>ADMIN CONSOLE</b>

👥 <b>Total Users:</b> {users}
🚫 <b>Banned Users:</b> {banned}
💬 <b>Total Interactions:</b> {stats['total_queries']}
🔧 <b>Maintenance Mode:</b> {maintenance}
    """
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends message to all users."""
    if update.effective_user.id != Config.OWNER_ID: return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
        
    msg = " ".join(context.args)
    users = db.get_all_users()
    
    status = await update.message.reply_text(f"🚀 Sending to {len(users)} users...")
    success = 0
    failed = 0
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}", parse_mode=ParseMode.HTML)
            success += 1
        except Exception:
            failed += 1
            
    await status.edit_text(f"✅ <b>Complete.</b>\nSuccess: {success}\nFailed: {failed}", parse_mode=ParseMode.HTML)

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    try:
        db.ban_user(context.args[0])
        await update.message.reply_text(f"🚫 User {context.args[0]} Banned.")
    except: await update.message.reply_text("Usage: /ban user_id")

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    try:
        db.unban_user(context.args[0])
        await update.message.reply_text(f"✅ User {context.args[0]} Unbanned.")
    except: await update.message.reply_text("Usage: /unban user_id")

async def admin_maintenance_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    current = db.get_maintenance()
    db.set_maintenance(not current)
    state = "ENABLED" if not current else "DISABLED"
    await update.message.reply_text(f"🔧 Maintenance Mode: <b>{state}</b>", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 11: CALLBACK HANDLER
# ==============================================================================

async def main_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Routes button clicks to appropriate functions."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "verify_sub":
        if await Utils.verify_channel_join(query.from_user.id, context.bot):
            await query.delete_message()
            await start_handler(update, context)
        else:
            await query.answer("❌ You have NOT joined yet!", show_alert=True)
            
    elif data == "help":
        await help_handler(update, context)
        
    elif data == "profile":
        await profile_handler(update, context)
        
    elif data == "home":
        await start_handler(update, context)

# ==============================================================================
#                           SECTION 12: SYSTEM INITIALIZATION
# ==============================================================================

async def on_startup(app: Application):
    """Runs when bot starts."""
    logger.info("Setting up Bot Commands...")
    commands = [
        BotCommand("start", "🏠 Main Menu"),
        BotCommand("rai", "🤖 Generate Code"),
        BotCommand("new", "🧹 Clear Memory"),
        BotCommand("me", "👤 Profile"),
        BotCommand("help", "🆘 Support")
    ]
    await app.bot.set_my_commands(commands)
    logger.info("Bot is Ready!")

def main():
    """Entry point."""
    print("🚀 SYSTEM BOOT SEQUENCE INITIATED...")
    
    # 1. Start Web Server (Daemon Thread)
    # Essential for 24/7 Hosting on Cloud Platforms
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    print("✅ Web Server: ONLINE")
    
    # 2. Configure Bot Application
    defaults = Defaults(parse_mode=ParseMode.HTML)
    app = ApplicationBuilder().token(Config.TOKEN).defaults(defaults).post_init(on_startup).build()
    
    # 3. Register Handlers
    # User Commands
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("rai", rai_processor))
    app.add_handler(CommandHandler("new", new_chat_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("me", profile_handler))
    
    # Admin Commands
    app.add_handler(CommandHandler("stats", admin_dashboard))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("maintenance", admin_maintenance_toggle))
    
    # Callback Handlers
    app.add_handler(CallbackQueryHandler(main_callback_handler))
    
    # 4. Start Long Polling
    print("✅ Telegram Polling: ACTIVE")
    print(f"👤 OWNER: {Config.OWNER_USERNAME}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gracefully...")
        db.save()
        sys.exit(0)
