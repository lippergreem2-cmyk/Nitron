"""
Nitron Project Engine
"""

from developer.project_analyzer import analyzer
from developer.project_builder import builder


class ProjectEngine:

    def build(self, request):

        info = analyzer.analyze(request)

        print("=" * 40)
        print("NITRON PROJECT ENGINE")
        print("=" * 40)
        print("Type      :", info["type"])
        print("Language  :", info["language"])
        print("Framework :", info["framework"])
        print("Features  :", ", ".join(info["features"]) or "None")
        print()

        name = request.replace("create", "").strip().title()

        builder.create(name)

        print("Project created.")

        return info


engine = ProjectEngine()
