import json
from pathlib import Path

import pandas as pd

from utils.claude import test_connection
from utils.config import DATASET_OUTPUT_DIR
from utils.dataset import generate_dataset


def check_claude_connection(model):
    """Run a lightweight Claude health check and return whether it succeeded."""
    print(f"Testing Claude connection with model: {model}")
    result = test_connection(model=model)
    if result == "OK":
        print("Claude connection successful.")
        return True

    print(f"Claude connection failed or returned unexpected response: {result}")
    return False


def run_health_check_dataset(model, output_dir=DATASET_OUTPUT_DIR):
    """Generate one small test batch and save it locally as part of startup health checks."""
    if not check_claude_connection(model):
        return False

    print("Running dataset generation health check...")
    batch_data = generate_dataset(n_users=2, batch_id=0)
    save_batch(batch_data, batch_id=0, output_dir=output_dir)
    print("Dataset health check succeeded.")
    return True


def save_batch(batch_data, batch_id, output_dir="."):
    output_path = Path(output_dir) / f"circle_dataset_batch_{batch_id:02d}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(batch_data, handle, ensure_ascii=False, indent=2)
    print(f"Saved batch {batch_id} to {output_path}")


def generate_and_save_datasets(n_batches=4, n_users=25, output_dir=DATASET_OUTPUT_DIR):
    all_users = []

    for batch_id in range(1, n_batches + 1):
        print(f"Generating batch {batch_id}/{n_batches}...")
        batch_data = generate_dataset(n_users=n_users, batch_id=batch_id)
        save_batch(batch_data, batch_id, output_dir=output_dir)
        all_users.extend(batch_data)

    print(f"Generated and saved {len(all_users)} users across {n_batches} batches.")
    return all_users

def analyze_saved_datasets(output_dir=DATASET_OUTPUT_DIR):
    dataset_path = Path(output_dir)
    dataset_files = sorted(dataset_path.glob("circle_dataset_batch_*.json"))
    if not dataset_files:
        print(f"No dataset files found in {output_dir}. Please generate them first.")
        return []

    all_users = []
    for path in dataset_files:
        with path.open("r", encoding="utf-8") as handle:
            batch = json.load(handle)
        print(f"Loaded {len(batch)} users from {path.name}")
        all_users.extend(batch)

    print(f"Loaded {len(all_users)} users across {len(dataset_files)} batches.")
    return all_users


def flatten_saved_dataset_to_dataframe(output_dir=DATASET_OUTPUT_DIR):
    users = analyze_saved_datasets(output_dir=output_dir)
    if not users:
        return pd.DataFrame()

    rows = []
    for user in users:
        row = {
            "user_id": user.get("user_id"),
        }
        answers = user.get("answers") or user.get("onboarding_responses") or {}
        if isinstance(answers, dict):
            for question, answer in answers.items():
                row[question] = answer
        else:
            row["answers"] = answers
        rows.append(row)

    df = pd.DataFrame(rows)
    print(f"Flattened dataset into DataFrame with shape {df.shape}")
    return df


def add_profile_text(df):
    """Add a single text profile for each user from all question columns."""
    if df.empty:
        return df

    question_cols = [c for c in df.columns if c != "user_id"]
    df = df.copy()
    df["profile_text"] = df.apply(
        lambda row: "\n".join([f"{col}: {row[col]}" for col in question_cols]),
        axis=1,
    )
    print(f"Added profile_text column with {len(df)} profiles")
    return df
