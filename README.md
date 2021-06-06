# Blender GPU Rendering using nvidia-docker

This is the repo for the [vogete/blender-cuda](https://hub.docker.com/r/vogete/blender-cuda) Docker image for Blender command line rendering with NVIDIA CUDA capable GPUs. The image is based on the [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda/) image (devel tag) and requires [NVIDIA Container Runtime for Docker (nvidia-docker)](https://github.com/NVIDIA/nvidia-docker) to be installed.

## Tags

- [blender2.79b-cuda10.0-ubuntu18.04](blender2.79b/cuda10.0/ubuntu18.04/Dockerfile)
- [blender2.83-cuda10.2-ubuntu18.04](blender2.83/cuda10.2/ubuntu18.04/Dockerfile)
- [blender2.83-cuda11.3-ubuntu18.04](blender2.83/cuda11.3/ubuntu18.04/Dockerfile)
- [blender2.83-cuda11.3-ubuntu20.04](blender2.83/cuda11.3/ubuntu20.04/Dockerfile)
- [blender2.92-cuda10.2-ubuntu18.04](blender2.92/cuda10.2/ubuntu18.04/Dockerfile)
- [blender2.92-cuda11.3-ubuntu18.04](blender2.92/cuda11.3/ubuntu18.04/Dockerfile)
- [blender2.92-cuda11.3-ubuntu20.04](blender2.92/cuda11.3/ubuntu20.04/Dockerfile)

## Requirements

- NVIDIA driver for your GPUs
- Docker
- [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) (NVIDIA Container Toolkit) to be installed ([CUDA container requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA))
- A [supported Linux distribution](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#linux-distributions) for the Nvidia Container Runtime.

_Note: I had to disable secure boot on Ubuntu 20.04 so that nvidia-docker can see the GPU(s) properly, but your mileage may vary._

## Usage

This tutorial is made for beginners in Docker and Blender. If you are experienced, you might find this repetitive.

The image starts with the entrypoint `/usr/local/blender/blender -b`. (`-b` argument is necessary for CLI (background) rendering). You can use any Blender [Command Line Argument](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html) just as you would normally.

To use your GPUs for rendering, you need to pass the `--runtime=nvidia` argument to Docker, set the `NVIDIA_VISIBLE_DEVICES` variable to your desired value (see below for examples), and pass the [force_gpu.py](force_gpu.py) Python script to Blender. In  Blender 2.8 or newer versions you should use the [enable_gpu.py](enable_gpu.py). This Python script also allows you to change between CUDA and OpenCL if you wish to do so (defaults to CUDA if you don't edit the script).

### Example usage

To render a single frame (using GPU(s)) from a blendfile.blend file located in /source/path on the docker host and save the result in the same directory. Make sure the `force_gpu.py` (or the `enable_gpu.py`) script is available as well!

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all --rm -v /source/path:/media vogete/blender-cuda /media/blendfile.blend -E CYCLES -t 0 -P /media/force_gpu.py -o /media/frame_### -f 1
```

This will render the first frame of your project using the CYCLES render engine, all available CUDA GPUs in your system, and outputs the rendered image in the same folder.

If you want to use Docker Compose, this template is doing the same as the `docker run` command above. You can run this docker-compose file with `docker-compose run --rm blender-cuda` (or just a simple `docker-compose up`).

```yaml
---
  version: "2.4"
  services:
    blender-cuda:
      image: vogete/blender-cuda
      container_name: blender-cuda
      runtime: nvidia
      environment:
        # 'all' uses all available GPUs. Specific GPU(s) can be selected with comma separated numbers, like '1,2' or '0,1,4'.
        NVIDIA_VISIBLE_DEVICES: all
      volumes:
        # Replace '/source/path' with your Blender project's location
        - /source/path:/media
      # Remember to change blendfile to your project's file name. Also make sure the force_gpu.py (or enable_gpu.py) is available in the same folder.
      command: '/media/blendfile.blend -E CYCLES -t 0 -P /media/force_gpu.py -o /media/frame_### -f 1'
```

_The `command` parameter is where you pass command line arguments to Blender._

If you want to reuse the container for multiple projects, the `--rm` flag is not necessary to pass to Docker.

### Multi-GPU setup and GPU selection

The image can run on a multi-gpu setup. The exact GPUs can be selected using the `NVIDIA_VISIBLE_DEVICES`. Value `all` will make the image use all available GPUs. Number values can be used to select a specific GPU. Multiple specific GPUs can be selected with comma separated numbers, like `1,2` or `0,1,4`.

#### GPU config examples

```
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_VISIBLE_DEVICES=1,3
NVIDIA_VISIBLE_DEVICES=2
NVIDIA_VISIBLE_DEVICES=0,2,3
```

GPU information (IDs, models, etc.) can be get from NVIDIA-SMI. The image comes with NVIDIA-SMI, so if you don't have it installed on your machine, you can run it with:

```bash
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all --rm --entrypoint "" vogete/blender-cuda nvidia-smi
```

This overrides the default entrypoint so you can use the `nvidia-smi` command instead.

### Build the images yourself

If you'd like to use your self-built images rather than downloading it from Docker Hub, just clone the repo, navigate to the repo folder, and build the image. Example usage:

```
git clone https://github.com/Vogete/blender-cuda-docker.git
cd blender-cuda-docker
docker build ./blender2.92/cuda11.3/ubuntu20.04/
```

If everything went well, you'll get a message like `Successfully built 6f91269abd09`. Take the hash ID from the output, and use it as your image name to run the image. For example:

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all --rm -v /source/path:/media 6f91269abd09 /media/blendfile.blend -E CYCLES -t 0 -P /media/enable_gpu.py -o /media/frame_### -f 1
```