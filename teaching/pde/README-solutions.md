# PDE worked solutions — instructor review draft

- `problems-solutions.pdf`: compiled 35-page document.
- `problems-solutions.tex`: editable LaTeX source.
- `solution_figures/`: six vector PDF sketches and their generation script.
- `problems-solutions-source.zip`: portable LaTeX source bundle, including the figures and this README.

## Mathematical status

Problems 1–7 and 9–11 have detailed worked solutions, characteristic-domain discussions, and direct verification. Both equations in Problem 10 are solved.

**Problem 8 is unresolved as written.** Its section explicitly identifies the missing construction, disproves the tempting candidate `a(x,y)=x²`, and proves two related statements without presenting them as solutions to the original problem. This draft is not a completed eleven-problem handout for distribution.

Classical solutions are interpreted as C¹. The notes explain the different global uniqueness answers when C² or smooth solutions are required, especially in Problem 11.

## Compile

From the directory containing the `.tex` file and `solution_figures/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error problems-solutions.tex
```

Or run `pdflatex problems-solutions.tex` twice. The checked-in figure PDFs are sufficient; Python is not needed to compile the handout.

To regenerate the sketches, with PyMuPDF installed:

```sh
python3 solution_figures/generate_figures.py
```

## Verification

- Compiled with pdfLaTeX / TeX Live 2025 and latexmk.
- Final compilation has no LaTeX warnings or overfull/underfull boxes.
- Rendered pages and all six vector sketches were visually inspected.
- PDF text geometry was checked for clipping outside the page margins.
- 200 randomized sets of independent first-derivative residual checks and characteristic-parameter inversion checks passed. These checks supplement the written mathematical proofs; they do not resolve Problem 8.

The original problem sheet and website pages were not edited.
