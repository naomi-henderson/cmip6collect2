# ESGF to Google Cloud CMIP6 workflow

This is a simplification of my old workflow.  It still handles requests, but the collection is now primarily updated by cycling through popular searches.  This is done by simply specifying the keyword values of the type of data desired. 
As before, the ESGF repo is searched for relevant data and a comparison with the GC catalog is made to see what new data is available.

The notebook
[GetSpecified.ipynb](https://github.com/naomi-henderson/cmip6collect2/blob/main/GetSpecified.ipynb) is now what I use day-to-day to update our GC collection.

The notebook
[GetRequested.ipynb](https://github.com/naomi-henderson/cmip6collect2/blob/main/GetRequested.ipynb) is now what I use day-to-day to handle data requests (may be be phased out in the future)

The [esm-collection-spec](https://github.com/NCAR/esm-collection-spec/tree/master/collection-spec/examples) CSV file for the Pangeo Google Cloud datasets is [pangeo-cmip6.csv](https://cmip6.storage.googleapis.com/pangeo-cmip6.csv).

My working request tracker for updating the Google Cloud CMIP6 zarr collection
is
[here](https://docs.google.com/spreadsheets/d/1yAt7604tVt7OXXZUyL2uALtGP2WVa-Pb5NMuTluFsAc/edit?usp=sharing).
