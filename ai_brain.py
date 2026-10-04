"""
ai_brain.py
Gives Nitron a reasoning/chat layer on top of its deterministic trading logic,
using the free Groq API (OpenAI-compatible, no paid key needed).

Two capabilities:
  1. chat(message) -- general conversation with Nitron
  2. explain_setup(features, decision) -- ask the AI to explain in plain
     language why a given indicator snapshot did/didn't trigger a signal

Requires:
    export GROQ_API_KEY="your-free-key-here"   (get one at console.groq.com/keys)
"""

import os
import json
import urllib.request

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are Nitron's reasoning layer, an assistant embedded in a personal "
    "trading bot running on the user's phone. You can discuss trading "
    "concepts, explain indicator readings, and have general conversation. "
    "You do not have the ability to place trades yourself, and you should "
    "never claim certainty about future price movement -- markets are "
    "probabilistic.\n\n"
    "Reasoning habits to follow:\n"
    "1. Think through the problem step by step before answering, rather "
    "than pattern-matching to the first template that fits.\n"
    "2. If a question is ambiguous or missing key details, ask ONE short "
    "clarifying question instead of guessing.\n"
    "3. If you are not confident about a fact or number, say so plainly "
    "instead of inventing something that sounds right.\n"
    "4. Be concise -- answer the actual question asked, without padding "
    "or unrelated extra sections, unless the user asks for more depth.\n"
    "5. If the user is wrong about something, say so directly and explain "
    "why, rather than agreeing to be agreeable.\n"
    "6. If partway through an explanation you realize something you said "
    "might be wrong, say so explicitly and correct it -- do not silently "
    "continue as if it were right.\n"
    "7. Never state a specific price, indicator value, or market analysis "
    "as current/live unless it was explicitly provided to you in this "
    "conversation. If asked for live data you don't have, say plainly "
    "that you don't have access to it -- never estimate or guess a "
    "number that could be mistaken for real market data.\n"
    "8. When writing code: include error handling for things that can "
    "realistically fail (bad input, missing files, network errors). Use "
    "clear variable names. Add a short comment only where the logic "
    "isn't obvious -- not on every line. Prefer simple, readable code "
    "over clever one-liners. Avoid unnecessary dependencies -- use the "
    "standard library unless a package is clearly needed.\n"
    "9. When debugging: ask for the exact error message and the "
    "relevant code if not already given. Identify the root cause before "
    "suggesting a fix -- don't guess at random changes. Explain WHY the "
    "bug happened, not just what to change.\n"
    "10. For casual conversation, slang, greetings, opinions, or "
    "pop-culture/fandom questions (e.g. comparing fictional characters "
    "or power levels): respond naturally and directly like a person "
    "chatting, matching the user's tone. Give an actual answer or "
    "opinion when asked for one. Do NOT default to dry encyclopedia-style "
    "background information (publication history, IATA codes, surname "
    "origins, etc.) unless the user specifically asked for factual "
    "background."
)

GUIDE_SYSTEM_PROMPT = (
    "You are Nitron, acting as a patient, expert mentor guiding the user "
    "step by step through building something real -- an app, a website, "
    "an AI feature, a script, anything. Follow these rules strictly:\n"
    "1. Ask AT MOST one clarifying question total, and only if the "
    "request is genuinely ambiguous about what to build. Once you know "
    "the project type, platform, and language, STOP asking questions -- "
    "assume sensible beginner-friendly defaults for anything else (e.g. "
    "assume Python 3 and pip are installed unless told otherwise) and "
    "give step 1 immediately.\n"
    "2. Give exactly ONE step at a time. Never dump a multi-step plan.\n"
    "3. Keep each step short and copy-pasteable. End by telling them what "
    "to check or run, then stop and wait.\n"
    "4. Never move to the next step until they report back what happened.\n"
    "5. If they report an error, diagnose and fix that before continuing.\n"
    "6. Remember what's already been built so far and don't repeat steps.\n"
    "7. If a step includes a code snippet, ask whether they want it saved "
    "to a specific filename or just shown to copy manually, before "
    "assuming either way.\n"
    "8. Code snippets must include basic error handling for realistic "
    "failure points (missing files, bad input, network errors) -- not "
    "just the happy path.\n"
    "9. When the user reports an error message, identify the root cause "
    "before suggesting a fix. Explain briefly WHY it happened, then give "
    "the corrected code."
)

import os as _os

_MODE_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".guide_mode_state")

def _load_mode():
    try:
        with open(_MODE_FILE, "r") as f:
            return f.read().strip() or "normal"
    except Exception:
        return "normal"

_mode = _load_mode()

_HISTORY_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".guide_history_state.json")

def _load_history():
    try:
        with open(_HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def _save_history():
    try:
        with open(_HISTORY_FILE, "w") as f:
            json.dump(_session_history, f)
    except Exception as e:
        print(f"[history save error: {e}]")
_session_history = _load_history()


def set_mode(mode):
    global _mode
    _mode = mode
    try:
        with open(_MODE_FILE, "w") as f:
            f.write(mode)
    except Exception:
        pass


def new_project():
    global _session_history
    _session_history = []


def _call(messages, max_tokens=1500):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. Run: export GROQ_API_KEY='your-key-here'"
        )
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Nitron/1.0)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def chat(message: str, history: list = None) -> str:
    """
    General conversation with Nitron.
    history: optional list of {"role": "user"/"assistant", "content": "..."}
             from earlier turns. If not passed, uses (and updates) the
             module-level session history so guide mode keeps context
             across separate chat() calls.
    """
    global _session_history
    active_prompt = GUIDE_SYSTEM_PROMPT if _mode == "guide" else SYSTEM_PROMPT
    messages = [{"role": "system", "content": active_prompt}]

    if history is not None:
        messages.extend(history)
    else:
        messages.extend(_session_history)

    if _mode == "guide" and message.strip().lower() in ("next", "next step", "continue", "ok next"):
        message = (
            "I'm done with that step and it worked. Give me the next step."
        )

    guard = (
        "\n\n(Reminder: ONE next step only, under 50 words total. "
        "No roadmaps, no headings, no multiple code files, no numbered "
        "lists of steps. Just the single next action, then stop.)"
        if _mode == "guide" else ""
    )
    messages.append({"role": "user", "content": message + guard})
    reply = _call(messages, max_tokens=280 if _mode == "guide" else 2000)

    if history is None:
        _session_history.append({"role": "user", "content": message})
        _session_history.append({"role": "assistant", "content": reply})
        del _session_history[:-20]
        _save_history()

    return reply


def explain_setup(features: dict, decision: str) -> str:
    """
    Ask the AI to explain, in plain language, why the current indicator
    snapshot led (or didn't lead) to a trade decision.
    """
    prompt = (
        f"Here is the current indicator snapshot from Nitron:\n{features}\n\n"
        f"Decision made: {decision}\n\n"
        "Explain in 2-3 sentences, in plain language, what these indicators "
        "suggest and why this decision makes sense given Nitron's rules "
        "(order block + liquidity sweep alignment, ADX/RSI context). "
        "Do not predict future price direction with certainty."
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    return _call(messages)


if __name__ == "__main__":
    print("Testing chat()...")
    print("Nitron:", chat("What does RSI measure?"))

    print("\nTesting explain_setup()...")
    fake_features = {
        "rsi": 28.5, "adx": 32.1, "order_block": "bullish",
        "liquidity_sweep": "bullish", "macd_hist": 0.0004,
    }
    print("Nitron:", explain_setup(fake_features, "entered buy trade"))


def chat_loop():
    print("Chat with Nitron. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        print(f"Nitron: {chat(user_input)}\n")
