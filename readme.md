I don't know anything about emscripten+WASM, so I'm going through the following process:

1. Generating tutorials (mostly ChatGPT),
2. Compiling and running the demos as I go along,
3. Cleaning up the tutorials and improving them.

I notice that the tutorials aren't that great without lots of editing. 

## Phase 1: Basic Compilation, Memory Management, and I/O

- [Problem 1. Basic Integer Addition (No ccall/ccall)](problem01)
- [Problem 2. Averaging a Float32 Array (No ccall/ccall)](problem02)
- [Problem 3. Reversing a String & EMSCRIPTEN_KEEPALIVE (No ccall/ccall)](problem03)
- [Problem 4. Re-Implement Basic Addition (Using cwrap/ccall)](problem04)
- [Problem 5. Re-Implement Averaging a Float32 Array (Using cwrap/ccall)](problem05)
- [Problem 6. Re-Implement String Reversal (Using cwrap/ccall)](problem06)
- [Problem 7. Using Module.print and Module.printErr](problem07)

## Phase 2: Advanced Memory, Canvas Integration, and MEMFS

- [Problem 8. Persistent Memory Array](problem08)
- [Problem 9. Canvas Drawing from a Shared Memory Buffer](problem09)
- [Problem 10. Using MEMFS to Store/Load Data](problem10)
- [Problem 11. Handling Alignment and Struct Layout](problem11)

## Phase 3: Benchmarking and Optimization

- [Problem 12. Prime Sieve Benchmark (No Optimization)](problem12)
- [Problem 13. Re-Compile with -O3](problem13)
- [Problem 14. O(N²) Distance Calculation and Flags](problem14)

## Phase 4: External Libraries (Eigen, FFT)

- [Problem 15. Eigen Integration for Matrix Operations](problem15)
- [Problem 16. FFT with an External Library](problem16)

## Phase 5: End-to-End Scientific Simulation Project

- [Problem 17. Monte-Carlo Simulation with Periodic Boundaries](problem17)
- [Problem 18. NPT Ensemble Control from JS](problem18)
- [Problem 19. Compute Pair Correlation Functions and FFT](problem19)
- [Problem 20. Final Visualization and Analysis Page](problem20)
