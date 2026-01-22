---
name: julia-doccitations
description: Add citations and bibliographies to Julia documentation using DocumenterCitations.jl. Use this skill when adding academic references to package documentation.
---

# Julia Documentation Citations

Add citations and bibliographies to Julia documentation using DocumenterCitations.jl.

## Quick Setup

### 1. Add to docs/Project.toml

```toml
[deps]
Documenter = "e30172f5-a6a5-5a46-863b-614d45cd2de4"
DocumenterCitations = "daee34ce-89f3-4625-b898-19384cb65244"

[compat]
Documenter = "1"
DocumenterCitations = "1"
```

### 2. Create docs/src/references.bib

```bibtex
@article{GoerzQ2022,
    author = {Goerz, Michael H. and others},
    title = {Quantum Optimal Control},
    journal = {Physical Review A},
    year = {2022},
    doi = {10.1103/PhysRevA.105.032401}
}

@book{NielsenChuang2010,
    author = {Nielsen, Michael A. and Chuang, Isaac L.},
    title = {Quantum Computation and Quantum Information},
    publisher = {Cambridge University Press},
    year = {2010}
}
```

### 3. Configure docs/make.jl

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
    pages = [
        "Home" => "index.md",
        "Bibliography" => "bibliography.md",
    ]
)
```

### 4. Create docs/src/bibliography.md

```markdown
# Bibliography

```@bibliography
```
```

## Citation Syntax

### In Markdown

```markdown
The stabilizer formalism [gottesman1998heisenberg](@cite) enables efficient simulation.

See [NielsenChuang2010; Chapter 10](@cite) for details.

Previous work [GoerzQ2022, NielsenChuang2010](@cite) has shown...
```

### In Docstrings

```julia
"""
    stabilizer_simulation(circuit)

Simulate using the stabilizer formalism [gottesman1998heisenberg](@cite).
"""
function stabilizer_simulation(circuit) end
```

### Footnote Style

```markdown
The tableaux formalism[^1] enables efficient simulation.

[^1]: [gottesman1998heisenberg](@cite)
```

## Citation Styles

```julia
bib = CitationBibliography("refs.bib", style = :authoryear)  # (Gottesman, 1998)
bib = CitationBibliography("refs.bib", style = :numeric)     # [1]
bib = CitationBibliography("refs.bib", style = :alpha)       # [Got98]
```

## Bibliography Options

```markdown
# All cited references
```@bibliography
```

# Specific entries only
```@bibliography
Keys = ["GoerzQ2022", "NielsenChuang2010"]
```

# All entries (including uncited)
```@bibliography
*
```

# Per-page bibliography
```@bibliography
Pages = ["chapter1.md"]
```
```

## Reference

- **[Complete Examples](references/examples.md)** - Full make.jl, BibTeX, and page examples

## Checklist

- [ ] `DocumenterCitations` in `docs/Project.toml`
- [ ] `.bib` file in `docs/src/`
- [ ] `CitationBibliography` created in `make.jl`
- [ ] Plugin passed to `makedocs(plugins = [bib], ...)`
- [ ] Bibliography page created with `@bibliography` block
- [ ] Bibliography page included in `pages`
