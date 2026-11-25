"""Run offline chat inference with the validated vLLM runtime."""

import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Checkpoint path or repository ID")
    parser.add_argument("--revision", help="Pinned model repository revision")
    parser.add_argument("--block-size", type=int, default=128)
    parser.add_argument(
        "--prompt",
        default=(
            "Why is it harder to keep a room cool when the door is open on a hot day? "
            "Explain in 3-4 simple sentences."
        ),
    )
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--max-model-len", type=int)
    args = parser.parse_args()
    for name in ("tensor_parallel_size", "max_model_len", "block_size"):
        value = getattr(args, name)
        if value is not None and value <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")

    from vllm import LLM, SamplingParams

    options = {
        "model": args.model,
        "tensor_parallel_size": args.tensor_parallel_size,
        "block_size": args.block_size,
    }
    if args.revision:
        options["revision"] = args.revision
    if args.max_model_len is not None:
        options["max_model_len"] = args.max_model_len

    llm = LLM(trust_remote_code=True, **options)
    params = SamplingParams(temperature=0.6, max_tokens=None)
    messages = [{"role": "user", "content": args.prompt}]
    for result in llm.chat(messages, params):
        print(result.outputs[0].text)


if __name__ == "__main__":
    main()
