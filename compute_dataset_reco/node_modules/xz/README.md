xz
==

Xz is the node binding for the xz library, which implements (streaming) LZMA2 compression.

LZMA2 is better than gzip & bzip2 in many cases. Read more about LZMA here: http://en.wikipedia.org/wiki/Lempel-Ziv-Markov_chain_algorithm


Install
-------

```sh
$ npm install
$ npm run test
```


API
---

The API consists of only two stream transform classes: `Compressor` and `Decompressor`.

- `new xz.Compressor([preset], [options])`
- `new xz.Decompressor([options])`

The options object is passed to node's `Transform`. Compression takes a "preset" number, which is an abstraction of the compression difficulty level, from 1 to 9, where 1 puts in the least effort. The default is 6.

Both objects are stream transforms that consume and produce Buffers. Here's example code to compress the sample file included with this distribution:

```javascript
var fs = require("fs");
var xz = require("xz");

var compression = new xz.Compressor(9);
var inFile = fs.createReadStream("./testdata/minecraft.png");
var outFile = fs.createWriteStream("./testdata/minecraft.png.lzma2");

inFile.pipe(compression).pipe(outFile);
```


License
-------

Apache 2 (open-source) license, included in 'LICENSE.txt'.


Authors
-------

- @robey - Robey Pointer <robeypointer@gmail.com>
