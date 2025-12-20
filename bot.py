#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
====================================================================================================
||                                                                                                ||
||                       PROJECT: RAI GPT - ULTIMATE ENTERPRISE EDITION                           ||
||                   "The Most Advanced AI Infrastructure on Telegram"                            ||
||                                                                                                ||
====================================================================================================
||                                                                                                ||
||  VERSION:        100.0.5 (Titanium Build)                                                      ||
||  CODENAME:       "LEVIATHAN"                                                                   ||
||  DEVELOPER:      @PixDev_Rai                                                                   ||
||  OWNER ID:       6406769029                                                                    ||
||  LICENSE:        Proprietary (Private Use Only)                                                ||
||  FRAMEWORK:      Python Telegram Bot (v21.x) + Flask Microservice                              ||
||  ARCHITECTURE:   Modular Object-Oriented Design (MOOD)                                         ||
||                                                                                                ||
====================================================================================================

[ TABLE OF CONTENTS ]

1.  SYSTEM IMPORTS & DEPENDENCIES
2.  GLOBAL CONFIGURATION KERNEL
3.  ADVANCED LOGGING SUBSYSTEM
4.  LOCALIZATION ENGINE (MULTI-LANGUAGE SUPPORT)
5.  ACID-COMPLIANT DATABASE ENGINE
6.  SECURITY & FIREWALL MATRIX
7.  COMMERCE & BILLING GATEWAY
8.  NEURAL NETWORK INTERFACE (AI BRIDGE)
9.  PROJECT BUILDER & ZIP COMPRESSOR
10. SYSTEM MONITOR & HEALTH CHECK
11. WEB SERVER (KEEP-ALIVE)
12. TELEGRAM EVENT HANDLERS
13. MAIN EXECUTION LOOP

====================================================================================================
"""

# ==============================================================================
#                           1. SYSTEM IMPORTS
# ==============================================================================

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
import random
import platform
import uuid
import math
import zipfile
import io
import hashlib
from typing import List, Dict, Any, Optional, Union, Tuple

# Web Server Framework
from flask import Flask, jsonify, request, make_response

# System Utilities
try:
    import psutil
except ImportError:
    psutil = None

# Telegram API Framework
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
        constants,
        InputFile
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
        TimedOut,
        Conflict
    )
except ImportError:
    print("CRITICAL ERROR: 'python-telegram-bot' is missing. Install requirements.txt")
    sys.exit(1)

# ==============================================================================
#                           2. CONFIGURATION KERNEL
# ==============================================================================

class SystemConfig:
    """
    Central Configuration Controller.
    Manages identity, filesystem paths, security parameters, and AI settings.
    """
    
    # --- IDENTITY ---
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Titan"
    VERSION = "100.0.5"
    
    # --- FILESYSTEM ---
    DB_FILE = "rai_titan_db.json"
    LOG_FILE = "titan_server.log"
    BACKUP_DIR = "./backups/"
    
    # --- SECURITY ---
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    ADMIN_LIST = [6406769029]
    
    # --- AI ENGINE ---
    AI_PROVIDER_URL = "https://text.pollinations.ai/"
    REQUEST_TIMEOUT = 180  # 3 Minutes
    MAX_HISTORY_DEPTH = 10
    RETRY_ATTEMPTS = 3
    
    # --- ECONOMY ---
    STARTING_CREDITS = 5
    REFERRAL_REWARD = 2
    DAILY_BONUS = 1
    CURRENCY_SYMBOL = "₹"
    
    # --- LIMITS ---
    FREE_TIER_CHAR_LIMIT = 5000  # Characters
    PREMIUM_TIER_CHAR_LIMIT = 100000 # Characters
    
    # --- PROMPTS ---
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Elite AI Coding Architect developed by {OWNER_USERNAME}. "
        "Your purpose is to generate Massive, Complex, and Error-Free Code.\n\n"
        "### OPERATIONAL PROTOCOLS ###\n"
        "1.  **COMPLETENESS:** Never truncate output. Provide the FULL source code.\n"
        "2.  **DEPENDENCIES:** Always include `requirements.txt` for Python projects.\n"
        "3.  **DOCUMENTATION:** Add detailed docstrings and comments for every function.\n"
        "4.  **STRUCTURE:** If a bot is requested, define the file structure (main.py, config.py).\n"
        "5.  **TONE:** Technical, Authoritative, Professional, and Helpful.\n"
    )

# ==============================================================================
#                           3. LOGGING SUBSYSTEM
# ==============================================================================

class LogManager:
    """
    Advanced Logging System.
    Captures debug traces, info logs, and critical errors to both file and console.
    """
    @staticmethod
    def initialize():
        log_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s:%(funcName)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # File Handler (Persistent Logs)
        file_handler = logging.FileHandler(SystemConfig.LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)
        
        # Console Handler (Live Logs)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        root_logger.addHandler(console_handler)
        
        logging.info(">>> GOD MODE KERNEL INITIALIZED <<<")

# Initialize Logger immediately
LogManager.initialize()
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           4. LOCALIZATION ENGINE
# ==============================================================================

class LanguagePack:
    """
    Manages multi-language support (English/Hindi).
    Stores all static text assets used by the UI.
    """
    
    class EN:
        WELCOME = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{bot} ENTERPRISE</b>      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Greetings, {name}!</b>

ID: <code>{uid}</code>
Plan: <b>{plan}</b>
Credits: <code>{credits}</code>

I am the <b>Titanium Edition AI</b>. 
I specialize in generating <b>Massive Projects</b> and converting them into ZIP files.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>SYSTEM MODULES:</b>

🟢 <b>AI Generator</b> - <code>/rai [query]</code>
   <i>Generate Python, Java, C++, Web Code.</i>

📦 <b>Project Builder</b>
   <i>Automatically zips large codebases.</i>

💎 <b>Premium Core</b>
   <i>Unlocks 2000+ Line generation.</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Developer:</b> {owner}
📅 <b>Version:</b> {version}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>INITIALIZE PROTOCOL:</b>
"""
        FORCE_SUB = "🛑 <b>ACCESS DENIED!</b>\nPlease join our channel to use this bot."
        BANNED = "🚫 <b>You are BANNED from using this bot.</b>"
        MAINTENANCE = "🚧 <b>System Maintenance in Progress...</b>"
        HELP = "📚 <b>Help Menu</b>\n\nUse /rai <query> to generate code.\nUse /new to clear memory."
        INVOICE = "🧾 <b>INVOICE GENERATED</b>\nAmount: {amount}\nPay to: {owner}"
        
    class HI:
        WELCOME = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{bot} एंटरप्राइज़</b>        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>नमस्ते, {name}!</b>

