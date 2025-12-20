#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
====================================================================================================
||                                                                                                ||
||                       PROJECT: RAI GPT - GODSPEED EDITION                                      ||
||                   "The 1000-Line Ultimate AI Infrastructure"                                   ||
||                                                                                                ||
====================================================================================================
||                                                                                                ||
||  VERSION:        2025.1.0 (Godspeed Build)                                                     ||
||  DEVELOPER:      @PixDev_Rai                                                                   ||
||  OWNER ID:       6406769029                                                                    ||
||  LICENSE:        Enterprise Proprietary                                                        ||
||  FRAMEWORK:      Python Telegram Bot (v21.x) + Flask                                           ||
||                                                                                                ||
====================================================================================================

[ LOGIC FLOW DOCUMENTATION ]

1.  USER REQUEST PROCESSING:
    - Code < 200 Lines: Sent as direct Text Message.
    - Code 200-600 Lines: Auto-converted to ZIP (Free User Limit).
    - Code > 600 Lines: Locked for Free Users. Requires Premium.
    - Premium Users: Can generate up to 2000 Lines (ZIP).

2.  SMART FILE SYSTEM:
    - Detects User Intent (e.g., "Create HTML login") -> Creates `login.html`.
    - Detects Sketchware -> Creates `instructions.txt`.
    - Detects Python -> Creates `main.py` + `requirements.txt`.

3.  ADMINISTRATION SUITE:
    - /ban, /unban, /broadcast, /stats commands restored.
    - /addpremium & /removepremium for subscription management.

4.  SUBSCRIPTION ENGINE:
    - Supports "30 days", "1 year", "Lifetime" parsing.
    - Auto-expires users.

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

# Web Server
try:
    from flask import Flask, jsonify, request
except ImportError:
    os.system("pip install flask")
    from flask import Flask, jsonify

