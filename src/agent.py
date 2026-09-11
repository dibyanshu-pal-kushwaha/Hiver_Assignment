from .intent_classifier import IntentClassifier
from .escalation_engine import EscalationEngine
from .reply_generator import ReplyGenerator

class SupportAgent:
    def __init__(self, kb_path="/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data/historical_kb.json"):
        self.intent_classifier = IntentClassifier()
        self.escalation_engine = EscalationEngine()
        self.reply_generator = ReplyGenerator(kb_path=kb_path)

    def process_message(self, tweet_text):
        intent_res = self.intent_classifier.predict(tweet_text)
        intent = intent_res["intent"]
        confidence = intent_res["confidence"]

        esc_res = self.escalation_engine.decide(tweet_text, intent)
        escalate = esc_res["escalate"]
        reason = esc_res["reason"]

        reply = self.reply_generator.draft_reply(tweet_text, intent, escalate, reason)

        return {
            "input_text": tweet_text,
            "predicted_intent": intent,
            "intent_confidence": confidence,
            "escalate": escalate,
            "escalation_reason": reason,
            "draft_reply": reply
        }
