import re

class EscalationEngine:
    def __init__(self):
        self.safety_triggers = ["swell", "swelling", "smoke", "hot", "fire", "exploded", "burning"]
        self.security_triggers = ["hacked", "stolen account", "unauthorized charge", "fraud", "unrecognized bill", "compromised"]
        self.damage_triggers = ["cracked", "shattered", "water", "pool", "laundry", "dropped", "liquid", "muffled speaker", "broken screen"]
        self.frustration_triggers = ["ridiculous", "worst", "samsung", "android", "lawsuit", "sue", "legal", "unusable", "terrible", "unacceptable", "switching"]

    def decide(self, text, intent):
        clean_text = text.lower()
        
        if any(term in clean_text for term in self.safety_triggers) and "battery" in clean_text:
            return {
                "escalate": True,
                "reason": "Physical safety hazard reported (battery expansion/overheating risk).",
                "risk_level": "CRITICAL"
            }

        if any(term in clean_text for term in self.security_triggers):
            return {
                "escalate": True,
                "reason": "Account security compromise or financial transaction dispute requiring human verification.",
                "risk_level": "HIGH"
            }

        if intent == "device_physical_damage" or any(term in clean_text for term in self.damage_triggers):
            return {
                "escalate": True,
                "reason": "Hardware replacement or liquid damage requires AppleCare store service inspection.",
                "risk_level": "MEDIUM"
            }

        if any(term in clean_text for term in self.frustration_triggers) or clean_text.isupper():
            return {
                "escalate": True,
                "reason": "High customer frustration or brand churn risk requiring empathetic human intervention.",
                "risk_level": "MEDIUM"
            }

        if "hours" in clean_text or "days" in clean_text or "weeks" in clean_text:
            numbers = re.findall(r'\d+', clean_text)
            if numbers and int(numbers[0]) > 5:
                return {
                    "escalate": True,
                    "reason": "Persistent unresolved issue (>5 hours/days) unresponsive to standard self-service.",
                    "risk_level": "MEDIUM"
                }

        return {
            "escalate": False,
            "reason": "Routine technical inquiry suitable for automated self-service guidance.",
            "risk_level": "LOW"
        }
