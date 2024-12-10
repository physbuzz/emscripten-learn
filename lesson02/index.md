```markdown
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson02" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson04/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 2 (No ccall/ccall): Averaging a Float32 Array

## Question

Write a C function `float computeAverage(float* arr, int length);` that takes a pointer to a float array and its length, computes the average, and returns a float. Pass a `Float32Array` from JavaScript to this function without using `ccall` or `cwrap`. Instead, manually write the data into `HEAPF32` and pass the pointer to the C function.

### Learning Goals:
- Gain hands-on experience with the Emscripten HEAP memory model.
- Understand how to allocate memory in JavaScript and pass typed arrays to C functions.
- Learn how to index `HEAPF32` and ensure correct data transfer between JavaScript and WebAssembly.

---

## Hints

1. **Exporting Functions**:  
   Use the `-s EXPORTED_FUNCTIONS` flag to ensure your C function is accessible from JavaScript. For this problem, you’ll need to export `computeAverage`, `malloc`, and `free`.

2. **Memory Allocation**:  
   Use `Module._malloc()` to allocate memory for the array in the WebAssembly heap. Remember to calculate the size of the memory block in bytes (e.g., `array.length * 4` for a `Float32Array`).

3. **Writing to HEAPF32**:  
   Use `Module.HEAPF32.set()` to copy the JavaScript `Float32Array` into the allocated memory. The pointer returned by `malloc` must be divided by 4 (since `HEAPF32` is a 32-bit view of the memory).

4. **Freeing Memory**:  
   Always free the allocated memory using `Module._free()` after the computation is complete to avoid memory leaks.

5. **Accessing the Function**:  
   Call the exported C function using `Module._computeAverage(ptr, length)` where `ptr` is the pointer to the array in memory.

---

## Solution

### Step 1: Write the C Code

Create a file `bindings.c` with the following implementation:

```c
// bindings.c
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
float computeAverage(float* arr, int length) {
    float sum = 0;
    for (int i = 0; i < length; i++) {
        sum += arr[i];
    }
    return sum / length;
}
```

### Step 2: Compile the C Code

Compile the C code to WebAssembly using the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_computeAverage', '_malloc', '_free']" -o bindings.js
```

### Step 3: Write the HTML and JavaScript

Create an `index.html` file to load the WebAssembly module and interact with it:

```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Average of [10.5, 20.3, 30.7, 40.1]:</p>
    <p id="result">Calculating...</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Step 1: Create a Float32Array in JavaScript
        const numbers = new Float32Array([10.5, 20.3, 30.7, 40.1]);

        // Step 2: Allocate memory in the WebAssembly heap
        const ptr = Module._malloc(numbers.length * 4); // 4 bytes per float

        // Step 3: Copy the Float32Array into the WebAssembly heap
        Module.HEAPF32.set(numbers, ptr >> 2); // Divide by 4 to get the correct index

        // Step 4: Call the C function
        const result = Module._computeAverage(ptr, numbers.length);

        // Step 5: Free the allocated memory
        Module._free(ptr);

        // Step 6: Display the result
        document.getElementById('result').innerHTML = `Average = ${result}`;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

---

## Demo

Average of [10.5, 20.3, 30.7, 40.1]: <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function () {
  const numbers = new Float32Array([10.5, 20.3, 30.7, 40.1]);
  const ptr = Module._malloc(numbers.length * 4);
  Module.HEAPF32.set(numbers, ptr >> 2);
  const result = Module._computeAverage(ptr, numbers.length);
  Module._free(ptr);
  document.getElementById('result').innerHTML = `Average = ${result}`;
};
</script>
<script src="bindings.js"></script>
```