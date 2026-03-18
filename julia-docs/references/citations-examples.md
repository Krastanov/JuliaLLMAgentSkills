# Complete Examples

## Table of Contents

- [Complete make.jl Example](#complete-makejl-example)
- [BibTeX Entry Types](#bibtex-entry-types)
- [BibTeX Tips](#bibtex-tips)
- [Full Documentation Example](#full-documentation-example)

## Complete make.jl Example

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

## BibTeX Entry Types

### Article

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
```

### Book

```bibtex
@book{key,
    author = {Author, Name},
    title = {Book Title},
    publisher = {Publisher Name},
    year = {2020},
    edition = {2nd}
}
```

### Conference Paper

```bibtex
@inproceedings{key,
    author = {Author, Name},
    title = {Paper Title},
    booktitle = {Conference Name},
    year = {2021},
    pages = {100--110}
}
```

### ArXiv Preprint

```bibtex
@misc{key,
    author = {Author, Name},
    title = {Preprint Title},
    year = {2023},
    eprint = {2301.12345},
    archiveprefix = {arXiv}
}
```

## BibTeX Tips

### Preserve Capitalization

```bibtex
title = {The {Heisenberg} Representation of Quantum Computers}
```

### LaTeX Math in Titles

```bibtex
title = {Computing $\pi$ to a Million Digits}
```

### Special Characters

```bibtex
author = {M{\"u}ller, Hans}
author = {O'Brien, James}
```

### Multiple Authors

```bibtex
author = {First, Author and Second, Author and Third, Author}
```

## Full Documentation Example

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

### docs/src/references.bib

```bibtex
@article{gottesman1998heisenberg,
    author = {Gottesman, Daniel},
    title = {The {Heisenberg} Representation of Quantum Computers},
    journal = {arXiv preprint quant-ph/9807006},
    year = {1998}
}

@article{aaronson2004improved,
    author = {Aaronson, Scott and Gottesman, Daniel},
    title = {Improved Simulation of Stabilizer Circuits},
    journal = {Physical Review A},
    year = {2004},
    volume = {70},
    pages = {052328}
}

@article{gottesman1997stabilizer,
    author = {Gottesman, Daniel},
    title = {Stabilizer Codes and Quantum Error Correction},
    journal = {PhD thesis, California Institute of Technology},
    year = {1997}
}
```
