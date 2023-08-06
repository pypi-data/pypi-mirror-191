# SPDX-FileCopyrightText: 2022  mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

/* begin projectnameTest
put the definitions for config.h specific to
your project here. Everything above will be
overwritten
*/

/* begin private */
/* Name of package */
#define PACKAGE "@DUNE_MOD_NAME@"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "@DUNE_MAINTAINER@"

/* Define to the full name of this package. */
#define PACKAGE_NAME "@DUNE_MOD_NAME@"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "@DUNE_MOD_NAME@ @DUNE_MOD_VERSION@"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "@DUNE_MOD_NAME@"

/* Define to the home page for this package. */
#define PACKAGE_URL "@DUNE_MOD_URL@"

/* Define to the version of this package. */
#define PACKAGE_VERSION "@DUNE_MOD_VERSION@"

/* end private */

/* Define to the version of projectnameTest */
#define projectnameTest_VERSION "@projectnameTest_VERSION@"

/* Define the sparse matrix addon for eigen */
#define EIGEN_SPARSEMATRIX_PLUGIN <projectnameTest/utils/eigenSparseAddon.hh>

/* Define to the major version of projectnameTest */
#define projectnameTest_VERSION_MAJOR @projectnameTest_VERSION_MAJOR@

/* Define to the minor version of projectnameTest */
#define projectnameTest_VERSION_MINOR @projectnameTest_VERSION_MINOR@

/* Define to the revision of projectnameTest */
#define projectnameTest_VERSION_REVISION @projectnameTest_VERSION_REVISION@

/* end projectnameTest
Everything below here will be overwritten
*/
