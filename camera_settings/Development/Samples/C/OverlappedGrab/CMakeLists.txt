  add_executable( OverlappedGrab OverlappedGrab.c)
  target_link_libraries( OverlappedGrab
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS OverlappedGrab )
