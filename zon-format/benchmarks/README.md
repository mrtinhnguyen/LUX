# Unified Benchmark Results

## JSON vs LUX

| Dataset | Records | JSON Size | LUX Size | Compression | JSON tk | LUX tk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| analytics | 60 | 5.9 KB | 2.1 KB | **+63.6%** | 2343 | 1396 |
| complex_nested | 1000 | 381.3 KB | 296.8 KB | **+22.2%** | 121213 | 108563 |
| employees | 100 | 13.7 KB | 5.9 KB | **+56.9%** | 3624 | 2083 |
| github-repos | 100 | 33.7 KB | 21.0 KB | **+37.8%** | 12124 | 8693 |
| hikes | 1 | 451.0 B | 264.0 B | **+41.5%** | 139 | 96 |
| internet_github_repos | 100 | 411.4 KB | 345.6 KB | **+16.0%** | 113357 | 98980 |
| internet_posts | 100 | 24.0 KB | 20.5 KB | **+14.6%** | 6093 | 5249 |
| internet_random_users | 50 | 53.4 KB | 44.5 KB | **+16.7%** | 19860 | 18637 |
| internet_users | 10 | 4.0 KB | 3.1 KB | **+23.8%** | 1225 | 1093 |
| mongodb_irregular | 50 | 16.0 KB | 13.5 KB | **+15.6%** | 5832 | 5570 |
| orders | 50 | 20.1 KB | 14.1 KB | **+29.9%** | 6906 | 5814 |

### Summary
- **Total JSON (compact) size**: 963.9 KB
- **Total LUX size**: 767.3 KB
- **Overall compression**: 20.4%

## TOON Comparison
*(datasets with .toon files)*

| Dataset | Records | JSON Size | LUX Size | TOON Size | vs TOON | JSON tk | LUX tk | TOON tk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| hikes | 3 | 451.0 B | 264.0 B | 286.0 B | **+7.7%** | 139 | 96 | 104 |
