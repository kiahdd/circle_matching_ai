#%%
from utils.claude import test_connection
from utils.dataset import generate_dataset
from utils.config import CLAUDE_MODEL_HAIKU, CLAUDE_MODEL_SONNET, CLAUDE_MODEL_OPUS

#%%
def check_claude_connection(model):
    """Run a lightweight Claude health check and return whether it succeeded."""
    print(f"Testing Claude connection with model: {model}")
    result = test_connection(model=model)
    if result == "OK":
        print("Claude connection successful.")
        return True

    print(f"Claude connection failed or returned unexpected response: {result}")
    return False


def run_dataset_demo():
    """Run a sample dataset generation flow after the connection test."""
    print("Generating a sample dataset after successful connection test...")
    response = generate_dataset()
    print("Synthetic dataset response:")
    print(response)


def main():
    """Entry point for CircleMatch.

    This startup flow performs a Claude connection check first, and only
    generates sample data after the connection is verified.
    """
    print("CircleMatch startup")

    model = CLAUDE_MODEL_HAIKU
    if not check_claude_connection(model):
        return

    run_dataset_demo()


if __name__ == "__main__":
    main()

# %%
