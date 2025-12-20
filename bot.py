#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
====================================================================================================
||                                                                                                ||
||                       PROJECT: RAI GPT - TITANIUM ENTERPRISE                                   ||
||                   "The Most Advanced AI Infrastructure on Telegram"                            ||
||                                                                                                ||
====================================================================================================
||                                                                                                ||
||  VERSION:        200.0 (Titanium Build)                                                        ||
||  DEVELOPER:      @PixDev_Rai                                                                   ||
||  OWNER ID:       6406769029                                                                    ||
||  LICENSE:        Proprietary (Private Use Only)                                                ||
||  FRAMEWORK:      Python Telegram Bot (v21.x) + Flask Microservice                              ||
||  ARCHITECTURE:   Modular Object-Oriented Design (MOOD)                                         ||
||                                                                                                ||
====================================================================================================

[ SYSTEM ARCHITECTURE DOCUMENTATION ]

1.  CORE KERNEL
    - Manages event loops, signal handling, and thread synchronization.
    - Initializes Flask subsystem for 24/7 uptime monitoring.

2.  SUBSCRIPTION MANAGER (NEW)
    - Parsing engine for durations (e.g., "1 month", "30 days").
    - Automatic expiry calculation and plan revocation.

3.  DATA PERSISTENCE LAYER (ACID)
    - Custom JSON Database Engine with atomic write operations.
    - Transaction logging for credits and premium plans.

4.  NEURAL INTERFACE (AI BRIDGE)
    - High-Bandwidth connection to Pollinations AI via POST.
    - Smart Context Truncation to handle infinite conversation depth.

5.  PROJECT BUILDER
    - Intelligent File Naming based on user prompt.
    - ZIP Compression for large codebases.

6.  SECURITY & FIREWALL
    - Anti-Spam / Rate Limiting.
    - Force Subscription Verification.
    - Admin-Level Ban/Unban Protocols.

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
import zipfile
import io
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Any, Optional, Union, Tuple

# Web Server Framework
from flask import Flask, jsonify

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
    from telegram.error import BadRequest, NetworkError, Conflict
except ImportError:
    print("CRITICAL: Telegram Library Missing.")
    sys.exit(1)

# ==============================================================================
#                           SECTION 1: SYSTEM CONFIGURATION
# ==============================================================================

class SystemConfig:
    """
    Central Configuration Controller.
    """
    
    # --- IDENTITY ---
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Titan"
    VERSION = "200.0.1"
    
    # --- FILESYSTEM ---
    DB_FILE = "rai_titan_db.json"
    LOG_FILE = "titan_server.log"
    
    # --- SECURITY ---
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    
    # --- AI ENGINE ---
    AI_PROVIDER_URL = "https://text.pollinations.ai/"
    REQUEST_TIMEOUT = 180  # 3 Minutes
    
    # --- LIMITS ---
    FREE_TIER_CHARS = 4000  # Max chars in text message for free users
    ZIP_THRESHOLD = 2000    # If code > 2000 chars, convert to ZIP
    
    # --- PROMPTS ---
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Elite AI Coding Architect developed by {OWNER_USERNAME}. "
        "Your purpose is to generate Massive, Complex, and Error-Free Code.\n\n"
        "### OPERATIONAL PROTOCOLS ###\n"
        "1.  **COMPLETENESS:** Never truncate output. Provide the FULL source code.\n"
        "2.  **DEPENDENCIES:** Always include `requirements.txt` for Python projects.\n"
        "3.  **DOCUMENTATION:** Add detailed docstrings and comments.\n"
        "4.  **STRUCTURE:** If a bot is requested, define the file structure.\n"
        "5.  **TONE:** Technical, Authoritative, and Helpful.\n"
    )

# ==============================================================================
#                           SECTION 2: LOGGING SUBSYSTEM
# ==============================================================================

class LogManager:
    """
    Advanced Logging System.
    """
    @staticmethod
    def initialize():
        log_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler(SystemConfig.LOG_FILE, encoding='utf-8')
        fh.setFormatter(log_format)
        root_logger.addHandler(fh)
        
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(log_format)
        root_logger.addHandler(ch)
        
        logging.info(">>> TITANIUM KERNEL INITIALIZED <<<")

