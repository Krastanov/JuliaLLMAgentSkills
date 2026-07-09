# External-Library Thread Control

Native Julia tasks compose through Julia's scheduler, but BLAS, FFT, and other native libraries may manage separate thread pools. Inspect and tune each layer instead of assuming the counts compose automatically.

## Inspect the active BLAS backend

```julia
using LinearAlgebra

BLAS.get_config()
BLAS.get_num_threads()
```

When many Julia threads each call OpenBLAS, start comparison with one OpenBLAS thread:

```julia
BLAS.set_num_threads(1)
```

This is a starting rule of thumb, not a universal optimum. A large isolated BLAS call may perform better with multiple BLAS threads. Benchmark the full workload across a small thread-count matrix and include memory use and latency, not only peak throughput.

## Account for backend differences

- Use `OPENBLAS_NUM_THREADS` before startup or `BLAS.set_num_threads` during the session for OpenBLAS.
- Inspect `BLAS.get_config()` before applying backend-specific advice.
- For MKL.jl, use `MKL.set_num_threads` for the global MKL count. `BLAS.set_num_threads` controls the BLAS domain and does not necessarily control LAPACK or other MKL domains.
- For FFTW.jl, set thread counts or plan-specific `num_threads` according to current FFTW.jl documentation, then recreate affected plans.
- Consult the active backend's documentation for OpenMP or other environment variables; do not copy OpenBLAS assumptions to another backend.

## Avoid nested oversubscription

Inventory all concurrency layers:

- Julia default-pool tasks
- interactive-pool tasks
- BLAS, FFT, OpenMP, or vendor-library threads
- worker processes or test processes
- container or scheduler CPU limits

Reduce or disable an inner thread pool when outer parallelism already fills the allotted CPUs. Also benchmark the opposite decomposition—fewer Julia tasks with more library threads—because large kernels may favor it.

Set counts explicitly in reproducible CI or batch jobs when host defaults vary. Record affinity or CPU quotas when they affect results.

## Sources

- [Julia performance tips: multithreading and linear algebra](https://docs.julialang.org/en/v1/manual/performance-tips/#Multithreading-and-linear-algebra)
- [MKL.jl thread-control notes](https://github.com/JuliaLinearAlgebra/MKL.jl#threading-control)
- [FFTW.jl documentation](https://juliamath.github.io/FFTW.jl/stable/)
