  add_executable( ParametrizeCamera ParametrizeCamera.c)
  target_link_libraries( ParametrizeCamera
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS ParametrizeCamera )
