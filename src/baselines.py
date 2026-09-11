import random

class TrivialBaseline:
    def __init__(self):
        self.name = "Trivial Baseline (Majority/Always-Escalate)"

    def process_message(self, tweet_text):
        return {
            "input_text": tweet_text,
            "predicted_intent": "software_update",
            "intent_confidence": 1.0,
            "escalate": True,
            "escalation_reason": "Trivial policy: Escalate 100% of customer tickets.",
            "draft_reply": "Thank you for contacting Apple Support. Please visit https://support.apple.com for help with your device."
        }


class SimpleBaseline:
    def __init__(self):
        self.name = "Simple Baseline (Keyword/Heuristic)"

    def process_message(self, tweet_text):
        clean = tweet_text.lower()
        
        if "battery" in clean or "charge" in clean:
            intent = "hardware_battery"
        elif "update" in clean or "ios" in clean:
            intent = "software_update"
        elif "bill" in clean or "charge" in clean or "id" in clean or "refund" in clean:
            intent = "account_billing"
        elif "bluetooth" in clean or "airpods" in clean or "wifi" in clean:
            intent = "connectivity_bluetooth"
        elif "crash" in clean or "app" in clean:
            intent = "app_crash_bug"
        elif "crack" in clean or "screen" in clean or "water" in clean:
            intent = "device_physical_damage"
        else:
            intent = "general_inquiry_feedback"

        escalate = len(tweet_text) > 120 or "!!" in tweet_text or "help" in clean
        reason = "Heuristic length (>120 chars) or punctuation trigger." if escalate else "Short message auto-handled."

        static_replies = {
            "hardware_battery": "Check your battery settings in iOS.",
            "software_update": "Try updating your iPhone over Wi-Fi.",
            "account_billing": "Go to reportaproblem.apple.com to check purchases.",
            "connectivity_bluetooth": "Turn Bluetooth off and on again.",
            "app_crash_bug": "Restart your phone and update apps.",
            "device_physical_damage": "Bring your device to an Apple Store.",
            "general_inquiry_feedback": "Check apple.com for details."
        }

        reply = static_replies.get(intent, "Please visit support.apple.com.")

        return {
            "input_text": tweet_text,
            "predicted_intent": intent,
            "intent_confidence": 0.5,
            "escalate": escalate,
            "escalation_reason": reason,
            "draft_reply": reply
        }
