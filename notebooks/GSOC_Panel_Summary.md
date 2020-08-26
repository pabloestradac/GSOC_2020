# GSoC 2020 - Panel Data Spatial Econometrics

This notebook summarize the work of the [PySAL Project on Panel Data Spatial Econometrics](https://summerofcode.withgoogle.com/projects/#6472262816890880). The work is divided in the following sections. First, I explain the utilities used to handle panel data in `spreg`. Second, I show the diagnostics implemented for spatial - panel estimations. Finally, I detail the different models that can be estimated. 

The notebook [Panel_example.ipynb](https://github.com/pabloestradac/GSOC2020/blob/master/notebooks/Panel_example.ipynb) offers an overview of the new estimations that can be useful from the user perspective. 

## Utilities

The utilities for the panel data estimation are located in the file `panel_utils.py`.

- The function `check_panel` handles the structure of the panel data in the estimations of `spreg`. This function converts a panel from wide to long format if needed.

- The function `demean_panel` transforms the variables for the estimations of `spreg`. The transformation assigns a weight from 0 to 1 attached to the cross-sectional component of the data.

## Diagnostics

Diagnostic statistics for the panel data estimation are located in the file `diagnostics_panel.py`.

- **Lagrange Multiplier test:** functions that calculate the classic Lagrange Multiplier test and the robust version for spatial lag and error specifications.

- **Hausman test:** functions to test fixed vs. random effects specifications.

## Estimation

The four basic estimations of panel data with spatial interactions are located in the files `panel_fe.py` and `panel_re.py`.

- `panel_fe.py`

    - **Panel_FE_Lag:** Fixed Effects estimation with spatial lagged dependent variable.

    - **Panel_FE_Error:** Fixed Effects estimation with spatial error interaction.

- `panel_re.py`

    - **Panel_RE_Lag:** Random Effects estimation with spatial lagged dependent variable.

    - **Panel_RE_Error:** Random Effects estimation with spatial error interaction.
    
The step by step explanation of the preceding estimations can be found on the notebooks:
- [FE_Lag_scratch.ipynb](https://github.com/pabloestradac/GSOC2020/blob/master/notebooks/FE_Lag_scratch.ipynb)
- [FE_Error_scratch.ipynb](https://github.com/pabloestradac/GSOC2020/blob/master/notebooks/FE_Error_scratch.ipynb)
- [RE_Lag_scratch.ipynb](https://github.com/pabloestradac/GSOC2020/blob/master/notebooks/RE_Lag_scratch.ipynb)
- [RE_Error_scratch.ipynb](https://github.com/pabloestradac/GSOC2020/blob/master/notebooks/RE_Error_scratch.ipynb)

Finally, all the work can be found in the following pull requests:
- [Random Effects Panel #50](https://github.com/pysal/spreg/pull/50)
- [Fixed Effects Panel - Spatial Error #45](https://github.com/pysal/spreg/pull/45)
- [Fixed Effects Panel - Spatial Lag #41](https://github.com/pysal/spreg/pull/41)

## Future Work

There are three issues outside the scope of the original project that is considered for future work:
- POLS class for Pooled OLS regresion of panel data.
- Add the diagnostics tests at the end of POLS summary.
- Lee-Yu bias correction for fixed effects estimation.
