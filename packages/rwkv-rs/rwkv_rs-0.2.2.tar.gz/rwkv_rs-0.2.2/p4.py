import argparse
import sys

import tiktoken
import rwkv_rs
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
parser.add_argument("text", type=str)
args = parser.parse_args()

assert args.model != '', "Model path can't be empty"
assert args.text != '', "Text can't be empty!"

print("Loading tokenizer")
p4 = tiktoken.get_encoding("cl100k_base")
EOS = p4.encode_single_token("<|endoftext|>")
tokens = p4.encode(args.text, allowed_special='all')

print("Loading model")
model = rwkv_rs.Rwkv(args.model)
state = rwkv_rs.State(model)

print("Preproc")
# model.forward_token(999999999, state)
logits = model.forward(tokens, state)

print("--- --- ---")
# for _ in range(767):
while True:
    token = np.argmax(logits)

    sys.stdout.buffer.write(p4.decode_single_token_bytes(token))
    sys.stdout.buffer.flush()

    if token == EOS:
        break
    logits = model.forward_token(token, state)
