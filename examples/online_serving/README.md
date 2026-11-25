# Maxwell-V1.0-Flash Online Serving

Serve **Maxwell-V1.0-Flash** with vLLM through an OpenAI-compatible HTTP API.
The model weights are **67 GiB**.

## Hardware and Runtime

The example has been validated on **NVIDIA H100, and B300** GPUs.

Requires NVIDIA driver >= 580 (CUDA 13.0). On older drivers, add
`-e VLLM_ENABLE_CUDA_COMPATIBILITY=1` to `docker run`.

## Download the Model

Download the weights to a local directory first with the Hugging Face CLI
(install it with `pip install -U huggingface_hub` if `hf` is not available):

```bash
export MODEL_DIR=$PWD/Maxwell-V1-Flash

hf download maxwell-model/Maxwell-V1-Flash --local-dir "$MODEL_DIR"
```

## Serve on B300

A single GPU is enough:

```bash
docker run --rm --init \
  --name vllm-maxwell \
  --gpus all \
  --shm-size 8g \
  --network host \
  -v "$MODEL_DIR":/models/Maxwell-V1-Flash:ro \
  --entrypoint vllm \
  maxwellmodel/vllm-openai:v0.30.0 \
  serve /models/Maxwell-V1-Flash \
  --trust-remote-code \
  --block-size 128 \
  --served-model-name Maxwell-V1.0-Flash \
  --port 8000 \
  --tensor-parallel-size 1 \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder
```

## Serve on H100

Requires at least two GPUs. Use the same command with `--tensor-parallel-size 2`.

## Send a Request

Once either service is ready, run in a second terminal:

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  --data '{
    "model": "Maxwell-V1.0-Flash",
    "messages": [
      {
        "role": "user",
        "content": "Why is it harder to keep a room cool when the door is open on a hot day? Explain in 3-4 simple sentences."
      }
    ],
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20
  }'
```
