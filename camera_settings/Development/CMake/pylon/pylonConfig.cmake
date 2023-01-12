set (CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_LIST_DIR}")
include(PylonFinder)
include(PylonVersion)
include(FindPackageHandleStandardArgs)

if (_pylon_PylonBase_FOUND)
    set(pylon_VERSION "${pylon_VERSION_MAJOR}.${pylon_VERSION_MINOR}.${pylon_VERSION_SUBMINOR}")
endif()

find_package_handle_standard_args( pylon
    REQUIRED_VARS _pylon_PylonBase_FOUND
    VERSION_VAR pylon_VERSION
)
