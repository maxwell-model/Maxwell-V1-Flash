# Maxwell-V1.0-Flash Offline Inference

Run **Maxwell-V1.0-Flash** locally with vLLM; no HTTP service is required.
The model weights are **67 GiB**.

## Hardware

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

## Run Inference

### Run on B300

A single GPU is enough:

```bash
docker run --rm --init \
  --gpus all \
  --shm-size 8g \
  -v "$PWD/examples/offline_inference:/workspace/offline_inference:ro" \
  -v "$MODEL_DIR":/models/Maxwell-V1-Flash:ro \
  --entrypoint python \
  maxwellmodel/vllm-openai:v0.30.0 \
  /workspace/offline_inference/offline_inference.py \
  --model /models/Maxwell-V1-Flash \
  --block-size 128 \
  --prompt "Why is it harder to keep a room cool when the door is open on a hot day? Explain in 3-4 simple sentences." \
  --tensor-parallel-size 1
```

### Run on H100

Requires at least two GPUs. Use the same command with `--tensor-parallel-size 2`.
