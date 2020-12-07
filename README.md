# ESGF to Google Cloud CMIP6 workflow

This is a simplification of my old workflow.  It no longer handles
requests. Instead, one specifies the keyword values of the type of data desired. 
The ESGF repo is searched for relevant data and a comparison with the GC catalog is made to see what new data is available.

The notebook
[GetSpecified.ipynb](https://github.com/naomi-henderson/cmip6collect2/blob/main/GetSpecified.ipynb) is now what I use day-to-day to update our GC collection.

The only step not here is the updating of the GC catalog - which is done only one or two times per day, via
a separate request.
