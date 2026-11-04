# 3DTeethLand: teeth segmentation evaluation fork

This repository is a fork of [nnistelrooij/3dteethland](https://github.com/nnistelrooij/3dteethland), the authors' solution to the 3DTeethLand challenge. It is used only to **evaluate tooth segmentation** on the 3DTeethSeg'22 test split. Landmark detection is not part of this fork's results.

Changes from the original repository:

- **Landmark step skipped.** `FullNet.landmarks_stage` returns after the refined segmentation, so `python infer.py landmarks` writes only the `STEM_(lower|upper).json` files and no `__kpt.json` files.
- **Binary single-tooth segmentation training.** `train.py binseg` trains the single-tooth segmentation model (`BinSegNet`) from scratch. The data module is in `teethland/datamodules/teethbinseg.py`, the model in `teethland/models/binsegnet.py`.
- **Segmentation-only checkpoint loading.** `FullNet.load_ckpt` can load a landmark checkpoint that contains only the segmentation head.
- **Benchmark config.** `teethland/config/config_bench.yaml` is the submitted configuration with only the paths changed, for running the benchmark.
- **Label shift for 3DTeethSeg'22.** `shift_instances.py` converts instance labels (see below).

Use the two configs as follows:

- `teethland/config/config_bench.yaml`: inference and benchmarking.
- `teethland/config/config.yaml`: training.


## Install

First, setup a Conda environment.

``` bash
conda create -n 3dteethland python=3.10
conda activate 3dteethland
```

Then, install the Pip requirements.

``` bash
pip install -r requirements.txt
```

Lastly, compile and install the Cuda kernels.

``` bash
pip install -e -v .
```


## Benchmark

### 1. Inference

``` bash
python infer.py landmarks --config teethland/config/config_bench.yaml
```

### 2. Shift instance labels

The official 3DTeethSeg'22 evaluation script expects gum to be `0` and teeth to start at `1`. Run `shift_instances.py` to add 1 to every instance value:

``` bash
python shift_instances.py
```

### 3. Evaluation

Use the official 3DTeethSeg'22 evaluation script available at [abenhamadou/3DTeethSeg_MICCAI_Challenges](https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges).


## Training

Training uses `teethland/config/config.yaml`. Set `root` to your training scans, and set the paths of the output and checkpoints.

``` bash
python train.py instseg
python train.py binseg
```