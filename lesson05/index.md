```markdown
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson04" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson06/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 5: Re-Implement Averaging a Float32 Array (Using cwrap/ccall)

## Question

Re-implement the averaging function from Problem 2, but this time use Emscripten's `cwrap` (or `ccall`) to simplify the interaction between JavaScript and the compiled WebAssembly module. 

Instead of manually allocating memory and managing pointers, let `cwrap` handle the type conversions for you. Compare the resulting code complexity to the previous implementation that used direct heap access.

**Learning Goals:**
- Understand how `cwrap` simplifies calling C functions from JavaScript.
- Learn how Emscripten maps JavaScript types to C types automatically.

## Hints

1. Use `cwrap` to wrap the `averageArray` function. This allows you to call it directly from JavaScript without manually managing memory.
2. When using `cwrap`, specify the function signature. For example:
   ```javascript
   const averageArray = Module.cwrap('averageArray', 'number', ['array', 'number']);
   ```
   - The first argument is the C function name.
   - The second argument is the return type (`'number'` for `float`).
   - The third argument is an array of parameter types (`'array'` for the Float32 array and `'number'` for the integer length).
3. Compile the C code with the `-s EXPORTED_FUNCTIONS="['_averageArray']"` flag to ensure the function is available for `cwrap`.

## Solution

### Step 1: Write the C Code (`bindings.c`)

The C function remains the same as in Problem 2:

```c
// bindings.c
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
float averageArray(float* arr, int length) {
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
emcc bindings.c -s EXPORTED_FUNCTIONS="['_averageArray']" -o bindings.js
```

### Step 3: Write the HTML and JavaScript (`index.html`)

Here, we use `cwrap` to simplify the interaction with the WebAssembly module:

```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Average of [1, 2, 3, 4, 5, 6]:</p>
    <p id="result">Calculating...</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Use cwrap to wrap the C function
        const averageArray = Module.cwrap('averageArray', 'number', ['array', 'number']);

        // Define the input array
        const numbers = [1, 2, 3, 4, 5, 6];

        // Call the wrapped function directly
        const result = averageArray(numbers, numbers.length);

        // Display the result
        document.getElementById('result').innerHTML = `Average = ${result}`;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Explanation of Changes:
1. **`cwrap` Usage**: The `cwrap` function wraps the C function `averageArray` and handles memory allocation, type conversion, and pointer management automatically.
2. **Simplified Code**: Unlike the previous implementation, there is no need to manually allocate memory (`_malloc`), copy data to the heap (`HEAPF32.set`), or free memory (`_free`).
3. **Direct Array Passing**: JavaScript arrays can be passed directly to the wrapped function.

## Demo

Average of [1, 2, 3, 4, 5, 6]: <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function () {
    const averageArray = Module.cwrap('averageArray', 'number', ['array', 'number']);
    const numbers = [1, 2, 3, 4, 5, 6];
    const result = averageArray(numbers, numbers.length);
    document.getElementById('result').innerHTML = `Average = ${result}`;
};
</script>
<script src="bindings.js"></script>
```

This implementation demonstrates how `cwrap` reduces boilerplate code and simplifies the interaction between JavaScript and WebAssembly, making it easier to work with C functions in a web environment.
```