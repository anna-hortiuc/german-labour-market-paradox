# The German Labour Market Paradox — and What Comes Next

*Unemployment, skills shortages and the jobs of the future*

## Why this project

My task was to analyse why unemployment and skills shortages exist at the same time in Germany.
While working with the data, I realised this question can't be separated from another one:
which occupations and skills will be needed tomorrow, shaped by AI, automation and demography.
So I combined both topics. Today's paradox shows where the gap already exists; the look ahead shows where it is moving.

## In one sentence

Germany does not lack people, it lacks people with the right qualification. Half of the unemployed look for unskilled jobs, while six in ten vacancies require vocational training. Automation is already reshaping which occupations grow, but so far it has not pushed skilled workers into unemployment.

## Key findings

### 1. The paradox is about skill level
| Skill level | Share of unemployed | Share of vacancies | Unemployed per vacancy |
|---|---|---|---|
| Helfer (unskilled) | **50.5%** | 17.1% | **13.3** |
| Fachkraft (vocational training) | 28.0% | **60.7%** | **2.1** |
| Spezialist | 7.8% | 12.9% | 2.7 |
| Experte (university) | 8.1% | 9.3% | 4.0 |

*BA, Arbeitsmarkt nach Berufen, October 2026*

### 2. Shortages follow the business cycle
Shortage occupations: 178 (2019) → 126 (2020, Covid) → peak **202 (2022)** → 157 (2025).
Most are at Fachkraft level (84 of 157). Shortages among Experten fell fastest since 2022 (40 → 25, −38%). Software development, for example, is no longer a shortage occupation.

### 3. Production shrinks, work with people grows (2015–2025)
Total employment grew by **+13.4%**. Five groups in material production shrank, among them metalworking (−17.2%, −228,000 jobs) and textiles (−18.8%). Product design and arts & crafts shrank too (−3.6%), and sales stagnated (+0.2%).
Fastest growth came in **IT (+67.2%)**, education & social work (+43.8%, +669,000 jobs, the largest absolute gain) and healthcare (+24.6%).

### 4. Growth and shortage do not always go together
- **Growing & short:** healthcare, building services, education & social work
- **Growing, no shortage:** IT (+67%, only 7% of its occupations in shortage), management, marketing
- **Shrinking & still short:** metalworking (−17%), plastics & wood (−11%). One possible reason: workers leave faster than jobs disappear.

### 5. The more automatable, the slower the growth
Across 14 occupation segments, the share of automatable tasks (IAB, 2022) and employment growth are strongly negatively correlated (**r = −0.69**; −0.86 without IT).
Production work: 87.9% automatable → −15%. Social & cultural services: 13.5% automatable → +39%.
**Exception: IT.** Its automation potential rose most (largely due to generative AI), yet it grew fastest. Combined with the disappearing IT shortage, this may be an early signal of change.

### 6. Unemployment risk depends on skill level, not on automation
Unemployed per 100 employed: Fachkräfte in highly automatable jobs **4.0**, Helfer **16 to 40** at any automation level.

### 7. Shortage occupations pay slightly less, but wages there rise faster
Median gross monthly wage, shortage vs. no shortage: Fachkräfte 3,763 € vs 3,932 € (−4%), Spezialisten 4,632 € vs 5,047 € (−8%). Wages in shortage occupations grew faster (+14.2% vs +10.4%). Nursing is an exception: it pays above average and is still short, so working conditions matter too.

### 8. The paradox exists in every state
In all 16 states there are far more unemployed per vacancy at Helfer level (7.7 in Bavaria to 39.8 in Berlin) than at Fachkraft level (1.4 to 5.0). Hessen: 4.8 overall, 11.3 for Helfer, 2.3 for Fachkräfte.

### 9. Demography affects all occupations
22.4% of employees (7.8 million) are aged 55–64 and will retire within about ten years. Employment of people aged 65+ grew by 15.2% in one year. The share of workers aged 55+ is similar across low, medium and high automation potential (23–26%).

## Hypotheses: status

| # | Hypothesis | Status |
|---|---|---|
| H1 | Shortage is concentrated in hands-on occupations, unemployment elsewhere | ✅ Supported |
| H2 | Highly automatable occupations are rarely shortage occupations | 🟡 Mixed: Fachkräfte have the highest share of automatable jobs (48%) and the largest shortage |
| H3 | Shortage occupations have an older workforce | ⏳ Open: no public data on age by occupation |
| H4 | Part of the "shortage" reflects pay and working conditions | 🟡 Partly supported, weak effect |
| H5 | Shrinking occupations are routine work, growing ones care, crafts and IT | ✅ Supported (r = −0.69) |

## What the data cannot show

- Only part of all vacancies is reported to the BA, especially for Experten.
- Civil servants (e.g. school teachers) are barely covered: "no shortage" in BA data does not mean no shortage in reality.
- Substitution potential measures which tasks *could* be automated, not job loss.
- All results are correlations, not causal effects.

Full list: [`notes/sources.md`](notes/sources.md)

## Open questions for discussion

- IT employment grows fastest while its shortage disappears. Is the IT market saturating, or is AI changing the work?
- Why do shrinking occupations still have shortages?
- Will AI close the gap, or shift unemployment towards office jobs?

## Charts

Interactive HTML charts in [`output/charts`](output/charts). Download a file and open it in a browser.

| Chart | Notebook |
|---|---|
| Unemployed vs vacancies by skill level | `02_mismatch_by_level` |
| Employment change 2015–2025 by occupation group | `03_shrinking_growing` |
| Growth × shortage matrix (36 groups) | `04_matrix` |
| Wages vs shortage | `05_wages` |
| Unemployed per vacancy by state (heatmap) | `06_regions` |
| Automation potential vs employment growth | `07_automation` |

## Data sources

Bundesagentur für Arbeit (Engpassanalyse, Arbeitsmarkt nach Berufen, Beschäftigungsstatistik, Strukturwandel nach Berufen, Entgeltatlas), IAB-Kurzbericht 5/2024. Details: [`notes/sources.md`](notes/sources.md)

## Project structure

```
data/raw/        original downloads (never edited)
data/clean/      cleaned, merged data
notebooks/       analysis, one notebook per question (01–07)
output/charts/   interactive charts (HTML)
notes/           sources and limitations
```

## Setup

```bash
pip install -r requirements.txt
```

## Status

🟢 Analysis done for the core questions · 🟡 Next: apprenticeship market, new occupations, article

---
Author: Anna Hortiuc · [LinkedIn](https://www.linkedin.com/in/anna-hortiuc)
