```html
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson03/" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson05/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 4: Re-Implement Basic Addition with cwrap

## Question

Revisit the addition function from Problem 1, but this time, use `cwrap` to create a JavaScript wrapper for the C function. The goal is to simplify calling the function from JavaScript without directly using `Module._functionName`. 

**Task:**  
1. Write a C function `int addIntegers(int a, int b);` that adds two integers.  
2. Compile the C file to WebAssembly using Emscripten.  
3. Use `cwrap` in JavaScript to create a wrapper for the `addIntegers` function.  
4. Call the wrapper function from JavaScript and display the result on a webpage.

**Learning Goals:**  
- Understand how `cwrap` simplifies calling exported C functions.  
- Observe the difference between direct `Module._functionName` calls and `Module.cwrap()` usage.

---

## Hints

1. **Exporting Functions:**  
   Use the `-s EXPORTED_FUNCTIONS="['_addIntegers']"` flag during compilation to ensure the `addIntegers` function is available for `cwrap`.

2. **Using cwrap:**  
   `cwrap` generates a JavaScript wrapper for a C function. Its syntax is:  
   ```javascript
   var wrappedFunction = Module.cwrap('functionName', 'returnType', ['argType1', 'argType2']);
   ```
   For this problem:  
   - `functionName` is `"addIntegers"`.  
   - `returnType` is `"number"`.  
   - `argType1` and `argType2` are both `"number"`.

3. **Displaying Results:**  
   Use `document.getElementById` to update the webpage with the result of the addition.

4. **Compilation Command:**  
   Compile the C file with:  
   ```bash
   emcc bindings.c -s EXPORTED_FUNCTIONS="['_addIntegers']" -o bindings.js
   ```

---

## Solution

### Step 1: C Code (`bindings.c`)
```c
#include <emscripten/emscripten.h>

// Export the function to WebAssembly
EMSCRIPTEN_KEEPALIVE
int addIntegers(int a, int b) {
    return a + b;
}
```

### Step 2: HTML and JavaScript (`index.html`)
```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Result of addition (using cwrap):</p>
    <p id="result">Calculating...</p>

    <script>
      // Define the Module object
      var Module = {};

      // Wait for the WebAssembly runtime to initialize
      Module.onRuntimeInitialized = function() {
          // Use cwrap to create a JavaScript wrapper for the C function
          const addIntegers = Module.cwrap('addIntegers', 'number', ['number', 'number']);

          // Call the wrapped function
          const result = addIntegers(7, 4);

          // Display the result on the webpage
          document.getElementById('result').innerHTML = `7 + 4 = ${result}`;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Step 3: Compilation Command
Run the following command to compile the C code into WebAssembly and JavaScript:
```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_addIntegers']" -o bindings.js
```

---

## Demo

Result of addition (using cwrap): <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    const addIntegers = Module.cwrap('addIntegers', 'number', ['number', 'number']);
    const result = addIntegers(7, 4);
    document.getElementById('result').innerHTML = `7 + 4 = ${result}`;
};
</script>
<script src="bindings.js"></script>
```