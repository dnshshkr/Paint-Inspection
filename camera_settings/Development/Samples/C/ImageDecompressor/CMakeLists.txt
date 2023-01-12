  add_executable( ImageDecompressor ImageDecompressor.c)
  target_link_libraries( ImageDecompressor
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS ImageDecompressor )
