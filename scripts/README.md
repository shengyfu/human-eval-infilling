# HumanEval Infilling Benchmarks

This is an evaluation harness for the HumanEval infilling benchmarks described in the [FIM paper](https://arxiv.org/abs/2207.14255).

## Installation

Make sure to use python 3.10 or later:
```
$ conda create -n codex python=3.10
$ conda activate codex
```

Check out and install this repository:
```
$ git clone https://github.com/openai/human-eval-infilling
$ pip install -e human-eval-infilling
```

## Usage

Run the eval.sh in /scripts folder, update the following parameters in eval.sh before running evaluation:
```
model_url="" # model_url
api_key="" # api_key
api_type="chat" # chat or fim
benchmark="test" # "test", "single-line", "multi-line", "random-span", "random-span-light"
model_output_file="gpt35-test.jsonl" # model output
eval_output_file="gpt35-test-eval.txt" # console output
```

```
$ cd scripts
$ ./eval.sh
```