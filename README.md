# NoteTUI

En tastatur-drevet terminal-applikasjon (TUI) for daglige markdown-notater.

## Hva er NoteTUI?

NoteTUI er en terminal-basert notatapplikasjon som lar deg skrive daglige notater i markdown-format. Hver dag får sin egen fil, og du kan enkelt navigere mellom dager med tastatursnarveier.

### Funksjoner

- **Daglige notater** - Automatisk filnavn basert på dato (`DD-Mmm-YYYY.md`)
- **Markdown-editor** - Syntaksutheving og linjenummerering
- **Kalendervisning** - Visuell navigering mellom datoer
- **Todo-liste** - Samler alle `##`-overskrifter fra notatene dine
- **Tastatur-drevet** - Rask navigering uten mus
- **Norsk språk** - Datoer og ukedager på norsk
- **Auto-lagring** - Notater lagres automatisk ved navigering

## Installasjon

### Krav

- Python 3.10 eller nyere
- [uv](https://github.com/astral-sh/uv) (anbefalt) eller pip

### Med uv (anbefalt)

```bash
# Installer direkte fra GitHub
uv tool install git+https://github.com/DITT-BRUKERNAVN/notetui.git

# Eller klon og installer lokalt
git clone https://github.com/DITT-BRUKERNAVN/notetui.git
cd notetui
uv tool install -e .
```

### Med pip

```bash
git clone https://github.com/DITT-BRUKERNAVN/notetui.git
cd notetui
pip install .
```

## Bruk

Start applikasjonen:

```bash
notetui
```

Notatene lagres i `~/notes/`.

## Tastatursnarveier

### Navigering

| Tast | Handling |
|------|----------|
| `Ctrl+N` | Neste dag |
| `Ctrl+P` | Forrige dag |
| `Ctrl+F` | Neste uke |
| `Ctrl+B` | Forrige uke |
| `Ctrl+T` | Gå til i dag |

### Visninger

| Tast | Handling |
|------|----------|
| `Ctrl+C` | Vis/skjul kalender |
| `Tab` | Fokuser todo-liste |
| `Escape` | Tilbake til editor |

### Redigering

| Tast | Handling |
|------|----------|
| `Ctrl+S` | Lagre notat |
| `Ctrl+D` | Marker todo som ferdig (i todo-listen) |
| `Ctrl+Enter` | Marker todo på linje som ferdig (i editoren) |

### Annet

| Tast | Handling |
|------|----------|
| `Ctrl+H` | Vis hjelp |
| `Ctrl+Q` | Avslutt |

### I kalendervisning

| Tast | Handling |
|------|----------|
| Piltaster | Naviger mellom dager |
| `Enter` | Velg dato |
| `[` / `]` | Forrige/neste måned |

## Todo-funksjonen

Alle `##`-overskrifter i notatene dine vises som todos i sidepanelet:

```markdown
# mandag, 01 desember 2025

## Handle mat
Kjøpe melk og brød

## Ringe legen
```

- Trykk `Tab` for å fokusere todo-listen
- Trykk `Enter` for å hoppe til datoen for en todo
- Trykk `Ctrl+D` for å markere en todo som ferdig (legger til ~~strikethrough~~)

## Teknologi

- [Textual](https://textual.textualize.io/) - Moderne Python TUI-rammeverk
- Python 3.10+

## Lisens

MIT License
