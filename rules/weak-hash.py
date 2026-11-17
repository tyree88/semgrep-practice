import hashlib

# ruleid: weak-hash
hashlib.md5(b"password")

# ruleid: weak-hash
hashlib.sha1(b"password")

# ruleid: weak-hash
hashlib.new("MD5", b"password")

# ok: weak-hash
hashlib.md5(b"cache-key", usedforsecurity=False)

# ok: weak-hash
hashlib.sha256(b"file contents")
