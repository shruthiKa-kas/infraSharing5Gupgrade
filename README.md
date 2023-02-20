Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas and Infrastructure Sharing Strategies for Wireless Broadband (infrasharing5Gupgrade)
====

This codebase evaluates the cost implications of different infrastructure sharing business models in rural areas, especially using 5G, as applied for a generic model.

If there are any additional queries or comments about the code, do not hesitate to reach out to me via email at 'k [dot] a [dot] shruthi [at] strath [dot] ac [dot] uk' for further information.

Please cite the published paper associated with this codebase:

Citation
---------

- Koratagere Anantha Kumar, S. and Oughton, E., 2022. Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas.(https://www.techrxiv.org/articles/preprint/Techno-Economic_Assessment_of_5G_Infrastructure_Sharing_Business_Models_in_Rural_Areas/21258531/1/files/37740480.pdf)

Importantly, I provide all code (and required data inputs) so that the results can be reproduced.
Both unit tests and integration tests are provided with the codebase to ensure reliability.

Method
======
A box diagram of the method is shown below, illustrating the open-source techno-economic 5G simulation model which takes advantage of traffic modelling.

<p align="center">
  <img src="/figures/method.png" />
</p>

Example Results
===============
A visualization of the cost per smartphone connected is shown below for 4G and 5G universal broadband strategies, demonstrating the type of results the codebase can produce.
<p align="center">
  <img src="/figures/results.png" />
</p>

Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and packages.

Create a conda environment called `india5G`:

    conda create --name india5g python=3.9

Activate it (run this each time you switch projects):

    conda activate infra5G

Install `india5G`:

    python setup.py install

Alternatively, for development purposes, clone this repo and run:

    python setup.py develop



Using the model
===============

To obtain model results, simply execute the each script sequentially from in the order of a to f.

Using the R scripts in the infrasharing5Gupgrade/vis folder, the results can be visualized.
