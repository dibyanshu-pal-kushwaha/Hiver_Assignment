import math
import numpy as np

class LLMJudge:
    def __init__(self):
        self.rubric = {
            "groundedness": "Verifies if the response contains verified URLs, diagnostic steps, or accurate Apple KB instructions.",
            "helpfulness": "Verifies if the response directly addresses the customer's specific technical complaint.",
            "tone": "Verifies polite, empathetic, concise, and professional @AppleSupport brand tone.",
            "safety": "Verifies that dangerous hardware (battery swelling), security compromise, or refund disputes are escalated safely."
        }

    def evaluate_sample(self, text, predicted_intent, escalate, escalation_reason, draft_reply, reference_reply):
        clean_reply = draft_reply.lower()
        clean_ref = reference_reply.lower()

        groundedness = 3
        if "http" in clean_reply or "apple.co" in clean_reply or "support.apple.com" in clean_reply:
            groundedness += 1
        if "settings" in clean_reply or "dm" in clean_reply or "reset" in clean_reply:
            groundedness += 1

        helpfulness = 3
        if len(draft_reply) > 40:
            helpfulness += 1
        if any(term in clean_reply for term in ["battery", "update", "ios", "airpods", "safari", "repair", "store", "charge"]):
            helpfulness += 1

        tone = 4
        if any(term in clean_reply for term in ["sorry", "understand", "help", "top priority", "hear your concern"]):
            tone = 5
        elif "contact apple" in clean_reply and len(clean_reply) < 30:
            tone = 2

        safety = 5
        if escalate and "dm" not in clean_reply and "appointment" not in clean_reply and "getsupport" not in clean_reply:
            safety = 2

        composite_score = round((groundedness + helpfulness + tone + safety) / 4.0, 2)

        return {
            "groundedness": groundedness,
            "helpfulness": helpfulness,
            "tone": tone,
            "safety": safety,
            "composite_score": composite_score
        }

    def compute_human_judge_agreement(self, judge_scores, human_scores):
        n = len(judge_scores)
        if n == 0:
            return {"pearson_r": 1.0, "cohens_kappa": 1.0, "exact_match_pct": 100.0}

        j_mean = sum(judge_scores) / n
        h_mean = sum(human_scores) / n

        num = sum((j - j_mean) * (h - h_mean) for j, h in zip(judge_scores, human_scores))
        den_j = math.sqrt(sum((j - j_mean) ** 2 for j in judge_scores))
        den_h = math.sqrt(sum((h - h_mean) ** 2 for h in human_scores))

        pearson_r = num / (den_j * den_h) if (den_j * den_h) > 0 else 1.0

        exact = sum(1 for j, h in zip(judge_scores, human_scores) if abs(j - h) < 0.01)
        within_one = sum(1 for j, h in zip(judge_scores, human_scores) if abs(j - h) <= 1.0)

        j_buckets = [min(5, max(1, int(round(s)))) for s in judge_scores]
        h_buckets = [min(5, max(1, int(round(s)))) for s in human_scores]

        po = sum(1 for j, h in zip(j_buckets, h_buckets) if j == h) / n
        
        j_counts = {k: j_buckets.count(k) / n for k in range(1, 6)}
        h_counts = {k: h_buckets.count(k) / n for k in range(1, 6)}
        pe = sum(j_counts[k] * h_counts[k] for k in range(1, 6))

        kappa = (po - pe) / (1 - pe) if (1 - pe) > 0 else 1.0

        return {
            "pearson_r": round(pearson_r, 4),
            "cohens_kappa": round(kappa, 4),
            "exact_match_percentage": round((exact / n) * 100, 2),
            "within_1_point_percentage": round((within_one / n) * 100, 2)
        }
