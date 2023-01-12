  add_executable( GenApiParam GenApiParam.c)
  target_link_libraries( GenApiParam
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS GenApiParam )
