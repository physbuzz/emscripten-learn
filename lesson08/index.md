```html
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson07" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson09/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 8: Persistent Memory Array

## Question

Create two C functions:  
1. `void storeArray(float* arr, int length);`  
2. `float* retrieveArray(int* length);`  

The first function should store an array of floats in a global static variable, and the second function should return a pointer to the stored array along with its length. Use these functions in JavaScript to update and retrieve the array over multiple frames, demonstrating that the data persists across calls.

### Learning Goals:
- Understand how global static memory in C persists across multiple calls.
- Learn how to manage persistent simulation state in a WebAssembly context.

---

## Hints

1. **Global Static Variables**:  
   Use a global static pointer in C to store the array and another static variable to store its length. These variables will persist across function calls.

2. **Memory Management**:  
   Allocate memory for the array using `malloc` in the `storeArray` function. Ensure that the memory is freed when no longer needed.

3. **Exporting Functions**:  
   Use the `-s EXPORTED_FUNCTIONS="['_storeArray', '_retrieveArray', '_malloc', '_free']"` flag when compiling with `emcc` to ensure the functions are accessible from JavaScript.

4. **JavaScript Integration**:  
   Use `Module._malloc` to allocate memory for the array in JavaScript and `Module.HEAPF32.set` to copy the array into the allocated memory before passing it to `storeArray`.

---

## Solution

### C Code (`bindings.c`)

```c
#include <emscripten/emscripten.h>
#include <stdlib.h>

// Global static variables to store the array and its length
static float* storedArray = NULL;
static int storedLength = 0;

// Function to store the array
EMSCRIPTEN_KEEPALIVE
void storeArray(float* arr, int length) {
    // Free previously allocated memory if it exists
    if (storedArray != NULL) {
        free(storedArray);
    }

    // Allocate memory and copy the new array
    storedArray = (float*)malloc(length * sizeof(float));
    for (int i = 0; i < length; i++) {
        storedArray[i] = arr[i];
    }
    storedLength = length;
}

// Function to retrieve the array
EMSCRIPTEN_KEEPALIVE
float* retrieveArray(int* length) {
    *length = storedLength;
    return storedArray;
}
```

### HTML and JavaScript (`index.html`)

```html
<html>
<body>
  <h2>Persistent Memory Array Demo</h2>
  <p>Stored Array:</p>
  <p id="storedArray">None</p>

  <button onclick="updateArray()">Update Array</button>
  <button onclick="retrieveArray()">Retrieve Array</button>

  <script>
    var Module = {};
    Module.onRuntimeInitialized = function() {
        console.log("WASM Module Loaded");
    };

    // Function to update the array in C
    function updateArray() {
        const newArray = new Float32Array([10.5, 20.5, 30.5, 40.5]);
        const ptr = Module._malloc(newArray.length * 4); // Allocate memory
        Module.HEAPF32.set(newArray, ptr >> 2); // Copy data to WASM memory

        Module._storeArray(ptr, newArray.length); // Call storeArray in C
        Module._free(ptr); // Free the allocated memory in JS

        document.getElementById('storedArray').innerText = `Updated to: [${newArray.join(", ")}]`;
    }

    // Function to retrieve the array from C
    function retrieveArray() {
        const lengthPtr = Module._malloc(4); // Allocate memory for the length
        const arrayPtr = Module._retrieveArray(lengthPtr); // Call retrieveArray in C

        const length = Module.HEAP32[lengthPtr >> 2]; // Read the length
        const retrievedArray = new Float32Array(Module.HEAPF32.buffer, arrayPtr, length); // Read the array

        Module._free(lengthPtr); // Free the allocated memory for the length

        document.getElementById('storedArray').innerText = `Retrieved: [${Array.from(retrievedArray).join(", ")}]`;
    }
  </script>
  <script src="bindings.js"></script>
</body>
</html>
```

### Compilation Command

Compile the C code with the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_storeArray', '_retrieveArray', '_malloc', '_free']" -o bindings.js
```

---

## Demo

### Steps to Test:
1. Open the HTML file in a browser.
2. Click the "Update Array" button to store a new array in the C code.
3. Click the "Retrieve Array" button to fetch the stored array and display it.

### Example Output:
- After clicking "Update Array":  
  `Stored Array: Updated to: [10.5, 20.5, 30.5, 40.5]`
- After clicking "Retrieve Array":  
  `Stored Array: Retrieved: [10.5, 20.5, 30.5, 40.5]`
```