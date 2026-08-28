import json
import os
import shutil
from datetime import datetime

DATABASE = "knowledge.json"
BACKUP = "knowledge_backup.json"


class KnowledgeBase:

    def __init__(self):

        self.data = self.load()

    def default_database(self):

        return {

            "python": {},

            "cpp": {},

            "general": {},

            "cybersecurity": {},

            "trading": {},

            "physics": {},

            "mathematics": {},

            "history": {},

            "science": {},

            "projects": {},

            "notes": {},

            "metadata": {

                "created": str(datetime.now()),

                "last_updated": str(datetime.now()),

                "version": "2.0"

            }

        }

    def load(self):

        if not os.path.exists(DATABASE):

            data = self.default_database()

            self.save_database(data)

            return data

        try:

            with open(DATABASE, "r") as file:

                return json.load(file)

        except:

            data = self.default_database()

            self.save_database(data)

            return data

    def save_database(self, database):

        with open(DATABASE, "w") as file:

            json.dump(database, file, indent=4)

    def save(self):

        self.data["metadata"]["last_updated"] = str(datetime.now())

        self.save_database(self.data)

    def backup(self):

        shutil.copy(DATABASE, BACKUP)

    def restore(self):

        if os.path.exists(BACKUP):

            shutil.copy(BACKUP, DATABASE)

            self.data = self.load()

            return True

        return False

    def add(self, category, title, content):

        category = category.lower()

        title = title.lower()

        if category not in self.data:

            self.data[category] = {}

        self.data[category][title] = {

            "content": content,

            "created": str(datetime.now()),

            "views": 0,

            "tags": []

        }

        self.save()

        return "Knowledge saved."

    def read(self, category, title):

        category = category.lower()

        title = title.lower()

        if category not in self.data:

            return None

        if title not in self.data[category]:

            return None

        self.data[category][title]["views"] += 1

        self.save()

        return self.data[category][title]["content"]

    def update(self, category, title, new_content):

        category = category.lower()

        title = title.lower()

        if category not in self.data:

            return "Category not found."

        if title not in self.data[category]:

            return "Topic not found."

        self.data[category][title]["content"] = new_content

        self.save()

        return "Updated."

    def delete(self, category, title):

        category = category.lower()

        title = title.lower()

        if category in self.data:

            if title in self.data[category]:

                del self.data[category][title]

                self.save()

                return "Deleted."

        return "Topic not found."

    def categories(self):

        result = []

        for category in self.data:

            if category != "metadata":

                result.append(category)

        return result

    def list_topics(self, category):

        category = category.lower()

        if category not in self.data:

            return []

        return sorted(self.data[category].keys())

    def statistics(self):

        total_topics = 0

        total_views = 0

        largest = ""

        largest_size = 0

        for category in self.data:

            if category == "metadata":

                continue

            size = len(self.data[category])

            total_topics += size

            if size > largest_size:

                largest_size = size

                largest = category

            for topic in self.data[category]:

                total_views += self.data[category][topic]["views"]

        return {

            "topics": total_topics,

            "views": total_views,

            "largest_category": largest,

            "categories": len(self.categories())

        }

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for category in self.data:

            if category == "metadata":

                continue

            for topic in self.data[category]:

                info = self.data[category][topic]

                if keyword in topic:

                    results.append((category, topic))

                    continue

                if keyword in info["content"].lower():

                    results.append((category, topic))

        return results

    def add_tag(self, category, title, tag):

        category = category.lower()

        title = title.lower()

        tag = tag.lower()

        if category not in self.data:

            return

        if title not in self.data[category]:

            return

        if tag not in self.data[category][title]["tags"]:

            self.data[category][title]["tags"].append(tag)

            self.save()

    def search_tag(self, tag):

        tag = tag.lower()

        results = []

        for category in self.data:

            if category == "metadata":

                continue

            for topic in self.data[category]:

                if tag in self.data[category][topic]["tags"]:

                    results.append((category, topic))

        return results

    def export(self, filename):

        with open(filename, "w") as file:

            json.dump(self.data, file, indent=4)

        return filename

    def import_file(self, filename):

        with open(filename, "r") as file:

            self.data = json.load(file)

        self.save()

        return "Imported successfully."

    def clear_category(self, category):

        category = category.lower()

        if category in self.data:

            self.data[category] = {}

            self.save()

            return "Category cleared."

    def reset(self):

        self.data = self.default_database()

        self.save()

        return "Database reset."

    def info(self):

        stats = self.statistics()

        return f"""
Knowledge Database

Categories : {stats['categories']}
Topics     : {stats['topics']}
Views      : {stats['views']}
Largest    : {stats['largest_category']}

Version    : {self.data['metadata']['version']}
Created    : {self.data['metadata']['created']}
Updated    : {self.data['metadata']['last_updated']}
"""
