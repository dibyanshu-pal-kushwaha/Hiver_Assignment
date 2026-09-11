import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class IntentClassifier:
    def __init__(self, kb_data=None):
        self.intents = [
            "hardware_battery",
            "software_update",
            "account_billing",
            "connectivity_bluetooth",
            "app_crash_bug",
            "device_physical_damage",
            "general_inquiry_feedback"
        ]
        
        self.keyword_rules = {
            "hardware_battery": ["battery", "drain", "charging", "overheating", "warm", "dying", "battery health"],
            "software_update": ["update", "ios", "ios17", "ios16", "boot loop", "freeze", "installing", "apple logo"],
            "account_billing": ["apple id", "charge", "refund", "unauthorized", "locked", "password", "billed", "subscription", "purchase"],
            "connectivity_bluetooth": ["bluetooth", "airpods", "wifi", "wi-fi", "cellular", "disconnect", "pairing", "signal"],
            "app_crash_bug": ["crash", "app", "safari", "camera", "glitch", "closing", "black screen"],
            "device_physical_damage": ["cracked", "shattered", "water", "liquid", "dropped", "broken", "speaker"],
            "general_inquiry_feedback": ["store", "hours", "trade-in", "price", "specs", "buy", "compatibility", "location"]
        }

        self.pipeline = self._train_model()

    def _train_model(self):
        training_texts = []
        training_labels = []

        training_seeds = {
            "hardware_battery": [
                "battery draining fast after update", "phone overheating while charging",
                "battery health dropped to 80%", "charger port not working", "phone dies at 20% battery"
            ],
            "software_update": [
                "stuck on apple logo during update", "unable to verify update ios",
                "phone frozen after downloading ios update", "update takes 10 hours", "ios update failed error"
            ],
            "account_billing": [
                "unauthorized purchase on app store", "apple id locked for security",
                "want refund for subscription", "charged twice for icloud storage", "forgot apple id password"
            ],
            "connectivity_bluetooth": [
                "airpods disconnecting randomly", "bluetooth won't connect to car",
                "wifi keeps dropping connection", "cellular data not working", "airpod sound muffled"
            ],
            "app_crash_bug": [
                "safari crashes immediately when opening", "camera app black screen",
                "photos app keeps freezing", "third party apps closing automatically", "keyboard glitch in messages"
            ],
            "device_physical_damage": [
                "cracked front screen shattered", "dropped phone in water pool",
                "back glass broken after drop", "speaker grille liquid damage", "volume button stuck broken"
            ],
            "general_inquiry_feedback": [
                "what is the trade-in value for iphone", "apple store opening hours holiday",
                "is iphone 13 compatible with magsafe", "where is nearest apple store", "how much is icloud 200gb"
            ]
        }

        for intent, seeds in training_seeds.items():
            for seed in seeds:
                training_texts.append(seed)
                training_labels.append(intent)
                training_texts.append(f"@AppleSupport {seed} please help")
                training_labels.append(intent)

        model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', LogisticRegression(C=1.0, random_state=42))
        ])
        model.fit(training_texts, training_labels)
        return model

    def predict(self, text):
        clean_text = text.lower()
        
        probs = self.pipeline.predict_proba([clean_text])[0]
        classes = self.pipeline.classes_
        top_idx = probs.argmax()
        predicted_intent = classes[top_idx]
        confidence = float(probs[top_idx])

        if confidence < 0.4:
            for intent, keywords in self.keyword_rules.items():
                if any(kw in clean_text for kw in keywords):
                    predicted_intent = intent
                    confidence = 0.85
                    break

        return {
            "intent": predicted_intent,
            "confidence": round(confidence, 4)
        }
