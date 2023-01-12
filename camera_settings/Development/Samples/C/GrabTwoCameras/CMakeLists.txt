  add_executable( GrabTwoCameras GrabTwoCameras.c)
  target_link_libraries( GrabTwoCameras
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS GrabTwoCameras )
