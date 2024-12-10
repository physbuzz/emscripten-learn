[View on github pages.](https://physbuzz.github.io/emscripten-learn/)

I don't know anything about emscripten+WASM, so I'm going through the following process:

1. Generate tutorials (mostly ChatGPT),
2. Compile and run the demos as I go along (lots of issues crop up here),
3. Clean up the tutorials and improv them as I go along.

I notice that the tutorials aren't that great without lots of editing. The edited / cleaned up examples that I'm going for are in examples/example1.md and examples/example2.md.

## Phase 1: Basic Compilation, Memory Management, and I/O

- [Problem 1. Basic Integer Addition](lesson01)
- [Problem 2. Averaging a Float32 Array](lesson02)
- [Problem 3. Reversing a String](lesson03)

Edited up to here. Next problems should be changed to: #4, reimplement problems 1-3 using ccall. #5, reimplement using cwrap. #6, other datatypes (bigint, float64)

- [Problem 4. Re-Implement Basic Addition (Using cwrap/ccall)](lesson04)
- [Problem 5. Re-Implement Averaging a Float32 Array (Using cwrap/ccall)](lesson05)
- [Problem 6. Re-Implement String Reversal (Using cwrap/ccall)](lesson06)
- [Problem 7. Using Module.print and Module.printErr](lesson07)

## Phase 2: Advanced Memory, Canvas Integration, and MEMFS

- [Problem 8. Persistent Memory Array](lesson08)
- [Problem 9. Canvas Drawing from a Shared Memory Buffer](lesson09)
- [Problem 10. Using MEMFS to Store/Load Data](lesson10)
- [Problem 11. Handling Alignment and Struct Layout](lesson11)

## Phase 3: Benchmarking and Optimization

- [Problem 12. Prime Sieve Benchmark (No Optimization)](lesson12)
- [Problem 13. Re-Compile with -O3](lesson13)
- [Problem 14. O(N²) Distance Calculation and Flags](lesson14)

## Phase 4: External Libraries (Eigen, FFT)

- [Problem 15. Eigen Integration for Matrix Operations](lesson15)
- [Problem 16. FFT with an External Library](lesson16)

## Phase 5: End-to-End Scientific Simulation Project

- [Problem 17. Monte-Carlo Simulation with Periodic Boundaries](lesson17)
- [Problem 18. NPT Ensemble Control from JS](lesson18)
- [Problem 19. Compute Pair Correlation Functions and FFT](lesson19)
- [Problem 20. Final Visualization and Analysis Page](lesson20)
