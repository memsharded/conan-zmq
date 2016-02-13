##=============================================================================
##
##  Copyright (c) Kitware, Inc.
##  All rights reserved.
##  See LICENSE.txt for details.
##
##  This software is distributed WITHOUT ANY WARRANTY; without even
##  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##  PURPOSE.  See the above copyright notice for more information.
##
##=============================================================================
# - Try to find ZeroMQ headers and libraries
#
# Usage of this module as follows:
#
#     find_package(ZeroMQ)
#
# Variables used by this module, they can change the default behaviour and need
# to be set before calling find_package:
#
#  ZeroMQ_ROOT_DIR  Set this variable to the root installation of
#                            ZeroMQ if the module has problems finding
#                            the proper installation path.
#
# Variables defined by this module:
#
#  ZEROMQ_FOUND              System has ZeroMQ libs/headers
#  ZeroMQ_LIBRARIES          The ZeroMQ libraries
#  ZeroMQ_INCLUDE_DIR        The location of ZeroMQ headers

MESSAGE(STATUS "CUSTOM CONAN FIND ZeroMQ")

find_path(ZeroMQ_ROOT_DIR
  NAMES include/zmq.h
  )

if(MSVC)
  #now try to find the release and debug version
  find_library(ZeroMQ_LIBRARY
    NAMES ${CONAN_LIBS_ZMQ} zmq libzmq
    HINTS ${ZeroMQ_ROOT_DIR}/bin
          ${ZeroMQ_ROOT_DIR}/lib
    )
else()
  find_library(ZeroMQ_LIBRARY
    NAMES zmq libzmq
    HINTS ${ZeroMQ_ROOT_DIR}/lib
    )
endif()

find_path(ZeroMQ_INCLUDE_DIR
  NAMES zmq.h
  HINTS ${ZeroMQ_ROOT_DIR}/include
  )

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(ZeroMQ DEFAULT_MSG
  ZeroMQ_LIBRARY
  ZeroMQ_INCLUDE_DIR
  )

set(ZeroMQ_INCLUDE_DIRS ${ZeroMQ_INCLUDE_DIR})
set(ZeroMQ_LIBRARIES ${ZeroMQ_LIBRARY})

mark_as_advanced(
  ZeroMQ_ROOT_DIR
  ZeroMQ_LIBRARY
  ZeroMQ_LIBRARY_DEBUG
  ZeroMQ_LIBRARY_RELEASE
  ZeroMQ_INCLUDE_DIR
  )