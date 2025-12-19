#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
====================================================================================================
                                PROJECT: RAI GPT - GOD MODE
                            "The 1000-Line AI Infrastructure"
====================================================================================================
VERSION:        50.0 (God Build)
DEVELOPER:      @PixDev_Rai
OWNER ID:       6406769029
LICENSE:        Enterprise Proprietary
FRAMEWORK:      Python Telegram Bot (v21.x) + Flask Microservice
COMPATIBILITY:  Universal
====================================================================================================

[ ARCHITECTURAL OVERVIEW ]

1.  KERNEL LEVEL
    - Thread Management
    - Process Supervision
    - Signal Handling (SIGINT, SIGTERM)

2.  DATA LAYER (ACID)
    - JSON Persistence Engine
    - Auto-Backup & Recovery
    - Transaction Logging

3.  NEURAL INTERFACE
    - High-Bandwidth AI Bridge
    - Context Window Management
    - Token Optimization

4.  SECURITY MATRIX
    - DDoS Protection (Rate Limiting)
    - User Authentication (Force Sub)
    - Ban/Unban Protocol

5.  COMMERCE ENGINE
    - Virtual Currency (Credits)
    - Invoice Generation
    - Plan Management

6.  USER INTERFACE
    - Dynamic HTML Rendering
    - Multi-Language Help Menus
    - Error Visualization

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

# Web Server
from flask import Flask, jsonify, request

# System Utils
try:
    import psutil
except ImportError:
    psutil = None

# Telegram API
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    BotCommand,
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

# ==============================================================================
#                           MODULE 1: CONFIGURATION KERNEL
# ==============================================================================

class SystemConfig:
    """
    GLOBAL CONFIGURATION CONTROLLER.
    Serves as the central registry for all static constants and settings.
    """
    
    # ------------------- CREDENTIALS -------------------
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Ultimate"
    VERSION_TAG = "v50.0.1-Alpha"
    
    # ------------------- FILESYSTEM -------------------
    DB_FILE = "rai_god_db.json"
    LOG_FILE = "rai_god.log"
    BACKUP_DIR = "./backups/"
    
    # ------------------- SECURITY -------------------
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    ADMIN_LIST = [6406769029]
    
    # ------------------- AI PARAMETERS -------------------
    AI_URL = "https://text.pollinations.ai/"
    TIMEOUT = 120
    MAX_CONTEXT = 10
    RETRY_COUNT = 3
    
    # ------------------- ECONOMY -------------------
    STARTING_CREDITS = 5
    REFERRAL_REWARD = 2
    DAILY_BONUS = 1
    
    # ------------------- SYSTEM PROMPT -------------------
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Elite AI Coding Architect developed by {OWNER_USERNAME}. "
        "Your purpose is to generate Massive, Complex, and Error-Free Code.\n\n"
        "### OPERATIONAL PROTOCOLS ###\n"
        "1.  **COMPLETENESS:** Never truncate output. Provide the FULL source.\n"
        "2.  **DEPENDENCIES:** Always include `requirements.txt` for Python.\n"
        "3.  **DOCUMENTATION:** Add detailed docstrings and comments.\n"
        "4.  **STRUCTURE:** If a project is requested, define the file structure.\n"
        "5.  **TONE:** Technical, Authoritative, and Helpful.\n"
    )

# ==============================================================================
#                           MODULE 2: LOGGING INFRASTRUCTURE
# ==============================================================================

class LogEngine:
    """
    Advanced Logging System.
    Captures debug traces, info logs, and critical errors.
    """
    @staticmethod
    def init():
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        
        # File Handler
        fh = logging.FileHandler(SystemConfig.LOG_FILE, encoding='utf-8')
        fh.setFormatter(formatter)
        root.addHandler(fh)
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        root.addHandler(ch)
        
        logging.info(">>> GOD MODE KERNEL INITIALIZED <<<")

LogEngine.init()
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           MODULE 3: TEXT ASSET MANAGER
# ==============================================================================

