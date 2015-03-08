# Python OpenGL RenderBuffer example

## About

This code is a standalone example of using multiple renderbuffers in Python.  In this case a Teapot is rendered 4 times to different viewports then a shader is applied, the output is then sent to a renderbuffer.

The renderbuffers are then rendered to screen aligned quads and another shader (optionally) applied to the whole screen.

## Running

You can install the required dependencies with the command

	pip install -r requirements.txt

## Screenshots

![screenshot](/shader1.png "Shader1")

![screenshot](/shader2.png "Shader2")