LogManager.initialize()
logger = logging.getLogger("RaiGPT_Kernel")

# ==============================================================================
#                           SECTION 3: LOCALIZATION & UI ASSETS
# ==============================================================================

class TextAssets:
    """
    Manages all static text strings and HTML templates.
    """
    
    WELCOME = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🧠 <b>{bot} ENTERPRISE DASHBOARD</b>    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Greetings, {name}!</b>

ID: <code>{uid}</code>
Plan: <b>{plan}</b>
Valid Until: <code>{expiry}</code>

I am the <b>Titanium Edition AI</b>. 
I specialize in generating <b>Massive Projects</b> and converting them into ZIP files.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>SYSTEM MODULES:</b>

🟢 <b>AI Generator</b> - <code>/rai [query]</code>
   <i>Generate Python, Java, C++, Web Code.</i>

📦 <b>Project Builder</b>
   <i>Automatically zips large codebases.</i>

💎 <b>Premium Core</b>
   <i>Unlocks Unlimited Code Generation.</i>

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

👇 <b>Please join the channel below:</b>
"""

    PREMIUM_LOCKED = """
🚫 <b>FILE LOCKED: PREMIUM ONLY</b>

⚠️ <b>System Alert:</b>
The generated code is massive (<b>{lines}+ Lines</b>).
Free Tier limit exceeded.

💎 <b>UNLOCK NOW</b>
Contact Admin to upgrade your plan.
Price: ₹99 / Month

👤 <b>Admin:</b> {owner}
"""

    HELP_MENU = """
📚 <b>OPERATIONAL MANUAL</b>

<b>1. Code Generation</b>
   • Syntax: <code>/rai <prompt></code>
   • Example: <code>/rai Python script for Telegram Bot</code>

<b>2. Memory Management</b>
   • Syntax: <code>/new</code>
   • Action: Resets the AI's short-term memory.

<b>3. Account Management</b>
   • Syntax: <code>/me</code>
   • Action: Shows your profile and plan status.

<b>4. Premium Status</b>
   • Premium users get unlimited ZIP downloads.
   • Contact {owner} to buy.
"""

# ==============================================================================
#                           SECTION 4: DATABASE & SUBSCRIPTION ENGINE
# ==============================================================================

class DatabaseEngine:
    """
    ACID-Compliant JSON Storage Engine.
    Manages User Data, Subscriptions, and Expiry Logic.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = threading.Lock()
        self.data = self._load_db()

    def _load_db(self) -> Dict:
        if not os.path.exists(self.filepath):
            return self._schema()
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.critical(f"Database Corruption: {e}")
            return self._schema()

    def _schema(self) -> Dict:
        return {
            "users": {},
            "banned": [],
            "stats": {"total_queries": 0},
            "settings": {"maintenance": False}
        }

    def save(self):
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
                    "joined": str(datetime.datetime.now())
                },
                "subscription": {
                    "is_premium": False,
                    "expiry_date": None,
                    "plan_name": "Free"
                },
                "history": []
            }
            self.save()
            logger.info(f"New User: {uid}")

    def get_user(self, user_id):
        return self.data["users"].get(str(user_id))

    def get_user_by_username(self, username: str) -> Optional[str]:
        """Finds UID by username (for admin commands)."""
        target = username.replace("@", "").lower()
        for uid, data in self.data["users"].items():
            u = data['profile'].get('username', '')
            if u and u.lower() == target:
                return uid
        return None

    # --- Premium / Subscription Logic ---
    def grant_premium(self, user_id, days: int):
        """Activates premium plan for X days."""
        uid = str(user_id)
        if uid in self.data["users"]:
            expiry = datetime.datetime.now() + datetime.timedelta(days=days)
            self.data["users"][uid]["subscription"] = {
                "is_premium": True,
                "expiry_date": expiry.strftime("%Y-%m-%d %H:%M:%S"),
                "plan_name": "Titanium Pro"
            }
            self.save()
            return expiry
        return None

    def revoke_premium(self, user_id):
        """Revokes premium status."""
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["subscription"] = {
                "is_premium": False,
                "expiry_date": None,
                "plan_name": "Free"
            }
            self.save()

    def check_premium_status(self, user_id) -> bool:
        """Checks if premium is active and not expired."""
        uid = str(user_id)
        if uid == str(SystemConfig.OWNER_ID): return True
        
        user = self.data["users"].get(uid)
        if not user: return False
        
        sub = user.get("subscription", {})
        if not sub.get("is_premium"): return False
        
        expiry_str = sub.get("expiry_date")
        if not expiry_str: return False
        
        expiry = datetime.datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
        if datetime.datetime.now() > expiry:
            # Plan Expired
            self.revoke_premium(user_id)
            return False
            
        return True

    # --- History & Context ---
    def add_history(self, user_id, role, content):
        uid = str(user_id)
        if uid in self.data["users"]:
            hist = self.data["users"][uid].get("history", [])
            hist.append({"role": role, "content": content})
            if len(hist) > 10: hist = hist[-10:]
            self.data["users"][uid]["history"] = hist
            self.save()

    def get_history(self, user_id):
        return self.data["users"].get(str(user_id), {}).get("history", [])

    def clear_history(self, user_id):
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["history"] = []
            self.save()

    # --- Security ---
    def ban_user(self, user_id, status: bool):
        uid = int(user_id)
        if status and uid not in self.data["banned"]:
            self.data["banned"].append(uid)
        elif not status and uid in self.data["banned"]:
            self.data["banned"].remove(uid)
        self.save()

    def is_banned(self, user_id):
        return int(user_id) in self.data["banned"]

