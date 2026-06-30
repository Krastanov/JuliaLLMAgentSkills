# Threading in External Libraries

When mixing Julia's native multithreading with external threaded libraries (like BLAS, LAPACK, or FFTW), you must carefully manage thread counts. Failing to do so can lead to **oversubscription**, where `N` Julia threads each spawn `N` external threads, resulting in `N^2` threads competing for `N` CPU cores and causing severe performance degradation.

## General Rule
If you are calling an externally threaded function *inside* a natively threaded Julia region (e.g., inside `@threads`, `@spawn`, or `@batch`), you **must** disable its internal threading by setting its thread count to `1` beforehand.

## BLAS
Julia uses OpenBLAS by default for dense linear algebra.
- **Check threads**: `LinearAlgebra.BLAS.get_num_threads()`
- **Set threads**: `LinearAlgebra.BLAS.set_num_threads(n)`

## MKL.jl (Intel Math Kernel Library)
When using MKL instead of OpenBLAS, `BLAS.set_num_threads()` only configures the BLAS routines. However, MKL also accelerates LAPACK and other domains.
- **Check global threads**: `MKL.get_num_threads()`
- **Set global threads**: `MKL.set_num_threads(n)`
- **Note**: Using `MKL.set_num_threads(n)` is the only way to correctly set the number of threads for MKL's LAPACK routines natively (see [MKL.jl PR #180](https://github.com/JuliaLinearAlgebra/MKL.jl/pull/180)).

## FFTW.jl
FFTW provides fast Fourier transforms and has its own threading engine.
- **Check threads**: `FFTW.get_num_threads()`
- **Set threads**: `FFTW.set_num_threads(n)`
- **Critical Note**: The FFTW threading policy is strictly fixed when a plan is created. You cannot change the number of threads for an existing FFTW plan. If you need both single-threaded and multi-threaded FFTs, you must create two separate plans with the respective thread counts set prior to their creation.
