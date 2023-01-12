  add_executable( Events Events.c)
  target_link_libraries( Events
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS Events )
