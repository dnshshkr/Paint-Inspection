include(CMakePrintHelpers)
#----------------------------------------------------------------------------------------------------------#
# find logic
#----------------------------------------------------------------------------------------------------------#

include( "${CMAKE_CURRENT_LIST_DIR}/PylonVersion.cmake")

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
# Helper Macro to find the genicam libraries in the filesystem
# IN module name in Camel casing without platform dependet
#                pre- and suffix
# OUT uniquely generated variables
#   _genicam_<module>_FOUND   TRUE iff module was found,
#   _<module>_lib     full path to dynamic library rsp. import library in case of windows,
#   _<module>_dll     full path to dynamic library in case of windows
#
macro(_find_genicam_library LIB_NAME)
    # creation of a list of all possible file names
    unset(_lib_names)
    unset(_dll_names)
    foreach(_suffix ${_genicam_known_suffixes})
        list(APPEND _lib_names "${_libprefix}${LIB_NAME}${_suffix}${_pylon_lib_file_extension}")

        # for windows, also the dll files must be found
        if (WIN32)
            list(APPEND _dll_names "${LIB_NAME}${_suffix}.dll")
        endif()
    endforeach()
    #cmake_print_variables( _genicam_known_suffixes _lib_names _pylon_lib_path)

    # find the library (.lib/.so)
    find_library(_${LIB_NAME}_lib
        NAMES ${_lib_names}
        PATHS ${_pylon_lib_path}
        NO_DEFAULT_PATH
    )

    # find the .dll
    if (WIN32)
        find_file(_${LIB_NAME}_dll
            NAMES ${_dll_names}
            PATHS ${pylon_ROOT}/../Runtime/${pylon_ARCH}
            NO_DEFAULT_PATH
        )
    endif()
   # handle the find result

    if (_${LIB_NAME}_lib OR _${LIB_NAME}_dll)
        set(_genicam_${LIB_NAME}_FOUND True)
    else()
        message(STATUS "[genicam] Unable to find ${LIB_NAME}")
    endif()

endmacro()

#---------------------------
# find dynamic libraries and import libraries
# IN module name in Camel casing without platform dependet
#                pre- and suffix
# OUT uniquely generated variables
#   _pylon_<module>_FOUND   TRUE iff module was found,
#   _<module>_lib     full path to dynamic library rsp. import library in case of windows,
#   _<module>_dll     full path to dynamic library in case of windows
#
#---------------------------
macro(_find_pylon_library LIB_NAME)
    # creation of a list of all possible file names
    unset(_lib_names)
    unset(_dll_names)
    foreach(_suffix ${_pylon_known_suffixes})
        if(UNIX)
            set( _cs_lib_name "${_libprefix}${LIB_NAME}${_pylon_lib_file_extension}${_suffix}")
        else()
            # PylonC is intended to have no vesion suffix due to user requirements.
            if (WIN32 AND "${LIB_NAME}" STREQUAL "PylonC")
                set( _cs_lib_name "${_libprefix}${LIB_NAME}${_pylon_lib_file_extension}")
            else()
                set( _cs_lib_name "${_libprefix}${LIB_NAME}${_suffix}${_pylon_lib_file_extension}")
            endif()
        endif()
        string( TOLOWER ${_cs_lib_name} _ci_lib_name )
        list(APPEND _lib_names ${_cs_lib_name} )
        list(APPEND _lib_names ${_ci_lib_name} )
        #cmake_print_variables( _cs_lib_name _ci_lib_name)

        # for windows, also the dll files must be found
        if (WIN32)
            list(APPEND _dll_names "${LIB_NAME}${_suffix}.dll")
        endif()
    endforeach()
    #cmake_print_variables( _lib_names )

    # find the library (.lib/.so)
    find_library(_${LIB_NAME}_lib
        NAMES ${_lib_names}
        PATHS ${_pylon_lib_path}
        NO_DEFAULT_PATH
    )

    # find the .dll
    if (WIN32)
        find_file(_${LIB_NAME}_dll
            NAMES ${_dll_names}
            PATHS ${pylon_ROOT}/../Runtime/${pylon_ARCH}
            NO_DEFAULT_PATH
        )
    endif()
   # handle the find result
    if (_${LIB_NAME}_lib)
        set(_pylon_${LIB_NAME}_FOUND True)
    else()
        message(STATUS "[pylon] Unable to find ${LIB_NAME}")
    endif()