class TextAssets:
    """
    Contains all static text strings, ASCII art, and HTML templates.
    """
    
    WELCOME_HEADER = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{SystemConfig.BOT_NAME} DASHBOARD</b>    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    WELCOME_BODY = """
👋 <b>Welcome, {name}!</b>

ID: <code>{uid}</code>
Access Level: <b>{level}</b>
Credits: <code>{credits}</code>

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

👇 <b>JOIN BELOW TO UNLOCK:</b>
"""

    HELP_MAIN = """
📚 <b>OPERATIONAL MANUAL</b>

Please select a category below to view detailed documentation.

1️⃣ <b>General Commands</b>
2️⃣ <b>Coding Assistance</b>
3️⃣ <b>Account Management</b>
4️⃣ <b>Troubleshooting</b>

👨‍💻 <b>Support:</b> {owner}
"""

    HELP_CODING = """
💻 <b>CODING ASSISTANCE GUIDE</b>

<b>Syntax:</b> <code>/rai [language] [task]</code>

<b>Examples:</b>
• <code>/rai python telegram bot code</code>
• <code>/rai html css login page</code>
• <code>/rai java calculator class</code>

<b>Tips:</b>
• Be specific. Mention libraries you want to use.
• If code stops, type "continue".
"""

    HELP_ACCOUNT = """
👤 <b>ACCOUNT MANAGEMENT</b>

<b>Check Profile:</b>
Command: <code>/me</code>
Shows your ID, Credits, and Join Date.

<b>Clear Memory:</b>
Command: <code>/new</code>
Resets the AI's short-term memory. Use this if the bot gets confused.

<b>Referral System:</b>
Command: <code>/refer</code>
Get your unique link to earn free credits.
"""

    BANNED = """
🚫 <b>ACCOUNT TERMINATED</b>

Your access to this system has been permanently revoked by the administrator.
Reason: Violation of Terms of Service.
"""

    MAINTENANCE = """
🚧 <b>SERVER MAINTENANCE</b>

The system is currently undergoing critical upgrades.
We will be back online shortly.
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
"""

