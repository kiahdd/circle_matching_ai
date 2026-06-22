#%%
import argparse

# Import the default Claude model and default dataset folder path.
from utils.config import CLAUDE_MODEL_HAIKU, DATASET_OUTPUT_DIR
# Import workflow utilities for dataset generation, health checks, and analysis.
from utils.workflow import (
    analyze_saved_datasets,
    generate_and_save_datasets,
    run_health_check_dataset,
)


def main(command=None, **kwargs):
    # Build a small CLI so we can choose generation vs. analysis at runtime.
    parser = argparse.ArgumentParser(description="CircleMatch pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for generating new synthetic dataset batches.
    gen_parser = subparsers.add_parser("generate", help="Generate and save dataset batches")
    gen_parser.add_argument("--n-batches", type=int, default=2, help="Number of dataset batches to generate")
    gen_parser.add_argument("--n-users", type=int, default=25, help="Number of users per batch")

    # Subcommand for analyzing previously generated datasets.
    analyze_parser = subparsers.add_parser("analyze", help="Analyze existing saved datasets")
    analyze_parser.add_argument("--path", type=str, default=DATASET_OUTPUT_DIR, help="Path to saved dataset files")

    if command is None:
        # Parse CLI arguments when run from the terminal or notebook with %run.
        args, unknown = parser.parse_known_args()
        if unknown:
            # Ignore extra arguments injected by notebook/kernel environments.
            print(f"Ignoring unknown arguments: {unknown}")

        if not args.command:
            parser.print_help()
            return
    else:
        # Allow direct programmatic execution from a notebook.
        args = argparse.Namespace(
            command=command,
            n_batches=kwargs.get("n_batches", 2),
            n_users=kwargs.get("n_users", 25),
            path=kwargs.get("path", DATASET_OUTPUT_DIR),
        )

    # Generate new data when the user asks for it.
    if args.command == "generate":
        print("CircleMatch dataset generation")
        model = CLAUDE_MODEL_HAIKU
        # Run a lightweight health check before generating a larger dataset.
        if not run_health_check_dataset(model, output_dir=DATASET_OUTPUT_DIR):
            return
        generate_and_save_datasets(
            n_batches=args.n_batches,
            n_users=args.n_users,
            output_dir=DATASET_OUTPUT_DIR,
        )

    # Analyze datasets already saved on disk.
    elif args.command == "analyze":
        print("CircleMatch analysis on existing datasets")
        analyze_saved_datasets(output_dir=args.path)


# Standard Python entry point for the script.
if __name__ == "__main__":
    main()

# %%