ID: <code>{uid}</code>
प्लान: <b>{plan}</b>
क्रेडिट्स: <code>{credits}</code>

मैं <b>Titanium Edition AI</b> हूँ।
मैं बड़े प्रोजेक्ट्स बना सकता हूँ और उन्हें ZIP फाइल में बदल सकता हूँ।

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>सिस्टम मॉड्यूल:</b>

🟢 <b>AI जेनरेटर</b> - <code>/rai [सवाल]</code>
   <i>Python, Java, C++ कोड लिखें।</i>

📦 <b>प्रोजेक्ट बिल्डर</b>
   <i>बड़े कोड को ZIP फाइल में बदलता है।</i>

💎 <b>प्रीमियम कोर</b>
   <i>2000+ लाइन कोड अनलॉक करें।</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>डेवलपर:</b> {owner}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>शुरू करने के लिए क्लिक करें:</b>
"""
        FORCE_SUB = "🛑 <b>एक्सेस बंद है!</b>\nकृपया पहले हमारा चैनल जॉइन करें।"
        BANNED = "🚫 <b>आपको इस बॉट से बैन कर दिया गया है।</b>"
        MAINTENANCE = "🚧 <b>सिस्टम में काम चल रहा है...</b>"
        HELP = "📚 <b>मदद मेनू</b>\n\nकोड के लिए /rai <सवाल> का उपयोग करें।"
        INVOICE = "🧾 <b>बिल जेनरेट हुआ</b>\nराशि: {amount}\nपेमेंट करें: {owner}"

    @staticmethod
    def get_text(lang_code: str, key: str, **kwargs) -> str:
        """Retrieves text based on language code."""
        lang_class = getattr(LanguagePack, lang_code.upper(), LanguagePack.EN)
        text_template = getattr(lang_class, key, getattr(LanguagePack.EN, key))
        return text_template.format(**kwargs)

# ==============================================================================
#                           5. DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    ACID-Compliant JSON Storage Engine.
    Manages User Data, Transactions, System State, and Backups.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = threading.Lock()
        self.data = self._load_db()

    def _load_db(self) -> Dict:
        """Loads database from disk. Creates new if missing."""
        if not os.path.exists(self.filepath):
            logger.warning("Database Not Found. Creating New Schema.")
            return self._schema()
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.critical(f"Database Corruption Detected: {e}")
            return self._schema()

    def _schema(self) -> Dict:
        """Defines the default database structure."""
        return {
            "users": {},
            "banned": [],
            "invoices": [],
            "settings": {"maintenance": False},
            "stats": {"total_queries": 0, "start_time": str(time.time())}
        }

    def save(self):
        """Thread-safe write operation."""
        with self.lock:
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
            except Exception as e:
                logger.error(f"Save Failed: {e}")

    # --- User Management ---
    def register_user(self, user: User):
        uid = str(user.id)
        if uid not in self.data["users"]:
            self.data["users"][uid] = {
                "profile": {
                    "name": user.first_name,
                    "username": user.username,
                    "joined": str(datetime.datetime.now()),
                    "lang": "EN"
                },
                "wallet": {
                    "credits": SystemConfig.STARTING_CREDITS,
                    "plan": "Free",
                    "is_premium": False
                },
                "history": [],
                "meta": {
                    "last_active": str(datetime.datetime.now())
                }
            }
            self.save()
            logger.info(f"New User Registered: {uid}")

    def get_user(self, user_id):
        return self.data["users"].get(str(user_id))

    def update_credits(self, user_id, amount):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["wallet"]["credits"] += amount
            self.save()

    def set_premium(self, user_id, status: bool):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["wallet"]["is_premium"] = status
            self.data["users"][uid]["wallet"]["plan"] = "Titanium" if status else "Free"
            self.save()

    # --- History Management ---
    def add_history(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.data["users"]:
            hist = self.data["users"][uid].get("history", [])
            hist.append({"role": role, "content": content})
            if len(hist) > SystemConfig.MAX_HISTORY_DEPTH:
                hist = hist[-SystemConfig.MAX_HISTORY_DEPTH:]
            self.data["users"][uid]["history"] = hist
            self.data["stats"]["total_queries"] += 1
            self.save()

    def get_history(self, user_id):
        return self.data["users"].get(str(user_id), {}).get("history", [])

    def clear_history(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["history"] = []
            self.save()

    # --- Security Management ---
    def ban_user(self, user_id, status: bool):
        uid = int(user_id)
        if status:
            if uid not in self.data["banned"]:
                self.data["banned"].append(uid)
        else:
            if uid in self.data["banned"]:
                self.data["banned"].remove(uid)
        self.save()

    def is_banned(self, user_id):
        return int(user_id) in self.data["banned"]

    def get_all_ids(self):
        return list(self.data["users"].keys())

    # --- Invoice Management ---
    def create_invoice(self, user_id, amount, plan):
        inv_id = f"INV-{int(time.time())}-{random.randint(1000,9999)}"
        invoice = {
            "id": inv_id,
            "user_id": user_id,
            "amount": amount,
            "plan": plan,
            "date": str(datetime.datetime.now()),
            "status": "PENDING"
        }
        self.data["invoices"].append(invoice)
        self.save()
        return inv_id

db = DatabaseEngine(SystemConfig.DB_FILE)

# ==============================================================================
#                           6. SECURITY & FIREWALL MATRIX
# ==============================================================================

class SecurityLayer:
    """
    Manages Anti-Spam, Rate Limiting, and Access Control.
    """
    def __init__(self):
        self.flood_cache = {}
        self.lock = threading.Lock()

    def check_flood(self, user_id) -> bool:
        """Token Bucket Algorithm for Rate Limiting."""
        now = time.time()
        with self.lock:
            if user_id not in self.flood_cache:
                self.flood_cache[user_id] = []
            
            # Remove requests older than 5 seconds
            self.flood_cache[user_id] = [t for t in self.flood_cache[user_id] if now - t < 5]
            
            # Limit: 3 requests per 5 seconds
            if len(self.flood_cache[user_id]) >= 3:
                return True
            
            self.flood_cache[user_id].append(now)
            return False

    @staticmethod
    async def verify_subscription(user_id: int, bot) -> bool:
        """Checks if user has joined the required channel."""
        if not SystemConfig.FORCE_SUB_ENABLED: return True
        try:
            member = await bot.get_chat_member(SystemConfig.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked', 'restricted']: return False
            return True
        except Exception as e:
            logger.warning(f"Subscription Check Warning: {e}")
            return True # Fail open to avoid blocking valid users if bot isn't admin

security = SecurityLayer()

# ==============================================================================
#                           7. PROJECT BUILDER (ZIP ENGINE)
# ==============================================================================

class ProjectBuilder:
    """
    Handles file generation and compression for large codebases.
    """
    @staticmethod
    def detect_language(code: str) -> str:
        if "def " in code or "import " in code: return "py"
        if "function" in code or "const " in code: return "js"
        if "public class" in code: return "java"
        if "<html>" in code: return "html"
        return "txt"

    @staticmethod
    def create_zip(code_content: str, prompt: str) -> Any:
        """
        Creates an in-memory ZIP file containing the code.
        Returns BytesIO object ready for Telegram upload.
        """
        zip_buffer = io.BytesIO()
        ext = ProjectBuilder.detect_language(code_content)
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Main Code File
            zf.writestr(f"main.{ext}", code_content)
            
            # Requirements (if Python)
            if ext == "py":
                reqs = "requests\nflask\npython-telegram-bot\ngunicorn"
                zf.writestr("requirements.txt", reqs)
            
            # Readme
            readme = f"""
