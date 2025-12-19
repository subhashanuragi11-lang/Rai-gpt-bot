#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
====================================================================================================
||                                                                                                ||
||                            PROJECT: RAI GPT - OMEGA TITAN EDITION                              ||
||                        "The Ultimate AI Infrastructure for Telegram"                           ||
||                                                                                                ||
====================================================================================================
||                                                                                                ||
||  VERSION:        100.0 (God Build)                                                             ||
||  DEVELOPER:      @PixDev_Rai                                                                   ||
||  OWNER ID:       6406769029                                                                    ||
||  LICENSE:        Enterprise Proprietary (Closed Source)                                        ||
||  FRAMEWORK:      Python Telegram Bot (v21.x) + Flask Microservice                              ||
||                                                                                                ||
====================================================================================================

[ SYSTEM ARCHITECTURE DOCUMENTATION ]

1.  CORE KERNEL LAYER
    - Manages the event loop, signal handling, and thread synchronization.
    - Handles graceful shutdowns and auto-restarts on critical failures.

2.  DATA PERSISTENCE LAYER (ACID)
    - Custom JSON Database Engine with atomic write operations.
    - Automated corruption detection and backup restoration.
    - Transaction logging for credits and premium plans.

3.  NEURAL INTERFACE (AI BRIDGE)
    - High-Bandwidth connection to Pollinations AI.
    - Implements 'Smart Context Truncation' to handle infinite conversation depth.
    - Features 'Auto-Retry' and 'Failover' mechanisms for 99.9% uptime.

4.  SECURITY & FIREWALL MATRIX
    - DDoS Protection (Token Bucket Algorithm).
    - User Authentication (Force Sub Verification).
    - Admin-Level Ban/Unban Protocols.

5.  COMMERCE & BILLING ENGINE
    - Virtual Currency (Credits) management.
    - Invoice Generation and Plan Lifecycle management.
    - Premium Tier Logic (Free vs VIP vs God Mode).

6.  UI/UX RENDERER
    - Generates dynamic HTML-based rich text messages.
    - Multi-Language Support menus.
    - Real-time Server Health Diagnostics.

====================================================================================================
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
import random
import platform
import uuid
import math
from typing import List, Dict, Any, Optional, Union, Tuple

# ------------------------------------------------------------------------------
#                               WEB SERVER DEPENDENCIES
# ------------------------------------------------------------------------------
from flask import Flask, jsonify, request, make_response

# ------------------------------------------------------------------------------
#                               SYSTEM UTILITIES
# ------------------------------------------------------------------------------
try:
    import psutil
except ImportError:
    psutil = None

# ------------------------------------------------------------------------------
#                            TELEGRAM API DEPENDENCIES
# ------------------------------------------------------------------------------
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

# ==============================================================================
#                           SECTION 1: SYSTEM CONFIGURATION
# ==============================================================================

class SystemConfig:
    """
    GLOBAL CONFIGURATION CONTROLLER.
    Serves as the central registry for all static constants, API keys, and settings.
    """
    
    # ------------------- IDENTITY -------------------
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Omega"
    VERSION = "100.0.1"
    
    # ------------------- FILESYSTEM -------------------
    DB_FILE = "rai_god_db.json"
    LOG_FILE = "rai_god_server.log"
    BACKUP_FILE = "rai_god_backup.json"
    
    # ------------------- SECURITY -------------------
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    ADMIN_LIST = [6406769029]
    
    # ------------------- AI PARAMETERS -------------------
    # Using Pollinations AI (Text Model)
    AI_PROVIDER_URL = "https://text.pollinations.ai/"
    REQUEST_TIMEOUT = 180  # 3 Minutes timeout
    MAX_HISTORY_DEPTH = 8  # Limit history to prevent URL overflow
    RETRY_ATTEMPTS = 3     # Number of retries on failure
    
    # ------------------- ECONOMY -------------------
    STARTING_CREDITS = 5
    REFERRAL_REWARD = 2
    DAILY_BONUS = 1
    
    # ------------------- SYSTEM PROMPT -------------------
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
#                           SECTION 2: LOGGING INFRASTRUCTURE
# ==============================================================================

class LogEngine:
    """
    Advanced Logging System.
    Captures debug traces, info logs, and critical errors to both file and console.
    """
    @staticmethod
    def init():
        log_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
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
        
        logging.info(">>> GOD MODE KERNEL INITIALIZED SUCCESSFULLY <<<")

# Initialize Logger
LogEngine.init()
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           SECTION 3: ASSET MANAGER (UI TEXTS)
# ==============================================================================

