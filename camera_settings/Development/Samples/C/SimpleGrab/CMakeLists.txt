  add_executable( SimpleGrab SimpleGrab.c)
  target_link_libraries( SimpleGrab
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS SimpleGrab )
