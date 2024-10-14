# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Set the working directory to /tmp for temporary operations
WORKDIR /tmp

# Update the package list and install necessary dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    libssl-dev \
    cmake \
    pkg-config \
    build-essential \
    curl \
    git \
    zip \
    unzip \
    tar

RUN cmake --version

# Clone vcpkg and install it
RUN git clone https://github.com/microsoft/vcpkg.git

# Navigate to the vcpkg directory and bootstrap vcpkg
WORKDIR /tmp/vcpkg
RUN ./bootstrap-vcpkg.sh

# Install the nlohmann/json library using vcpkg
RUN ./vcpkg install nlohmann-json
RUN ./vcpkg install boost

# Set the working directory for the application
WORKDIR /app

# Copy the source code into the container
COPY . .

# Set the environment variable to point to vcpkg
ENV VCPKG_ROOT=/tmp/vcpkg
ENV PATH="${VCPKG_ROOT}:${PATH}"

# Compile the C++ code using vcpkg integration
RUN g++ -o main main.cpp -I/tmp/vcpkg/installed/x64-linux/include -L/tmp/vcpkg/installed/x64-linux/lib 

