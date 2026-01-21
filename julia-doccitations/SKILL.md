# Julia Documentation Citations

Add citations and bibliographies to Julia documentation using DocumenterCitations.jl.

## Installation

Add to `docs/Project.toml`:

```toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
DocumenterCitations = "daee34ce-89f3-4625-b898-19384cb65244"

[compat]
Documenter = "1"
DocumenterCitations = "1"
```

## Setup

### 1. Create a BibTeX File

Place a `.bib` file in `docs/src/`:

```bibtex
# docs/src/references.bib

@article{GoerzQ2022,
    author = {Goerz, Michael H. and others},
    title = {Quantum Optimal Control},
    journal = {Physical Review A},
    year = {2022},
    volume = {105},
    pages = {032401},
    doi = {10.1103/PhysRevA.105.032401}
}

@book{NielsenChuang2010,
    author = {Nielsen, Michael A. and Chuang, Isaac L.},
    title = {Quantum Computation and Quantum Information},
    publisher = {Cambridge University Press},
    year = {2010},
    edition = {10th Anniversary},
    isbn = {978-1107002173}
}

@article{gottesman1998heisenberg,
    author = {Gottesman, Daniel},
    title = {The {Heisenberg} Representation of Quantum Computers},
    journal = {arXiv preprint quant-ph/9807006},
    year = {1998}
}
```

### 2. Configure make.jl

```julia
using Documenter
using DocumenterCitations
using MyPackage

bib = CitationBibliography(
    joinpath(@__DIR__, "src", "references.bib"),
    style = :authoryear  # or :numeric, :alpha
)

makedocs(
    plugins = [bib],
    sitename = "MyPackage.jl",
    # ... other options
)
```

### 3. Add a Bibliography Page

Create `docs/src/bibliography.md`:

```markdown
# Bibliography

```@bibliography
```
```

Include it in your pages:

```julia
pages = [
    # ...
    "References" => [
        "API" => "API.md",
        "Bibliography" => "bibliography.md",
    ],
]
```

## Citation Syntax

### Basic Citations

```markdown
The stabilizer formalism [gottesman1998heisenberg](@cite) enables efficient simulation.

See [NielsenChuang2010; Chapter 10](@cite) for details.
```

Renders as: "The stabilizer formalism [Gottesman1998] enables efficient simulation."

### Multiple Citations

```markdown
Previous work [GoerzQ2022, NielsenChuang2010](@cite) has shown...
```

### Citation in Docstrings

```julia
"""
    stabilizer_simulation(circuit)

Simulate a Clifford circuit using the stabilizer formalism [gottesman1998heisenberg](@cite).

See also [aaronson2004improved](@cite) for performance improvements.
"""
function stabilizer_simulation(circuit)
    # ...
end
```

### Footnote-Style Citations

Use footnotes with citations for cleaner prose:

```markdown
The tableaux formalism[^1] with destabilizer improvements[^2] enables efficient simulation.

[^1]: [gottesman1998heisenberg](@cite)
[^2]: [aaronson2004improved](@cite)
```

## Citation Styles

### Available Styles

```julia
# Author-year style: (Gottesman, 1998)
bib = CitationBibliography("refs.bib", style = :authoryear)

# Numeric style: [1]
bib = CitationBibliography("refs.bib", style = :numeric)

# Alpha style: [Got98]
bib = CitationBibliography("refs.bib", style = :alpha)
```

### Custom Styles

See DocumenterCitations.jl documentation for custom citation styles.

## Bibliography Options

### Full Bibliography

```markdown
```@bibliography
```
```

Lists all cited references.

### Filtered Bibliography

```markdown
# Only specific entries
```@bibliography
Keys = ["GoerzQ2022", "NielsenChuang2010"]
```

# All entries (including uncited)
```@bibliography
*
```
```

### Multiple Bibliographies

For large documentation with section-specific bibliographies:

```markdown
# Chapter 1 references
```@bibliography
Pages = ["chapter1.md"]
```

# Chapter 2 references
```@bibliography
Pages = ["chapter2.md"]
```
```

## Complete Example

### docs/make.jl

```julia
using Documenter
using DocumenterCitations
using MyPackage

bib = CitationBibliography(
    joinpath(@__DIR__, "src", "references.bib"),
    style = :authoryear
)

makedocs(
    plugins = [bib],
    sitename = "MyPackage.jl",
    modules = [MyPackage],
    format = Documenter.HTML(
        assets = ["assets/citations.css"]
    ),
    pages = [
        "Home" => "index.md",
        "Manual" => "manual.md",
        "API" => "API.md",
        "Bibliography" => "bibliography.md",
    ]
)

deploydocs(repo = "github.com/YourOrg/MyPackage.jl.git")
```

### docs/src/index.md

```markdown
# MyPackage.jl

MyPackage implements quantum algorithms based on the stabilizer formalism[^1].

## Key Features

- Efficient Clifford simulation [aaronson2004improved](@cite)
- Error correction codes [gottesman1997stabilizer](@cite)

## References

[^1]: [gottesman1998heisenberg](@cite)
```

### docs/src/bibliography.md

```markdown
# Bibliography

The following references are cited throughout this documentation.

```@bibliography
```
```

## BibTeX Tips

### Common Entry Types

```bibtex
@article{key,
    author = {Last, First and Other, Author},
    title = {Article Title},
    journal = {Journal Name},
    year = {2022},
    volume = {10},
    pages = {1--15},
    doi = {10.1234/example}
}

@book{key,
    author = {Author, Name},
    title = {Book Title},
    publisher = {Publisher Name},
    year = {2020}
}

@inproceedings{key,
    author = {Author, Name},
    title = {Paper Title},
    booktitle = {Conference Name},
    year = {2021},
    pages = {100--110}
}

@misc{key,
    author = {Author, Name},
    title = {Preprint Title},
    year = {2023},
    eprint = {2301.12345},
    archiveprefix = {arXiv}
}
```

### Special Characters

```bibtex
# Preserve capitalization with braces
title = {The {Heisenberg} Representation}

# LaTeX math
title = {Computing $\pi$ to a Million Digits}

# Special characters
author = {M{\"u}ller, Hans}
```

## Checklist

- [ ] `DocumenterCitations` in `docs/Project.toml`
- [ ] `.bib` file in `docs/src/`
- [ ] `CitationBibliography` created in `make.jl`
- [ ] Plugin passed to `makedocs(plugins = [bib], ...)`
- [ ] Bibliography page created with `@bibliography` block
- [ ] Bibliography page included in `pages`
