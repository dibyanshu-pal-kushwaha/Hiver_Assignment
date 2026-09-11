from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from rouge_score import rouge_scorer
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class EvaluatorMetrics:
    def __init__(self):
        self.rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.smooth = SmoothingFunction().method1

    def evaluate_intent(self, y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)

        return {
            "accuracy": round(acc, 4),
            "macro_f1": round(f1_macro, 4),
            "weighted_f1": round(f1_weighted, 4),
            "macro_precision": round(p_macro, 4),
            "macro_recall": round(r_macro, 4)
        }

    def evaluate_escalation(self, y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', zero_division=0)
        
        fn = sum(1 for t, p in zip(y_true, y_pred) if t and not p)
        tp = sum(1 for t, p in zip(y_true, y_pred) if t and p)
        fp = sum(1 for t, p in zip(y_true, y_pred) if not t and p)
        tn = sum(1 for t, p in zip(y_true, y_pred) if not t and not p)
        
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        return {
            "accuracy": round(acc, 4),
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1": round(f1, 4),
            "false_negative_rate": round(fnr, 4),
            "false_positive_rate": round(fpr, 4)
        }

    def evaluate_replies(self, references, predictions):
        r1_list, r2_list, rl_list, bleu_list = [], [], [], []

        for ref, pred in zip(references, predictions):
            scores = self.rouge.score(ref, pred)
            r1_list.append(scores['rouge1'].fmeasure)
            r2_list.append(scores['rouge2'].fmeasure)
            rl_list.append(scores['rougeL'].fmeasure)

            ref_tokens = ref.lower().split()
            pred_tokens = pred.lower().split()
            bleu = sentence_bleu([ref_tokens], pred_tokens, smoothing_function=self.smooth)
            bleu_list.append(bleu)

        return {
            "rouge1_f1": round(sum(r1_list) / len(r1_list), 4),
            "rouge2_f1": round(sum(r2_list) / len(r2_list), 4),
            "rougeL_f1": round(sum(rl_list) / len(rl_list), 4),
            "bleu_score": round(sum(bleu_list) / len(bleu_list), 4)
        }
