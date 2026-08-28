def image_prompt(subject, style="realistic"):
    return f"Create a high-quality {style} image of {subject}."


def video_prompt(subject, duration=30):
    return (
        f"Create a {duration}-second video about {subject}. "
        "Include an introduction, main content, smooth transitions, "
        "background music, and a cinematic ending."
    )
