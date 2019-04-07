# Blender GPU Rendering using nvidia-docker

This is the repo for the [vogete/blender-cuda](https://hub.docker.com/r/vogete/blender-cuda) Docker image for Blender command line rendering with NVIDIA CUDA capable GPUs. The image is based on the [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda/) image (devel tag) and requires [NVIDIA Container Runtime for Docker (nvidia-docker)](https://github.com/NVIDIA/nvidia-docker) to be installed.

## Tags

- [blender2.79b-cuda10.0-ubuntu18.04](blender2.79b/cuda10.0/ubuntu18.04/Dockerfile)

## Requirements

- NVIDIA driver for your GPUs
- Docker
- nvidia-docker to be installed ([CUDA container requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA))
- Linux, since nvidia-docker can only be installed on Linux!

## Usage

This tutorial is made for beginners in Docker and Blender. If you are experienced, you might find this repetitive.

The image starts with the entrypoint `/usr/local/blender/blender -b`. (`-b` argument is necessary for CLI (background) rendering). You can use any Blender [Command Line Argument](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html) just as you would normally.

To use your GPUs for rendering, you need to pass the `--runtime=nvidia` argument to Docker, set the `NVIDIA_VISIBLE_DEVICES` variable to your desired value (see below for examples), and pass the [force_gpu.py](force_gpu.py) Python script to Blender.

#### Example command

To render a single frame (using GPU(s)) from a blendfile.blend file located in /source/path on the docker host and save the result in the same directory. Make sure the `force_gpu.py` script is available as well!

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all --rm -v /source/path:/media vogete/blender-cuda /media/blendfile.blend -E CYCLES -t 0 -P /media/force_gpu.py -o /media/frame_### -f 1
```

This will render the first frame of your project using the CYCLES render engine, all available CUDA GPUs in your system, and outputs the rendered image in the same folder.

### Multi-GPU setup and GPU selection

The image can run on a multi-gpu setup. The exact GPUs can be selected using the `NVIDIA_VISIBLE_DEVICES`. Value `all` will make the image use all available GPUs. Number values can be used to select a specific GPU. Multiple specific GPUs can be selected with comma separated numbers, like `1,2` or `0,1,4`.

#### Examples

```
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_VISIBLE_DEVICES=1,3
NVIDIA_VISIBLE_DEVICES=2
NVIDIA_VISIBLE_DEVICES=0,2,3
```

GPU information (IDs, models, etc.) can be get from NVIDIA-SMI. The image comes with NVIDIA-SMI, so if you don't have it installed on your machine, you can run it with:

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all --rm --entrypoint "" vogete/blender-cuda nvidia-smi
```

This overrides the default entrypoint so you can use the `nvidia-smi` command instead.
