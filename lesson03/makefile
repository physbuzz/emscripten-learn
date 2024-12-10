


default: wasm markdown

wasm:
	emcc bindings.c \
		-sEXPORTED_FUNCTIONS="['_reverseString', '_malloc', '_free']" \
		-sEXPORTED_RUNTIME_METHODS="['lengthBytesUTF8', 'stringToUTF8', 'UTF8ToString']" \
		-o bindings.js

markdown:
	../scripts/md2html.py index.md

clean:
	-rm bindings.js
	-rm bindings.wasm
	-rm index.html
