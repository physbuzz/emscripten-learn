<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson05" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson07/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 6: Re-Implement String Reversal with ccall

## Question

Revisit the string reversal function from Problem 3, but this time, use `ccall` to invoke the function from JavaScript. The goal is to simplify the handling of string arguments and return values by leveraging `ccall`, which abstracts away manual memory management.

### Task:
1. Write a C function `char* reverseString(const char* str);` that reverses a given string.
2. Compile the C function to WebAssembly using Emscripten.
3. Use `ccall` in JavaScript to call the function, passing a string as an argument and receiving the reversed string as the return value.
4. Display the reversed string on a webpage.

### Learning Goals:
- Understand how `ccall` simplifies the process of passing strings between JavaScript and WebAssembly.
- Learn the trade-offs between manual memory management and the convenience of `ccall`.

---

## Hints

1. **Using `ccall`:**
   - `ccall` is a utility provided by Emscripten that allows you to call exported WebAssembly functions directly from JavaScript.
   - It automatically handles string arguments and return values, so you don’t need to manually allocate or free memory.

2. **Exporting the Function:**
   - Ensure the function is exported by compiling with the `-s EXPORTED_FUNCTIONS="['_reverseString']"` flag.

3. **String Handling in C:**
   - Remember that strings in C are null-terminated character arrays. Use `strlen` to determine the length of the input string and reverse it.

4. **Compilation Command:**
   - Use the following command to compile your C code:
     ```bash
     emcc bindings.c -s EXPORTED_FUNCTIONS="['_reverseString']" -o bindings.js
     ```

5. **Example `ccall` Syntax:**
   - Use `ccall` like this:
     ```javascript
     const reversed = Module.ccall('reverseString', 'string', ['string'], ['hello']);
     ```

---

## Solution

### C Code (`bindings.c`):
```c
#include <emscripten/emscripten.h>
#include <string.h>
#include <stdlib.h>

// Function to reverse a string
EMSCRIPTEN_KEEPALIVE
char* reverseString(const char* str) {
    int length = strlen(str);
    char* reversed = (char*)malloc(length + 1); // Allocate memory for the reversed string
    for (int i = 0; i < length; i++) {
        reversed[i] = str[length - i - 1]; // Reverse the string
    }
    reversed[length] = '\0'; // Null-terminate the string
    return reversed;
}
```

### HTML and JavaScript (`index.html`):
```html
<!DOCTYPE html>
<html>
  <head>
    <title>String Reversal with ccall</title>
  </head>
  <body>
    <h2>String Reversal Demo</h2>
    <p>Original String: <span id="original">hello</span></p>
    <p>Reversed String: <span id="reversed">Calculating...</span></p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Original string
        const originalString = "hello";

        // Call the reverseString function using ccall
        const reversedString = Module.ccall(
          "reverseString", // Function name
          "string",        // Return type
          ["string"],      // Argument types
          [originalString] // Arguments
        );

        // Display the results
        document.getElementById("original").innerText = originalString;
        document.getElementById("reversed").innerText = reversedString;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Compilation Command:
```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_reverseString']" -o bindings.js
```

---

## Demo

Original String: <span id="original">hello</span>  
Reversed String: <span id="reversed">Calculating...</span>

<script>
var Module = {};
Module.onRuntimeInitialized = function () {
  const originalString = "hello";
  const reversedString = Module.ccall("reverseString", "string", ["string"], [originalString]);
  document.getElementById("original").innerText = originalString;
  document.getElementById("reversed").innerText = reversedString;
};
</script>
<script src="bindings.js"></script>

---

### Key Takeaways:
- `ccall` simplifies string handling by abstracting memory allocation and deallocation.
- While `ccall` is convenient, it may not be as flexible as manually managing memory for more complex use cases.