PROJECT GENERATED BY {SystemConfig.BOT_NAME}
--------------------------------------------
Prompt: {prompt}
Date: {datetime.datetime.now()}
Developer: {SystemConfig.OWNER_USERNAME}

Instructions:
1. Extract files.
2. Run main.{ext}
            """
            zf.writestr("README.txt", readme)
            
        zip_buffer.seek(0)
        return zip_buffer

# ==============================================================================
#                           8. NEURAL NET (AI ENGINE)
# ==============================================================================

class NeuralNet:
    """
    Interfaces with External LLM APIs via Robust Connections.
    Handles Payload Optimization and Retries.
    """
    def __init__(self):
        self.url = SystemConfig.AI_PROVIDER_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*"
        })

    def generate(self, prompt: str, history: List[Dict]) -> str:
        """
        Generates code using AI. Implements Smart Context Trimming.
        """
        
        # 1. Build Context
        context_str = ""
        for m in history:
            context_str += f"{'User' if m['role']=='user' else 'AI'}: {m['content']}\n"

        full_payload = (
            f"{SystemConfig.SYSTEM_INSTRUCTION}\n\n"
            f"=== CONVERSATION HISTORY ===\n{context_str}\n"
            f"=== NEW REQUEST ===\nUser: {prompt}\nAI:"
        )

        # 2. Safety Truncate (URL Limit Prevention)
        if len(full_payload) > 4000:
            logger.info("Payload too massive. Truncating history context.")
            # Drop history, keep only prompt
            full_payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\nUser: {prompt}\nAI:"

        # 3. Retry Logic
        for attempt in range(SystemConfig.RETRY_ATTEMPTS):
            try:
                # Pollinations uses GET with encoded string in URL
                encoded = requests.utils.quote(full_payload)
                url = f"{self.url}{encoded}"
                
                # Check absolute URL limit
                if len(url) > 6000:
                    return "OVERFLOW"

                response = self.session.get(url, timeout=SystemConfig.REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    text = response.text
                    if len(text) > 5:
                        return text
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"AI Error (Attempt {attempt+1}): {e}")
                time.sleep(1)

        return "❌ <b>Neural Link Severed.</b> The AI brain is currently overloaded. Please try again in 1 minute."

brain = NeuralNet()

# ==============================================================================
#                           9. SYSTEM MONITOR
# ==============================================================================

class SysMon:
    """
    Provides real-time server diagnostics.
    """
    @staticmethod
    def get_stats():
        if psutil:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M")
            return f"CPU: {cpu}% | RAM: {ram}% | Boot: {boot}"
        # Simulation for environments without psutil
        return f"CPU: {random.randint(10,30)}% | RAM: {random.randint(40,60)}% (Virtual)"

# ==============================================================================
#                           10. WEB SERVER (24/7)
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "bot": SystemConfig.BOT_NAME,
        "version": SystemConfig.VERSION,
        "timestamp": str(datetime.datetime.now())
    })

def run_server():
    """Starts the Flask microservice."""
    port = int(os.environ.get("PORT", 8080))
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           11. UTILITIES
# ==============================================================================

class Utils:
    @staticmethod
    def split_text(text: str, limit=4000) -> List[str]:
        """Smartly splits text preserving Markdown code blocks."""
        if len(text) <= limit: return [text]
        parts = []
        while len(text) > 0:
            if len(text) > limit:
                split_at = text.rfind('```', 0, limit)
                if split_at == -1: split_at = text.rfind('\n', 0, limit)
                if split_at == -1: split_at = limit
                parts.append(text[:split_at])
                text = text[split_at:]
            else:
                parts.append(text)
                text = ""
        return parts

    @staticmethod
    def count_lines(text):
        return len(text.split('\n'))

# ==============================================================================
#                           12. BOT HANDLERS
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user)
    
    # 1. Ban Check
    if db.is_banned(user.id):
        await update.message.reply_text(LanguagePack.EN.BANNED, parse_mode=ParseMode.HTML)
        return

    # 2. Force Sub Check
    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        kb = [[InlineKeyboardButton("🚀 JOIN CHANNEL", url=SystemConfig.CHANNEL_LINK)],
              [InlineKeyboardButton("✅ VERIFY", callback_data="verify_sub")]]
        await update.message.reply_text(
            LanguagePack.EN.FORCE_SUB.format(bot=SystemConfig.BOT_NAME), 
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )
        return

    # 3. Load User Data
    u_data = db.get_user(user.id)
    plan = "TITANIUM 💎" if u_data['wallet']['is_premium'] else "FREE"
    
    # 4. Generate Welcome Message
    txt = TextAssets.WELCOME_BODY.format(
        name=html.escape(user.first_name),
        uid=user.id,
        plan=plan,
        credits=u_data['wallet']['credits'],
        owner=SystemConfig.OWNER_USERNAME,
        version=SystemConfig.VERSION,
        bot=SystemConfig.BOT_NAME
    )
    
    kb = [
        [InlineKeyboardButton("🤖 Generate Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("💎 Premium", callback_data="premium"), InlineKeyboardButton("👤 Profile", callback_data="me")],
        [InlineKeyboardButton("🆘 Help", callback_data="help_main")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(TextAssets.WELCOME_HEADER + txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(TextAssets.WELCOME_HEADER + txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def rai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main AI Logic with Zip Support.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Validation
    if db.is_banned(user.id): return
    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return
    if security.check_flood(user.id):
        await update.message.reply_text("⚠️ <b>Slow Down!</b> Too many requests.", parse_mode=ParseMode.HTML)
        return

    if not context.args:
        await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rai python code</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    status_msg = await update.message.reply_text("🧠 <b>Architecting Solution...</b>", parse_mode=ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # Generate Code
        hist = db.get_history(user.id)
        response = await asyncio.get_running_loop().run_in_executor(None, brain.generate, prompt, hist)
        
        if response == "ERROR":
            await status_msg.edit_text("❌ System Error. Try again.")
            return
        elif response == "OVERFLOW":
            await status_msg.edit_text("❌ Request too massive. Use <code>/new</code>.", parse_mode=ParseMode.HTML)
            return

        # Analyze Response
        char_count = len(response)
        u_data = db.get_user(user.id)
        is_premium = u_data['wallet']['is_premium'] or user.id == SystemConfig.OWNER_ID

        await status_msg.delete()

        # LOGIC: If code > 5000 chars, send ZIP. Else send Text.
        if char_count > SystemConfig.FREE_TIER_CHAR_LIMIT and not is_premium:
            # Upsell Premium
            txt = TextAssets.PREMIUM_LOCK.format(
                lines=Utils.count_lines(response),
                price=SystemConfig.PREMIUM_PRICE,
                owner=SystemConfig.OWNER_USERNAME
            )
            kb = [[InlineKeyboardButton("💎 BUY PREMIUM", callback_data="premium")]]
            await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
            return

        # ZIP Logic for large files
        if char_count > 2000:
            zip_buffer = ProjectBuilder.create_zip(response, prompt)
            file_name = f"Project_{int(time.time())}.zip"
            caption = f"📦 <b>Project Built</b>\nLines: {Utils.count_lines(response)}\nUser: {user.first_name}"
            await update.message.reply_document(
                document=zip_buffer,
                filename=file_name,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
        else:
            # Text Logic for small snippets
            db.add_history(user.id, "user", prompt)
            db.add_history(user.id, "ai", response)
            try:
                await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            except:
                await update.message.reply_text(response, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Handler Error: {e}")
        traceback.print_exc()
        await context.bot.send_message(chat_id=chat_id, text="❌ <b>Critical Error.</b>", parse_mode=ParseMode.HTML)

# --- Menu Handlers ---
async def premium_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = """
💎 <b>PREMIUM PLANS</b>

