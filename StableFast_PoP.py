import torch


# ---------------------------------------------------------------------------
# Node definition
# ---------------------------------------------------------------------------

class StableFastNode_PoP:
    """
    Accelerates a diffusion model's UNet forward pass using
    ``torch.compile`` (PyTorch ≥ 2.0).

    **What Stable-Fast does**

    Stable-Fast is a technique that compiles model inference code to
    optimised native kernels (via Triton or other backends), removes
    Python interpreter overhead through graph capture, and fuses
    operations that would normally run as separate CUDA kernels.  The
    result is typically a significant reduction in per-step latency with
    no change to output quality.

    **Implementation note**

    This node wraps the ComfyUI UNet call with ``torch.compile``.  The
    compiled function is cached so the expensive compilation step only
    happens on the first inference call; subsequent calls use the cached
    kernel and run at full speed.

    Backends:
        * ``inductor`` (default) — PyTorch's built-in compiler; best
          general-purpose choice.  Requires Triton (Linux / CUDA).
        * ``cudagraphs`` — Captures a static CUDA graph; very fast for
          fixed-shape inputs but cannot handle dynamic shapes.
        * ``eager`` — No compilation; effectively a no-op useful for
          debugging or when running on CPU.

    Args:
        model: The ComfyUI MODEL to optimise.
        backend: torch.compile backend to use.
        fullgraph: If True, require the entire UNet to be compiled into a
            single graph (errors if graph breaks occur).  If False,
            graph breaks fall back to eager execution.
        dynamic: If True, allow symbolic shapes so the compiled kernel
            works across multiple resolutions without recompilation.

    Raises:
        RuntimeError: If ``torch.compile`` is unavailable (PyTorch < 2.0).
    """

    BACKENDS = ["inductor", "cudagraphs", "eager"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "backend": (
                    cls.BACKENDS,
                    {
                        "default": "inductor",
                        "tooltip": (
                            "torch.compile backend.  'inductor' is the recommended "
                            "default; 'cudagraphs' can be faster for fixed-size inputs; "
                            "'eager' disables compilation (debug/CPU use)."
                        ),
                    },
                ),
                "fullgraph": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": (
                            "Require the full UNet to compile as a single graph. "
                            "Raises an error on graph breaks when enabled."
                        ),
                    },
                ),
                "dynamic": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": (
                            "Allow symbolic (dynamic) shapes.  Keeps the compiled "
                            "kernel valid across different resolutions."
                        ),
                    },
                ),
            }
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "apply_stable_fast"
    CATEGORY = "PoP/StableFast"

    def apply_stable_fast(self, model, backend: str, fullgraph: bool, dynamic: bool):
        if not hasattr(torch, "compile"):
            raise RuntimeError(
                "torch.compile is not available.  "
                "Upgrade to PyTorch 2.0 or later to use the Stable-Fast node."
            )

        model = model.clone()

        # Cache the compiled callable so compilation only happens once.
        compiled_fn = None

        _backend = backend
        _fullgraph = fullgraph
        _dynamic = dynamic

        def stable_fast_wrapper(apply_model, inputs):
            nonlocal compiled_fn
            if compiled_fn is None:
                try:
                    compiled_fn = torch.compile(
                        apply_model,
                        backend=_backend,
                        fullgraph=_fullgraph,
                        dynamic=_dynamic,
                    )
                except Exception as exc:
                    raise RuntimeError(
                        f"torch.compile failed with backend='{_backend}': {exc}"
                    ) from exc

            return compiled_fn(
                inputs["input"],
                inputs["timestep"],
                **inputs["c"],
            )

        model.set_model_unet_function_wrapper(stable_fast_wrapper)
        return (model,)


NODE_CLASS_MAPPINGS = {
    "StableFastNode_PoP": StableFastNode_PoP,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StableFastNode_PoP": "Stable-Fast (PoP)",
}
