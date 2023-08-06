include(CMakeFindDependencyMacro)

# Same syntax as find_package
find_dependency(OpenSSL REQUIRED)

# Add the targets file
include("${CMAKE_CURRENT_LIST_DIR}/QvlTargets.cmake")