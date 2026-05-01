def clean_marathi(text):
    """
    Optimizes Marathi text for professional TTS pronunciation.
    """
    replacements = {
        "भारत": "भारत देश",
        "₹": "रुपये",
        "%": "टक्के",
        "cm": "सेंटीमीटर",
        "pm": "पंतप्रधान",
        "$": "डॉलर",
        "km": "किलोमीटर",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Add rhythmic pauses (Critical for authoritative news tone)
    # The '...' tells the TTS to breathe between headlines
    text = text.replace("।", "। ... ")
    text = text.replace(".", "। ... ")

    return text
