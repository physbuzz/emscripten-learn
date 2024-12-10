<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson14" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson16/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 15: Eigen Integration for Matrix Operations

## Question

Integrate the Eigen library (a header-only C++ library for linear algebra) into a WebAssembly project. Implement a matrix multiplication function in C++ using Eigen, compile it with Emscripten, and run it in the browser. Verify the correctness of the matrix multiplication by displaying the result on a webpage.

### Requirements:
1. Use Eigen to multiply two 2x2 matrices.
2. Compile the code to WebAssembly using Emscripten.
3. Pass the matrices from JavaScript to WebAssembly, perform the multiplication, and return the result to JavaScript.
4. Display the resulting matrix on the webpage.

---

## Hints

1. **Including Eigen**:  
   Eigen is a header-only library, so you don't need to link any external libraries. Simply download the Eigen library from its official website (https://eigen.tuxfamily.org/) and include the header files in your project directory.

2. **Compiling with Emscripten**:  
   Use the `-I` flag to specify the path to the Eigen headers when compiling with Emscripten. For example:  
   ```bash
   emcc matrix_multiply.cpp -I/path/to/eigen -s EXPORTED_FUNCTIONS="['_matrixMultiply', '_malloc', '_free']" -o matrix_multiply.js
   ```

3. **Memory Management**:  
   Use `Module._malloc()` and `Module._free()` to allocate and free memory for the input and output matrices. Use `Module.HEAPF32` to transfer data between JavaScript and WebAssembly.

4. **Matrix Representation**:  
   Represent matrices as 1D arrays in JavaScript (e.g., `[a, b, c, d]` for a 2x2 matrix). This simplifies memory management when passing data to WebAssembly.

---

## Solution

### Step 1: Implement the Matrix Multiplication in C++  
Save the following code in a file named `matrix_multiply.cpp`.

```cpp
#include <emscripten/emscripten.h>
#include <Eigen/Dense>

extern "C" {

// Function to multiply two 2x2 matrices
EMSCRIPTEN_KEEPALIVE
void matrixMultiply(float* matA, float* matB, float* result) {
    // Map the input arrays to Eigen matrices
    Eigen::Map<Eigen::Matrix<float, 2, 2, Eigen::RowMajor>> A(matA);
    Eigen::Map<Eigen::Matrix<float, 2, 2, Eigen::RowMajor>> B(matB);
    Eigen::Map<Eigen::Matrix<float, 2, 2, Eigen::RowMajor>> R(result);

    // Perform matrix multiplication
    R = A * B;
}
}
```

### Step 2: Compile the Code  
Compile the C++ code to WebAssembly using Emscripten. Replace `/path/to/eigen` with the actual path to the Eigen library on your system.

```bash
emcc matrix_multiply.cpp -I/path/to/eigen -s EXPORTED_FUNCTIONS="['_matrixMultiply', '_malloc', '_free']" -o matrix_multiply.js
```

### Step 3: Create the HTML File  
Save the following code in a file named `index.html`.

```html
<html>
  <body>
    <h2>Matrix Multiplication with Eigen</h2>
    <p>Matrix A:</p>
    <pre id="matrixA">[[1, 2], [3, 4]]</pre>
    <p>Matrix B:</p>
    <pre id="matrixB">[[5, 6], [7, 8]]</pre>
    <p>Result of A * B:</p>
    <pre id="result">Calculating...</pre>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Define the input matrices
        const matA = new Float32Array([1, 2, 3, 4]); // 2x2 matrix: [[1, 2], [3, 4]]
        const matB = new Float32Array([5, 6, 7, 8]); // 2x2 matrix: [[5, 6], [7, 8]]

        // Allocate memory for the matrices and the result
        const matASize = matA.length * 4; // 4 bytes per float
        const matBSize = matB.length * 4;
        const resultSize = matA.length * 4;

        const matAPtr = Module._malloc(matASize);
        const matBPtr = Module._malloc(matBSize);
        const resultPtr = Module._malloc(resultSize);

        // Copy the matrices into WebAssembly memory
        Module.HEAPF32.set(matA, matAPtr >> 2);
        Module.HEAPF32.set(matB, matBPtr >> 2);

        // Call the matrixMultiply function
        Module._matrixMultiply(matAPtr, matBPtr, resultPtr);

        // Retrieve the result matrix
        const result = new Float32Array(Module.HEAPF32.buffer, resultPtr, matA.length);

        // Display the result
        document.getElementById('result').innerText = `[[${result[0]}, ${result[1]}], [${result[2]}, ${result[3]}]]`;

        // Free the allocated memory
        Module._free(matAPtr);
        Module._free(matBPtr);
        Module._free(resultPtr);
      };
    </script>
    <script src="matrix_multiply.js"></script>
  </body>
</html>
```

---

## Demo

Matrix A:  
```
[[1, 2], [3, 4]]
```

Matrix B:  
```
[[5, 6], [7, 8]]
```

Result of A * B:  
```
[[19, 22], [43, 50]]
```

<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const matA = new Float32Array([1, 2, 3, 4]);
    const matB = new Float32Array([5, 6, 7, 8]);

    const matASize = matA.length * 4;
    const matBSize = matB.length * 4;
    const resultSize = matA.length * 4;

    const matAPtr = Module._malloc(matASize);
    const matBPtr = Module._malloc(matBSize);
    const resultPtr = Module._malloc(resultSize);

    Module.HEAPF32.set(matA, matAPtr >> 2);
    Module.HEAPF32.set(matB, matBPtr >> 2);

    Module._matrixMultiply(matAPtr, matBPtr, resultPtr);

    const result = new Float32Array(Module.HEAPF32.buffer, resultPtr, matA.length);

    document.write(`<pre>[[${result[0]}, ${result[1]}], [${result[2]}, ${result[3]}]]</pre>`);

    Module._free(matAPtr);
    Module._free(matBPtr);
    Module._free(resultPtr);
  };
</script>
<script src="matrix_multiply.js"></script>