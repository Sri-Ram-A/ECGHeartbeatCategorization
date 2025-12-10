from PIL import Image
from pathlib import Path
import random

def inspect_model(
    model, 
    input_size=(1, 3, 64, 1024), 
    criterion=None, 
    optimizer=None, 
    model_name: str = "Model Summary"
):
    """
    Inspect a PyTorch model: prints architecture, MACs, parameters using Rich, 
    and returns a dictionary with key stats for logging.
    """
    from torchinfo import summary as torch_summary
    from ptflops import get_model_complexity_info
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()
    console.rule(f"[bold blue]{model_name}")

    # --- 1. Torchinfo Summary ---
    console.print("[bold yellow]Architecture Summary:")
    torch_summary(model, input_size=input_size, col_names=["input_size", "output_size", "num_params"], verbose=1)

    # --- 2. ptflops: MACs & Params ---
    console.print("\n[bold yellow]MACs and Parameters (ptflops):")
    try:
        macs, params = get_model_complexity_info(
            model,
            input_res=input_size[1:],  # (C,H,W)
            as_strings=True,
            print_per_layer_stat=False,
            verbose=False
        )
    except Exception as e:
        macs, params = "N/A", "N/A"
        console.print(f"[red]ptflops failed: {e}")

    # --- 3. Count Parameters ---
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    # --- 4. Model Size ---
    model_size_mb = sum(p.numel() * p.element_size() for p in model.parameters()) / (1024 ** 2)

    # --- 5. Criterion & Optimizer Info ---
    criterion_name = criterion.__class__.__name__ if criterion else "None"
    optimizer_name = optimizer.__class__.__name__ if optimizer else "None"
    optimizer_params = sum(p.numel() for group in optimizer.param_groups for p in group['params']) if optimizer else 0

    # --- 6. Rich Table Display ---
    table = Table(box=box.MINIMAL_DOUBLE_HEAD, pad_edge=True)
    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="white")

    table.add_row("Total Parameters", f"{total_params:,}")
    table.add_row("Trainable Parameters", f"{trainable_params:,}")
    table.add_row("Optimizer Params", f"{optimizer_params:,}")
    table.add_row("Model Size (MB)", f"{model_size_mb:.3f}")
    table.add_row("MACs", macs)
    table.add_row("FLOPs (approx)", macs)  # MACs ≈ FLOPs
    table.add_row("Loss Function", criterion_name)
    table.add_row("Optimizer", optimizer_name)

    console.print(table)

    # --- 7. Return dictionary for MLflow logging ---
    summary_dict = {
        "total_params": total_params,
        "trainable_params": trainable_params,
        "optimizer_params": optimizer_params,
        "model_size_mb": model_size_mb,
        "MACs": macs,
        "FLOPs": macs,
        "criterion": criterion_name,
        "optimizer": optimizer_name
    }

    return summary_dict
