# ItsyBitser
Tools to assist development of tiny programs on resource-constrained platforms (such as 8-bit micros).

**NOTE**: Code is currently in a pre-alpha state, there are a number of known bugs and limitations.

## Getting Started
This set of (Python-based) utilities uses [Pipenv](https://pipenv.pypa.io/en/latest/)
to handle dependencies.  You may need to install it if not already present on you system.
The following command should install it:

    pip3 install --user pipenv

Before using the utilities, you must activate the virtual environment created by Pipenv. To do
so, `cd` into the ItsyBitser directory and type:

    pipenv shell

## Summary of Utilities
* **atasciipng.py**: Utility that renders an ATASCII text file as a PNG graphic, with native Atari 8-bit font
* **csvextract.py**: Extract column(s) from CSV file and encode in Hextream format
* **datagen.py**: Generates BASIC DATA statements from Varipacked content
* **fbhtmllist.py**: Generate colorized HTML listing of FastBasic code
* **fbminify.py**: Strip comments, abbreviate, and pack FastBasic code into fewest possible lines
* **glyphextract.py**: Extracts 8x8 monochrome glyphs from a PNG-format "sprite atlas" file
* **hexclean.py**: Strip comments and normalize whitespace for Hextream format content
* **mapextract.py**: Extract map cell content of a Tiled .tmx file as a commented Hextream
* **mapindex.py**: Takes Hextream-encoded map data (as produced by mapextract.py) and produces a comma-delimited list of unique cell values, and the offsets of the map cells where those values first appear
* **varigap.py**: Creates a Varipacker-format "gap" chunk
* **varipack.py**: Packs/unpacks Hextream content to/from the Varipacker format

## “VariPacker” Data Packing and Unpacking
### Overview
"VariPacker" is a general purpose binary data packing system, designed to be easily decoded in constrained environments, such as BASIC interpreters running on 8-bit platforms.  It combines binary-to-text encoding with simple data compression techniques.
* Source data will be ASCII-encoded in DATA statements, using 64 discrete characters.
* The 64 character region used is between $30 and $6F (48 - 111, zero through lowercase letter “o”)
* These characters are:
  * All contiguous, making encoding and decoding a trivial matter of addition or subtraction of the offset (48), with no space-consuming translation table required.
  * All “string and DATA statement friendly.”
* Using these 64 character codes, VariPacker can encode 6 bits per character in a string (log<sub>2</sub> 64 = 6).
### VariPacker Concepts
* Hextream - ASCII-coded hexadecimal (with optional [ignored] whitespace and comments [starting with “#”]).  This is an intermediate format not used by VariPacker directly, but rather used by the toolset that helps encode VariPacker
* .varp – recommended file extension for VariPacker-encoded data
* .hxst - recommended file extension for Hextream-encoded data
* Cycle - a sequence of 1-4 characters (depending on the encoding scheme) which are decoded together as a set
* Chunk – data and metadata for a contiguous sequence of bytes to be loaded into memory
  * Chunk Header - metadata for the chunk.  Consists of two sextets, together holding two fields 
    * Chunk Encoding (3 bits) – how the data are stored and interpreted
    * Chunk Length (9 bits) – size of the chunk payload, measured in output bytes
  * Chunk Payload - zero or more data bytes for the chunk
  * Chunk Encodings  (all are compressive, except Linear64 which is 4/3 expansive, and SextetStream which is neutral)
    * OctetStream a/k/a Linear64 – Encodes 3 bytes using 4 printable characters (i.e. has a cycle length of 4).  This is equivalent to Base64 encoding, but uses a character range and packing layout intended to make it easier to decode in Basic (i.e. uses minimal bit manipulation, no translation table required, no special cases for input length mod 3 ≠ 0).
    * SextetStream – This packs a 6-bit value into each character (i.e. has a cycle length of 1).  This is more efficient than Linear64 for storing byte values that don’t exceed 64
    * TriadStream – This packs two 3-bit values into each character (i.e. has a cycle length of 1).  This is much more efficient than Linear64 or even SextextStream for storing small byte values in the range 0 through 7
    * OctetRun – This is a run-length encoding of n repetitions of the byte represented by the 2-character payload (cycle length of 2)
    * SextetRun – This is a run-length encoding of n repetitions of the 6-bit value represented by the 1-character payload (cycle length of 1)
    * Header – An encoding that is always used for chunk headers, and never for payloads.  It encodes the three bits of the Chunk Type field and nine bits of the Length field into two printable characters (i.e. has a cycle length of 2).
    * Gap – Not actually a chunk, and has no associated payload.  When the decoder encounters this, it increments the output destination pointer by the number of bytes indicated by the length field
* Input Buffer – string into which data from DATA statements are read, prior to decoding them
* Run – a chunk consisting of the same encoded value that is repeated a specified number of times
* Stream – a chunk consisting of a sequence of different encoded values
* Terminal Chunk – “chunk” whose defining characteristic is a length of 0, and which indicates that there is nothing left to unpack, and the decoder should terminate.
