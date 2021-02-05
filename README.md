# GeoModelBuilder

The Geometry Model Builder (GMB) is a tool for generating olympiad-level geometry diagrams.
The GMB takes Geometry Model-Building Language programs as input.
For an overview of the GMBL, please refer to our [arXiv paper](https://arxiv.org/abs/2012.02590) or run this program as a local web server and read the tutorial.

## Quick Start

The GMB can be run either as a locally-hosted web server or a command line tool.

### Web Server

Requred once: `cd geo-model-builder && pip3 install -r requirements.txt`

Required for each terminal session: `cd src/ && FLASK_APP=server.py`

To run server: `flask run`

### Command Line Tool

`cd geo-model-builder/src && python3 builder_cli.py --problem INPUT_FILE`

## Parameters

The command line version accepts the following parameteters...
* `problem`: Input GMBL file (required)
* `n_models`: The number of diagrams to generate for the GMBL file (maximum of 10).
* `n_tries`: The maximum number of tries to generate `n_models`. For example, if `n_models = 2` and `n_tries = 2` but GMB fails once, only 1 diagram will be returned.
* `n_inits`: The number of initializations to sample
* `min_dist`: The minimum distance between points
* `plot_freq`: The frequency (in number of steps) of plotting the current model during optimization
* `losses_freq`: The frequency (in number of steps) of printing a summary of loss values
* `loss_freq`: The frequency (in number of steps) of printing the cumulative loss value
* `verbosity`: A coarser-grained control of plotting and loss printing

...as well as the following parameters for Tensorflow optimization:
* `learning_rate`: Initial learning rate
* `decay_rate`: Decay rate
* `eps`: Epsilon value for stopping criteria
* `n_iterations`: Maximum number of iterations for gradient descent
