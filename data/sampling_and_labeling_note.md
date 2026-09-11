# Golden Evaluation Set: Sampling & Labeling Methodology

## 1. Overview & Dataset Source
This evaluation dataset comprises **200 hand-curated and labeled customer-support threads** targeted specifically at **@AppleSupport**, derived from customer support conversations on Twitter.

## 2. Sampling Strategy
To ensure the evaluation dataset reflects real-world operational challenges rather than clean synthetic data, sampling was executed using a **stratified multi-criteria approach**:

1. **Stratification by Real-world Intent Distribution**:
   - `hardware_battery` (18%): Battery drain, charging issues, overheating.
   - `software_update` (22%): iOS post-update slowdowns, installation errors, boot loops.
   - `account_billing` (20%): Apple ID locks, unauthorized App Store charges, subscriptions.
   - `connectivity_bluetooth` (14%): AirPods dropouts, Wi-Fi connectivity, cellular signal loss.
   - `app_crash_bug` (12%): Native app freezes (Safari, Photos) and 3rd party crashes.
   - `device_physical_damage` (8%): Cracked screen, liquid damage, broken buttons.
   - `general_inquiry_feedback` (6%): Store hours, trade-in value, device compatibility.

2. **Hard-Case Over-sampling**:
   - **Ambiguous Queries (15%)**: Tweets containing multiple complaints (e.g. "My phone updated and now battery drains AND Wi-Fi drops").
   - **High-Emotion / Threat of Churn (10%)**: Swear words, ALL CAPS, threats to switch to Android.
   - **Out-of-Scope / Security Vulnerabilities (5%)**: Requests for free hardware, claims of stolen accounts needing password override.

## 3. Labeling Protocol & Annotation Rules
Each example in `golden_set.json` contains:
- `tweet_id`: Unique identifier.
- `text`: Incoming customer message.
- `true_intent`: Assigned single primary intent from 7 target classes.
- `true_escalate`: Boolean (`true` or `false`).
- `true_escalate_reason`: Clear operational reason for the escalation decision.
- `reference_reply`: Grounded historical gold-standard response.

### Escalation Guidelines:
- **MUST ESCALATE (`true`) if**:
  1. Physical damage / liquid exposure requiring hardware replacement / AppleCare store visit.
  2. Account security / unauthorized charges where human verification is required.
  3. High-frustration customers threatening legal action or expressing severe dissatisfaction after multiple failed self-service attempts.
  4. Ambiguous safety or hardware expansion (battery swelling/overheating dangerously).
- **AUTO-HANDLE (`false`) if**:
  1. Routine diagnostic or settings guidance can resolve the issue (e.g. forced restart, checking `Settings > Battery`, checking Wi-Fi router settings).
  2. Public standard URL guidance (e.g., Apple ID password self-service link).

## 4. Quality Control & Agreement Verification
- Dual-pass annotation review was conducted to ensure label consistency.
- Any disagreement on escalation boundaries was resolved by strictly prioritizing customer safety and security (when in doubt, escalate).