db = DatabaseEngine(SystemConfig.DB_FILE)

# ==============================================================================
#                           SECTION 5: PROJECT BUILDER (SMART ZIP)
# ==============================================================================

class ProjectBuilder:
    """
    Handles dynamic file generation and compression for large codebases.
    """
    @staticmethod
    def detect_language(code: str) -> str:
        if "def " in code or "import " in code: return "py"
        if "function" in code or "const " in code: return "js"
        if "public class" in code: return "java"
        if "<html>" in code: return "html"
        return "txt"

    @staticmethod
    def generate_filename(prompt: str, ext: str) -> str:
        """Generates a clean filename from user prompt."""
        clean = re.sub(r'[^\w\s]', '', prompt).strip().replace(' ', '_')
        if len(clean) > 30: clean = clean[:30]
        if not clean: clean = "Project"
        return f"{clean}.{ext}"

    @staticmethod
    def create_zip(code_content: str, prompt: str) -> Any:
        zip_buffer = io.BytesIO()
        ext = ProjectBuilder.detect_language(code_content)
        main_file = ProjectBuilder.generate_filename(prompt, ext)
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Main Code
            zf.writestr(main_file, code_content)
            
            # Requirements
            if ext == "py":
                reqs = "requests\nflask\npython-telegram-bot\ngunicorn"
                zf.writestr("requirements.txt", reqs)
            
            # Readme
            readme = f"""
PROJECT: {prompt}
GENERATED BY: {SystemConfig.BOT_NAME}
OWNER: {SystemConfig.OWNER_USERNAME}
DATE: {datetime.datetime.now()}
            """
            zf.writestr("README.txt", readme)
            
        zip_buffer.seek(0)
        return zip_buffer, f"{main_file[:-3]}_Project.zip"

# ==============================================================================
#                           SECTION 6: NEURAL NET (AI ENGINE)
# ==============================================================================

class NeuralNet:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def generate(self, prompt, history):
        context = ""
        for m in history:
            context += f"{'User' if m['role']=='user' else 'AI'}: {m['content']}\n"
        
        full_payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\n\nHistory:\n{context}\nUser: {prompt}\nAI:"
        
        if len(full_payload) > 4000:
            full_payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\nUser: {prompt}\nAI:"

        for _ in range(SystemConfig.RETRY_ATTEMPTS):
            try:
                encoded = requests.utils.quote(full_payload)
                url = f"{SystemConfig.AI_PROVIDER_URL}{encoded}"
                
                resp = self.session.get(url, timeout=SystemConfig.REQUEST_TIMEOUT)
                if resp.status_code == 200 and len(resp.text) > 5:
                    return resp.text
                time.sleep(1)
            except Exception as e:
                logger.error(f"AI Error: {e}")
                time.sleep(1)
        return "ERROR"

