
**Problem 9: Canvas Drawing from a Shared Memory Buffer**  
**Task:**  
Allocate a buffer in the Emscripten heap that represents image data or particle positions. Continuously update it in C, and from JS draw these updated points/pixels on an HTML `<canvas>`.  
**Learning Goals:**  
- Learn how to directly access the same memory buffer from both C and JS for rendering.  
- Understand alignment and structure issues in shared data meant for graphics operations.
