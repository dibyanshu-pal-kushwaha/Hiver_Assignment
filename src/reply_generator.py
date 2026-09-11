import json
import os

class ReplyGenerator:
    def __init__(self, kb_path="/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data/historical_kb.json"):
        self.kb = self._load_kb(kb_path)

    def _load_kb(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []

    def draft_reply(self, text, intent, escalate, escalation_reason):
        matched_entry = None
        for entry in self.kb:
            if entry["intent"] == intent:
                matched_entry = entry
                break

        if not matched_entry:
            matched_entry = {
                "sample_response": "We want to help you with your Apple device. Please reach out to our team via Direct Message so we can investigate further.",
                "url": "https://getsupport.apple.com"
            }

        if escalate:
            reply = (
                f"We hear your concern and want to make sure you get expert care right away. "
                f"Due to the nature of your issue ({escalation_reason.lower()[:-1]}), "
                f"please DM us your iOS version and device serial number, or schedule an Apple Support appointment: {matched_entry['url']}"
            )
            return reply

        reply = matched_entry["sample_response"]
        return reply
