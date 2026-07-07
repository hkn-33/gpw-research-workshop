[English](README.md) | Polski

# Warsztat analizy GPW

Warsztat agentowy do analizy akcji na Giełdzie Papierów Wartościowych w Warszawie: **co kupić, co sprzedać i kiedy**. Cztery perspektywy inwestowania w wartość — Buffett, Munger, Duan Yongping, Li Lu — zamienione w 14 powtarzalnych procedur badawczych z twardymi zasadami przeciw błędom poznawczym, dokładną arytmetyką dziesiętną i audytem liczb, zanim raport stanie się podstawą decyzji.

Inspirowane projektem [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) (MIT), zbudowane od nowa pod GPW z własnymi narzędziami.

> Narzędzie badawcze, nie porada inwestycyjna. Niczego nie kupuje — decyzje i zlecenia u brokera należą do Ciebie.

## Jak to działa

Skille to procedury w markdownie: precyzyjny przepis, który agent LLM wykonuje — jakie dane pobrać, jakie narzędzia uruchomić, co musi zawierać raport (zawsze zakończony przedziałami cenowymi, nigdy „z jednej strony... z drugiej strony"). Agenci to definicje ról dla cięższych skilli: zwiadowca danych, cztery niezależne perspektywy mistrzów zaprojektowane tak, by się spierały, audytor liczb, specjalista od timingu. Narzędzia to Python bez zależności: notowania, skaner, backtest, dokładna arytmetyka.

## Szybki start (Claude Code)

```bash
git clone <adres-twojego-repo> gpw && cd gpw
scripts\install-claude.bat        # Windows; macOS/Linux: sh scripts/install-claude.sh
copy portfolio.example.md portfolio.md   # i wpisz swoje pozycje
```

Otwórz folder w Claude Code i wpisz pierwszą komendę:

```
/gpw-scanner            # polowanie na sygnały kupna momentum+wartość
/gpw-analyze XTB        # pełna analiza 4 perspektyw z przedziałami kupna/sprzedaży
/gpw-portfolio          # rozkazy SPRZEDAJ / KUP / CZEKAJ dla Twoich pozycji
```

Raporty powstają w języku, w którym piszesz — piszesz po polsku, dostajesz raporty po polsku.

## Inne modele (ChatGPT, DeepSeek, Codex, ...)

Nic tu nie jest specyficzne dla Claude:

- **Dowolny model czatowy**: wklej treść pliku `skills/*.md` plus ticker jako prompt. Gdy skill odwołuje się do ról, dołóż pliki `agents/*.md`. Zasady projektu siedzą w `AGENTS.md` — wiele narzędzi agentowych (np. Codex) czyta go automatycznie.
- **Narzędzia**: czysty Python 3, sama biblioteka standardowa — `python tools/gpw_data.py quote PKN` działa wszędzie.

## 14 skilli

### Szukanie okazji
| Skill | Co robi | Czas |
|-------|---------|------|
| `gpw-scanner` | wybicia 60-dniowe + wolumen, potwierdzone fundamentami → sygnały KUPUJ z wagą 3/5/8% | minuty |
| `gpw-quality-screen` | 7 twardych kryteriów (ROE, FCF, marże, dług, rozwadnianie) eliminuje słabe spółki | ~30 min |
| `gpw-funnel` | cały temat → ≤10 kandydatów → 3 głębokie analizy → propozycja portfela | godziny |
| `gpw-sector` | mapa łańcucha wartości: kto na czym zarabia, które ogniwo jest na GPW | godziny |

### Decyzja
| Skill | Co robi | Czas |
|-------|---------|------|
| `gpw-checklist` | 6 bram Buffetta + test lustra — czy w ogóle drążyć | ~10 min |
| `gpw-analyze` | **koń roboczy**: 4 perspektywy w jednym przebiegu → oceny, przedziały kupuj/trzymaj/sprzedaj w PLN | 10–20 min |
| `gpw-analyze-team` | wersja ciężka: 4 niezależnych agentów równolegle + pełny audyt liczb — na duże pozycje | 30–60 min |
| `gpw-management` | prześwietlenie zarządu: obietnice vs realizacja, insiderzy, nadania polityczne | ~30 min |

### Monitoring
| Skill | Co robi | Czas |
|-------|---------|------|
| `gpw-daily` | briefing: rynek, alerty cenowe pozycji, komunikaty ESPI, kalendarz wyników | ~5 min |
| `gpw-pulse` | akcja mocno się ruszyła — atrybucja: co się NAPRAWDĘ stało | 10–15 min |
| `gpw-earnings` | raport kwartalny czytany ze źródeł pierwotnych, wpływ na tezę | ~30 min |
| `gpw-thesis` | kontrola tezy: czy powody zakupu nadal obowiązują? Sfalsyfikowana = jasne „SPRZEDAJ" | ~10 min |

### Portfel i jakość
| Skill | Co robi |
|-------|---------|
| `gpw-portfolio` | pełny przegląd: rozkazy SPRZEDAJ / KUP / CZEKAJ z poziomami cen |
| `gpw-audit` | weryfikacja próbki liczb raportu w niezależnych źródłach |

Typowy przepływ:

```
gpw-scanner → sygnał → gpw-checklist (10 min) → przeszło?
→ gpw-analyze → przedziały cen + teza → zlecenie u brokera składasz Ty
→ pozycja trafia do portfolio.md → codziennie gpw-daily, co tydzień gpw-portfolio
```

## 7 agentów

| Agent | Rola |
|-------|------|
| `gpw-scout` | zbiera dane: notowania, fundamenty, ESPI, newsy — każda kluczowa liczba z 2 źródeł |
| `master-business` | Duan Yongping: czy to w ogóle dobry biznes |
| `master-financials` | Buffett: liczby, wycena, przedziały cenowe |
| `master-risk` | Munger: adwokat diabła — jak ta spółka umiera |
| `master-certainty` | Li Lu: test 10 lat, jakość zarządu |
| `gpw-auditor` | weryfikuje liczby raportów (werdykt PASS/FAIL) |
| `gpw-timing` | kiedy wejść/wyjść: transze, poziomy, unieważnienie |

## Narzędzia

```
python tools/gpw_data.py quote PKN CDR ALE       # notowania z Yahoo (.WA doklejane)
python tools/gpw_data.py signals XTB             # SMA50/200, momentum, odległość od 52w
python tools/gpw_screener.py                     # skan momentum+wartość watchlisty
python tools/gpw_backtest.py XTB --years 5       # test uczciwości: strategia vs kup-i-trzymaj
python tools/report_audit.py extract --report reports/XTB/XTB-analysis-20260707.md
python tools/financial_rigor.py three-scenario --price 121 --eps 10.5 --growth 20 10 0 --pe 15 11 8
```

Zero zależności poza biblioteką standardową Pythona 3. Cała arytmetyka finansowa na `decimal.Decimal`.

## Tryb ciągły

Jednorazowo: odpalasz skille, kiedy chcesz. Ciągle: zaplanuj `gpw-daily` co rano (w Claude Code: `/schedule uruchamiaj /gpw-daily codziennie o 8:00`) — dostajesz alert tylko, gdy pozycja przekroczy przedział sprzedaży, obserwowana spółka wejdzie w strefę kupna, wyzwoli się warunek tezy albo zbliżają się wyniki.

## Układ repozytorium

```
skills/     14 procedur badawczych         agents/    7 definicji ról
tools/      narzędzia Python (stdlib)      docs/      metodologia
reports/    publikowane raporty            research/  notatki robocze
data/       watchlista + fundamenty        scripts/   instalatory Claude Code
assets/     grafiki do README
```

`.gitignore` trzyma poza repozytorium tylko `portfolio.md` (Twoje pozycje), `CLAUDE.local.md` (preferencje osobiste) i zainstalowane kopie `.claude/` — repo publikuje system i raporty, nie Twoje pieniądze.

## Metodologia

Framework, mechanizmy anty-biasowe, wyjątki sita jakości i dyscyplina po zakupie: [docs/methodology.md](docs/methodology.md).

## Licencja

MIT. Struktura metodologii inspirowana [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) (MIT).
