configure_file(config.h.in config.h)
ADD_LIBRARY(clustering
  kmeans.c
  )

  # add the executable
add_executable(kmeans kmeans.c)