endmacro()

#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#
function (_pylon_add_target  _target _import _location _dependencies)


   #cmake_print_variables( _target _import _location _dependencies )

   # if the target was already added, just return
   if (TARGET ${_target})
      return()
   endif()

   add_library(${_target} SHARED IMPORTED)
   if (WIN32)
     set_target_properties( ${_target}
       PROPERTIES
       IMPORTED_LOCATION
        "${_location}"
       INTERFACE_LINK_LIBRARIES
        "${_dependencies}"
       IMPORTED_IMPLIB
        "${_import}"
     )
   else()
     set_target_properties( ${_target}
       PROPERTIES
       IMPORTED_LOCATION
        "${_import}"
       INTERFACE_LINK_LIBRARIES
        "${_dependencies}"
       IMPORTED_IMPLIB
        "${_import}"
      )
   endif()

   target_link_directories(${_target} INTERFACE ${_pylon_lib_path})

   #cmake_print_properties( TARGETS ${_target} PROPERTIES INTERFACE_LINK_LIBRARIES IMPORTED_IMPLIB IMPORTED_LOCATION )

endfunction()
#----------------------------------------------------------------------------------#
macro (_find_pylon_root)
  find_path( _rootpath
    NAMES
       PylonVersionNumber.h
    HINTS
       "$ENV{ProgramFiles}/Basler/pylon ${pylon_VERSION_MAJOR}/Development"
       /Library/Frameworks/pylon.framework
       /opt/pylon
    PATH_SUFFIXES
       include/pylon
       Headers
  )
  if (_rootpath)
    cmake_path(GET _rootpath PARENT_PATH _pylonpath )
    if (UNIX OR WIN32)
      cmake_path(GET _pylonpath PARENT_PATH _pylonpath )
    endif()
    cmake_print_variables( _rootpath _pylonpath )
    set( pylon_ROOT ${_pylonpath} )
    message( "pylon_ROOT=${_pylonpath}")
  endif()
endmacro()

if (WIN32)
    GET_FILENAME_COMPONENT( PYLON_INSTALL_DIR "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Basler\\pylon;InstallationFolder]" ABSOLUTE CACHE )
    message( "[pylon] installation = ${PYLON_INSTALL_DIR}" )
endif()

if (DEFINED pylon_ROOT)
    message( "pylon_ROOT set")
elseif (DEFINED ENV{PYLON_DEV_DIR})
    message( "pylon_ROOT=$ENV{PYLON_DEV_DIR}")
    set(pylon_ROOT $ENV{PYLON_DEV_DIR})
elseif (DEFINED ENV{PYLON_ROOT})
    message( "pylon_ROOT=$ENV{PYLON_ROOT}")
    set(pylon_ROOT $ENV{PYLON_ROOT})
elseif(DEFINED PYLON_INSTALL_DIR)
    set(pylon_ROOT "${PYLON_INSTALL_DIR}/Development")
else()
  _find_pylon_root()
endif()

# pylon_ROOT is set or registry is found
if (NOT DEFINED pylon_ROOT)
    set(_undefined_message "${_undefined_message} Request to find pylon, but [pylon_ROOT] not defined\n")
endif()

# pylon_ARCH / genicam_ARCH must be set
if (DEFINED pylon_ARCH)
    message( "pylon_ARCH set" )
