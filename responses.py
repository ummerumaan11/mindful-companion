"""
Rule-based, keyword-triggered response flows inspired by common CBT
(cognitive behavioral therapy) psychoeducation techniques. Every technique
here is a standard, widely-published self-help coping tool (grounding,
breathing, thought reframing, gratitude) — nothing clinical or prescriptive.

This is intentionally NOT a general-purpose chatbot: it recognizes a small
set of topics via keywords and offers one relevant, well-known coping
technique per topic, rather than generating open-ended advice.
"""
import re

TOPICS = {
    "anxiety": {
        "keywords": [r"\banxious\b", r"\banxiety\b", r"\bnervous\b", r"\bpanick?y?\b", r"\bworried\b", r"\bworry\b"],
        "acknowledgment": "That sounds really uncomfortable to sit with. Anxiety can make everything feel more urgent than it is.",
        "technique_name": "5-4-3-2-1 grounding",
        "technique": (
            "This technique uses your senses to bring your attention back to the present moment:\n\n"
            "- Name **5** things you can see\n"
            "- Name **4** things you can touch\n"
            "- Name **3** things you can hear\n"
            "- Name **2** things you can smell\n"
            "- Name **1** thing you can taste\n\n"
            "Take your time with each one."
        ),
    },
    "stress": {
        "keywords": [r"\bstressed\b", r"\bstress\b", r"\boverwhelmed\b", r"\bburnt?[\s-]?out\b", r"\btoo much\b"],
        "acknowledgment": "It makes sense that you're feeling stretched thin. Being overwhelmed is exhausting.",
        "technique_name": "Box breathing",
        "technique": (
            "A simple way to calm your nervous system:\n\n"
            "1. Breathe in slowly for **4 seconds**\n"
            "2. Hold for **4 seconds**\n"
            "3. Breathe out slowly for **4 seconds**\n"
            "4. Hold for **4 seconds**\n\n"
            "Repeat this for a minute or two."
        ),
    },
    "low_mood": {
        "keywords": [r"\bsad\b", r"\bdown\b", r"\bdepress\w*\b", r"\bhopeless\b", r"\bempty\b", r"\blow\b"],
        "acknowledgment": "Thank you for sharing that. It's okay to not be okay, and naming it takes something.",
        "technique_name": "One small thing",
        "technique": (
            "When everything feels heavy, big goals can feel impossible. Instead, try naming just "
            "**one small, doable thing** for the next hour — drinking a glass of water, opening a window, "
            "sending one text. Not to fix everything, just to take one small step."
        ),
    },
    "negative_thoughts": {
        "keywords": [r"\bi'?m (a )?failure\b", r"\bi am (a )?failure\b", r"\bhate myself\b", r"\bnot good enough\b", r"\beveryone hates me\b", r"\bi'?m worthless\b", r"\bi am worthless\b"],
        "acknowledgment": "That's a really harsh thing to be carrying about yourself. Thoughts like that can feel completely true even when they're distorted by how we're feeling.",
        "technique_name": "Thought reframe",
        "technique": (
            "Try asking yourself:\n\n"
            "- What's the evidence *for* this thought, and what's the evidence *against* it?\n"
            "- What would I say to a friend who told me this about themselves?\n"
            "- Is there a more balanced way to think about this situation?\n\n"
            "You don't have to believe the reframe right away — just notice there might be more than one way to see it."
        ),
    },
    "sleep": {
        "keywords": [r"\bcan'?t sleep\b", r"\binsomnia\b", r"\btired\b", r"\bexhausted\b", r"\bno sleep\b"],
        "acknowledgment": "Poor sleep makes everything else so much harder to deal with.",
        "technique_name": "Wind-down check",
        "technique": (
            "A few things that reliably help sleep, if you haven't tried them tonight:\n\n"
            "- Dim lights and put the phone away 30 minutes before bed\n"
            "- Write down anything on your mind so it's 'out of your head' and on paper\n"
            "- Keep the room cool and dark\n\n"
            "If your mind is racing, it's okay to get up and do something calm for a few minutes rather than lying there frustrated."
        ),
    },
}


def find_topic(text: str):
    """Returns the topic dict for the first matching topic, or None."""
    text = text.lower()
    for topic_id, topic in TOPICS.items():
        for pattern in topic["keywords"]:
            if re.search(pattern, text):
                return topic_id, topic
    return None, None


FALLBACK_RESPONSES = [
    "Thanks for sharing that. Would you like to tell me a bit more about what's on your mind?",
    "I'm listening. What's been the hardest part of today?",
    "That sounds like a lot to carry. Is there something specific you'd like to talk through?",
]

GREETING = (
    "Hi, I'm here to listen. I can offer a few grounding and coping techniques if something's on your mind — "
    "what's going on today?"
)
