Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas 
====

Evaluating the cost implications of infrastructure sharing business models in rural areas.

The research in these paper explores future infrastructure sharing strategies, especially for rural areas, predicated on the notion that most locations already have at least some existing infrastructure assets providing basic connectivity (for example, 2G, 3G, or 4G). The key contribution is the estimation of quantitative viability metrics and sensitivity analysis for four different infrastructure sharing strategies to address the digital divide, especially in rural and remote areas. 

Please cite the published paper associated with this codebase:

Citation
---------

- Koratagere Anantha Kumar, S. and Oughton, E., 2022. Techno-Economic Assessment of 5G Infrastructure Sharing Business Models in Rural Areas.(doi:https://dx.doi.org/10.36227/techrxiv.21258531.v1)


Method
======
A box diagram of the method is shown below, illustrating the open-source techno-economic 5G simulation model which takes advantage of traffic modelling. The techno-economic modeling framework used in this study for understanding the business case feasibility of 5G rural upgrades via different infrastructure sharing business models.

<p align="center">
  <img src="/figures/method.png" />
</p>

Example Results
===============
The results shows the NPV for a revenue variation scenario over 10 years in the rural brownfield deployment scenario.
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

For additional queries or comments, please reach out to 'k.a.shruthi@strath.ac.uk' and 'eoughton@gmu.edu' for further information.
