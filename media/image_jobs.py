"""
Nitron Image Jobs
"""

import os
import json
from datetime import datetime

OUTPUT = os.path.expanduser("~/Nitron/media/generated")

os.makedirs(OUTPUT, exist_ok=True)


def create_image(prompt):

    filename = prompt.lower().replace(" ", "_")

    data = {
        "prompt": prompt,
        "created": datetime.now().isoformat(),
        "status": "pending",
        "output": f"{filename}.png"
    }

    job = os.path.join(
        OUTPUT,
        f"{filename}.json"
    )

    with open(job, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "status": "success",
        "job": job,
        "image": os.path.join(
            OUTPUT,
            f"{filename}.png"
        )
    }
