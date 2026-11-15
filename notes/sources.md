# Data sources

Record every file: source, link, download date, notes.

| File                                        | Source | Link | Downloaded | Notes |
|---------------------------------------------|--------|------|------------|-------|
| berufe-heft-kldb2010-dwol-0-202610-xlsx.xlsx | BA – Arbeitsmarkt nach Berufen (KldB 2010) | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Themen-im-Fokus/Berufe/Berufe-Nav.html | 2026-11-15 | October 2026; Germany, East/West, Länder; by skill level incl. Helfer || BA – Arbeitsmarkt nach Berufen (KldB 2010) | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Themen-im-Fokus/Berufe/Berufe-Nav.html | | |
| epa_2025.csv                                | BA – Fachkräfteengpassanalyse 2019–2025 | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Interaktive-Statistiken/Fachkraeftebedarf/Engpassanalyse-Nav.html (Gesamtdownload CSV) | 2026-11-15 | all years, regions, skill levels |
| entgelte_berufe_2025.xlsx | BA – Entgeltatlas (Entgelte nach Berufen im Vergleich) | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Themen-im-Fokus/Berufe/Berufe-Nav.html | 2026-11-15 | Dec 2025; median gross monthly wage, 140 groups × skill level ||                                              | BA – Ausbildungsmarkt | | | |
|                                             | BA – Beschäftigte nach Berufen (age) | | | |
|                                             | IAB – Job-Futuromat | https://job-futuromat.iab.de/ | | values per occupation only online → manual table |
| iab_kurzbericht_2024_05.pdf | IAB – Kurzbericht 05/2024 | https://doku.iab.de/kurzber/2024/kb2024-05.pdf | 2026-11-15 | Abb. A2: substitution potential 2022 by segment (values typed manually) ||                                             | BIBB/IAB – QuBe projections | | | |
|                                             | Destatis – GENESIS 12421 (population projection) | https://www-genesis.destatis.de/ | | |
|                                             | KldB 2010 classification | | | key for merging |
| kldb2010-zeitreihe-d-0-xlsx.xlsx | BA – Beschäftigte nach Berufen (KldB 2010), Zeitreihe Quartalszahlen | https://statistik.arbeitsagentur.de | 2026-11-15 | Germany, 36 occupation groups, 2012–03/2026 |
| swb_*.csv (4 files) | BA – Strukturwandel nach Berufen (dashboard) | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Interaktive-Statistiken/Strukturwandel-Berufe/Strukturwandel-Berufe-Nav.html | 2026-11-15 | by IAB substitution potential 2022; 14 segments; core group only |
| laenderreport_2026q1.xlsx | BA – Länderreport über Beschäftigte, Deutschland | https://statistik.arbeitsagentur.de | 2026-11-15 | March 2026; age, qualification; no age × occupation |
| swb/alo_level/age_x_substitution.csv (4 files) | BA – Strukturwandel nach Berufen, Soziodemografie | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Interaktive-Statistiken/Strukturwandel-Berufe/Strukturwandel-Berufe-Nav.html | 2026-11-15 | 2025; employed & unemployed by skill level/age × substitution potential |

## Limitations to keep in mind

- Only ~half of vacancies are reported to the BA.
- Job-Futuromat measures technical potential, not job loss.
- BA rounds values to multiples of ten for statistical confidentiality.
- From 2025 on, BA no longer lists occupations without a rating ("keine Bewertung möglich"); compare years using rated occupations only.
- BA data barely covers civil servants (Beamte), e.g. school teachers: no shortage in BA data ≠ no shortage in reality.
- Some indicator values look implausible (e.g. vacancy time 0 days for train drivers) and must be checked.
- Employment totals differ between files: Zeitreihe counts all SvB (34.9 M), Strukturwandel only the "core group" (32.3 M); do not compare levels across files.
- Wages are medians for full-time employees; wages above the social security ceiling are shown as "> 8,050 €" and set to 8,050.
- Wages (3-digit groups) and shortage (4-digit occupations) are matched at group level: a group counts as "shortage" if at least one occupation in it is a shortage occupation.
- 2021 Engpassanalyse values are missing (X) for many occupations due to the KldB revision; 2021 counts are not comparable.
- Shortage share per group is based on few rated occupations in small groups (e.g. group 21: only 2) — interpret with caution.
- Substitution potential 2022 by segment was typed manually from IAB-Kurzbericht 5/2024 (Abb. A2); earlier years are not labelled in the chart. Correlation across only 14 segments is indicative, not causal.