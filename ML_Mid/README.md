# DNNb with Mid & Low Level Variables

### Mid&Low Level Variable Distribution
__Mid and low level variables overview__ ([output format reference](https://github.com/dguest/delphes-rave/wiki/Output-Format#jet-properties))

The mid and low variables are organized as:

> [{primary_track_1}, {primary_track_2}, ... {secondary_track_1}, {secondary_track_2}, ...]

There are **15** tracks in total. Within each track, **28** variables are grouped as:

> {{track_variables}, {track_covariance}, {track_weight}, {vertex_variables}}

There are **5** ``track_variables``:

> D0, Z0, PHI, THETA, QOVERP

There are **15** ``track_covariance``:

> D0D0,

> Z0D0, Z0Z0,

> PHID0, PHIZ0, PHIPHI,

> THETAD0, THETAZ0, THETAPHI, THETATHETA,

> QOVERPD0, QOVERPZ0, QOVERPPHI, QOVERPTHETA, QOVERPQOVERP

``track_weight`` is a single value that is related to how strongly the track is associated with the corresponding vertex.

--a higher value means the track is a better fit to the vertex.

There are **7** vertex variables:

> mass, displacement, delta_eta_jet, delta_phi_jet,
> displacement_significance, n_tracks, energy_fraction

__Mid and Low Level Distribution Result__

![Image of mid_level variables](https://github.com/cniii/DNNb-/blob/master/Distribution_Plot/mid_variables_c.png)



### HDF5 Data Format
``gjj_Variables_mid.hdf5`` contains two data set:
1. ``mid_variables`` stores the mid & low level jet and track variables

   *Shape*: (1, 422, number of events)

   **422** variables: **15** tracks \* **28** track variables + **2** jet variables.

2. ``mid_pid`` stores the particle ID

   **Shape**: (1, 422, number of events)

   boolean flag:

   0 column -> bottom

   1st column -> charm

   2nd colum -> background


### Getting Ready for Machine Learning
__Mid Level variables Correlation Matrix__
Correlation matrix for each track:
![track1](DNNb-/ML_Mid/Mid_Corr_track1.png)
![track2](DNNb-/ML_Mid/Mid_Corr_track2.png)
![track3](DNNb-/ML_Mid/Mid_Corr_track3.png)
![track4](DNNb-/ML_Mid/Mid_Corr_track4.png)
![track5](DNNb-/ML_Mid/Mid_Corr_track5.png)

![track6](DNNb-/ML_Mid/Mid_Corr_track6.png)
![track7](DNNb-/ML_Mid/Mid_Corr_track7.png)
![track8](DNNb-/ML_Mid/Mid_Corr_track8.png)
![track9](DNNb-/ML_Mid/Mid_Corr_track9.png)
![track10](DNNb-/ML_Mid/Mid_Corr_track10.png)
*Note* data from \#10+ tracks is too sparse for plotting.

TODO
-[x] plot the correlation matrices
-[] understanding the plots
-[] implement simple feedforward for mid level


