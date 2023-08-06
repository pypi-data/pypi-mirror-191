IDF converter is a set of Python tools to convert satellite, in-situ and
numerical model data into Intermediary Data Format, i.e. self-contained,
CF-compliant NetCDF files that are easier to analyse than the original files.

The IDF files produced by the converter can also be visualised using SEAScope,
a viewer which offers advanced rendering functionalities that ease the
detection of synergies between several sources of observations and simulations
(available on Linux, Windows and macOS).

For more information about the Intermediate Data Format (IDF), please read the
`IDF specifications document`_

You can download SEAScope and some examples of IDF files on the
`SEAScope website`_.

.. _IDF specifications document: https://seascope.oceandatalab.com/docs/idf_specifications_1.5.pdf
.. _SEAScope website: https://seascope.oceandatalab.com


Changelog
=========

0.1.312 (2022-10-06)
--------------------

* Readers for Sentinel-1 L2 data have been modified to include the name of the
  L2 SAFE as a global attribute (named L2_SAFE) in the output IDF file. This
  only applies when the input file was located in a directory layout matching
  the SAFE specifications.

0.1.309 (2022-10-03)
--------------------

* Readers for Sentinel-1 L2 data have been modified to avoid naming conflicts
  for granules from the same datatake and inaccurate temporal coverage for
  files generated with versions of the Instrument Processing Facility (IPF)
  below 3.40.

0.1.308 (2022-09-09)
--------------------

* Initial version
