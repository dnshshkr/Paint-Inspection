add_executable( Utility_GrabAvi Utility_GrabAvi.cpp)
target_link_libraries( Utility_GrabAvi PRIVATE pylon::pylon )  
install( TARGETS Utility_GrabAvi )