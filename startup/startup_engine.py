# ~/Nitron/startup/startup_engine.py

import json
import os
import random


IDEA_FILE = "startup/ideas.json"


def load_ideas():

    if not os.path.exists(IDEA_FILE):
        return []

    try:

        with open(IDEA_FILE, "r") as file:

            return json.load(file)

    except Exception:

        return []



def save_ideas(ideas):

    with open(IDEA_FILE, "w") as file:

        json.dump(
            ideas,
            file,
            indent=4
        )



def create_idea():

    ideas = [

        "AI productivity assistant",

        "Smart education platform",

        "Business automation service",

        "Personal finance tracker",

        "Developer collaboration platform",

        "AI customer support system"

    ]


    idea = random.choice(ideas)


    data = load_ideas()

    data.append({
        "idea": idea,
        "stage": "idea"
    })


    save_ideas(data)


    return f"""
Startup Idea:

{idea}

Next Steps:
1. Research users
2. Build MVP
3. Test with customers
4. Improve product
"""



def analyze_business(name):

    return f"""
Business Analysis:

Name:
{name}

Questions:
- Who is the customer?
- What problem does it solve?
- How will it make money?
- What is the smallest MVP?
"""



def create_mvp(name):

    return f"""
MVP Plan:

Project:
{name}

Version 1:
- Basic working feature
- User testing
- Feedback collection
- Improvements

Technology:
- Frontend
- Backend
- Database
- Deployment
"""



def ask_startup(command):

    command = command.lower().strip()


    if "startup idea" in command:

        return create_idea()


    if "analyze business" in command:

        name = command.replace(
            "analyze business",
            ""
        ).strip()

        return analyze_business(name)



    if "mvp" in command:

        name = command.replace(
            "make mvp plan",
            ""
        ).strip()

        return create_mvp(name)



    return None
