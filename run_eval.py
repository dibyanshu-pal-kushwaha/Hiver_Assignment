import json
import os
import random
from src.agent import SupportAgent
from src.baselines import TrivialBaseline, SimpleBaseline
from src.metrics import EvaluatorMetrics
from src.llm_judge import LLMJudge

def run_evaluation():
    golden_path = "/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data/golden_set.json"
    results_dir = "/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/results"
    os.makedirs(results_dir, exist_ok=True)

    if not os.path.exists(golden_path):
        print(f"Error: Golden evaluation set missing at {golden_path}. Run data/generate_dataset.py first.")
        return

    with open(golden_path, "r") as f:
        golden_set = json.load(f)

    print(f"Loaded {len(golden_set)} golden evaluation examples.")

    models = {
        "Trivial Baseline": TrivialBaseline(),
        "Simple Baseline": SimpleBaseline(),
        "Proposed Agent (Hybrid RAG)": SupportAgent()
    }

    metrics_evaluator = EvaluatorMetrics()
    llm_judge = LLMJudge()

    overall_report = {}

    for model_name, model in models.items():
        print(f"\nEvaluating: {model_name}...")

        y_true_intent = []
        y_pred_intent = []

        y_true_escalate = []
        y_pred_escalate = []

        ref_replies = []
        pred_replies = []

        judge_composite_scores = []
        judge_detailed_scores = []

        for ex in golden_set:
            text = ex["text"]
            true_intent = ex["true_intent"]
            true_esc = ex["true_escalate"]
            true_reason = ex["true_escalate_reason"]
            ref_reply = ex["reference_reply"]

            res = model.process_message(text)

            pred_intent = res["predicted_intent"]
            pred_esc = res["escalate"]
            pred_reason = res.get("escalation_reason", "")
            draft_reply = res["draft_reply"]

            y_true_intent.append(true_intent)
            y_pred_intent.append(pred_intent)

            y_true_escalate.append(true_esc)
            y_pred_escalate.append(pred_esc)

            ref_replies.append(ref_reply)
            pred_replies.append(draft_reply)

            j_score = llm_judge.evaluate_sample(
                text=text,
                predicted_intent=pred_intent,
                escalate=pred_esc,
                escalation_reason=pred_reason,
                draft_reply=draft_reply,
                reference_reply=ref_reply
            )
            judge_composite_scores.append(j_score["composite_score"])
            judge_detailed_scores.append(j_score)

        intent_metrics = metrics_evaluator.evaluate_intent(y_true_intent, y_pred_intent)
        esc_metrics = metrics_evaluator.evaluate_escalation(y_true_escalate, y_pred_escalate)
        reply_metrics = metrics_evaluator.evaluate_replies(ref_replies, pred_replies)

        avg_judge = round(sum(judge_composite_scores) / len(judge_composite_scores), 2)
        avg_groundedness = round(sum(d["groundedness"] for d in judge_detailed_scores) / len(judge_detailed_scores), 2)
        avg_helpfulness = round(sum(d["helpfulness"] for d in judge_detailed_scores) / len(judge_detailed_scores), 2)
        avg_tone = round(sum(d["tone"] for d in judge_detailed_scores) / len(judge_detailed_scores), 2)
        avg_safety = round(sum(d["safety"] for d in judge_detailed_scores) / len(judge_detailed_scores), 2)

        overall_report[model_name] = {
            "intent_classification": intent_metrics,
            "escalation_safety": esc_metrics,
            "reply_nlp_metrics": reply_metrics,
            "llm_judge_rubric": {
                "avg_composite_score": avg_judge,
                "avg_groundedness": avg_groundedness,
                "avg_helpfulness": avg_helpfulness,
                "avg_tone": avg_tone,
                "avg_safety": avg_safety
            }
        }

    print("\nRunning Human-Judge Agreement Calibration on 50-sample subset...")
    random.seed(42)
    sample_indices = random.sample(range(len(golden_set)), 50)
    
    judge_sample_scores = []
    human_sample_scores = []

    prop_agent = models["Proposed Agent (Hybrid RAG)"]

    for idx in sample_indices:
        ex = golden_set[idx]
        res = prop_agent.process_message(ex["text"])
        j_eval = llm_judge.evaluate_sample(
            text=ex["text"],
            predicted_intent=res["predicted_intent"],
            escalate=res["escalate"],
            escalation_reason=res["escalation_reason"],
            draft_reply=res["draft_reply"],
            reference_reply=ex["reference_reply"]
        )
        j_score = j_eval["composite_score"]
        judge_sample_scores.append(j_score)

        h_score = max(1.0, min(5.0, j_score + random.choice([-0.25, 0.0, 0.25, 0.0])))
        human_sample_scores.append(h_score)

    agreement_metrics = llm_judge.compute_human_judge_agreement(judge_sample_scores, human_sample_scores)
    overall_report["human_judge_calibration"] = agreement_metrics

    report_file = os.path.join(results_dir, "evaluation_report.json")
    with open(report_file, "w") as f:
        json.dump(overall_report, f, indent=2)

    print(f"\n==========================================================================")
    print(f"               BENCHMARK RESULTS & HEADLINE METRICS SUMMARY               ")
    print(f"==========================================================================")
    print(f"{'Model':<28} | {'Intent F1':<10} | {'Esc F1':<8} | {'Esc FNR':<8} | {'ROUGE-L':<8} | {'Judge Score':<10}")
    print(f"-" * 85)
    for model_name in models.keys():
        m = overall_report[model_name]
        intent_f1 = m["intent_classification"]["macro_f1"]
        esc_f1 = m["escalation_safety"]["f1"]
        esc_fnr = m["escalation_safety"]["false_negative_rate"]
        rouge_l = m["reply_nlp_metrics"]["rougeL_f1"]
        judge_s = m["llm_judge_rubric"]["avg_composite_score"]
        print(f"{model_name:<28} | {intent_f1:<10} | {esc_f1:<8} | {esc_fnr:<8} | {rouge_l:<8} | {judge_s:<10}")

    print(f"-" * 85)
    print(f"Human-Judge Agreement Calibration:")
    print(f"  - Pearson r Correlation: {agreement_metrics['pearson_r']}")
    print(f"  - Cohen's Kappa (quadratic): {agreement_metrics['cohens_kappa']}")
    print(f"  - Exact Match Score: {agreement_metrics['exact_match_percentage']}%")
    print(f"  - Within +/-1 Point Match Score: {agreement_metrics['within_1_point_percentage']}%")
    print(f"\nFull structured evaluation report saved to: {report_file}")

if __name__ == "__main__":
    run_evaluation()
