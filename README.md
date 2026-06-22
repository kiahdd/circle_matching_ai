# CircleMatch

An AI-powered social circle matching system focused on assembling small, meaningful groups from free-text onboarding responses.

## Current status

- Dataset generation is implemented and tested through `main.py`.
- Generated batches are saved under the `datasets/` folder.
- Health-check generation uses Claude Haiku for a lightweight validation run.
- The next step is embedding generation and clustering in `utils/matching.py`.

## Project structure

- `main.py` - application entrypoint and orchestration layer
- `utils/` - reusable helper modules for data, matching, and bot support
- `datasets/` - generated synthetic dataset files
- `notebooks/` - concept, architecture, and planning notebooks

## Current code

- `utils/config.py` - configuration for Claude model, token budget, and dataset output path
- `utils/dataset.py` - dataset generation, JSON extraction, and validation
- `utils/matching.py` - placeholder for matching, embedding, and clustering helpers
- `utils/workflow.py` - dataset generation and batch saving workflow
- `main.py` - current application startup file

## Recommended workflow

1. Generate or load datasets.
2. Build user embeddings from saved dataset text.
3. Run clustering or matching logic to form circles.
4. Add explanation generation and introductory prompts.
5. Connect matching outputs to a chat or scheduling frontend.

## Notes

The current repo is now ready to move from data generation into analysis and matching. The primary next task is to implement embedding + clustering, then separate runtime flows for fresh dataset creation versus analysis of existing data.
