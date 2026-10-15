# Technical Jargon Simplifier

**Avinash · ASI23CA024**

A small Python NLP course project that explains technical text with a custom 42-term glossary. It is a deterministic, rule-based system, not an advanced AI or a trained machine-learning model.

## Run the notebook

Use Python 3.10+ and run these commands inside the project folder:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m notebook
```

On macOS/Linux use `.venv/bin/python` instead. Open **Technical_Jargon_Simplifier.ipynb** and choose **Run All**. The notebook is self-contained: no sibling files or downloads are required after opening it in a notebook environment. For Google Colab, upload the `.ipynb` and select **Runtime → Run all**. No package-install cell is needed in Colab.

Edit `USER_TEXT` in the user-input cell to try your own text. Interactive `input()` is optional and disabled so all cells run without waiting.

## Run the optional local UI

The engine and browser UI require only Python's standard library; Jupyter is unnecessary for this mode.

```powershell
python app.py
```

Open **http://127.0.0.1:8527**. Keep the terminal running. Text is sent only to this local Python process. There are no external API calls, accounts, databases, or stored messages. Stop it with Ctrl+C.

## Features and NLP techniques

- 42 terms across AI, computer science, networking and programming, with full definitions and aliases.
- Unicode/whitespace normalization and regex tokenization.
- Stopword filtering for inspection only, preserving full sentence structure and negation when rewriting.
- Case-insensitive word-boundary matching, longest phrases first, plural aliases and repeated-term counts.
- A single replacement pass, simple sentence splitting, a small word-rewrite list and an explicit learning-pattern sentence rule.
- Original text, simplified reading, recognized terms, full definitions and preprocessing steps.
- Empty input and text without recognized terms are handled explicitly.
- 18 notebook demonstrations, including 16 technical examples, plain text and empty input.

## Example

Input:

> Machine learning algorithms utilize training datasets to optimize predictive models.

Simplified reading:

> Machine learning methods learn from examples to make better predictions.

The full explanation also lists each detected term's definition. `simplifier.py` is the local UI engine; the notebook embeds the same functions and glossary so it works independently.

## Tests and evaluation

```powershell
python -m unittest -v test_simplifier.py
python -c "from simplifier import evaluate; r=evaluate(); print(r['passed'], '/', r['total']); print(r['note'])"
```

Notebook evaluation compares each detected term set to manually listed expected terms, and checks that every detected definition appears in the complete explanation. The case success rate is specific to these handcrafted examples. It is not an accuracy score for human comprehension, semantic preservation, or unknown text. The examples were used during development; there is no independent held-out benchmark. Unit tests additionally exercise boundaries, multiword priority, negation, aliases, articles, Unicode and invalid input.

## Limitations

Only listed glossary terms are explained. Ambiguous terms can have a different meaning in context. Sentence splitting and article cleanup are deliberately basic, and some rewrites can sound awkward or alter nuance. The system does not assess factual correctness. Abbreviations match only explicit aliases. Review output before using it in academic or technical writing.

No deep learning, large language model, training dataset, paid API, cloud service, database, authentication, React or Streamlit is used.

## Files

- `Technical_Jargon_Simplifier.ipynb`: complete runnable notebook with demonstrations and evaluation.
- `simplifier.py`: glossary, preprocessing, matching, sentence rules and sample evaluation.
- `app.py` and `index.html`: minimal optional local Python/browser UI.
- `test_simplifier.py`: engine tests.
- `requirements.txt`: Jupyter Notebook for local notebook use; engine/UI have no external dependencies.
- `report/`: template-based course report in Word and PDF.

To edit behavior, update `simplifier.py` and the corresponding notebook cells together. Planned GitHub repository: https://github.com/AVINASH-V-BHASKARAN/Technical_Jargon_Simplifier. Publication is pending; this project is currently kept in a local Git repository.
