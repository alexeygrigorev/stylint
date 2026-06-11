# Code style inside examples

Educational clarity beats defensive coding:

- Access known keys directly. Write `data['web']['results']`, not
  `data.get('web', {}).get('results', [])`. Let required keys fail loudly.
- No `try/except` unless the example is specifically about error handling.
- No speculative validation. Examples are here to show the happy path.
- Use `.get(key, default)` only when the key is optional and absence
  is expected.

This does not apply to production code pasted as reference. Show it as-is, but
say when the final version handles edge cases the notebook skips.

The checker catches double blank lines inside Python examples.

## Show usage, not internals

When you document a code file, do not paste its internal implementation. The
reader does not need the pooling math, the candidate-path loop, or the
normalization steps to use the file. Show how to call it, show the result or
shape it returns, link to the full file, and tell the reader they can read the
code and ask their AI assistant if something is unclear.

Before:

```python
def encode(self, text):
    tokens = self.tokenizer(text, return_tensors="pt")
    output = self.model(**tokens)
    hidden = output.last_hidden_state
    mask = tokens["attention_mask"].unsqueeze(-1)
    summed = (hidden * mask).sum(1)
    counts = mask.sum(1)
    return (summed / counts).squeeze().numpy()
```

After:

```python
vec = embedder.encode("a short sentence")  # (384,)
```

The full `encode` lives in
[embedder.py](https://github.com/example/repo/blob/main/embedder.py). Read it
if you want the pooling details, and ask your AI assistant about anything that
is unclear.
