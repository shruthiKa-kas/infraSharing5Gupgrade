Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas 
====

This codebase evaluates the cost implications of different infrastructure sharing business models in rural areas.

Please cite the published paper associated with this codebase:

Citation
---------

- Koratagere Anantha Kumar, S. and Oughton, E., 2022. Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas.(https://www.techrxiv.org/articles/preprint/Techno-Economic_Assessment_of_5G_Infrastructure_Sharing_Business_Models_in_Rural_Areas/21258531/1/files/37740480.pdf)


Method
======
A box diagram of the method is shown below, illustrating the open-source techno-economic 5G simulation model which takes advantage of traffic modelling.

<p align="center">
  <img src="/figures/method.png" />
</p>

Example Results
===============
The results shows the NPV for a revenue variation scenario
<p align="center">
  <img src="/figures/results.png" />
</p>

Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and packages.

Create a conda environment called `infrashare5G`:

    conda create --name infrashare5G python=3.9

Activate it (run this each time you switch projects):

    conda activate infrashare5G



Using the model
===============

To obtain model results, simply execute each script sequentially. The obtained results can be plotted on R using the code in "vis" folder.

Contact
=======

For additional queries or comments, please reach out to 'k.a.shruthi@strath.ac.uk' for further information.

