  add_executable( ActionCommands ActionCommands.c)
  target_link_libraries( ActionCommands
                         PRIVATE
                         pylon::PylonC
  )
  install( TARGETS ActionCommands )
