FROM nvidia/cuda:10.2-devel-ubuntu18.04
MAINTAINER Zoltán Fraknói

ENV BLENDER_MAJOR 2.92
ENV BLENDER_VERSION 2.92.0
ENV BLENDER_TAR_URL https://download.blender.org/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux64.tar.xz

RUN apt-get update && \
	apt-get install -y \
		curl wget nano \
		bzip2 libfreetype6 libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 libxrender1 && \
	apt-get -y autoremove

# Install blender

RUN mkdir /usr/local/blender && \
	wget --quiet ${BLENDER_TAR_URL} -O blender.tar.xz && \
	tar -xvf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
	rm blender.tar.xz


VOLUME /media


ENTRYPOINT ["/usr/local/blender/blender", "-b"]