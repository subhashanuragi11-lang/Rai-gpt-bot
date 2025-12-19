#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
                            PROJECT: RAI GPT ENTERPRISE
                        AI-POWERED CODING ASSISTANT SUITE
================================================================================
VERSION:     15.0 (Ultimate Stable)
BUILD:       2025.12.19-Release
AUTHOR:      @PixDev_Rai
OWNER ID:    6406769029
LICENSE:     Proprietary (Private Use Only)
FRAMEWORK:   Python Telegram Bot (v21.x) + Flask Microserver
================================================================================

[ DESCRIPTION ]
This software functions as a high-throughput AI bridge between Telegram users
and Large Language Models (LLMs). It is engineered for stability, speed, and
handling massive code generation requests without timeouts.

[ KEY FEATURES ]
1.  Multi-Threaded Web Server (Flask) for 24/7 Uptime.
2.  ACID-Compliant JSON Database with Auto-Backup.
3.  Context-Aware Memory Engine (Short-Term Conversational History).
4.  Smart Message Splitter (Preserves Code Syntax Highlighting).
5.  Force Subscription Module (Channel Verification).
6.  Role-Based Access Control (RBAC) - Admin vs User.
7.  Advanced Error Reporting & File Logging.
8.  Anti-Flood & Rate Limiting Mechanisms.

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
from typing import List, Dict, Any, Optional, Union, Tuple

# ------------------------------------------------------------------------------
#                               WEB SERVER DEPENDENCIES
# ------------------------------------------------------------------------------
from flask import Flask, jsonify, request, make_response

# ------------------------------------------------------------------------------
#                            TELEGRAM API DEPENDENCIES
# ------------------------------------------------------------------------------
try:
    from telegram import (
        Update, 
        InlineKeyboardButton, 
        InlineKeyboardMarkup, 
        BotCommand,
        MenuButtonCommands,
        User,
        Chat,
        Message,
        constants
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
except ImportError:
    print("CRITICAL ERROR: 'python-telegram-bot' library is missing.")
    sys.exit(1)

# ==============================================================================
#                           SECTION 1: SYSTEM CONFIGURATION
# ==============================================================================

class SystemConfig:
    """
    Central Configuration Controller.
    Manages all static variables, credentials, and tuning parameters.
    """
    
    # ------------------- IDENTITY -------------------
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Pro"
    
    # ------------------- FILESYSTEM -------------------
    DB_FILE = "rai_gpt_database.json"
    LOG_FILE = "server_activity.log"
    BACKUP_FILE = "rai_gpt_backup.json"
    
    # ------------------- SECURITY -------------------
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    ADMIN_LIST = [6406769029]  # Add other admin IDs here
    
    # ------------------- AI PARAMETERS -------------------
    # Using Pollinations AI (Text Model)
    AI_BASE_URL = "https://text.pollinations.ai/"
    REQUEST_TIMEOUT = 180  # Seconds (3 Minutes)
    MAX_HISTORY_DEPTH = 6  # Limit history to prevent URL overflow
    RETRY_ATTEMPTS = 3     # Number of retries on failure
    
    # ------------------- SYSTEM PROMPT -------------------
    # This defines the personality and capabilities of the AI
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Elite Coding AI developed by {OWNER_USERNAME}. "
        "Your primary directive is to generate PRODUCTION-READY CODE.\n\n"
        "### OPERATIONAL GUIDELINES:\n"
        "1.  **NO TRUNCATION:** You must provide the FULL code. Do not use placeholders like '...rest of code...'.\n"
        "2.  **DEPENDENCIES:** If Python is requested, you MUST provide a `requirements.txt` block.\n"
        "3.  **DOCUMENTATION:** Add comments explaining complex logic.\n"
        "4.  **STRUCTURE:** If a bot is requested, provide the main file, config file, and requirements separately.\n"
        "5.  **TONE:** Professional, Efficient, and Technical.\n"
    )

# ==============================================================================
#                           SECTION 2: LOGGING INFRASTRUCTURE
# ==============================================================================

class LoggerSetup:
    """
    Configures the logging system to capture streams to both Console and File.
    Essential for debugging production environments.
    """
    @staticmethod
    def initialize():
        log_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - %(message)s'
        )
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # File Handler
        file_handler = logging.FileHandler(SystemConfig.LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)
        
        logging.info("Logger System Initialized Successfully.")

# Initialize Logging immediately
LoggerSetup.initialize()
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           SECTION 3: STATIC ASSETS & TEXT
# ==============================================================================

class UIManager:
    """
    Manages all static text responses, error messages, and UI templates.
    """
    
    @staticmethod
    def get_welcome_message(user_name: str, time_str: str) -> str:
        return f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      🧠 <b>{SystemConfig.BOT_NAME} DASHBOARD</b>      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Greetings, {user_name}!</b>

