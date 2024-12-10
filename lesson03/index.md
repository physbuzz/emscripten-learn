<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson02" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson04/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 3: Reversing a String & EMSCRIPTEN_KEEPALIVE

## Question

Create a C function `char* reverseString(const char* str)` that takes a `const char*` string, reverses it, and returns a newly allocated reversed string. Ensure the function is not removed by dead code elimination by using `EMSCRIPTEN_KEEPALIVE`. In JavaScript, manually handle UTF8 conversions to pass the string to and from the WebAssembly heap. Display the reversed string on a webpage.

### Learning Goals:
1. Understand how to pass strings between JavaScript and C by writing to and reading from the WebAssembly heap.
2. Learn how `EMSCRIPTEN_KEEPALIVE` ensures symbol visibility and prevents function elimination.
3. Practice manual memory management and string handling without relying on convenience wrappers like `ccall` or `cwrap`.

---

## Hints

1. **UTF8 Encoding and Decoding**:
   - Use `lengthBytesUTF8` and `stringToUTF8` to write a JavaScript string to the WebAssembly heap.
   - Use `UTF8ToString` to read a C string from the WebAssembly heap back into JavaScript.

2. **Memory Management**:
   - Allocate memory for the input string using `Module._malloc()`.
   - Allocate memory for the reversed string inside the C function using `malloc()`.
   - Free the input string memory in JavaScript using `Module._free()` after the function call.
   - Free the reversed string memory in C after returning it to JavaScript.

3. **Compilation**:
   - Use the `-s EXPORTED_FUNCTIONS="['_reverseString', '_malloc', '_free']"` flag to export the necessary functions.

4. **Reversing Logic**:
   - Iterate over the input string in reverse order and copy characters to a new buffer.

---

## Solution

### C Code (`bindings.c`)

```c
#include <emscripten/emscripten.h>
#include <stdlib.h>
#include <string.h>

// Prevent the function from being removed by dead code elimination
EMSCRIPTEN_KEEPALIVE
char* reverseString(const char* str) {
    int length = strlen(str);
    char* reversed = (char*)malloc(length + 1); // Allocate memory for the reversed string (+1 for null terminator)
    if (!reversed) return NULL; // Handle memory allocation failure

    for (int i = 0; i < length; i++) {
        reversed[i] = str[length - i - 1]; // Copy characters in reverse order
    }
    reversed[length] = '\0'; // Null-terminate the reversed string

    return reversed; // Return the pointer to the reversed string
}
```

### HTML and JavaScript (`index.html`)

```html
<!DOCTYPE html>
<html>
  <body>
    <h2>Demo</h2>
    <p>Original String: <span id="original">Hello, WebAssembly!</span></p>
    <p>Reversed String: <span id="result">Calculating...</span></p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Original string to reverse
        const originalString = "Hello, WebAssembly!";
        document.getElementById("original").innerText = originalString;

        // Allocate memory for the input string
        const length = Module.lengthBytesUTF8(originalString) + 1; // Include null terminator
        const inputPtr = Module._malloc(length);

        // Write the string to the WebAssembly heap
        Module.stringToUTF8(originalString, inputPtr, length);

        // Call the reverseString function
        const reversedPtr = Module._reverseString(inputPtr);

        // Read the reversed string from the WebAssembly heap
        const reversedString = Module.UTF8ToString(reversedPtr);

        // Free the allocated memory
        Module._free(inputPtr);
        Module._free(reversedPtr);

        // Display the result
        document.getElementById("result").innerText = reversedString;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Compilation Command

Compile the C code into WebAssembly using the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_reverseString', '_malloc', '_free']" -o bindings.js
```

---

## Demo

Original String: <span id="original">Hello, WebAssembly!</span>  
Reversed String: <span id="result">Calculating...</span>  

<script>
var Module = {};
Module.onRuntimeInitialized = function () {
  const originalString = "Hello, WebAssembly!";
  document.getElementById("original").innerText = originalString;

  const length = Module.lengthBytesUTF8(originalString) + 1;
  const inputPtr = Module._malloc(length);
  Module.stringToUTF8(originalString, inputPtr, length);

  const reversedPtr = Module._reverseString(inputPtr);
  const reversedString = Module.UTF8ToString(reversedPtr);

  Module._free(inputPtr);
  Module._free(reversedPtr);

  document.getElementById("result").innerText = reversedString;
};
</script>
<script src="bindings.js"></script>