# Gladier HEDM Application

High-Energy Diffraction Microscopy (HEDM) is a 3D technique which resolves the structures and strains of individual grains within bulk polycrystalline materials.

The HEDM flow uses [MIDAS](https://github.com/marinerhemant/MIDAS) for reduction of Near-Field and Far-Field High Energy Diffraction Microscopy (HEDM) data developed at Advanced Photon Source. This flow shows using MIADS for on-demand Far-Field analysis.

The flow is implemented using Globus Flows and relies on Globus Compute to perform remote execution.

## Installing Gladier HEDM

To run the flow you will need to configure an appropriate environment for the Globus Compute functions to execute.

    conda create -n gladier pip
    conda activate gladier

    git clone https://github.com/globus-gladier/gladier-hedm
    cd gladier-hedm

    pip install -e .

You will also need to install MIDAS. Instructions can be found [here.](https://github.com/marinerhemant/MIDAS)

## Running the HEDM Flow

Running the flow can be achieved by customizing a deployment configuration, calling gen_input(), and then starting a flow.