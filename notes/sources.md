# Data sources

Record every file: source, link, download date, notes.

| File         | Source | Link | Downloaded | Notes |
|--------------|--------|------|------------|-------|
|              | BA – Arbeitsmarkt nach Berufen (KldB 2010) | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Themen-im-Fokus/Berufe/Berufe-Nav.html | | |
| epa_2025.csv | BA – Fachkräfteengpassanalyse 2019–2025 | https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Interaktive-Statistiken/Fachkraeftebedarf/Engpassanalyse-Nav.html (Gesamtdownload CSV) | 2026-11-15 | all years, regions, skill levels |
|              | BA – Entgeltatlas | | | |
|              | BA – Ausbildungsmarkt | | | |
|              | BA – Beschäftigte nach Berufen (age) | | | |
|              | IAB – Job-Futuromat | https://job-futuromat.iab.de/ | | values per occupation only online → manual table |
|              | IAB – Kurzbericht 05/2024 | | | aggregates of substitution potential |
|              | BIBB/IAB – QuBe projections | | | |
|              | Destatis – GENESIS 12421 (population projection) | https://www-genesis.destatis.de/ | | |
|              | KldB 2010 classification | | | key for merging |

## Limitations to keep in mind

- Only ~half of vacancies are reported to the BA.
- Job-Futuromat measures technical potential, not job loss.
- BA rounds values to multiples of ten for statistical confidentiality.
- From 2025 on, BA no longer lists occupations without a rating ("keine Bewertung möglich"); compare years using rated occupations only.
- BA data barely covers civil servants (Beamte), e.g. school teachers: no shortage in BA data ≠ no shortage in reality.
- Some indicator values look implausible (e.g. vacancy time 0 days for train drivers) and must be checked.
