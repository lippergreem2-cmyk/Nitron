"""
Nitron AI Studio
Version 1
"""

from developer.project_analyzer import analyzer
from developer.project_planner import planner
from developer.project_builder import builder


class AIStudio:

    def build(self, request):

        print("=" * 50)
        print("        NITRON AI STUDIO")
        print("=" * 50)

        print("\nAnalyzing request...")

        analysis = analyzer.analyze(request)

        print("Type:", analysis["type"])
        print("Language:", analysis["language"])
        print("Framework:", analysis["framework"])
        print("Features:", analysis["features"])

        print("\nPlanning project...")

        plan = planner.plan(request)

        print("Folders:")
        for folder in plan["folders"]:
            print(" -", folder)

        print("\nFiles:")
        for file in plan["files"]:
            print(" -", file)

        print("\nBuilding project...")

        name = request.replace("create", "").strip().title()

        builder.create(name)

        print("\nProject created successfully!")

        return {
            "project": name,
            "analysis": analysis,
            "plan": plan,
            "status": "success"
        }


studio = AIStudio()
