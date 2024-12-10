<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson02/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 1: Basic Integer Addition (No `ccall`/`cwrap`)

## Question

Write a C function that takes two integers and returns their sum. Export this function to JavaScript using Emscripten, but **do not use `ccall` or `cwrap`**. Instead, manually manage the function’s address and call it using `Module._functionName`.

### Requirements:
1. Create a C function `int add(int a, int b)` that returns the sum of two integers.
2. Compile the C code to WebAssembly using Emscripten.
3. Access the function in JavaScript using `Module._add` and call it directly.
4. Display the result of the addition on a webpage.

### Learning Goals:
- Understand how to compile a C function with Emscripten and access it from JavaScript.
- Learn how to call exported functions directly using `Module._functionName`.
- Get comfortable with the Emscripten build process and JavaScript integration.

---

## Hints

1. **Exporting Functions**:  
   When compiling with Emscripten, use the `-s EXPORTED_FUNCTIONS="['_add']"` flag to ensure the `add` function is exported and accessible in JavaScript.  

2. **Accessing Functions**:  
   After loading the compiled WebAssembly module, Emscripten exposes exported functions as `Module._functionName`. For example, if your function is named `add`, you can call it in JavaScript as `Module._add`.

3. **Compiling the Code**:  
   Use the following command to compile your C code into WebAssembly:  
   ```bash
   emcc add.c -s EXPORTED_FUNCTIONS="['_add']" -o add.js
   ```

4. **Calling the Function**:  
   When calling the function in JavaScript, ensure that the WebAssembly runtime has been initialized. Use `Module.onRuntimeInitialized` to safely call the function after the module is ready.

---

## Solution

### Step 1: Write the C Code (`add.c`)
```c
#include <emscripten/emscripten.h>

// Export the function so it can be accessed from JavaScript
EMSCRIPTEN_KEEPALIVE
int add(int a, int b) {
    return a + b;
}
```

### Step 2: Compile the C Code
Run the following command to compile the C code into WebAssembly:
```bash
emcc add.c -s EXPORTED_FUNCTIONS="['_add']" -o add.js
```

- `-s EXPORTED_FUNCTIONS="['_add']"` ensures the `add` function is exported.
- `-o add.js` specifies the output JavaScript file that will load the WebAssembly module.

### Step 3: Create the HTML File (`index.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Basic Integer Addition</title>
</head>
<body>
    <h2>Basic Integer Addition</h2>
    <p>Result of 7 + 8:</p>
    <p id="result">Calculating...</p>

    <script>
        // Initialize the Emscripten Module
        var Module = {};
        Module.onRuntimeInitialized = function() {
            // Call the exported function directly
            const result = Module._add(7, 8);

            // Display the result on the webpage
            document.getElementById('result').innerHTML = `7 + 8 = ${result}`;
        };
    </script>
    <script src="add.js"></script>
</body>
</html>
```

### Explanation:
1. **C Code**: The `add` function takes two integers as input and returns their sum. The `EMSCRIPTEN_KEEPALIVE` macro ensures the function is not removed during optimization.
2. **Compilation**: The `emcc` command compiles the C code into WebAssembly and generates a JavaScript file (`add.js`) to load the module.
3. **JavaScript Integration**: The `Module._add` function is used to call the `add` function directly. The result is displayed on the webpage.

---

## Demo

Result of 7 + 8: <span id="result">Calculating...</span>

<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    const result = Module._add(7, 8);
    document.getElementById('result').innerHTML = `7 + 8 = ${result}`;
};
</script>
<script src="add.js"></script>

---

### How It Works:
1. When the webpage loads, the `add.js` file initializes the WebAssembly module.
2. Once the module is ready (`onRuntimeInitialized`), the `Module._add` function is called with the arguments `7` and `8`.
3. The result of the addition is displayed in the `<p>` element with the ID `result`.