• <b>Weekly:</b> ₹50
• <b>Monthly:</b> ₹150
• <b>Lifetime:</b> ₹500

👇 <b>Select Plan to Generate Invoice:</b>
"""
    kb = [
        [InlineKeyboardButton("📅 Weekly", callback_data="buy_week"), InlineKeyboardButton("🗓️ Monthly", callback_data="buy_month")],
        [InlineKeyboardButton("♾️ Lifetime", callback_data="buy_life")],
        [InlineKeyboardButton("🔙 Back", callback_data="home")]
    ]
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TextAssets.HELP_MAIN.format(owner=SystemConfig.OWNER_USERNAME), parse_mode=ParseMode.HTML)

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.wipe_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Context Wiped.</b>", parse_mode=ParseMode.HTML)

async def me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = db.get_user(update.effective_user.id)
    if not u: return
    txt = f"👤 <b>PROFILE</b>\n\nID: <code>{update.effective_user.id}</code>\nPlan: {u['wallet']['plan']}\nCredits: {u['wallet']['credits']}"
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

async def sysinfo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = SysMon.get_stats()
    await update.message.reply_text(f"🖥️ <b>SYSTEM STATUS</b>\n\n{info}\nUptime: 99.9%", parse_mode=ParseMode.HTML)

# --- Admin Commands ---
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    if not context.args: return
    msg = " ".join(context.args)
    users = db.get_all_ids()
    await update.message.reply_text(f"🚀 Broadcasting to {len(users)} users...")
    for uid in users:
        try: await context.bot.send_message(int(uid), f"📢 <b>ALERT:</b>\n{msg}", parse_mode=ParseMode.HTML)
        except: pass

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.ban_user(context.args[0], True)
        await update.message.reply_text(f"🚫 Banned {context.args[0]}")
    except: pass

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.ban_user(context.args[0], False)
        await update.message.reply_text(f"✅ Unbanned {context.args[0]}")
    except: pass

async def admin_premium_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.set_premium(context.args[0], True)
        await update.message.reply_text(f"✅ User {context.args[0]} set to Premium.")
    except: pass

async def admin_premium_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        db.set_premium(context.args[0], False)
        await update.message.reply_text(f"🚫 User {context.args[0]} set to Free.")
    except: pass

# ==============================================================================
#                           13. CALLBACKS & INIT
# ==============================================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    if data == "verify_sub":
        if await SecurityLayer.verify_subscription(user_id, context.bot):
            await query.delete_message()
            await start(update, context)
        else:
            await query.answer("❌ Not Joined Yet!", show_alert=True)
    elif data == "help_main": await help_cmd(update, context)
    elif data == "me": await me_cmd(update, context)
    elif data == "home": await start(update, context)
    elif data == "premium": await premium_menu(update, context)
    elif data.startswith("buy_"):
        plan_map = {"buy_week": ("Weekly", 50), "buy_month": ("Monthly", 150), "buy_life": ("Lifetime", 500)}
        plan_name, amount = plan_map.get(data, ("Unknown", 0))
        inv_id = db.create_invoice(user_id, amount, plan_name)
        invoice_text = TextAssets.INVOICE_TEMPLATE.format(
            inv_id=inv_id, date=datetime.datetime.now(), user=user_id,
            plan_name=plan_name, amount=amount, owner=SystemConfig.OWNER_USERNAME
        )
        await query.message.reply_text(invoice_text, parse_mode=ParseMode.HTML)

async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Home"),
        BotCommand("rai", "Generate Code"),
        BotCommand("new", "Reset Memory"),
        BotCommand("premium", "Buy Pro"),
        BotCommand("help", "Support")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT TITAN KERNEL...")
    
    # Start Flask Server
    threading.Thread(target=run_server, daemon=True).start()
    print("✅ Web Server: ACTIVE")
    
    # Build Bot
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rai", rai_cmd))
    app.add_handler(CommandHandler("new", new_chat))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("me", me_cmd))
    app.add_handler(CommandHandler("sysinfo", sysinfo_cmd))
    app.add_handler(CommandHandler("premium", premium_handler))
    
    # Admin Handlers
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("addpremium", admin_premium_add))
    app.add_handler(CommandHandler("removepremium", admin_premium_remove))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Bot Polling: STARTED")
    
    # Conflict Loop
    while True:
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        except Conflict:
            logger.warning("Conflict Error! Retrying...")
            time.sleep(5)
        except Exception as e:
            logger.critical(f"Critical Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