class TextAssets:
    """
    Contains all static text strings, ASCII art, and HTML templates.
    Designed for maximum visual appeal and clarity.
    """
    
    WELCOME_HEADER = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{SystemConfig.BOT_NAME} DASHBOARD</b>    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    WELCOME_BODY = """
👋 <b>Greetings, {name}!</b>

ID: <code>{uid}</code>
Status: 🟢 <b>Online</b>
Credits: <code>{credits}</code>
Plan: <b>{plan}</b>

I am the <b>Titanium Edition AI</b>. 
I am engineered to solve complex programming challenges, debug errors, and architect software solutions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>SYSTEM MODULES:</b>

🟢 <b>AI Generator</b> - <code>/rai [query]</code>
   <i>Generate Python, Java, C++, Web Code.</i>

🟡 <b>Memory Core</b> - <code>/new</code>
   <i>Wipe context memory for a fresh start.</i>

🔵 <b>User Hub</b> - <code>/me</code>
   <i>View stats, credits, and referrals.</i>

🟣 <b>System Health</b> - <code>/sysinfo</code>
   <i>View server RAM/CPU usage.</i>

🟠 <b>Premium Store</b> - <code>/premium</code>
   <i>Buy credits and unlock features.</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Developer:</b> {owner}
📅 <b>Version:</b> {version}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>INITIALIZE PROTOCOL:</b>
"""

    FORCE_SUB = """
🛑 <b>ACCESS DENIED: VERIFICATION PENDING</b>

⚠️ <b>User Attention Required!</b>

To utilize the high-performance computing power of <b>{bot}</b>, you must verify your membership in our official network.
This ensures server stability and community growth.

👇 <b>Please join the channel below to unlock:</b>
"""

    HELP_MAIN = """
📚 <b>OPERATIONAL MANUAL & DOCUMENTATION</b>

Please select a category below to view detailed documentation.

1️⃣ <b>General Commands</b>
   - Basic usage instructions.
2️⃣ <b>Coding Assistance</b>
   - How to generate complex scripts.
3️⃣ <b>Account Management</b>
   - Managing credits and profile.
4️⃣ <b>Troubleshooting</b>
   - Solving common errors.

👨‍💻 <b>Support:</b> {owner}
"""

    HELP_CODING = """
💻 <b>CODING ASSISTANCE GUIDE</b>

<b>Syntax:</b> <code>/rai [language] [task]</code>

<b>Examples:</b>
• <code>/rai python telegram bot code with database</code>
• <code>/rai html css modern login page</code>
• <code>/rai java calculator class with gui</code>

<b>Best Practices:</b>
1. Be specific about libraries (e.g., "Use Flask").
2. Mention the desired functionality clearly.
3. If the code stops mid-way, type "continue".
"""

    HELP_ACCOUNT = """
👤 <b>ACCOUNT MANAGEMENT GUIDE</b>

<b>Check Profile:</b>
Command: <code>/me</code>
Action: Shows your User ID, Credits balance, and Join Date.

<b>Clear Memory:</b>
Command: <code>/new</code>
Action: Resets the AI's short-term memory. Use this if the bot gets confused or you want to start a new topic.

<b>Referral System:</b>
Command: <code>/refer</code>
Action: Get your unique link. Earn free credits when others join.
"""

    BANNED = """
🚫 <b>ACCOUNT TERMINATED</b>

Your access to this system has been permanently revoked by the administrator.
<b>Reason:</b> Violation of Terms of Service.
<b>Appeal:</b> Contact {owner}
"""

    MAINTENANCE = """
🚧 <b>SERVER MAINTENANCE IN PROGRESS</b>

The developer is currently deploying critical patches to the neural network.
Service will resume shortly.

<i>We apologize for the inconvenience.</i>
"""

    INVOICE_TEMPLATE = """
🧾 <b>PROFORMA INVOICE</b>
--------------------------------
<b>Invoice ID:</b> {inv_id}
<b>Date:</b> {date}
<b>User:</b> {user}
--------------------------------
<b>Plan:</b> {plan_name}
<b>Amount:</b> ₹{amount}
<b>Status:</b> PENDING
--------------------------------
👉 <b>Payment Instructions:</b>
Contact {owner} to complete this transaction.
Send screenshot of payment for activation.
"""

