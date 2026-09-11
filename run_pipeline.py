import argparse
import json
import sys
from src.agent import SupportAgent

def main():
    parser = argparse.ArgumentParser(description="Run @AppleSupport AI Support Agent Pipeline")
    parser.add_argument("--text", type=str, help="Single tweet text to process")
    parser.add_argument("--file", type=str, help="JSON file containing list of tweets")
    args = parser.parse_args()

    agent = SupportAgent()

    if args.text:
        res = agent.process_message(args.text)
        print(json.dumps(res, indent=2))
    elif args.file:
        with open(args.file, "r") as f:
            tweets = json.load(f)
        results = [agent.process_message(t.get("text", t)) for t in tweets]
        print(json.dumps(results, indent=2))
    else:
        sample = "@AppleSupport My iPhone 14 battery drains completely in 2 hours after updating to iOS 17. Help!"
        print(f"\n--- Processing Sample Tweet ---\nInput: {sample}\n")
        res = agent.process_message(sample)
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
