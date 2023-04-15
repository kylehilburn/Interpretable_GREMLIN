This is a README for the shared code repository for:
Hilburn, K. A., 2023: Understanding spatial context in convolutional neural networks using explainable methods: Application to Interpretable GREMLIN. AIES, in review.

This code was run using Python 3.7.3 and Gfortran 8.5.0 on Rocky Linux 8.5 using Intel(R) Core(TM) i7-6850K CPU @ 3.60GHz.
The following Python module versions were used:
    matplotlib 3.1.1
    mpl_toolkits.basemap 1.1.0
    netCDF4 1.4.2
    numpy 1.17.2
    scipy 1.3.1
    skimage 0.16.2
    tensorflow 1.14.0

This README contains instructions for training the interpretable model, and running the analysis in the paper.
Running all of this code will generate a folder with 126 GB of material.

--------------------------------------------------------------------------------

1) Instructions to train the interpretable model

First download the CONUS2 dataset:
    curl https://mountainscholar.org/bitstream/handle/10217/235392/gremlin_conus2_dataset.nc -o gremlin_conus2_dataset.nc
    curl https://mountainscholar.org/bitstream/handle/10217/235392/README_GREMLIN_CONUS2.pdf -o README_GREMLIN_CONUS2.pdf

Then prepare the data:
    python prep_data.py
    python print_datetimes.py > sample_datetimes.txt

Then prepare the interpretable model inputs:
    python prep_inputs.py 1d
    python prep_inputs.py 2d

    The "1d" inputs are used for training, and the "2d" inputs are used for predictions.
    You should now have two files with sizes in bytes:
        gremlin_conus2_inputs_1d.bin 24,199,048,664
        gremlin_conus2_inputs_2d.bin 38,270,402,600

Compile the Fortran code:
    ./compile.sh

Split the training data into batches:
    ./split_data.exe

    The number of batches is determined by:
        integer(4), parameter :: nfiles = 10
    The number of batches will depend on your computer's memory, number of CPUs, and how quickly you want results. 
    If you use a different number for "nfiles", you will also need to modify that variable in
        combine_covar.f90
        calc_intercept.f90

Calculate the covariance matrix:
    nohup ./calc_covar.exe 1 &> nohup_calc1.out &
    nohup ./calc_covar.exe 2 &> nohup_calc2.out &
    nohup ./calc_covar.exe 3 &> nohup_calc3.out &
    nohup ./calc_covar.exe 4 &> nohup_calc4.out &
    nohup ./calc_covar.exe 5 &> nohup_calc5.out &
    nohup ./calc_covar.exe 6 &> nohup_calc6.out &
    nohup ./calc_covar.exe 7 &> nohup_calc7.out &
    nohup ./calc_covar.exe 8 &> nohup_calc8.out &
    nohup ./calc_covar.exe 9 &> nohup_calc9.out &
    nohup ./calc_covar.exe 10 &> nohup_calc10.out &

    Dividing the data into 10 batches runs in 24 hours on my machine, using 1.9 GB per process.

Combine covariance files:
    ./combine_covar.exe

Calculate the coefficients:
    python calc_coefs.py

Calculate the intercept:
    ./calc_intercept.exe

The coefficients and intercept for the linear model have been copied to the files below for reference.
    model_linear_coefs.dat
    model_linear_intercept.dat

Finally, calculate predictions for the interpretable model:
    ./make_linear_predictions_2d.exe test
    ./make_linear_predictions_2d.exe train

--------------------------------------------------------------------------------

2) Instructions for running the analysis in the paper

First, prepare inputs without the gamma correction:
    python prep_inputs.py 2d nogamma

Next generate the predictions for the dense model and GREMLIN CNN:
    python make_dense_predictions_2d.py
    python make_gremlin_predictions_2d.py

    These make use of the GREMLIN CNN:
        model_K12_WTD_ALL_3x3_T_SEQ_blocks_3_epochs_100.h5
    and the DENSE interpretable model:
        model_tune34_epochs100_batchsize10000_layers3_units64.h5
    which are TensorFlow models.

Then run analysis on the predictions:
    python make_stats.py gremlin > stats_gremlin.txt
    python make_stats.py dense > stats_dense.txt
    python make_stats.py linear > stats_linear.txt

    python make_bootstrap_cis.py gremlin 10000 > cis_gremlin_10000.txt &
    python make_bootstrap_cis.py dense 10000 > cis_dense_10000.txt &
    python make_bootstrap_cis.py linear 10000 > cis_linear_10000.txt &

    ./make_bin_avgs.exe data
    ./make_bin_avgs.exe gremlin
    ./make_bin_avgs.exe dense
    ./make_bin_avgs.exe linear

Finally, run scripts to generate figures:
    python plot_stats_with_cis.py
    python plot_compare_prediction_maps.py
    python plot_bin_avgs_1d.py
    python plot_bin_avgs_2d_dxdy.py
    python plot_bin_avgs_2d_levs.py
    python plot_bin_avgs_2d_chans.py