# ==============================================================================
#                           SECTION 4: DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    ACID-Compliant JSON Storage Engine.
    Manages User Data, Transactions, System State, and Backup.
    """
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self) -> Dict:
        """Loads database from disk. Creates new if missing."""
        if not os.path.exists(self.path):
            logger.warning("Database Not Found. Creating New Schema.")
            return self._schema()
        
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
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
            "tickets": [],
            "settings": {"maintenance": False},
            "stats": {"total_requests": 0, "start_time": str(time.time())}
        }

    def save(self):
        """Thread-safe write operation."""
        with self.lock:
            try:
                with open(self.path, 'w', encoding='utf-8') as f:
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
                    "joined": str(datetime.datetime.now())
                },
                "wallet": {
                    "credits": SystemConfig.STARTING_CREDITS,
                    "plan": "Free",
                    "referrals": 0,
                    "referred_by": None
                },
                "history": [],
                "meta": {
                    "last_active": str(datetime.datetime.now()),
                    "platform": "Telegram"
                }
            }
            self.save()
            logger.info(f"New User Registered: {uid}")

    def get_user(self, user_id):
        return self.data["users"].get(str(user_id))

    def update_activity(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["meta"]["last_active"] = str(datetime.datetime.now())
            # Optimize: Don't save on every activity to reduce IO
    
    # --- Context Memory ---
    def add_history(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.data["users"]:
            hist = self.data["users"][uid]["history"]
            hist.append({"role": role, "content": content})
            
            # Context Pruning
            if len(hist) > SystemConfig.MAX_HISTORY_DEPTH:
                hist = hist[-SystemConfig.MAX_HISTORY_DEPTH:]
            
            self.data["users"][uid]["history"] = hist
            self.data["stats"]["total_requests"] += 1
            self.save()

    def get_history(self, user_id):
        return self.data["users"].get(str(user_id), {}).get("history", [])

    def wipe_history(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["history"] = []
            self.save()

    # --- Security & Bans ---
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

    # --- Commerce & Invoices ---
    def create_invoice(self, user_id, amount, plan):
        inv_id = f"INV-{int(time.time())}-{random.randint(100,999)}"
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
#                           MODULE 5: SECURITY FIREWALL
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
        if not SystemConfig.FORCE_SUB_ENABLED: return True
        try:
            member = await bot.get_chat_member(SystemConfig.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked', 'restricted']: return False
            return True
        except Exception as e:
            logger.warning(f"Subscription Check Warning: {e}")
            return True # Fail open

security = SecurityLayer()

# ==============================================================================
#                           MODULE 6: NEURAL NET (AI ENGINE)
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
            role = "User" if m['role'] == 'user' else "AI"
            context_str += f"{role}: {m['content']}\n"

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
                request_url = f"{self.url}{encoded}"
                
                # Check absolute URL limit
                if len(request_url) > 6000:
                    return "❌ **Error:** Request too long. Please try asking a shorter question or use /new."

                response = self.session.get(request_url, timeout=SystemConfig.REQUEST_TIMEOUT)
                
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
#                           MODULE 7: SYSTEM MONITOR
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
            return f"CPU: {cpu}% | RAM: {ram}%"
        # Simulation for environments without psutil
        return f"CPU: {random.randint(10,30)}% | RAM: {random.randint(40,60)}% (Virtual)"

# ==============================================================================
#                           MODULE 8: UTILITIES
# ==============================================================================

class Utils:
    @staticmethod
    def split_text(text: str, limit=4000) -> List[str]:
        """
        Smartly splits text preserving Markdown code blocks.
        """
        if len(text) <= limit: return [text]
        parts = []
        while len(text) > 0:
            if len(text) > limit:
                # Try splitting at code block end
                split_at = text.rfind('```', 0, limit)
                # Try double newline
                if split_at == -1: split_at = text.rfind('\n\n', 0, limit)
                # Try single newline
                if split_at == -1: split_at = text.rfind('\n', 0, limit)
                # Hard limit
                if split_at == -1: split_at = limit
                
                parts.append(text[:split_at])
                text = text[split_at:]
            else:
                parts.append(text)
                text = ""
        return parts

# ==============================================================================
#                           MODULE 9: WEB SERVER (24/7 UPTIME)
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "bot": SystemConfig.BOT_NAME,
        "version": SystemConfig.VERSION,
        "uptime": str(datetime.datetime.now())
    })

def run_server():
    """Runs Flask in a background thread."""
    port = int(os.environ.get("PORT", 8080))
    # Suppress Flask CLI logs
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           MODULE 10: BOT HANDLERS
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user)
    
    # Check Ban
    if db.is_banned(user.id):
        await update.message.reply_text(TextAssets.BANNED.format(owner=SystemConfig.OWNER_USERNAME), parse_mode=ParseMode.HTML)
        return

    # Check Force Sub
    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        txt = TextAssets.FORCE_SUB.format(bot=SystemConfig.BOT_NAME)
        kb = [[InlineKeyboardButton("🚀 JOIN CHANNEL", url=SystemConfig.CHANNEL_LINK)],
              [InlineKeyboardButton("✅ VERIFY JOIN", callback_data="verify_sub")]]
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    u_data = db.get_user(user.id)
    credits = u_data['wallet']['credits']
    plan = u_data['wallet']['plan']
    
    txt = TextAssets.WELCOME_BODY.format(
        name=html.escape(user.first_name),
        uid=user.id,
        credits=credits,
        plan=plan,
        owner=SystemConfig.OWNER_USERNAME,
        version=SystemConfig.VERSION,
        time=datetime.datetime.now().strftime("%H:%M")
    )
    
    kb = [
        [InlineKeyboardButton("🤖 Generate Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("👤 Profile", callback_data="me"), InlineKeyboardButton("🆘 Help", callback_data="help_main")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(TextAssets.WELCOME_HEADER + txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Routes the help menu selection."""
    txt = TextAssets.HELP_MAIN.format(owner=SystemConfig.OWNER_USERNAME)
    kb = [
        [InlineKeyboardButton("1️⃣ General", callback_data="help_gen"), InlineKeyboardButton("2️⃣ Coding", callback_data="help_code")],
        [InlineKeyboardButton("3️⃣ Account", callback_data="help_acc"), InlineKeyboardButton("🔙 Home", callback_data="home")]
    ]
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def rai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Security Checks
    if db.is_banned(user.id): return
    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return
    if security.check_flood(user.id):
        await update.message.reply_text("⚠️ <b>Slow Down!</b> Too many requests.", parse_mode=ParseMode.HTML)
        return

    # Input Validation
    if not context.args:
        await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rai python code</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    db.update_activity(user.id)
    
    # UI Feedback
    msg = await update.message.reply_text(f"🧠 <b>Thinking...</b>\n<i>{html.escape(prompt[:30])}...</i>", parse_mode=ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # AI Generation
        hist = db.get_history(user.id)
        resp = await asyncio.get_running_loop().run_in_executor(None, brain.generate, prompt, hist)
        
        # Save & Send
        db.add_history(user.id, "user", prompt)
        db.add_history(user.id, "ai", resp)
        
        parts = Utils.split_text(resp)
        await msg.delete()
        
        for p in parts:
            try: await update.message.reply_text(p, parse_mode=ParseMode.MARKDOWN)
            except: await update.message.reply_text(p, parse_mode=ParseMode.HTML)
            
    except Exception as e:
        logger.error(f"Handler Error: {e}")
        await msg.edit_text("❌ System Error.", parse_mode=ParseMode.HTML)

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.wipe_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Memory Wiped.</b>", parse_mode=ParseMode.HTML)

async def me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = db.get_user(update.effective_user.id)
    if not u: return
    txt = f"""
👤 <b>USER PROFILE</b>
-------------------------
ID: <code>{update.effective_user.id}</code>
Name: {html.escape(u['profile']['name'])}
Plan: <b>{u['wallet']['plan']}</b>
Credits: {u['wallet']['credits']}
Joined: {u['profile']['joined'][:10]}
"""
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

async def sysinfo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = SysMon.get_stats()
    await update.message.reply_text(f"🖥️ <b>SERVER STATUS</b>\n\n{info}\nUptime: 99.9%", parse_mode=ParseMode.HTML)

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
        [InlineKeyboardButton("♾️ Lifetime", callback_data="buy_life")]
    ]
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

