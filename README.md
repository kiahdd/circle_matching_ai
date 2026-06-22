# CircleMatch

An AI-powered social circle matching system focused on assembling small, meaningful groups from free-text onboarding responses.

## Project structure

- `main.py` - application entrypoint and orchestration layer
- `utils/` - reusable helper modules for data, matching, and bot support
- `notebooks/` - concept, architecture, and planning notebooks

## Initial scaffold

This repo is currently structured as an early-stage prototype with the following scaffold:

- `README.md` - project overview and structure
- `notebooks/00-project-structure.ipynb` - notebook describing the architecture and key components
- `utils/__init__.py` - utility package entrypoint
- `utils/data.py` - placeholder for data schema and persistence helpers
- `utils/matching.py` - placeholder for matching and clustering helpers
- `utils/telebot.py` - placeholder for Telegram bot integration helpers
- `main.py` - current application startup file

## What to build next

1. Define onboarding questions and answer storage
2. Add embedding generation and trait extraction
3. Implement grouping and circle formation logic
4. Add explanation generation and initial meetup prompts
5. Connect to Telegram or another chat frontend

## Notes

The current project scaffold is intentionally minimal. The first iteration should validate whether free-text onboarding can be converted into coherent circles of 4–6 people before adding coordination or scheduling features.
