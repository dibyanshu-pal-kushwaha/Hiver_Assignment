import json
import random
import os

def build_datasets():
    os.makedirs("/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data", exist_ok=True)

    kb_entries = [
        {
            "intent": "hardware_battery",
            "keywords": ["battery", "drain", "charge", "heat", "overheating", "dying"],
            "resolution_pattern": "Check Settings > Battery to see app power usage. If battery health is below 80%, recommend visiting an Apple Store.",
            "sample_response": "We want your iPhone to stay charged! Take a look at Settings > Battery to see if a specific app is using extra power: https://apple.co/BatteryInfo If issues persist, send us a DM.",
            "url": "https://support.apple.com/iphone/battery-health"
        },
        {
            "intent": "software_update",
            "keywords": ["update", "ios", "ios17", "ios16", "freeze", "stuck", "installing", "slow"],
            "resolution_pattern": "Force restart device, verify iCloud backup, ensure at least 5GB free storage before installing update.",
            "sample_response": "Let's get your iPhone updating smoothly again. Try a force restart: https://apple.co/ForceRestart If it's stuck on the Apple logo, connect to iTunes/Finder to update.",
            "url": "https://support.apple.com/ios/update"
        },
        {
            "intent": "account_billing",
            "keywords": ["apple id", "charge", "refund", "unauthorized", "locked", "password", "subscription", "billed"],
            "resolution_pattern": "Direct user to reportaproblem.apple.com for unrecognized billing, or iforgot.apple.com for locked Apple ID.",
            "sample_response": "We can help you review your account charges. Check your purchase history or request a refund at https://reportaproblem.apple.com. For account security, DM us your Apple ID email.",
            "url": "https://reportaproblem.apple.com"
        },
        {
            "intent": "connectivity_bluetooth",
            "keywords": ["bluetooth", "airpods", "wifi", "cellular", "disconnect", "pairing", "signal", "drop"],
            "resolution_pattern": "Forget network/device in Settings, Reset Network Settings, or reset AirPods by holding setup button for 15 seconds.",
            "sample_response": "Sorry your AirPods are disconnecting! Try resetting them by holding the button on the back of the charging case until the light flashes amber: https://apple.co/ResetAirPods",
            "url": "https://support.apple.com/airpods/reset"
        },
        {
            "intent": "app_crash_bug",
            "keywords": ["crash", "app", "safari", "camera", "freeze", "black screen", "glitch", "closing"],
            "resolution_pattern": "Force close app, check App Store for updates, restart device, or reinstall the affected app.",
            "sample_response": "App crashes are no fun. First, swipe up to force close the app, check App Store for updates, then restart your iPhone: https://apple.co/AppFix DM us if it keeps happening!",
            "url": "https://support.apple.com/apps/troubleshoot"
        },
        {
            "intent": "device_physical_damage",
            "keywords": ["cracked", "screen", "water", "dropped", "broken", "liquid", "speaker", "shattered"],
            "resolution_pattern": "Escalate to AppleCare store repair appointment. Water/physical damage cannot be fixed via software troubleshooting.",
            "sample_response": "We're sorry to hear about the screen damage! For safety and proper repair, please schedule a service appointment at an Apple Authorized Service Provider: https://getsupport.apple.com",
            "url": "https://getsupport.apple.com"
        },
        {
            "intent": "general_inquiry_feedback",
            "keywords": ["store", "hours", "trade-in", "price", "compatibility", "specs", "buy", "feedback"],
            "resolution_pattern": "Provide direct Apple support/store link or trade-in estimator link.",
            "sample_response": "Thanks for reaching out to Apple! You can check your trade-in estimate directly on our website: https://apple.co/TradeIn Let us know if you have any questions!",
            "url": "https://apple.co/TradeIn"
        }
    ]

    kb_path = "/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data/historical_kb.json"
    with open(kb_path, "w") as f:
        json.dump(kb_entries, f, indent=2)

    golden_examples = []
    
    templates = [
        ("@AppleSupport My iPhone 14 battery is dropping 20% per hour after updating to the latest iOS. Help!", "hardware_battery", False, "Standard battery drain troubleshooting applies.", "We know battery drain can be frustrating. Check Settings > Battery to see if an app is consuming unusual background power: https://apple.co/BatteryInfo"),
        ("@AppleSupport battery health dropped from 98% to 75% in two weeks and the back panel is swelling hot!!", "hardware_battery", True, "Physical swelling/overheating poses a safety hazard.", "Your safety is our top priority! Please immediately stop charging the device and schedule an urgent Apple Store inspection: https://getsupport.apple.com"),
        ("@AppleSupport phone gets warm while charging overnight. Is this normal?", "hardware_battery", False, "Normal thermal behavior check.", "It's normal for iPhone to warm up while charging. Learn more about optimal operating temperatures: https://support.apple.com/iphone/thermals"),
        ("@AppleSupport updated to iOS 17.2 and now my phone is stuck on the Apple logo boot loop!", "software_update", False, "Standard recovery mode instructions.", "Let's get your phone restored! Connect your iPhone to a computer and put it in Recovery Mode: https://support.apple.com/ios/recovery"),
        ("@AppleSupport iOS update says 'Unable to Verify Update' every single time I try.", "software_update", False, "Storage / network check requirement.", "This often happens if storage is low or connection interrupts. Delete the downloaded update in Settings > Storage and retry: https://apple.co/iOSUpdate"),
        ("@AppleSupport my phone has been updating for 14 hours straight and screen is completely frozen black.", "software_update", True, "Prolonged freeze requires human tier hardware/recovery support.", "Fourteen hours is definitely unexpected. We need to walk you through a forced recovery. Please send us a DM or contact AppleCare support directly: https://getsupport.apple.com"),
        ("@AppleSupport I got a random bill for $89.99 for an in-app purchase I NEVER made! Refund me now!", "account_billing", True, "Financial transaction refund requiring customer authentication.", "We understand your urgency regarding unauthorized charges. Please report the item immediately at https://reportaproblem.apple.com and DM us to secure your Apple ID."),
        ("@AppleSupport My Apple ID is locked for security reasons and I can't access my work email or iCloud!", "account_billing", False, "Self-service recovery url provided.", "You can unlock your account securely by following the steps at https://iforgot.apple.com. Let us know if you run into any issues during verification."),
        ("@AppleSupport Someone hacked my Apple ID and changed my email and phone number!! HELP ME NOW!!", "account_billing", True, "Account takeover / security compromise critical escalation.", "We take account security extremely seriously. Please call AppleCare account security immediately or DM us right now so our team can lock the account: https://getsupport.apple.com"),
        ("@AppleSupport My left AirPod Pro has no sound and won't connect to my iPhone 13.", "connectivity_bluetooth", False, "Standard AirPod reset procedure.", "Let's get sound back in both ears! Reset your AirPods by placing them in the case and holding the back button for 15 seconds: https://support.apple.com/airpods/reset"),
        ("@AppleSupport Bluetooth keeps disconnecting from my car audio every 2 minutes after updating.", "connectivity_bluetooth", False, "Network/Bluetooth reset guidance.", "Car pairing issues can often be fixed by tapping 'Forget This Device' in Bluetooth settings and pairing again: https://apple.co/BluetoothFix"),
        ("@AppleSupport AirPods case was washed in the laundry machine and now red light won't stop blinking.", "connectivity_bluetooth", True, "Liquid damage hardware failure.", "Liquid exposure can damage internal circuits. Please do not place them on a charger. Visit an Apple Store for service options: https://getsupport.apple.com"),
        ("@AppleSupport Safari closes instantly every time I try to open a new tab. Unusable!", "app_crash_bug", False, "Standard browser cache / restart troubleshooting.", "Sorry for the glitch! Try clearing Safari cache in Settings > Safari > Clear History and Website Data, then restart: https://apple.co/SafariHelp"),
        ("@AppleSupport Camera app shows a black screen whenever I switch to 0.5x ultra-wide lens.", "app_crash_bug", False, "Diagnostic restart and camera test.", "Let's check if this is software related. Restart your iPhone first. If the camera still shows black, send us a DM so we can run remote diagnostics."),
        ("@AppleSupport Dropped my phone on pavement and screen is completely shattered and touch screen isn't working.", "device_physical_damage", True, "Hardware replacement required.", "We're sorry to hear about the drop! You can view screen repair estimates and set up a service appointment here: https://support.apple.com/iphone/repair/screen-replacement"),
        ("@AppleSupport Phone fell into pool and speaker sounds muffled like underwater.", "device_physical_damage", True, "Liquid exposure hardware check.", "Please turn off your device and let it dry completely. If muffled sound persists after 24 hours, schedule an Apple Store diagnostic: https://getsupport.apple.com"),
        ("@AppleSupport What is the trade-in value for an iPhone 11 Pro 64GB in good condition?", "general_inquiry_feedback", False, "General self-service trade-in inquiry.", "You can get an instant trade-in quote for your iPhone 11 Pro on our website: https://apple.co/TradeIn Let us know if you need help ordering!"),
        ("@AppleSupport Are Apple Stores open on Thanksgiving day in NYC?", "general_inquiry_feedback", False, "Store locator inquiry.", "Store hours vary by location. You can check holiday hours for your local NYC store here: https://apple.co/StoreLocator")
    ]

    idx = 1
    while len(golden_examples) < 200:
        base = templates[(idx - 1) % len(templates)]
        text, intent, escalate, reason, ref_reply = base
        
        variant_suffix = ""
        if idx > len(templates):
            noises = [
                " Please fix ASAP!",
                " This is ridiculous @AppleSupport",
                " Anyone else having this problem??",
                " I've been a loyal customer for 10 years!!",
                " ughhhh fix this!!",
                " DM me please.",
                " Is there a fix for this?",
                " smh Apple..."
            ]
            variant_suffix = noises[(idx // len(templates)) % len(noises)]

        if idx % 11 == 0:
            text = f"{text} If this isn't fixed today I am switching to Samsung/Android forever!"
            escalate = True
            reason = "High customer churn threat / severe escalation requested."

        golden_examples.append({
            "tweet_id": f"tweet_{idx:03d}",
            "text": f"{text}{variant_suffix}",
            "true_intent": intent,
            "true_escalate": escalate,
            "true_escalate_reason": reason,
            "reference_reply": ref_reply
        })
        idx += 1

    golden_path = "/Users/dibyanshukushwaha/Desktop/AI_Support_Agent/data/golden_set.json"
    with open(golden_path, "w") as f:
        json.dump(golden_examples, f, indent=2)

if __name__ == "__main__":
    build_datasets()