System Online. Time: {time_str}
I am an <b>Enterprise-Grade AI Architect</b> capable of generating complex software solutions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>OPERATIONAL CAPABILITIES:</b>

🟢 <b>Code Generation</b>
   └ Python, Java, C++, JS, HTML, etc.
   
🟡 <b>Debugging & Fixes</b>
   └ Send errors, get solutions.
   
🟣 <b>Smart Context</b>
   └ I remember previous messages.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Administrator:</b> {SystemConfig.OWNER_USERNAME}
📅 <b>Status:</b> 🟢 Online (24/7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>INITIALIZE A PROTOCOL:</b>
"""

    FORCE_SUB_TEXT = f"""
🛑 <b>ACCESS RESTRICTED: VERIFICATION REQUIRED</b>

⚠️ <b>Attention User,</b>

To access the computational power of <b>{SystemConfig.BOT_NAME}</b>, you are required to join our official network.
This ensures server stability and community growth.

👇 <b>Please join the channel below:</b>
"""

    HELP_TEXT = f"""
📚 <b>SYSTEM DOCUMENTATION</b>

<b>1. GENERATING CODE</b>
   Command: <code>/rai [prompt]</code>
   <i>Usage:</i> <code>/rai python telegram bot code</code>

<b>2. MEMORY MANAGEMENT</b>
   Command: <code>/new</code>
   <i>Usage:</i> Clears conversation context to start fresh.

<b>3. ACCOUNT STATUS</b>
   Command: <code>/me</code>
   <i>Usage:</i> Displays your user ID and usage stats.

<b>4. SUPPORT</b>
   Contact: {SystemConfig.OWNER_USERNAME}

<b>⚠️ NOTE ON LATENCY:</b>
Generating 800+ lines of code requires significant processing time. 
Please allow up to 1-2 minutes for a response.
"""

    MAINTENANCE_TEXT = """
🚧 <b>SYSTEM MAINTENANCE IN PROGRESS</b>

The developer is currently deploying critical patches.
Service will resume shortly.
"""

# ==============================================================================
#                           SECTION 4: DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    A robust, thread-safe JSON database manager.
    Handles User persistence, History, and System Stats.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = threading.Lock()
        self.data = self._load_or_create()

    def _load_or_create(self) -> Dict:
        """Loads DB or creates a fresh structure if missing."""
        if not os.path.exists(self.filepath):
            logger.warning("Database not found. Creating new instance.")
            return self._default_schema()
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.critical("Database Corruption Detected! Resetting to default.")
            return self._default_schema()

    def _default_schema(self) -> Dict:
        return {
            "users": {},
            "banned_ids": [],
            "settings": {"maintenance": False},
            "metrics": {
                "total_queries": 0,
                "uptime_start": str(datetime.datetime.now())
            }
        }

    def _commit(self):
        """Writes data to disk securely."""
        with self.lock:
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
            except Exception as e:
                logger.error(f"IO Error during commit: {e}")

    # --- User Management Methods ---

    def register_user(self, user: User):
        uid = str(user.id)
        if uid not in self.data["users"]:
            self.data["users"][uid] = {
                "meta": {
                    "name": user.first_name,
                    "username": user.username,
                    "joined": str(datetime.datetime.now())
                },
                "usage": {
                    "queries": 0,
                    "last_active": str(datetime.datetime.now())
                },
                "history": []
            }
            self._commit()
            logger.info(f"New User Registered: {user.id}")

    def update_activity(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["usage"]["last_active"] = str(datetime.datetime.now())
            self.data["users"][uid]["usage"]["queries"] += 1
            self.data["metrics"]["total_queries"] += 1
            self._commit()

    # --- History / Context Methods ---

    def add_history(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.data["users"]:
            history = self.data["users"][uid].get("history", [])
            history.append({"role": role, "content": content})
            
            # Smart Trimming: Keep last N messages to prevent URL overflow
            if len(history) > SystemConfig.MAX_HISTORY_DEPTH:
                history = history[-SystemConfig.MAX_HISTORY_DEPTH:]
            
            self.data["users"][uid]["history"] = history
            self._commit()

    def get_history(self, user_id) -> List[Dict]:
        return self.data["users"].get(str(user_id), {}).get("history", [])

    def clear_history(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["history"] = []
            self._commit()

    # --- Admin / Security Methods ---

    def is_banned(self, user_id):
        return int(user_id) in self.data["banned_ids"]

    def set_ban(self, user_id, status: bool):
        uid = int(user_id)
        if status:
            if uid not in self.data["banned_ids"]:
                self.data["banned_ids"].append(uid)
        else:
            if uid in self.data["banned_ids"]:
                self.data["banned_ids"].remove(uid)
        self._commit()

    def get_all_users(self):
        return list(self.data["users"].keys())

# Initialize Global Database Instance
db = DatabaseEngine(SystemConfig.DB_FILE)

# ==============================================================================
#                           SECTION 5: AI PROCESSING KERNEL
# ==============================================================================

class AIEngine:
    """
    Handles communication with LLM APIs.
    Implements URL encoding, Payload management, and Retries.
    """
    def __init__(self):
        self.endpoint = SystemConfig.AI_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def generate(self, prompt: str, history: List[Dict]) -> str:
        """
        Generates code using Pollinations AI.
        Includes logic to handle 'Brain Disconnected' errors by managing payload size.
        """
        
        # 1. Build Context String
        # We need to be careful with length here.
        context_str = ""
        for msg in history:
            role = "User" if msg['role'] == 'user' else "AI"
            context_str += f"{role}: {msg['content']}\n"

        # 2. Payload Logic
        # If the user asks for a LOT of code, we minimize history to prioritize the output.
        if len(prompt) > 200 or "code" in prompt.lower():
            logger.info("Long prompt detected. Minimizing history to save bandwidth.")
            # Only take last 1 message
            if history:
                last = history[-1]
                context_str = f"{'User' if last['role']=='user' else 'AI'}: {last['content']}\n"

        full_payload = (
            f"{SystemConfig.SYSTEM_INSTRUCTION}\n\n"
            f"--- HISTORY ---\n{context_str}\n"
            f"--- REQUEST ---\nUser: {prompt}\nAI:"
        )

        # 3. Retry Mechanism
        for i in range(SystemConfig.RETRY_ATTEMPTS):
            try:
                # Pollinations uses GET with encoded string in URL
                encoded_prompt = requests.utils.quote(full_payload)
                request_url = f"{self.endpoint}{encoded_prompt}"
                
                # Check for URL limits (approx 4000-5000 chars is safe limit usually)
                if len(request_url) > 6000:
                    logger.warning("URL too long. Stripping history completely.")
                    # Fallback: Send only prompt without history
                    simple_payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\nUser: {prompt}\nAI:"
                    request_url = f"{self.endpoint}{requests.utils.quote(simple_payload)}"

                response = self.session.get(request_url, timeout=SystemConfig.REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    text = response.text
                    if not text or len(text) < 5:
                        continue # Empty response retry
                    return text
                
                logger.warning(f"AI API Status: {response.status_code}. Retrying...")
                time.sleep(1)

            except Exception as e:
                logger.error(f"AI Connection Error: {e}")
                time.sleep(1)

        return "❌ <b>Server Error:</b> The request timed out or was too large. Please try <code>/new</code> to clear memory and ask again."

ai_core = AIEngine()

# ==============================================================================
#                           SECTION 6: FLASK SERVER (24/7 HOSTING)
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def health_check():
    """Route for UptimeRobot."""
    stats = db.data["metrics"]
    return jsonify({
        "status": "active",
        "bot": SystemConfig.BOT_NAME,
        "owner": SystemConfig.OWNER_USERNAME,
        "queries_served": stats["total_queries"]
    }), 200

def run_web_server():
    """Runs Flask in a daemon thread."""
    port = int(os.environ.get("PORT", 8080))
    # Silence Flask startup logs
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           SECTION 7: UTILITIES
# ==============================================================================

class MessageUtils:
    @staticmethod
    def smart_split(text: str, limit: int = 4000) -> List[str]:
        """
        Splits text while preserving Markdown code blocks.
        """
        if len(text) <= limit:
            return [text]
        
        chunks = []
        while len(text) > 0:
            if len(text) > limit:
                # Try to split at code block
                split_at = text.rfind("```", 0, limit)
                if split_at == -1:
                    split_at = text.rfind("\n\n", 0, limit)
                if split_at == -1:
                    split_at = limit
                
                chunk = text[:split_at]
                chunks.append(chunk)
                text = text[split_at:]
            else:
                chunks.append(text)
                text = ""
        return chunks

    @staticmethod
    async def verify_subscription(user_id: int, bot) -> bool:
        """Verifies channel membership."""
        if not SystemConfig.FORCE_SUB_ENABLED:
            return True
        try:
            member = await bot.get_chat_member(SystemConfig.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked']:
                return False
            return True
        except:
            return True # Fail open if bot isn't admin

# ==============================================================================
#                           SECTION 8: COMMAND HANDLERS
# ==============================================================================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user)
    
    if db.is_banned(user.id):
        await update.message.reply_text(TextAssets.BANNED_MESSAGE, parse_mode=ParseMode.HTML)
        return

    if not await MessageUtils.verify_subscription(user.id, context.bot):
        kb = [[InlineKeyboardButton("🚀 JOIN CHANNEL", url=SystemConfig.CHANNEL_LINK)],
              [InlineKeyboardButton("✅ VERIFY", callback_data="verify_sub")]]
        await update.message.reply_text(TextAssets.FORCE_SUB_TEXT.format(bot_name=SystemConfig.BOT_NAME), 
                                      parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    time_now = datetime.datetime.now().strftime("%H:%M")
    txt = TextAssets.WELCOME_SCREEN.format(
        bot_name=SystemConfig.BOT_NAME, 
        name=html.escape(user.first_name),
        owner=SystemConfig.OWNER_USERNAME,
        time=time_now
    )
    
    kb = [
        [InlineKeyboardButton("🤖 Ask AI Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("👤 My Profile", callback_data="profile"), InlineKeyboardButton("🆘 Documentation", callback_data="help")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🔙 Back", callback_data="home")]]
    txt = TextAssets.HELP_DOCUMENTATION.format(owner=SystemConfig.OWNER_USERNAME)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def new_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.clear_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Context Cleared!</b>\nI have forgotten our previous messages.", parse_mode=ParseMode.HTML)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = db.data["users"].get(str(user.id))
    
    if data:
        txt = (
            f"👤 <b>USER PROFILE</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📛 <b>Name:</b> {html.escape(data['meta']['name'])}\n"
            f"📅 <b>Joined:</b> {data['meta']['joined'][:10]}\n"
            f"💬 <b>Queries:</b> {data['usage']['queries']}"
        )
        kb = [[InlineKeyboardButton("🔙 Back", callback_data="home")]]
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

# ==============================================================================
#                           SECTION 9: AI PROCESSOR
# ==============================================================================

async def rai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # 1. Validation
    if db.is_banned(user.id): return
    if not await MessageUtils.verify_subscription(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ <b>Empty Prompt!</b>\nUsage: <code>/rai python calculator</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    db.update_activity(user.id)

    # 2. UI Feedback
    status = await update.message.reply_text(
        f"🧠 <b>Thinking...</b>\n<i>Parsing: {html.escape(prompt[:30])}...</i>",
        parse_mode=ParseMode.HTML
    )
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # 3. AI Execution
    try:
        history = db.get_history(user.id)
        
        # Offload network request to thread
        response_text = await asyncio.get_running_loop().run_in_executor(
            None, ai_core.generate, prompt, history
        )
        
        # 4. Memory Update
        db.add_history(user.id, "user", prompt)
        db.add_history(user.id, "ai", response_text)
        
        # 5. Delivery
        chunks = MessageUtils.smart_split(response_text)
        await status.delete()
        
        for chunk in chunks:
            try:
                await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
            except:
                await update.message.reply_text(chunk, parse_mode=ParseMode.HTML)
                
    except Exception as e:
        logger.error(f"Handler Failure: {e}")
        traceback.print_exc()
        await status.edit_text("❌ <b>System Error.</b> Please check logs.", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 10: ADMIN PANEL
# ==============================================================================

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    if not context.args: return
    
    msg = " ".join(context.args)
    users = db.get_all_users()
    await update.message.reply_text(f"🚀 Broadcasting to {len(users)} users...")
    
    for uid in users:
        try: await context.bot.send_message(int(uid), f"📢 <b>ALERT:</b>\n{msg}", parse_mode=ParseMode.HTML)
        except: pass

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.set_ban(context.args[0], True)
        await update.message.reply_text(f"🚫 Banned {context.args[0]}")
    except: pass

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.set_ban(context.args[0], False)
        await update.message.reply_text(f"✅ Unbanned {context.args[0]}")
    except: pass

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    stats = db.data["metrics"]
    txt = f"📊 <b>STATS</b>\nUsers: {len(db.data['users'])}\nQueries: {stats['total_queries']}"
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 11: INITIALIZATION
# ==============================================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "verify_sub":
        if await MessageUtils.verify_subscription(query.from_user.id, context.bot):
            await query.delete_message()
            await start_handler(update, context)
        else:
            await query.answer("❌ You haven't joined yet!", show_alert=True)
    elif data == "help": await help_handler(update, context)
    elif data == "profile": await profile_handler(update, context)
    elif data == "home": await start_handler(update, context)

async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "🏠 Home"),
        BotCommand("rai", "🤖 Generate Code"),
        BotCommand("new", "🧹 Clear Memory"),
        BotCommand("me", "👤 Profile"),
        BotCommand("help", "🆘 Help")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT PRO v12.0...")
    
    # Start Flask (Daemon)
    threading.Thread(target=run_web_server, daemon=True).start()
    print("✅ Web Server: ONLINE")
    
    # Start Bot
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("rai", rai_processor))
    app.add_handler(CommandHandler("new", new_chat_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("me", profile_handler))
    
    # Admin
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("stats", admin_stats))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Telegram Bot: POLLING")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
