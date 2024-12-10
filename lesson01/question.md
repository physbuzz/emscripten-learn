

**Problem 1 (No ccall/ccall): Basic Integer Addition**  
**Task:**  
Write a C function that takes two integers and returns their sum. Export it to JavaScript without using `ccall` or `cwrap`. Manually manage the function’s address and call it via `Module._functionName`.  
**Learning Goals:**  
- Understand how to compile a C function with Emscripten and access it from JavaScript.  
- Learn basic symbol naming (`Module._myFunction`) and how to call it directly.  
- Get comfortable with the initial Emscripten build commands and environment.
