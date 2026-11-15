# The German Labour Market Paradox — and What Comes Next

*Unemployment, skills shortages and the jobs of the future*

## Why this project

I was asked to analyse why unemployment and skills shortages exist at the same time in Germany.
While working with the data, I realised this question can't be separated from another one:
which occupations and skills will be in demand tomorrow, shaped by AI, automation and demography.
So this project combines both.

## Research questions

1. **Today:** Why do ~3 million unemployed people coexist with persistent shortages in specific occupations?
2. **Anatomy of the mismatch:** How much of the gap is qualification, region, age/demography or working conditions?
3. **Tomorrow:** Will AI and automation shrink the mismatch, or deepen it?

## Hypotheses

- H1: The shortage is concentrated in hands-on occupations (care, crafts, construction), while unemployment is concentrated elsewhere.
- H2: Occupations with high automation potential are rarely shortage occupations.
- H3: Shortage occupations have an older workforce, so demography will widen the gap.
- H4: Part of the "shortage" reflects pay and working conditions, not only a lack of people.

## Data sources

See [`notes/sources.md`](notes/sources.md).

## Project structure

```
data/raw/        original downloads (never edited)
data/clean/      cleaned, merged data
notebooks/       exploration and analysis
src/             reusable Python code
output/charts/   final visualisations
notes/           sources, methodology, limitations
```

## Setup

```bash
pip install -r requirements.txt
```

## Status

🟡 Phase 1 — questions, hypotheses, data collection
