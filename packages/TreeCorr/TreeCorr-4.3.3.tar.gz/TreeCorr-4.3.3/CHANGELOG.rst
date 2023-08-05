Changes from version 4.2 to 4.3
===============================

See the listing below for the complete list of new features and changes.
`Relevant PRs and Issues,
<https://github.com/rmjarvis/TreeCorr/issues?q=milestone%3A%22Version+4.3%22+is%3Aclosed>`_
whose issue numbers are listed below for the relevant items.

System Support Changes
----------------------

- Starting with this version, TreeCorr no longer supports Python 2.7 or 3.6.
  We currently support Python versions 3.7, 3,8, 3.9, 3.10.

- We now support Windows machines, which we hadn't before this.  Code is now regularly
  tested on ubuntu, macos and windows. (#136, #143)


API Changes
-----------

- Many function parameters are now keyword-only.  The old syntax allowing these parameters
  to be positional still works, but is deprecated. (#129)


Performance improvements
------------------------

- Added ability to compute patch-based covariance matrices using MPI. (#138, #139)


New features
------------

- Add `BinnedCorr2.build_cov_design_matrix` and `build_multi_cov_design_matrix` functions (#132)
- Added ability to write out the full set of pair-wise results in the write commands, and to
  read them back in.  This allows correlation objects to still be able to correctly calculate
  the various patch-based covariance matrix estimates after round-tripping through a file.
  To use this feature, use ``corr.write(..., write_patch_results=True)``. (#141)
- Allow None as a configuration parameter to be equivalent to not specifying a parameter.
  E.g. ``bin_size=0.1, min_sep=1., max_sep=100., nbins=None`` is allowed now. (#142)


Bug fixes
---------

- Fixed a bug where correlation objects using bin_type=TwoD could not be correctly read back
  in after being written to a file. (#141)


Changes from version 4.3.0 to 4.3.1
===================================

- Added `set_max_omp_threads` function to enable turning off OpenMP completely for TreeCorr.

Changes from version 4.3.1 to 4.3.2
===================================

- Added ``dxnom`` and ``dynom`` properties when bin_type is 'TwoD'.

Changes from version 4.3.2 to 4.3.3
===================================

- Fixed a bug in how TwoD and Linear bin_types handle bin_slop.
- Raise an error if user tries to use TwoD bin_type with non-flat coords.
- Delay calculation of covariance matrix until requested.  (Especially important for TwoD binning
  with many bins.)
