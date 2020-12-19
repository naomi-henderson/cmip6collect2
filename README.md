# ESGF to Google Cloud CMIP6 workflow

This is a simplification of my old workflow.  It still handles requests, but the collection is now primarily updated by cycling through popular searches.  This is done by simply specifying the keyword values of the type of data desired. 
As before, the ESGF repo is searched for relevant data and a comparison with the GC catalog is made to see what new data is available.

The notebook
[GetSpecified.ipynb](https://github.com/naomi-henderson/cmip6collect2/blob/main/GetSpecified.ipynb) is now what I use day-to-day to update our GC collection.

The notebook
[Requests.ipynb](https://github.com/naomi-henderson/cmip6collect2/blob/main/Requests.ipynb) is now what I use day-to-day to handle data requests (may be be phased out in the future)

The only steps not here are the updating of the GC catalog - which is done only one or two times per day, via
a separate script and the updating of the ES-DOC errata list.
