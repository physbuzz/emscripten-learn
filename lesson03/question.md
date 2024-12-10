
**Problem 3 (No ccall/ccall): Reversing a String & EMSCRIPTEN_KEEPALIVE**  
**Task:**  
Create a function that takes a `const char*` string and returns a newly allocated reversed string. Ensure it is not removed by dead code elimination by using `EMSCRIPTEN_KEEPALIVE`. Manually handle UTF8 conversions in JS.  
**Learning Goals:**  
- Understand how to pass strings between JS and C by writing to and reading from the heap.  
- See how `EMSCRIPTEN_KEEPALIVE` affects symbol visibility and prevents function elimination.  
- Reinforce manual memory management and string handling without convenience wrappers.
