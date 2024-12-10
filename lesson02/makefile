

default: wasm markdown

wasm:
	emcc bindings.c -s EXPORTED_FUNCTIONS="['_computeAverage', '_malloc', '_free']" -o bindings.js

markdown:
	../scripts/md2html.py index.md

clean:
	-rm bindings.js
	-rm bindings.wasm
	-rm index.html
