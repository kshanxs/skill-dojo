# Third-Party Notices

Skill Dojo is MIT licensed. Its code and text were written for this project. No third-party source code is included.

## Projects That Informed the Design

These projects were read for ideas such as which checks are useful and how to report them. Their code and prose were not copied. They are credited here because their work shaped ours.

| Project | License | What it informed |
|---|---|---|
| [proselint](https://github.com/amperser/proselint) | BSD-3-Clause | Precision-first prose checks |
| [write-good](https://github.com/btford/write-good) | MIT | Repeated-word and wordiness checks |
| [textstat](https://github.com/textstat/textstat) | MIT | Choice of readability measures |
| [humanizer](https://github.com/blader/humanizer) | MIT | Pattern categories for AI-sounding prose |
| [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | MIT | Separating detection from editing |
| [stop-slop](https://github.com/hardikpandya/stop-slop) | MIT | Throat-clearing and filler categories |
| [citecheck](https://github.com/tobiasosDev/citecheck) | MIT | Conservative citation verdicts and retraction checks |

The Flesch Reading Ease and Flesch-Kincaid formulas are published mathematical formulas.

## Reference Material

- Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), by WikiProject AI Cleanup, is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). It informed the general pattern categories. Its text is not reproduced here.
- Earlier versions of Calligraph Sensei credited a `biostartechnology/humanizer` package for pattern ideas. That repository is no longer available, so its license could not be confirmed. The catalog has been rewritten in this project's own words.

## Test Corpus

The excerpts in `tests/corpus/` come from Project Gutenberg editions of works in the US public domain: *On the Origin of Species* (Darwin), *Pride and Prejudice* (Austen), *Narrative of the Life of Frederick Douglass*, and *On Liberty* (Mill).

## Online Services

With `--online`, Research Dojo queries [Crossref](https://www.crossref.org/) (including its [Retraction Watch](https://retractionwatch.com/) data), [doi.org](https://www.doi.org/), [arXiv](https://arxiv.org/), and [Open Library](https://openlibrary.org/). Each service has its own terms. None is affiliated with this project.