elseif(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(pylon_ARCH "x64")
else()
    set(pylon_ARCH "Win32")
endif()
if (NOT DEFINED pylon_ARCH)
    set(_undefined_message "${_undefined_message} Request to find pylon, but [pylon_ARCH] not defined\n")
endif()
set( genicam_ARCH $pylon_ARCH )

# report an error to the user, some variables are not defined
if (DEFINED _undefined_message)
    message(SEND_ERROR ${_undefined_message})
    return()
endif()



# create an interface library for the headers only
#message( STATUS "pylon_ROOT = ${pylon_ROOT}")
if (NOT TARGET pylon::Headers)
    add_library(pylon::Headers INTERFACE IMPORTED)
endif()

if (APPLE)
    # Find pylon framework includes
    find_path(_PYLON_CORE_SDK_INCLUDE_DIR
        NAMES pylon/PylonIncludes.h
        HINTS
            "${pylon_ROOT}"
            "/Library/Frameworks"
    )

    # Find pylon framework GeniCam includes
    find_path(_PYLON_CORE_SDK_GENICAM_INCLUDE_DIR
        NAMES Base/GCTypes.h
        HINTS
            "${_PYLON_CORE_SDK_INCLUDE_DIR}/Headers"
        PATH_SUFFIXES GenICam
    )

    set(pylon_HEADERS "${_PYLON_CORE_SDK_INCLUDE_DIR};${_PYLON_CORE_SDK_GENICAM_INCLUDE_DIR}")
    set_target_properties(pylon::Headers PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${pylon_HEADERS}"
    )
elseif (WIN32 OR UNIX)
    set(pylon_HEADERS "${pylon_ROOT}/include")
    set_target_properties(pylon::Headers PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${pylon_HEADERS}"
    )
else()
    message ("Unsupported OS")
endif()

# these lists must be extended whenever a new version or a new compiler
# is used

if (APPLE)
    set(_genicam_known_suffixes "_gcc_v3_1_Basler_pylon" )
    set(_pylon_known_suffixes "${pylon_VERSION_SUFFIX}")

    set(_pylon_lib_path ${pylon_ROOT}/Libraries)
    set(_pylon_lib_file_extension "")
elseif (WIN32)
    set(_genicam_known_suffixes "_MD_VC141_v3_1_Basler_pylon")
    set(_pylon_known_suffixes "${pylon_VERSION_SUFFIX}")

    set(_pylon_lib_path "${pylon_ROOT}/lib/${pylon_ARCH}")
    set(_pylon_lib_file_extension ".lib")
    set(_pylon_lib_dll_extension ".dll")
elseif (UNIX)
    set(_genicam_known_suffixes "_gcc_v3_1_Basler_pylon" )
    set(_pylon_known_suffixes "${pylon_VERSION_SUFFIX}")

    set(_pylon_lib_path ${pylon_ROOT}/lib)
    set(_pylon_lib_file_extension ".so")

    set(_libprefix "lib")
else()
    message ("Unsupported OS")
endif()

#----------------------------------------------------------------------------------------------------------#
set(pylon_LIBRARIES pylon::Headers)

# pylon::GCBase
_find_genicam_library(GCBase)
if (_genicam_GCBase_FOUND)
    message( "[genicam] Add GCBase")
    _pylon_add_target(pylon::GCBase "${_GCBase_lib}" "${_GCBase_dll}" pylon::Headers )
    if (_GCBase_lib) # <-- linking only possible if lib was found
        list(APPEND pylon_LIBRARIES pylon::GCBase)
        set(__GCBaseTarget pylon::GCBase)
    endif()
endif()

# pylon::GenApi
_find_genicam_library(GenApi)
if (_genicam_GenApi_FOUND)
    message( "[genicam] Add GenApi")
    _pylon_add_target(pylon::GenApi "${_GenApi_lib}" "${_GenApi_dll}" "pylon::Headers;${__GCBaseTarget}" )
    if (_GenApi_lib)
        list(APPEND pylon_LIBRARIES pylon::GenApi)
        set(__GenApiTarget pylon::GenApi)
    endif()
endif()

# pylon::FirmwareUpdate
_find_genicam_library(FirmwareUpdate)
if (_genicam_FirmwareUpdate_FOUND)
    message( "[genicam] Add FirmwareUpdate")
    _pylon_add_target(pylon::FirmwareUpdate "${_FirmwareUpdate_lib}" "${_FirmwareUpdate_dll}" "pylon::Headers;${__GCBaseTarget}")
    if (_FirmwareUpdate_lib)
        list(APPEND pylon_LIBRARIES pylon::FirmwareUpdate)
        set(__FirmwareUpdateTarget pylon::FirmwareUpdate)
    endif()
endif()

# pylon::log4cpp
_find_genicam_library(log4cpp)
if (_genicam_log4cpp_FOUND)
    message("[genicam] Add log4cpp")
    _pylon_add_target(pylon::log4cpp "${_log4cpp_lib}" "${_log4cpp_dll}" "pylon::Headers")
    if (_log4cpp_lib)
        list(APPEND pylon_LIBRARIES pylon::log4cpp)
        set(__log4cppTarget pylon::log4cpp)
endif()
endif()


# pylon::MathParser
_find_genicam_library(MathParser)
if (_genicam_MathParser_FOUND)
    message("[genicam] Add MathParser")
    _pylon_add_target(pylon::MathParser "${_MathParser_lib}" "${_MathParser_dlll}" "pylon::Headers;${__GCBaseTarget}")
    if (_MathParser_lib)
        list(APPEND pylon_LIBRARIES pylon::MathParser)
        set(__MathParserTarget pylon::MathParser)
    endif()
endif()


# pylon::NodeMapData
_find_genicam_library(NodeMapData)
if (_genicam_NodeMapData_FOUND)
    message("[genicam] Add NodeMapData")
    _pylon_add_target(pylon::NodeMapData "${_NodeMapData_lib}" "${_NodeMapData_dll}"  "pylon::Headers;${__GCBaseTarget}")
    if (_NodeMapData_lib)
        list(APPEND pylon_LIBRARIES pylon::NodeMapData)
        set(__NodeMapDataTarget pylon::NodeMapData)
    endif()
endif()

# pylon::XmlParser
_find_genicam_library(XmlParser)
if (_genicam_XmlParser_FOUND)
    message("[genicam] Add XmlParser")
    _pylon_add_target(pylon::XmlParser "${_XmlParser_lib}" "${_XmlParser_dll}" "pylon::Headers;${__GCBaseTarget}")
    if (_XmlParser_lib)
        list(APPEND pylon_LIBRARIES pylon::XmlParser)
        set(__XmlParserTarget pylon::XmlParser)
    endif()
endif()

# pylon::Log
_find_genicam_library(Log)
if (_genicam_Log_FOUND)
    message("[genicam] Add Log")
    _pylon_add_target(pylon::Log "${_Log_lib}" "${_Log_dll}"  "pylon::Headers;${__GCBaseTarget}")        
    if (_Log_lib)
        list(APPEND pylon_LIBRARIES pylon::Log)
        set(__LogTarget pylon::Log)
    endif()
endif()

# pylon::PylonBase
_find_pylon_library(PylonBase)
if (_pylon_PylonBase_FOUND)
    message("[pylon] Add PylonBase")
    _pylon_add_target(pylon::PylonBase "${_PylonBase_lib}" "${_PylonBase_dll}" "pylon::Headers;${__GenApiTarget};${__GCBaseTarget}")
    list(APPEND pylon_LIBRARIES pylon::PylonBase)
endif()

if (WIN32)
    # pylon::PylonGUI
    _find_pylon_library(PylonGUI)
    if (_pylon_PylonGUI_FOUND)
        message("[pylon] Add PylonGUI")
        _pylon_add_target(pylon::PylonGUI "${_PylonGUI_lib}" "${_PylonGUI_dll}" "pylon::Headers;pylon::PylonBase;pylon::PylonUtility;${__GCBaseTarget}")
        list(APPEND pylon_LIBRARIES pylon::PylonGUI)
    endif()
endif()

# pylon::PylonUtility
_find_pylon_library(PylonUtility)
if (_pylon_PylonUtility_FOUND)
    message("[pylon] Add PylonUtility")
    _pylon_add_target(pylon::PylonUtility "${_PylonUtility_lib}" "${_PylonUtility_dll}" "pylon::PylonBase;pylon::Headers")
    list(APPEND pylon_LIBRARIES pylon::PylonUtility)
endif()

# pylon::PylonC
_find_pylon_library(PylonC)
if (_pylon_PylonC_FOUND)
    message("[pylon] Add PylonC")
    _pylon_add_target(pylon::PylonC "${_PylonC_lib}" "${_PylonC_dll}" "pylon::Headers")
    list(APPEND pylon_LIBRARIES pylon::PylonC)
endif()

# generic module pylon::pylon
if (NOT TARGET pylon::pylon)
add_library(pylon::pylon INTERFACE IMPORTED)
if (WIN32)
    set_target_properties( pylon::pylon
    PROPERTIES
    INTERFACE_LINK_LIBRARIES "${pylon_LIBRARIES}"
    INTERFACE_COMPILE_DEFINITIONS "PYLON_NO_AUTO_IMPLIB=1"
    )
else()
    set_target_properties( pylon::pylon
    PROPERTIES
    INTERFACE_LINK_LIBRARIES "${pylon_LIBRARIES}"
    )
    endif()
endif()