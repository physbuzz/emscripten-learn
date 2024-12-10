```html
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson06" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson08/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 7: Using Module.print and Module.printErr

## Question

Create a C function that prints output using `printf` and verify that the output appears in the browser console through `Module.print` and `Module.printErr`.

### Learning Goals:
- Understand how standard I/O from C maps into JavaScript’s logging facilities.
- Learn how to configure or redirect output streams in an Emscripten module.

## Hints

1. **Standard Output and Error Streams**:  
   In Emscripten, `printf` writes to the standard output (`stdout`), which is mapped to `Module.print` by default. Similarly, standard error (`stderr`) is mapped to `Module.printErr`.

2. **Customizing Output**:  
   You can override `Module.print` and `Module.printErr` in JavaScript to customize how the output is handled (e.g., logging to the console, displaying on the webpage, etc.).

3. **Compilation Command**:  
   Use the following command to compile your C code:  
   ```bash
   emcc bindings.c -o bindings.js
   ```

4. **JavaScript Integration**:  
   Use `Module.onRuntimeInitialized` to ensure the WebAssembly module is fully loaded before calling the C function.

## Solution

### C Code (`bindings.c`)

```c
#include <emscripten/emscripten.h>
#include <stdio.h>

// A function that prints to stdout and stderr
EMSCRIPTEN_KEEPALIVE
void logMessages() {
    printf("This is a message from stdout.\n");
    fprintf(stderr, "This is a message from stderr.\n");
}
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Check the browser console for output from the WebAssembly module.</p>

    <script>
      // Customize Module.print and Module.printErr
      var Module = {
        print: function (text) {
          console.log("stdout: " + text); // Redirect stdout to console.log
        },
        printErr: function (text) {
          console.error("stderr: " + text); // Redirect stderr to console.error
        },
      };

      // Call the C function once the module is initialized
      Module.onRuntimeInitialized = function () {
        console.log("Calling logMessages()...");
        Module._logMessages(); // Call the C function
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Compilation Command

Run the following command to compile the C code into WebAssembly and JavaScript:

```bash
emcc bindings.c -o bindings.js
```

This will generate `bindings.js` and `bindings.wasm`, which can be loaded in the browser.

## Demo

### Expected Output in the Browser Console:

1. When the page is loaded, the following messages should appear in the browser console:
   ```
   Calling logMessages()...
   stdout: This is a message from stdout.
   stderr: This is a message from stderr.
   ```

2. The `stdout` message is logged using `console.log`, and the `stderr` message is logged using `console.error`.

### Example Usage:

- Open the `index.html` file in a browser.
- Open the browser developer tools (usually accessible via F12 or right-click → "Inspect").
- Navigate to the "Console" tab to view the output.

This demonstrates how standard I/O from C maps to JavaScript logging facilities and how you can customize the behavior using `Module.print` and `Module.printErr`.
```