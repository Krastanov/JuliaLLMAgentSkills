---
name: julia-doccitations
description: Add citations and bibliographies to Julia documentation using DocumenterCitations.jl. Use this skill when adding academic references to package documentation.
---

# Julia Documentation Citations

Add citations and bibliographies to Julia documentation with
DocumenterCitations.jl.

## Add Dependencies (docs/)

```julia
using Pkg
Pkg.activate("docs")
Pkg.add(["Documenter", "DocumenterCitations"])
```

## Add a BibTeX File

Create `docs/src/references.bib` with your entries.

## Configure docs/make.jl

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
    pages = [
        "Home" => "index.md",
        "Bibliography" => "bibliography.md",
    ]
)
```

## Add a Bibliography Page

````markdown
# Bibliography

```@bibliography
```
````

## Cite in Docs and Docstrings

```markdown
See [NielsenChuang2010](@cite) for details.
```

```julia
"""
    stabilizer_simulation(circuit)

Simulate using the stabilizer formalism [gottesman1998heisenberg](@cite).
"""
function stabilizer_simulation(circuit) end
```

## Reference

- **[Complete Examples](references/examples.md)** - Styles, filters, and full pages

## Checklist

- [ ] `DocumenterCitations` added to docs env via Pkg
- [ ] `docs/src/references.bib` created
- [ ] `CitationBibliography` added to `makedocs`
- [ ] Bibliography page included in `pages`