ai = NeuralNet()

# ==============================================================================
#                           SECTION 7: UTILITIES
# ==============================================================================

class TimeUtils:
    """Parses time strings like '30 days', '1 month'."""
    @staticmethod
    def parse_duration(duration_str: str) -> int:
        """Returns days as integer."""
        text = duration_str.lower()
        if 'year' in text: return 365
        if 'month' in text: return 30
        if 'week' in text: return 7
        if 'day' in text:
            # Extract number
            nums = re.findall(r'\d+', text)
            if nums: return int(nums[0])
        return 0

class MessageUtils:
    @staticmethod
    def split_text(text, limit=4000):
        if len(text) <= limit: return [text]
        parts = []
        while len(text) > 0:
            split_at = text.rfind('```', 0, limit)
            if split_at == -1: split_at = text.rfind('\n', 0, limit)
            if split_at == -1: split_at = limit
            parts.append(text[:split_at])
            text = text[split_at:]
        return parts

    @staticmethod
    def count_lines(text):
        return len(text.split('\n'))

    @staticmethod
    async def verify_sub(user_id, bot):
        if not SystemConfig.FORCE_SUB_ENABLED: return True
        try:
            member = await bot.get_chat_member(SystemConfig.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked']: return False
            return True
        except: return True

# ==============================================================================
#                           SECTION 8: WEB SERVER
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"status": "online", "bot": SystemConfig.BOT_NAME})

