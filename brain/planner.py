"""
Nitron Task Planner
"""

from datetime import datetime


class Planner:
    def __init__(self):
        self.tasks = []

    def create_plan(self, goal):
        """
        Create a new plan for a goal.
        """
        plan = {
            "goal": goal,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "steps": [],
            "completed": False
        }

        self.tasks.append(plan)
        return plan

    def add_step(self, goal, step):
        """
        Add a step to an existing plan.
        """
        for plan in self.tasks:
            if plan["goal"] == goal:
                plan["steps"].append({
                    "task": step,
                    "done": False
                })
                return True
        return False

    def complete_step(self, goal, index):
        """
        Mark a step as completed.
        """
        for plan in self.tasks:
            if plan["goal"] == goal:
                if 0 <= index < len(plan["steps"]):
                    plan["steps"][index]["done"] = True

                    if all(step["done"] for step in plan["steps"]):
                        plan["completed"] = True

                    return True
        return False

    def get_plan(self, goal):
        """
        Return a plan by goal.
        """
        for plan in self.tasks:
            if plan["goal"] == goal:
                return plan
        return None

    def list_plans(self):
        """
        Return all plans.
        """
        return self.tasks

    def clear(self):
        """
        Remove all plans.
        """
        self.tasks = []


planner = Planner()
