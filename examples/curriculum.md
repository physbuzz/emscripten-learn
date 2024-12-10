Below is an outline of problems with clear statements and associated learning goals, organized by the previously discussed phases. The focus is on the progression of Emscripten-specific features, memory models, and integration strategies, rather than on the physics or math of the examples. Each problem states what the student will do and what they should learn from doing it. The exact details of each solution are not included, as the emphasis is on what skills are developed.

---

### Phase 1: Basic Compilation, Memory Management, and I/O Without/With cwrap & ccall

**Problem 1 (No ccall/ccall): Basic Integer Addition**  
**Task:**  
Write a C function that takes two integers and returns their sum. Export it to JavaScript without using `ccall` or `cwrap`. Manually manage the function’s address and call it via `Module._functionName`.  
**Learning Goals:**  
- Understand how to compile a C function with Emscripten and access it from JavaScript.  
- Learn basic symbol naming (`Module._myFunction`) and how to call it directly.  
- Get comfortable with the initial Emscripten build commands and environment.

**Problem 2 (No ccall/ccall): Averaging a Float32 Array**  
**Task:**  
Write a function in C that takes a pointer to a float array and its length, computes the average, and returns a float. Pass a `Float32Array` from JS to this function without `ccall`/`cwrap`, by manually writing the data into `HEAPF32` and passing the pointer.  
**Learning Goals:**  
- Gain hands-on experience with the Emscripten HEAP memory model.  
- Understand how to allocate memory in JS and pass typed arrays to C functions.  
- Learn about indexing `HEAPF32` and ensuring correct data transfer.

**Problem 3 (No ccall/ccall): Reversing a String & EMSCRIPTEN_KEEPALIVE**  
**Task:**  
Create a function that takes a `const char*` string and returns a newly allocated reversed string. Ensure it is not removed by dead code elimination by using `EMSCRIPTEN_KEEPALIVE`. Manually handle UTF8 conversions in JS.  
**Learning Goals:**  
- Understand how to pass strings between JS and C by writing to and reading from the heap.  
- See how `EMSCRIPTEN_KEEPALIVE` affects symbol visibility and prevents function elimination.  
- Reinforce manual memory management and string handling without convenience wrappers.

**Problem 4 (With cwrap/ccall): Re-Implement Basic Addition**  
**Task:**  
Take the addition function from Problem 1 and now call it from JavaScript using `cwrap` to generate a convenient JS function wrapper.  
**Learning Goals:**  
- Understand how `cwrap` simplifies calling exported C functions.  
- Observe the difference between direct `Module._myFunction` calls and `Module.cwrap()` usage.

**Problem 5 (With cwrap/ccall): Re-Implement Averaging a Float32 Array**  
**Task:**  
Use `cwrap` (or `ccall`) to call the averaging function from Problem 2. Let `cwrap` handle pointer and type conversions, and compare the code complexity to the previous direct heap-access method.  
**Learning Goals:**  
- Appreciate how `cwrap` reduces boilerplate code in data passing.  
- Reinforce understanding of how Emscripten’s convenience functions map JS types to C types.

**Problem 6 (With cwrap/ccall): Re-Implement String Reversal**  
**Task:**  
Use `ccall` to invoke the string reversal function from Problem 3, noting how string arguments and return values are handled automatically.  
**Learning Goals:**  
- Learn how `ccall` manages string arguments and return values with less manual memory handling.  
- Understand the trade-offs between manual memory control and automated convenience.

**Problem 7: Using Module.print and Module.printErr**  
**Task:**  
Create a C function that prints output using `printf` and verify that the output appears in the browser console through `Module.print` and `Module.printErr`.  
**Learning Goals:**  
- Understand how standard I/O from C maps into JavaScript’s logging facilities.  
- Learn how to configure or redirect output streams in an Emscripten module.

---

### Phase 2: Advanced Memory, Persistent Data, Canvas Integration, and MEMFS

**Problem 8: Persistent Memory Array**  
**Task:**  
Implement a function that stores an array of floats persistently between calls (global static memory in C) and another function that retrieves it. Update and read this data over multiple frames from JS.  
**Learning Goals:**  
- Understand that global data in C persists across multiple JS calls.  
- Learn best practices for handling persistent simulation state.

**Problem 9: Canvas Drawing from a Shared Memory Buffer**  
**Task:**  
Allocate a buffer in the Emscripten heap that represents image data or particle positions. Continuously update it in C, and from JS draw these updated points/pixels on an HTML `<canvas>`.  
**Learning Goals:**  
- Learn how to directly access the same memory buffer from both C and JS for rendering.  
- Understand alignment and structure issues in shared data meant for graphics operations.

