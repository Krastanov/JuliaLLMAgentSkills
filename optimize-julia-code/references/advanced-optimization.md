# Advanced Optimization

Apply these techniques only to a measured hot kernel after tests cover its assumptions.

## Use annotations narrowly

Use `@inbounds` only when every index is proven valid for every supported array and index origin. Keep it around the smallest loop that needs it, and test with bounds checking enabled before benchmarking.

Use `@simd` only when loop iterations are independent and reordering is valid. Benchmark it; the compiler may already vectorize the loop.

Use `@fastmath` only when changed IEEE behavior is acceptable, including reassociation and special-value behavior. State the numerical tolerance and add tests for the supported domain. Do not apply it broadly to library code.

## Control specialization deliberately

Use `Val` or value parameters only when the value is already known in the type domain and the resulting specialization improves a measured kernel. Avoid creating large numbers of types or compiled methods from ordinary runtime data.

Add explicit specialization for `Type`, `Function`, or `Vararg` arguments only after confirming that Julia's specialization heuristic limits the hot method.

## Consider concurrency last

Parallelize only when work is independent, large enough to amortize scheduling, and limited by available compute rather than memory bandwidth. Compare the parallel version with the sequential baseline across thread counts. Follow `orchestrate-julia-workloads` for task lifetime, race safety, scheduling, and external-library thread control.

## Gate external optimizers

- Prefer Base Julia and standard libraries until a benchmark identifies a remaining bottleneck.
- Check the candidate package's current documentation, Julia compatibility, maintenance status, and semantic constraints.
- Benchmark the package against the clear Base implementation on representative inputs.
- Preserve a tested fallback when the package uses narrower array, aliasing, numerical, or platform assumptions.
- Remove the dependency when it does not provide a stable material improvement.

Avoid universal claims about a loop library, SIMD strategy, or compiler limitation. Results depend on Julia version, element type, memory layout, CPU, and workload size.

## Sources

- [Julia performance annotations](https://docs.julialang.org/en/v1/manual/performance-tips/#man-performance-annotations)
- [Julia bounds-checking internals](https://docs.julialang.org/en/v1/devdocs/boundscheck/)
- [Julia SIMD support](https://docs.julialang.org/en/v1/base/simd-types/)