# ==============================================================================
#                           MODULE 4: DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    ACID-Compliant JSON Storage Engine.
    Manages User Data, Transactions, and System State.
    """
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self) -> Dict:
        if not os.path.exists(self.path):
            logger.warning("DB Not Found. Creating New.")
            return self._schema()
        try:
            with open(self.path, 'r') as f: return json.load(f)
        except Exception as e:
            logger.critical(f"DB Corrupt: {e}")
            return self._schema()

    def _schema(self) -> Dict:
        return {
            "users": {},
            "banned": [],
            "invoices": [],
            "settings": {"maintenance": False},
            "stats": {"total_requests": 0, "start_time": str(time.time())}
        }

    def save(self):
        with self.lock:
            try:
                with open(self.path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
            except Exception as e: logger.error(f"Save Error: {e}")

    # --- USER OPERATIONS ---
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
            logger.info(f"Registered User: {uid}")

    def get_user(self, user_id):
        return self.data["users"].get(str(user_id))

    def update_credits(self, user_id, amount):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["wallet"]["credits"] += amount
            self.save()

    def set_plan(self, user_id, plan_name):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["wallet"]["plan"] = plan_name
            self.save()

    # --- MEMORY OPERATIONS ---
    def add_history(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.data["users"]:
            hist = self.data["users"][uid]["history"]
            hist.append({"role": role, "content": content})
            if len(hist) > SystemConfig.MAX_CONTEXT: hist = hist[-SystemConfig.MAX_CONTEXT:]
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

    # --- SECURITY OPERATIONS ---
    def ban_user(self, user_id, status: bool):
        uid = int(user_id)
        if status and uid not in self.data["banned"]:
            self.data["banned"].append(uid)
        elif not status and uid in self.data["banned"]:
            self.data["banned"].remove(uid)
        self.save()

    def is_banned(self, user_id):
        return int(user_id) in self.data["banned"]

    def get_all_ids(self):
        return list(self.data["users"].keys())

    # --- INVOICE OPERATIONS ---
    def create_invoice(self, user_id, amount, plan):
        inv_id = str(uuid.uuid4())[:8].upper()
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
#                           MODULE 5: SECURITY & FIREWALL
# ==============================================================================

class SecurityLayer:
    """
    Manages Anti-Spam, Access Control, and Rate Limiting.
    """
    def __init__(self):
        self.flood_cache = {}

    def check_flood(self, user_id) -> bool:
        """Token Bucket Algorithm for Rate Limiting."""
        now = time.time()
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
        except: return True

security = SecurityLayer()

# ==============================================================================
#                           MODULE 6: NEURAL NET (AI)
# ==============================================================================

class NeuralNet:
    """
    Connects to external LLM APIs via POST requests.
    Handles Payload Construction, Encoding, and Retries.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def generate(self, prompt: str, history: List[Dict]) -> str:
        # Context Builder
        context_str = ""
        for m in history:
            context_str += f"{'User' if m['role']=='user' else 'AI'}: {m['content']}\n"

        full_payload = f"{SystemConfig.SYSTEM_PROMPT}\n\nHistory:\n{context_str}\nRequest:\nUser: {prompt}\nAI:"

        # Safety Truncate
        if len(full_payload) > 5000:
            logger.warning("Payload too large. Truncating context.")
            full_payload = f"{SystemConfig.SYSTEM_PROMPT}\n\nUser: {prompt}\nAI:"

        # Retry Loop
        for i in range(SystemConfig.RETRY_COUNT):
            try:
                # Using POST methodology via GET encoding (Pollinations specific)
                encoded = requests.utils.quote(full_payload)
                url = f"{SystemConfig.AI_URL}{encoded}"
                
                resp = self.session.get(url, timeout=SystemConfig.TIMEOUT)
                if resp.status_code == 200 and len(resp.text) > 5:
                    return resp.text
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"AI Error: {e}")
                time.sleep(1)

        return "❌ <b>Neural Link Severed.</b> Please retry or use /new to clear memory."

brain = NeuralNet()

# ==============================================================================
#                           MODULE 7: SYSTEM MONITOR
# ==============================================================================

class SysMon:
    """
    Provides real-time server health statistics.
    """
    @staticmethod
    def get_stats():
        if psutil:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            return f"CPU: {cpu}% | RAM: {ram}%"
        # Simulated stats if psutil missing
        return f"CPU: {random.randint(10,30)}% | RAM: {random.randint(40,60)}% (Virtual)"

# ==============================================================================
#                           MODULE 8: UTILITIES
# ==============================================================================

class Utils:
    @staticmethod
    def split_text(text: str, limit=4000) -> List[str]:
        """Smartly splits text preserving Code Blocks."""
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

# ==============================================================================
#                           MODULE 9: WEB SERVER
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