**Problem 10: Using MEMFS to Store/Load Data**  
**Task:**  
Write a function in C that saves the current simulation state (e.g., positions) to a file on the in-memory filesystem (MEMFS), and another that loads it back. From JS, trigger saves/loads and confirm the state restoration.  
**Learning Goals:**  
- Gain experience with the Emscripten virtual filesystem.  
- Understand how to simulate file I/O within a WebAssembly environment.

**Problem 11: Alignment and Struct Layout**  
**Task:**  
Define a C struct that contains mixed data types. Write a function to populate it, and another to read it from JS. Ensure correct memory alignment and demonstrate what happens if alignment is off. Fix any issues with explicit alignment directives or careful data handling.  
**Learning Goals:**  
- Develop a clear understanding of memory alignment and data layout in Wasm.  
- Learn to diagnose and solve alignment-related issues when sharing complex data structures.

---

### Phase 3: Benchmarking and Optimization

**Problem 12: Prime Sieve Benchmark (No Optimization)**  
**Task:**  
Implement a simple Sieve of Eratosthenes in C and measure its run time from JS (e.g., by using `performance.now()`).  
**Learning Goals:**  
- Learn how to benchmark code running in the browser.  
- Understand baseline performance before optimization.

**Problem 13: Re-Compile with -O3**  
**Task:**  
Recompile the prime sieve with `-O3` and measure performance again. Compare run times and observe the difference.  
**Learning Goals:**  
- Understand how compiler optimization flags affect performance.  
- See how Emscripten maps typical C optimization approaches into WebAssembly.

**Problem 14: O(N²) Distance Calculation and Flags**  
**Task:**  
Implement an O(N²) pairwise distance calculation. Experiment with `-O3`, `-s WASM=1`, and other flags. Observe memory and runtime differences, and note any gains or issues.  
**Learning Goals:**  
- Learn to tune performance by trying different compiler and linker flags.  
- Gain insight into how memory usage patterns impact performance.

---

### Phase 4: External Libraries (Eigen and FFT)

**Problem 15: Eigen Integration for Matrix Operations**  
**Task:**  
Integrate Eigen (header-only) and implement a matrix multiplication in C. Compile with Emscripten and run it in the browser, verifying correctness.  
**Learning Goals:**  
- Learn how to include and compile external libraries with Emscripten.  
- Understand how complex linear algebra computations fit into a WebAssembly workflow.

**Problem 16: FFT with an External Library**  
**Task:**  
Link in a small FFT library (like KissFFT) and implement a function to take a time-domain signal from JS, run FFT in C, and return frequency-domain data back to JS.  
**Learning Goals:**  
- Understand how to link against external libraries and manage their memory and interfaces.  
- Gain experience integrating more advanced computational routines into your web pipeline.

---

### Phase 5: End-to-End Scientific Simulation Project

**Problem 17: Monte-Carlo Simulation with Periodic Boundaries**  
**Task:**  
Implement a Monte-Carlo step in C that updates particle positions in a box with periodic boundary conditions.  
**Learning Goals:**  
- Integrate memory management, persistent state, and problem-solving logic in a complex scenario.

**Problem 18: NPT Ensemble Control from JS**  
**Task:**  
Expose functions to tune parameters like temperature, density, or pressure from JavaScript. Run the simulation and observe the system’s evolution.  
**Learning Goals:**  
- Manage simulation parameters dynamically and connect user input to the C simulation engine.

**Problem 19: Compute Pair Correlation Functions and FFT**  
**Task:**  
After equilibrating your particle system, compute the pair correlation function. Use the previously integrated FFT library to process the correlation data, and return these results for visualization in JS.  
**Learning Goals:**  
- Combine simulation data with advanced numerical analysis.  
- Validate that external math routines work in tandem with the simulation.

**Problem 20: Final Visualization and Analysis Page**  
**Task:**  
Put it all together: run the simulation in real-time, control it from the browser, store/load states with MEMFS, apply FFT-based analysis, and visualize results via canvas charts. Compare performance with and without optimization flags.  
**Learning Goals:**  
- Demonstrate mastery of all learned concepts—memory management, external libraries, I/O, optimization, and interactivity.  
- Show a complete end-to-end scientific workflow hosted in the browser.

---

This sequence of problems starts with the very basics and moves toward increasingly complex tasks, each with explicitly stated learning goals. The student can see at every step what Emscripten concept or technique they are building toward, ensuring a clear progression and a solid foundation for advanced applications.