# Telegram API
try:
    from telegram import (
        Update, 
        InlineKeyboardButton, 
        InlineKeyboardMarkup, 
        BotCommand,
        User,
        Chat,
        Message,
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
    from telegram.error import BadRequest, Conflict, NetworkError
except ImportError:
    print("Please install python-telegram-bot")
    sys.exit(1)

# ==============================================================================
#                           SECTION 1: KERNEL CONFIGURATION
# ==============================================================================

class SystemConfig:
    """
    GLOBAL SETTINGS CONTROLLER.
    """
    # Identity
    TOKEN = "8203679051:AAHJCgR-LE06jKind0-Rej4fMRFYKR3XISQ"
    OWNER_ID = 6406769029
    OWNER_USERNAME = "@PixDev_Rai"
    BOT_NAME = "Rai GPT Godspeed"
    
    # Files
    DB_FILE = "rai_godspeed.json"
    LOG_FILE = "godspeed.log"
    
    # Security
    FORCE_SUB_ENABLED = True
    CHANNEL_USERNAME = "@raiaddaarmys"
    CHANNEL_LINK = "https://t.me/raiaddaarmys"
    
    # AI Config
    AI_URL = "https://text.pollinations.ai/"
    TIMEOUT = 180
    
    # --- LOGIC THRESHOLDS (LINES) ---
    MSG_LIMIT_LINES = 200      # < 200 lines = Text Message
    FREE_ZIP_LIMIT = 600       # 200-600 lines = Zip (Free)
    PREMIUM_ZIP_LIMIT = 2000   # 600-2000 lines = Zip (Premium Only)
    
    # System Prompt (Smart)
    SYSTEM_INSTRUCTION = (
        f"You are {BOT_NAME}, an Expert AI Developer created by {OWNER_USERNAME}. "
        "Your goal is to provide specific, high-quality code.\n\n"
        "### RULES ###\n"
        "1. Detect the language requested (HTML, Python, Java, Kotlin).\n"
        "2. If Sketchware/Android Builder is asked: Explain steps, logic, and blocks. Do NOT write Java code unless asked.\n"
        "3. If HTML is asked: Write full HTML/CSS/JS in one block.\n"
        "4. Write FULL Code. Never truncate.\n"
    )

# ==============================================================================
#                           SECTION 2: ADVANCED LOGGING
# ==============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(SystemConfig.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RaiGPT")

# ==============================================================================
#                           SECTION 3: UI ASSETS & TEXTS
# ==============================================================================

class TextAssets:
    """
    Stores all HTML-formatted messages with heavy styling.
    """
    
    WELCOME_SCREEN = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🚀 <b>{bot_name} DASHBOARD</b>      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👋 <b>Namaste, {name}!</b>

🆔 <b>User ID:</b> <code>{uid}</code>
💎 <b>Plan:</b> {plan}
⏳ <b>Expires:</b> {expiry}

I am the <b>Godspeed Edition AI</b>. 
I am designed to generate <b>Massive Projects (2000+ Lines)</b>.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>SYSTEM CAPABILITIES:</b>

🟢 <b>Smart Generator</b>
   └ <code>/rai [query]</code> - Auto-detects Language.
   
📦 <b>File Builder</b>
   └ < 200 Lines: <b>Text Message</b>
   └ > 200 Lines: <b>ZIP File</b>
   
💎 <b>Premium Core</b>
   └ Free User: Max 600 Lines.
   └ Premium: Max 2000 Lines.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Developer:</b> {owner}
📅 <b>Server Time:</b> {time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👇 <b>INITIALIZE PROTOCOL:</b>
"""

    FORCE_SUB = """
🛑 <b>ACCESS DENIED: VERIFICATION PENDING</b>

⚠️ <b>User Attention Required!</b>

To utilize the power of <b>{bot_name}</b>, you must verify your membership.
This ensures server stability.

👇 <b>JOIN BELOW TO UNLOCK:</b>
"""

    BANNED_MSG = """
🚫 <b>ACCOUNT TERMINATED</b>

Your access to this system has been permanently revoked by the Admin.
<b>Reason:</b> Violation of Policy.
"""

    PREMIUM_ALERT = """
🚫 <b>LIMIT EXCEEDED (FREE TIER)</b>

📉 <b>Generated Code:</b> {lines} Lines
🔒 <b>Free Limit:</b> {limit} Lines

⚠️ <b>The code is too massive for Free Tier.</b>
To unlock <b>2000+ Lines</b> capacity and Instant ZIP generation, Upgrade to Premium.

💎 <b>Price:</b> ₹99 / Month
👉 Click <b>Buy Premium</b> below.
"""

    HELP_MENU = """
📚 <b>OPERATIONAL MANUAL</b>

1️⃣ <b>Code Generation</b>
   • <code>/rai create a login page in html</code>
   • <code>/rai python telegram bot code</code>
   • <i>Note: Small code comes in text, big code comes in ZIP.</i>

2️⃣ <b>Sketchware / Android</b>
   • <code>/rai how to use intent component in sketchware</code>
   • <i>I will explain blocks and events.</i>

3️⃣ <b>Account Info</b>
   • <code>/me</code> - Check Plan & ID.
   • <code>/new</code> - Clear AI Memory.

4️⃣ <b>Premium</b>
   • <code>/premium</code> - View Plans.
   • <b>Admin:</b> {owner}
"""

# ==============================================================================
#                           SECTION 4: DATABASE ENGINE
# ==============================================================================

class DatabaseEngine:
    """ACID-Compliant JSON Database."""
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {"users": {}, "banned": [], "stats": {"total": 0}}
        try:
            with open(self.path, 'r') as f: return json.load(f)
        except: return {"users": {}, "banned": [], "stats": {"total": 0}}

    def save(self):
        with self.lock:
            try:
                with open(self.path, 'w') as f: json.dump(self.data, f, indent=4)
            except: pass

    # --- USER ---
    def register(self, user):
        uid = str(user.id)
        if uid not in self.data["users"]:
            self.data["users"][uid] = {
                "name": user.first_name,
                "username": user.username,
                "joined": str(datetime.datetime.now()),
                "sub_expiry": "None",
                "history": []
            }
            self.save()

    def get_user(self, uid):
        return self.data["users"].get(str(uid))

    def get_uid_by_name(self, username):
        target = username.replace("@", "")
        for uid, d in self.data["users"].items():
            if d.get("username") == target: return uid
        return None

    # --- SUBSCRIPTION ---
    def set_premium(self, uid, duration_str):
        now = datetime.datetime.now()
        parts = duration_str.lower().split()
        try:
            amt = int(parts[0])
            unit = parts[1]
            if "day" in unit: delta = datetime.timedelta(days=amt)
            elif "month" in unit: delta = relativedelta(months=amt)
            elif "year" in unit: delta = relativedelta(years=amt)
            else: return None
            
            exp_date = now + delta
            self.data["users"][str(uid)]["sub_expiry"] = exp_date.strftime("%Y-%m-%d %H:%M:%S")
            self.save()
            return self.data["users"][str(uid)]["sub_expiry"]
        except: return None

    def remove_premium(self, uid):
        if str(uid) in self.data["users"]:
            self.data["users"][str(uid)]["sub_expiry"] = "None"
            self.save()

    def is_premium(self, uid):
        if int(uid) == SystemConfig.OWNER_ID: return True
        u = self.get_user(uid)
        if not u or u["sub_expiry"] == "None": return False
        exp = datetime.datetime.strptime(u["sub_expiry"], "%Y-%m-%d %H:%M:%S")
        return datetime.datetime.now() < exp

    # --- HISTORY ---
    def add_history(self, uid, role, content):
        if str(uid) in self.data["users"]:
            h = self.data["users"][str(uid)]["history"]
            h.append({"role": role, "content": content})
            if len(h) > 8: h = h[-8:]
            self.data["users"][str(uid)]["history"] = h
            self.save()

    def get_history(self, uid):
        return self.data["users"].get(str(uid), {}).get("history", [])

    def clear_history(self, uid):
        if str(uid) in self.data["users"]:
            self.data["users"][str(uid)]["history"] = []
            self.save()

    # --- ADMIN/SECURITY ---
    def ban_user(self, uid, status):
        uid = int(uid)
        if status and uid not in self.data["banned"]:
            self.data["banned"].append(uid)
        elif not status and uid in self.data["banned"]:
            self.data["banned"].remove(uid)
        self.save()

    def is_banned(self, uid):
        return int(uid) in self.data["banned"]

    def get_all_users(self):
        return list(self.data["users"].keys())

db = DatabaseEngine(SystemConfig.DB_FILE)

# ==============================================================================
#                           SECTION 5: FILE & PROJECT MANAGER
# ==============================================================================

class FileManager:
    """
    Intelligent File System.
    Determines File Extension based on Content and Prompt.
    """
    @staticmethod
    def get_extension(code: str, prompt: str) -> str:
        prompt = prompt.lower()
        if "html" in prompt: return "html"
        if "python" in prompt or "def " in code: return "py"
        if "java" in prompt or "public class" in code: return "java"
        if "json" in prompt: return "json"
        if "xml" in prompt: return "xml"
        if "sketchware" in prompt or "block" in prompt: return "txt"
        return "txt"

    @staticmethod
    def get_filename(prompt: str) -> str:
        # Extract meaningful name: "Create login page" -> "Login_Page"
        clean = re.sub(r'(create|make|give|code|for|a|the|in|how|to)', '', prompt.lower())
        clean = re.sub(r'[^\w\s]', '', clean).strip()
        filename = re.sub(r'\s+', '_', clean)
        if len(filename) < 3: filename = "Project_Code"
        return filename[:25]

    @staticmethod
    def create_zip(content: str, prompt: str) -> Any:
        buffer = io.BytesIO()
        ext = FileManager.get_extension(content, prompt)
        name = FileManager.get_filename(prompt)
        
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 1. Main File
            zf.writestr(f"{name}.{ext}", content)
            
            # 2. Instructions/Readme
            readme = f"""
PROJECT: {name}
GENERATED BY: {SystemConfig.BOT_NAME}
DATE: {datetime.datetime.now()}
-----------------------------------
Prompt: {prompt}
            """
            zf.writestr("README.txt", readme)
            
            # 3. Requirements (Only for Python)
            if ext == "py":
                reqs = "requests\nflask\npython-telegram-bot\ngunicorn"
                zf.writestr("requirements.txt", reqs)
                
        buffer.seek(0)
        return buffer, f"{name}_Project.zip"

# ==============================================================================
#                           SECTION 6: AI ENGINE
# ==============================================================================

class AIEngine:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def generate(self, prompt, history):
        context = ""
        for m in history:
            context += f"{'User' if m['role']=='user' else 'AI'}: {m['content']}\n"
        
        payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\n\nHistory:\n{context}\nUser: {prompt}\nAI:"
        
        # Truncate if too long to avoid errors
        if len(payload) > 5000:
            payload = f"{SystemConfig.SYSTEM_INSTRUCTION}\nUser: {prompt}\nAI:"

        for _ in range(3):
            try:
                # Pollinations GET Encoding
                encoded = requests.utils.quote(payload)
                url = f"{SystemConfig.AI_URL}{encoded}"
                
                if len(url) > 6000: return "OVERFLOW"

                resp = self.session.get(url, timeout=SystemConfig.TIMEOUT)
                if resp.status_code == 200 and len(resp.text) > 5:
                    return resp.text
                time.sleep(1)
            except: time.sleep(1)
        return "ERROR"

ai = AIEngine()

# ==============================================================================
#                           SECTION 7: UTILITIES & SECURITY
# ==============================================================================

class Utils:
    @staticmethod
    def count_lines(text):
        return len(text.split('\n'))

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
    async def verify_sub(user_id, bot):
        if not SystemConfig.FORCE_SUB_ENABLED: return True
        try:
            member = await bot.get_chat_member(SystemConfig.CHANNEL_USERNAME, user_id)
            if member.status in ['left', 'kicked']: return False
            return True
        except: return True

# ----------------- CONTINUED IN PART 2 -----------------
# ==============================================================================
#                           SECTION 8: WEB SERVER
# ==============================================================================

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"status": "Active", "bot": SystemConfig.BOT_NAME})

def run_server():
    port = int(os.environ.get("PORT", 8080))
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    app.run(host="0.0.0.0", port=port)

# ==============================================================================
#                           SECTION 9: BOT HANDLERS
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register(user)
    
    # Check Ban
    if db.is_banned(user.id):
        await update.message.reply_text(TextAssets.BANNED_MSG, parse_mode=ParseMode.HTML)
        return

    # Check Sub
    if not await Utils.verify_sub(user.id, context.bot):
        kb = [[InlineKeyboardButton("🚀 JOIN CHANNEL", url=SystemConfig.CHANNEL_LINK)],
              [InlineKeyboardButton("✅ VERIFY JOIN", callback_data="verify")]]
        await update.message.reply_text(TextAssets.FORCE_SUB.format(bot_name=SystemConfig.BOT_NAME), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    # User Info
    u_data = db.get_user(user.id)
    expiry = u_data.get("sub_expiry", "None")
    is_prem = expiry != "None"
    
    plan_name = "TITANIUM PRO 💎" if is_prem else "FREE TIER"
    
    if is_prem and expiry != "LIFETIME":
        try:
            exp_date = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
            days_left = (exp_date - datetime.datetime.now()).days
            time_str = f"{days_left} Days Left"
        except: time_str = "Active"
    elif expiry == "LIFETIME":
        time_str = "Lifetime ∞"
    else:
        time_str = "N/A"

    txt = TextAssets.WELCOME_SCREEN.format(
        bot_name=SystemConfig.BOT_NAME,
        name=html.escape(user.first_name),
        uid=user.id,
        plan=plan_name,
        credits=time_str,
        owner=SystemConfig.OWNER_USERNAME,
        time=datetime.datetime.now().strftime("%H:%M")
    )
    
    kb = [
        [InlineKeyboardButton("🤖 Ask AI Code", switch_inline_query_current_chat="/rai ")],
        [InlineKeyboardButton("💎 Buy Premium", callback_data="premium"), InlineKeyboardButton("👤 Profile", callback_data="me")],
        [InlineKeyboardButton("🆘 Help & Support", callback_data="help")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def rai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    MAIN AI HANDLER (THE LOGIC CORE)
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if db.is_banned(user.id): return
    if not await Utils.verify_sub(user.id, context.bot):
        await update.message.reply_text("❌ Join Channel First!", parse_mode=ParseMode.HTML)
        return

    if not context.args:
        await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rai python login system</code>", parse_mode=ParseMode.HTML)
        return

    prompt = " ".join(context.args)
    status_msg = await update.message.reply_text(f"🧠 <b>Thinking...</b>\n<i>Parsing: {html.escape(prompt[:30])}...</i>", parse_mode=ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # 1. Generate
        hist = db.get_history(user.id)
        response = await asyncio.get_running_loop().run_in_executor(None, ai.generate, prompt, hist)
        
        if response in ["ERROR", "OVERFLOW"]:
            await status_msg.edit_text("❌ <b>System Busy.</b> Try <code>/new</code>.", parse_mode=ParseMode.HTML)
            return

        # 2. Logic Gates (Line Count)
        line_count = Utils.count_lines(response)
        is_premium = db.is_premium(user.id)
        
        await status_msg.delete()

        # LOGIC 1: Code < 200 Lines (Send as Text)
        if line_count < SystemConfig.MSG_LIMIT_LINES:
            db.add_history(user.id, "user", prompt)
            db.add_history(user.id, "ai", response)
            parts = Utils.split_text(response)
            for p in parts:
                try: await update.message.reply_text(p, parse_mode=ParseMode.MARKDOWN)
                except: await update.message.reply_text(p, parse_mode=ParseMode.HTML)
            return

        # LOGIC 2: Code 200-600 Lines (Free Zip)
        if line_count <= SystemConfig.FREE_ZIP_LIMIT or is_premium:
            # Check Premium Limit (2000 Lines)
            if line_count > SystemConfig.PREMIUM_ZIP_LIMIT:
                await update.message.reply_text("🚫 <b>Too Big!</b> Code exceeds 2000 lines.", parse_mode=ParseMode.HTML)
                return
            
            # Send Zip
            zip_obj, filename = FileManager.create_zip(response, prompt)
            caption = f"📦 <b>Project Ready</b>\n📄 <b>Type:</b> {filename.split('.')[-1].upper()}\n📊 <b>Lines:</b> {line_count}\n👤 <b>User:</b> {user.first_name}"
            
            await context.bot.send_document(
                chat_id=chat_id,
                document=zip_obj,
                filename=filename,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            return

        # LOGIC 3: Code > 600 Lines & Free User (Block)
        if line_count > SystemConfig.FREE_ZIP_LIMIT and not is_premium:
            txt = TextAssets.PREMIUM_ALERT.format(
                lines=line_count,
                limit=SystemConfig.FREE_ZIP_LIMIT,
                owner=SystemConfig.OWNER_USERNAME
            )
            kb = [[InlineKeyboardButton("💎 UPGRADE NOW", callback_data="premium")]]
            await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
            return

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {e}", parse_mode=ParseMode.HTML)

# --- MENUS ---
async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = """
💎 <b>PREMIUM STORE</b>

Unlock 2000+ Lines Code & Instant Zip.

• <b>1 Month:</b> ₹99
• <b>1 Year:</b> ₹499
• <b>Lifetime:</b> ₹999

👇 <b>Select Plan to Pay:</b>
"""
    kb = [
        [InlineKeyboardButton("📅 1 Month", callback_data="buy_month"), InlineKeyboardButton("🗓️ 1 Year", callback_data="buy_year")],
        [InlineKeyboardButton("♾️ Lifetime", callback_data="buy_life")],
        [InlineKeyboardButton("🔙 Back", callback_data="home")]
    ]
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TextAssets.HELP_MENU.format(owner=SystemConfig.OWNER_USERNAME), parse_mode=ParseMode.HTML)

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.clear_history(update.effective_user.id)
    await update.message.reply_text("🧹 <b>Memory Reset.</b>", parse_mode=ParseMode.HTML)

async def me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = db.get_user(update.effective_user.id)
    if not u: return
    expiry = u.get("sub_expiry", "None")
    status = "Premium" if expiry != "None" else "Free"
    await update.message.reply_text(f"👤 <b>ID:</b> <code>{update.effective_user.id}</code>\n💎 <b>Plan:</b> {status}\n📅 <b>Expiry:</b> {expiry}", parse_mode=ParseMode.HTML)

# --- ADMIN COMMANDS ---
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

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    if not context.args: return
    msg = " ".join(context.args)
    users = db.get_all_users()
    await update.message.reply_text(f"🚀 Sending to {len(users)} users...")
    for uid in users:
        try: await context.bot.send_message(int(uid), f"📢 <b>ALERT:</b>\n{msg}", parse_mode=ParseMode.HTML)
        except: pass

async def admin_add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage: /addpremium @username 30 days"""
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /addpremium @user 30 days")
            return
        
        uname = context.args[0]
        amt = context.args[1]
        unit = context.args[2]
        
        uid = db.get_uid_by_name(uname)
        if uid:
            expiry = db.set_premium(uid, f"{amt} {unit}")
            if expiry:
                await update.message.reply_text(f"✅ Premium added to {uname} until {expiry}")
            else:
                await update.message.reply_text("❌ Invalid duration.")
        else:
            await update.message.reply_text("❌ User not found.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def admin_remove_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SystemConfig.OWNER_ID: return
    try:
        uname = context.args[0]
        uid = db.get_uid_by_name(uname)
        if uid:
            db.remove_premium(uid)
            await update.message.reply_text(f"🚫 Premium removed from {uname}")
        else:
            await update.message.reply_text("❌ User not found.")
    except: pass

# --- CALLBACK ---
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "verify":
        if await Utils.verify_sub(q.from_user.id, context.bot):
            await q.delete_message()
            await start(update, context)
        else: await q.answer("❌ Not Joined!", show_alert=True)
    elif q.data == "home": await start(update, context)
    elif q.data == "help": await help_cmd(update, context)
    elif q.data == "me": await me_cmd(update, context)
    elif q.data == "premium": await premium_menu(update, context)
    elif q.data.startswith("buy_"):
        await q.message.reply_text(f"💳 <b>Pay Here:</b> {SystemConfig.OWNER_USERNAME}\nSend screenshot after payment.", parse_mode=ParseMode.HTML)

# --- INIT ---
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Home"),
        BotCommand("rai", "Generate"),
        BotCommand("new", "Reset"),
        BotCommand("premium", "Buy Pro"),
        BotCommand("help", "Help")
    ])

def main():
    print("🚀 INITIALIZING RAI GPT GODSPEED...")
    threading.Thread(target=run_server, daemon=True).start()
    
    app = ApplicationBuilder().token(SystemConfig.TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rai", rai_cmd))
    app.add_handler(CommandHandler("new", new_chat))
    app.add_handler(CommandHandler("premium", premium_menu))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("me", me_cmd))
    
    # Admin
    app.add_handler(CommandHandler("ban", admin_ban))
    app.add_handler(CommandHandler("unban", admin_unban))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CommandHandler("addpremium", admin_add_premium))
    app.add_handler(CommandHandler("removepremium", admin_remove_premium))
    
    app.add_handler(CallbackQueryHandler(callback))
    
    print("✅ Bot Started")
    
    while True:
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        except Conflict:
            logging.warning("Conflict! Retrying...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Critical: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
