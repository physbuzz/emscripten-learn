<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson10" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson12/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 11: Alignment and Struct Layout

## Question

Define a C struct that contains mixed data types (e.g., `int`, `float`, and `char`). Write a function to populate the struct and another function to read its values from JavaScript. Demonstrate what happens when memory alignment is incorrect and how to fix it using explicit alignment directives or careful data handling.

**Learning Goals:**
- Understand memory alignment and struct layout in WebAssembly.
- Learn to identify and resolve alignment-related issues when sharing complex data structures between C and JavaScript.

## Hints

1. **Struct Layout in C**:  
   In C, structs are laid out in memory with padding to ensure proper alignment of each member. For example, an `int` (4 bytes) may require padding if it follows a `char` (1 byte).

2. **Alignment in WebAssembly**:  
   WebAssembly enforces strict alignment rules. Misaligned memory access can lead to incorrect results or runtime errors.

3. **Exporting Structs**:  
   To share a struct between C and JavaScript, you can use a pointer to the struct and access its fields using the `Module.HEAP` views (e.g., `HEAP32`, `HEAPF32`, etc.).

4. **Fixing Alignment Issues**:  
   Use `__attribute__((packed))` to disable padding or rearrange struct members to minimize alignment issues. Be cautious, as disabling padding can reduce performance.

5. **Compilation Command**:  
   Use `emcc` with the `-s EXPORTED_FUNCTIONS="['_populateStruct', '_readStruct']"` flag to export the required functions.

## Solution

### Step 1: Define the Struct and Functions in C

```c
// bindings.c
#include <emscripten/emscripten.h>
#include <stdint.h>
#include <string.h>

// Define a struct with mixed data types
typedef struct {
    int id;         // 4 bytes
    float value;    // 4 bytes
    char label[8];  // 8 bytes (fixed-size string)
} MyStruct;

// Function to populate the struct
EMSCRIPTEN_KEEPALIVE
void populateStruct(MyStruct* s, int id, float value, const char* label) {
    s->id = id;
    s->value = value;
    strncpy(s->label, label, sizeof(s->label) - 1);
    s->label[sizeof(s->label) - 1] = '\0'; // Ensure null termination
}

// Function to read the struct and return its `id` (for demonstration)
EMSCRIPTEN_KEEPALIVE
int readStruct(MyStruct* s) {
    return s->id; // Return the `id` field for simplicity
}
```

### Step 2: Compile the Code

Compile the C code into WebAssembly using the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_populateStruct', '_readStruct', '_malloc', '_free']" -o bindings.js
```

### Step 3: Create the HTML and JavaScript Interface

```html
<html>
<body>
  <h2>Demo</h2>
  <p>Struct Data:</p>
  <p id="result">Calculating...</p>

  <script>
    var Module = {};
    Module.onRuntimeInitialized = function () {
      // Allocate memory for the struct
      const structSize = 16; // 4 (int) + 4 (float) + 8 (char[8])
      const structPtr = Module._malloc(structSize);

      // Populate the struct
      const label = "Test";
      Module._populateStruct(structPtr, 42, 3.14, label);

      // Read the struct's `id` field
      const id = Module._readStruct(structPtr);

      // Free the allocated memory
      Module._free(structPtr);

      // Display the result
      document.getElementById("result").innerHTML = `Struct ID: ${id}`;
    };
  </script>
  <script src="bindings.js"></script>
</body>
</html>
```

### Explanation of the Code

1. **Struct Definition**:  
   The `MyStruct` struct contains an `int`, a `float`, and a fixed-size `char` array. This layout ensures proper alignment by default.

2. **Memory Allocation**:  
   Memory for the struct is allocated in JavaScript using `Module._malloc`.

3. **Populate Function**:  
   The `populateStruct` function initializes the struct fields, including copying the string into the `label` array.

4. **Read Function**:  
   The `readStruct` function demonstrates how to access struct fields from JavaScript.

5. **Memory Management**:  
   Allocated memory is freed using `Module._free` to avoid memory leaks.

### Step 4: Fixing Alignment Issues (Optional)

If alignment issues arise, you can explicitly disable padding using `__attribute__((packed))`:

```c
typedef struct __attribute__((packed)) {
    int id;
    float value;
    char label[8];
} MyStruct;
```

However, this may reduce performance on some architectures. Alternatively, rearrange the struct members to minimize padding:

```c
typedef struct {
    float value;    // 4 bytes
    int id;         // 4 bytes
    char label[8];  // 8 bytes
} MyStruct;
```

## Demo

Struct Data: <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function () {
  const structSize = 16; // 4 (int) + 4 (float) + 8 (char[8])
  const structPtr = Module._malloc(structSize);
  const label = "Test";
  Module._populateStruct(structPtr, 42, 3.14, label);
  const id = Module._readStruct(structPtr);
  Module._free(structPtr);
  document.getElementById("result").innerHTML = `Struct ID: ${id}`;
};
</script>
<script src="bindings.js"></script>