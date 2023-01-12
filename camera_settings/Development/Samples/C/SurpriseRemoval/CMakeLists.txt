  add_executable( SurpriseRemoval SurpriseRemoval.c)
  target_link_libraries( SurpriseRemoval
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS SurpriseRemoval )
