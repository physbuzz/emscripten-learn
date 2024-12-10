
**Problem 5 (With cwrap/ccall): Re-Implement Averaging a Float32 Array**  
**Task:**  
Use `cwrap` (or `ccall`) to call the averaging function from Problem 2. Let `cwrap` handle pointer and type conversions, and compare the code complexity to the previous direct heap-access method.  
**Learning Goals:**  
- Appreciate how `cwrap` reduces boilerplate code in data passing.  
- Reinforce understanding of how Emscripten’s convenience functions map JS types to C types.
