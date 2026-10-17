# Storyboard

## Narrative arc (~2:30–3:00)

| # | Scene | Job | Example content | Length |
|---|---|---|---|---|
| 1 | Hook | Set up the field in one picture, end on a question | the standard pipeline as a loop (input → model → output → feedback); "where does it fall short?" | 15–20 s |
| 2 | Problem | Make the gap concrete and *name* it | a chain of intermediate states; the shortcoming shown on the running example; the named failure mode | 45–60 s |
| 3 | Idea | The key insight on the running toy example | "What if we …?"; the toy example; the new quantity with concrete numbers (good 3→6, bad 3→1) | 25–30 s |
| 4 | Why it works | The rule and its theoretical grounding, named, not derived | one-line rule; the theorem or principle it follows from; one numeric consequence | 15–20 s |
| 5 | Reveal | Method name/acronym and the objective in the video's symbols | acronym letters; the loss written with the symbols introduced on screen | 10–15 s |
| 6 | Mechanism | How the method runs on one example | boxes and arrows: model → components → the two quantities the objective balances | 15–20 s |
| 7 | Results | Headline number, per-task view, efficiency | grouped average bars with the margin; per-task zoomed panels; compute or data savings | 20–25 s |
| 8 | Outro | Title card | acronym, title, (authors unless double-blind) | 5–7 s |

Adapt the arc to the paper. A dataset paper replaces Idea/Mechanism with "what's in it / how it was built", and
a theory paper replaces Results with "what the theorem buys". Keep Hook → Problem → Insight → Evidence → Card.

## Template (`video/STORYBOARD.md`)

```markdown
# <Short title>: storyboard

Paper: <title> (<source file>). Target length: <m:ss>. Running example: <toy example>.
Colour meanings: BLUE = <method>, AMBER = <key quantity>, RED = <bad>, GREEN = <good>.

## 1. Hook (<n> s)
Purpose: <one line>
Visuals: <what is drawn, in order>
Header: "<...>"
Captions: "<caption with [[key]] words>" (emph) / "<...>"
Numbers: <none | values with FACTS.md ids>

## 2. ...
```

Show the storyboard to the user before coding. Their edits are cheaper here than after rendering.
