# Draft-model speculative decoding for repository-scale code completion

## Abstract

We study speculative decoding for code completion when the prompt contains several thousand tokens of repository context.
A small draft model proposes tokens and a large target model verifies them in one forward pass.

## 1 Introduction

Latency limits interactive code completion.
Our contribution is a measurement of acceptance rate as repository context grows from 1k to 16k tokens.

## 2 Related work

TODO: write this section. Cover speculative decoding and its variants, and say how our measurement differs.

## 3 Method

We pair a 1B-parameter draft model with a 34B-parameter target model and measure acceptance rate per token position.
