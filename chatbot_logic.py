import wikipedia

def search_browser(query):
    """
    Generate a Google Search URL as fallback.
    """
    try:
        encoded_query = query.replace(" ", "+")
        google_link = f"https://www.google.com/search?q={encoded_query}"
        return None, google_link
    except Exception as e:
        print("Google link creation failed:", e)
        return None, None


def get_bot_response(message):
    try:
        msg = message.strip().lower()

        # Friendly greetings
        if msg in ["hi", "hello", "hey"]:
            return ("👋 Hello! How can I assist you today?", True)

        elif msg in ["bye", "goodbye", "see you"]:
            return ("👋 Bye! Take care.", True)

        elif msg in ["thanks", "thank you"]:
            return ("You're very welcome! 😊 I'm here whenever you need me.", True)

        # Try Wikipedia first
        try:
            summary = wikipedia.summary(message, sentences=2)
            return (f"📘 Wikipedia Answer:<br>{summary}", True)
        except Exception:
            pass

        # Google search fallback
        _, link = search_browser(message)
        if link:
            response = (
                f"🌐 I couldn't find a specific answer, but try this below link:<br>"
                f"<a href='{link}' target='_blank'>🔍 View on Google</a>"
            )
            return (response, False)

        return ("😕 I couldn’t find anything helpful. Try rephrasing.", False)

    except Exception as e:
        print("Chatbot error:", e)
        return ("⚠️ Something went wrong. Please try again later.", False)