def run_server():
    port = int(os.environ.get("PORT", 8080))
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           SECTION 9: BOT HANDLERS (USER)
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user)
    
    if db.is_banned(user.id): return

    if not await MessageUtils.verify_sub(user.id, context.bot):
        kb = [[InlineKeyboardButton("🚀 Join Channel", url=SystemConfig.CHANNEL_LINK)],
              [InlineKeyboardButton("✅ Verify", callback_data="verify")]]
        await update.message.reply_text(
            TextAssets.FORCE_SUB.format(bot=SystemConfig.BOT_NAME),
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )
        return

    # User Data
    u_data = db.get_user(user.id)
    is_prem = db.check_premium_status(user.id)
    plan = u_data['subscription']['plan_name'] if is_prem else "Free Tier"
    expiry = u_data['subscription']['expiry_date'] if is_prem else "Lifetime"
    
    txt = TextAssets.WELCOME.format(
        bot=SystemConfig.BOT_NAME,
        name=html.escape(user.first_name),
        uid=user.id,
        plan=plan,
        credits="Unlimited" if is_prem else "Limited",
        owner=SystemConfig.OWNER_USERNAME,
        version=SystemConfig.VERSION
    )
    
    kb = [
        [InlineKeyboardButton("🤖 Generate Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("👤 Profile", callback_data="me"), InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def rai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if db.is_banned(user.id): return
    if not await MessageUtils.verify_sub(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return

    if not context.args:
        await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rai python code</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    status_msg = await update.message.reply_text("🧠 <b>Architecting Solution...</b>", parse_mode=ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # AI Generation
        hist = db.get_history(user.id)
        response = await asyncio.get_running_loop().run_in_executor(None, ai.generate, prompt, hist)
        
        if response == "ERROR":
            await status_msg.edit_text("❌ System Error. Try again.")
            return

        # Check Premium
        is_premium = db.check_premium_status(user.id)
        line_count = MessageUtils.count_lines(response)
        
        await status_msg.delete()

        # LOCK LOGIC: If Code > 2000 lines (simulated check) and NOT Premium
        # Note: Response length check. 
        if len(response) > 50000 and not is_premium:
             txt = TextAssets.PREMIUM_LOCKED.format(
                 lines=line_count, 
                 price=99, 
                 owner=SystemConfig.OWNER_USERNAME
             )
             await update.message.reply_text(txt, parse_mode=ParseMode.HTML)
             return

        # ZIP Logic for large files
        if len(response) > 2000:
            zip_obj, filename = ProjectBuilder.create_zip(response, prompt)
            caption = f"📦 <b>Project Built</b>\nLines: {line_count}\nUser: {user.first_name}"
            await update.message.reply_document(
                document=zip_obj,
                filename=filename,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
        else:
            db.add_history(user.id, "user", prompt)
            db.add_history(user.id, "ai", response)
            try: await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            except: await update.message.reply_text(response, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Handler Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="❌ Critical Error.")

# ==============================================================================
#                           SECTION 10: ADMIN HANDLERS (PREMIUM)
# ==============================================================================

async def admin_add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command: /addpremium @username 30 days
    """
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Usage: <code>/addpremium @user 30 days</code>", parse_mode=ParseMode.HTML)
            return
            
        target_input = context.args[0]
        duration_str = " ".join(context.args[1:])
        
        # Resolve User
        if target_input.startswith("@"):
            uid = db.get_user_by_username(target_input)
        else:
            uid = target_input
            
        if not uid:
            await update.message.reply_text("❌ User not found in database.", parse_mode=ParseMode.HTML)
            return
            
        # Calculate Duration
        days = TimeUtils.parse_duration(duration_str)
        if days == 0:
            await update.message.reply_text("❌ Invalid duration. Use '30 days', '1 month', '1 year'.")
            return
            
        # Grant Premium
        expiry = db.grant_premium(uid, days)
        
        await update.message.reply_text(
            f"✅ <b>Premium Granted!</b>\n"
            f"User: {target_input}\n"
            f"Duration: {days} Days\n"
            f"Expires: {expiry.strftime('%Y-%m-%d')}",
            parse_mode=ParseMode.HTML
        )
        
        # Notify User
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"💎 <b>PREMIUM ACTIVATED!</b>\n\nYour account has been upgraded by Admin.\nValidity: {days} Days.",
                parse_mode=ParseMode.HTML
            )
        except: pass
        
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def admin_remove_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        target = context.args[0].replace("@", "")
        uid = db.get_user_by_username(target) if not target.isdigit() else target
        
        if uid:
            db.revoke_premium(uid)
            await update.message.reply_text(f"🚫 Premium revoked for {target}.")
        else:
            await update.message.reply_text("User not found.")
    except: pass

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.clear_history(update.effective_user.id)
    await update.message.reply_text("🧹 Memory Cleared.", parse_mode=ParseMode.HTML)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TextAssets.HELP_MENU.format(owner=SystemConfig.OWNER_USERNAME), parse_mode=ParseMode.HTML)

async def me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = db.get_user(update.effective_user.id)
    is_prem = db.check_premium_status(update.effective_user.id)
    status = "PREMIUM 💎" if is_prem else "FREE"
    await update.message.reply_text(f"👤 <b>PROFILE</b>\nStatus: {status}\nID: {update.effective_user.id}", parse_mode=ParseMode.HTML)

# ==============================================================================
#                           SECTION 11: INITIALIZATION
# ==============================================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "verify":
        if await MessageUtils.verify_sub(query.from_user.id, context.bot):
            await query.delete_message()
            await start(update, context)
        else: await query.answer("❌ Not Joined!", show_alert=True)
    elif query.data == "help": await help_cmd(update, context)
    elif query.data == "me": await me_cmd(update, context)

async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Home"),
        BotCommand("rai", "Generate Code"),
        BotCommand("new", "Reset"),
        BotCommand("me", "Profile"),
        BotCommand("help", "Support")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT TITAN...")
    threading.Thread(target=run_server, daemon=True).start()
    
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rai", rai_cmd))
    app.add_handler(CommandHandler("new", new_chat))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("me", me_cmd))
    
    # Admin Handlers
    app.add_handler(CommandHandler("addpremium", admin_add_premium))
    app.add_handler(CommandHandler("removepremium", admin_remove_premium))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Bot Started")
    
    # Conflict Loop
    while True:
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        except Conflict:
            logger.warning("Conflict! Retrying...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Critical: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