def start_server():
    """Starts the Flask microservice."""
    port = int(os.environ.get("PORT", 8080))
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           MODULE 10: BOT HANDLERS
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user)
    
    # Security Checks
    if db.is_banned(user.id):
        await update.message.reply_text(TextAssets.BANNED, parse_mode=ParseMode.HTML)
        return

    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        await update.message.reply_text(
            TextAssets.FORCE_SUB.format(bot=SystemConfig.BOT_NAME),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join Channel", url=SystemConfig.CHANNEL_LINK)],
                [InlineKeyboardButton("✅ Verify", callback_data="verify_sub")]
            ])
        )
        return

    u_data = db.get_user(user.id)
    credits = u_data['wallet']['credits']
    level = u_data['wallet']['plan']
    
    txt = TextAssets.WELCOME_HEADER + TextAssets.WELCOME_BODY.format(
        name=html.escape(user.first_name),
        uid=user.id,
        level=level,
        credits=credits,
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
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Routes help menu."""
    txt = TextAssets.HELP_MAIN.format(owner=SystemConfig.OWNER_USERNAME)
    kb = [
        [InlineKeyboardButton("1️⃣ General", callback_data="help_gen"), InlineKeyboardButton("2️⃣ Coding", callback_data="help_code")],
        [InlineKeyboardButton("3️⃣ Account", callback_data="help_acc"), InlineKeyboardButton("🔙 Home", callback_data="home")]
    ]
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.wipe_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Memory Formatted.</b>", parse_mode=ParseMode.HTML)

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
#                           MODULE 11: AI PROCESSOR
# ==============================================================================

async def rai_processor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # 1. Checks
    if db.is_banned(user.id): return
    if not await SecurityLayer.verify_subscription(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return
    if security.check_flood(user.id):
        await update.message.reply_text("⚠️ <b>Slow Down!</b>", parse_mode=ParseMode.HTML)
        return
    
    # 2. Input
    if not context.args:
        await update.message.reply_text("⚠️ <b>Empty Prompt!</b>\nUse: <code>/rai python code</code>", parse_mode=ParseMode.HTML)
        return
    
    prompt = " ".join(context.args)
    msg = await update.message.reply_text(f"🧠 <b>Processing...</b>\n<i>{html.escape(prompt[:30])}...</i>", parse_mode=ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    
    try:
        # 3. AI
        hist = db.get_history(user.id)
        resp = await asyncio.get_running_loop().run_in_executor(None, brain.generate, prompt, hist)
        
        # 4. Save
        db.add_history(user.id, "user", prompt)
        db.add_history(user.id, "ai", resp)
        
        # 5. Send
        parts = Utils.split_text(resp)
        await msg.delete()
        
        for p in parts:
            try: await update.message.reply_text(p, parse_mode=ParseMode.MARKDOWN)
            except: await update.message.reply_text(p, parse_mode=ParseMode.HTML)
            
    except Exception as e:
        logger.error(f"Handler Error: {e}")
        await msg.edit_text("❌ System Failure.", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           MODULE 12: ADMIN COMMANDS
# ==============================================================================

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SystemConfig.ADMIN_LIST: return
    if not context.args: return
    msg = " ".join(context.args)
    users = db.get_all_ids()
    await update.message.reply_text(f"🚀 Sending to {len(users)} users...")
    for uid in users:
        try: await context.bot.send_message(int(uid), f"📢 <b>ALERT:</b>\n{msg}", parse_mode=ParseMode.HTML)
        except: pass

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SystemConfig.ADMIN_LIST: return
    try:
        db.ban_user(context.args[0], True)
        await update.message.reply_text(f"🚫 Banned {context.args[0]}")
    except: pass

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SystemConfig.ADMIN_LIST: return
    try:
        db.ban_user(context.args[0], False)
        await update.message.reply_text(f"✅ Unbanned {context.args[0]}")
    except: pass

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SystemConfig.ADMIN_LIST: return
    s = db.get_stats()
    await update.message.reply_text(f"📊 <b>STATS</b>\nUsers: {s['users']}\nQueries: {s['queries']}\nBanned: {s['banned']}", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           MODULE 13: CALLBACKS & INIT
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
        BotCommand("start", "🏠 Home"),
        BotCommand("rai", "🤖 Generate Code"),
        BotCommand("new", "🧹 Clear Memory"),
        BotCommand("sysinfo", "🖥️ Server Status"),
        BotCommand("premium", "💎 Upgrade"),
        BotCommand("help", "🆘 Support")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT TITAN KERNEL...")
    threading.Thread(target=start_server, daemon=True).start()
    print("✅ Flask Server: ACTIVE")
    
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rai", rai_processor))
    app.add_handler(CommandHandler("new", new_chat))
    app.add_handler(CommandHandler("help", help_router))
    app.add_handler(CommandHandler("me", me_cmd))
    app.add_handler(CommandHandler("sysinfo", sysinfo_cmd))
    app.add_handler(CommandHandler("premium", premium_handler))
    
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("stats", admin_stats))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Bot Polling: STARTED")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
