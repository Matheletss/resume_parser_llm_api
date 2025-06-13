import os
import json
from datetime import datetime

SAVE_DIR = "training_data"

def save_training_example(prompt_input: str, parsed_resume):
    print("🔧 save_training_example() called")

    os.makedirs(SAVE_DIR, exist_ok=True)

    if isinstance(parsed_resume, str):
        try:
            parsed_resume = json.loads(parsed_resume)
            print("✅ parsed_resume decoded successfully")
        except json.JSONDecodeError as e:
            print("❌ Failed to decode parsed_resume:", e)
            return

    # 🕒 Use timestamp as filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"
    full_path = os.path.join(SAVE_DIR, filename)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump({
                "messages": [
                    { "role": "user", "content": prompt_input },
                    { "role": "assistant", "content": parsed_resume }
                ]
            }, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved training data to: {full_path}")
    except Exception as e:
        print("❌ Error writing file:", e)