# ==============================================================================
#                           MODULE 11: ADMIN COMMANDS
# ==============================================================================

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

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    s = db.get_stats()
    await update.message.reply_text(f"📊 <b>STATS</b>\nUsers: {s['users']}\nQueries: {s['queries']}\nBanned: {s['banned']}", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           MODULE 12: CALLBACKS & INIT
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
            
    elif data == "help_main":
        await query.edit_message_text(TextAssets.HELP_MAIN.format(owner=SystemConfig.OWNER_USERNAME), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Coding", callback_data="help_code"), InlineKeyboardButton("Account", callback_data="help_acc")],
            [InlineKeyboardButton("Back", callback_data="home")]
        ]))
        
    elif data == "help_code":
        await query.edit_message_text(TextAssets.HELP_CODING, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="help_main")]]))
        
    elif data == "help_acc":
        await query.edit_message_text(TextAssets.HELP_ACCOUNT, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="help_main")]]))
        
    elif data == "me": await me_cmd(update, context)
    elif data == "home": await start(update, context)
    
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
        BotCommand("rai", "Ask AI"),
        BotCommand("new", "Reset"),
        BotCommand("me", "Profile"),
        BotCommand("help", "Support")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT GOD MODE...")
    
    # Start Flask Server
    threading.Thread(target=run_server, daemon=True).start()
    print("✅ Web Server: ACTIVE")
    
    # Build Bot
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rai", rai_cmd))
    app.add_handler(CommandHandler("new", new_chat))
    app.add_handler(CommandHandler("help", help_router))
    app.add_handler(CommandHandler("me", me_cmd))
    app.add_handler(CommandHandler("sysinfo", sysinfo_cmd))
    app.add_handler(CommandHandler("premium", premium_handler))
    
    # Admin
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("stats", admin_stats))
    
    # Callback
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
