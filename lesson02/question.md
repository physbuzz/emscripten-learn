**Problem 2 (No ccall/ccall): Averaging a Float32 Array**  
**Task:**  
Write a function in C that takes a pointer to a float array and its length, computes the average, and returns a float. Pass a `Float32Array` from JS to this function without `ccall`/`cwrap`, by manually writing the data into `HEAPF32` and passing the pointer.  
**Learning Goals:**  
- Gain hands-on experience with the Emscripten HEAP memory model.  
- Understand how to allocate memory in JS and pass typed arrays to C functions.  
- Learn about indexing `HEAPF32` and ensuring correct data transfer.
