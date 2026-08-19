"""File hashing utility for report artifact provenance (D1).

Computes the exact SHA-256 of the final on-disk bytes of a generated artifact
(canonical JSON, machine index, HTML, PDF). Metadata only — never used in
engine calculations. Deterministic: identical file bytes => identical hash.
"""
import hashlib


def sha256_file(path: str) -> str:
    """Return the lowercase hex SHA-256 digest of the exact file bytes.

    Reads in fixed-size chunks so large PDFs are not loaded into memory whole.
    Raises FileNotFoundError if the file does not exist.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
