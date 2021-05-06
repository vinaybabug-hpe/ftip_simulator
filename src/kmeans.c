/*
 * kmeans.c
 *  This file is part of FTiP Simulator.
 *
 *  FTiP Simulator is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  FTiP Simulator is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with FTiP Simulator.  If not, see <https://www.gnu.org/licenses/>.
 *  Created on: Mar 16, 2021
 *      Modified from Vinay's stripped k-means.
 *      -Hisham.
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <assert.h>
#include <ctype.h>

#define VERTICES_FILE "vertices.txt" 
#define EDGES_FILE "edges.txt" 

static unsigned long long int vertex_id = 0;

// Note: This function returns a pointer to a substring of the original string.
// If the given string was allocated dynamically, the caller must not overwrite
// that pointer with the returned value, since the original pointer must be
// deallocated using the same allocator with which it was allocated.  The return
// value must NOT be deallocated using free() etc.
char *trimwhitespace(char *str)
{
  char *end;

  // Trim leading space
  while(isspace((unsigned char)*str)) str++;
  if(*str == 0) { // All spaces?
    return str;
  }

  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;
  // Write new null terminator character
  end[1] = '\0';
  return str;
}

const char* getfield(char* line, int num)
{
	const char* tok;
	for (tok = strtok(line, ",");
			tok && *tok;
			tok = strtok(NULL, ",\n"))
	{
		if (!--num)
			return tok;
	}
	return NULL;
}

/* return an array of cluster centers of size [numClusters][numCoords] */
int 
seq_kmeans (		  
	int bootstrap,
	float **objects,  /* in: [numObjs][numCoords] */
	int numCoords,	  /* no. features */
	int numObjs,	  /* no. objects */
	int numClusters,  /* no. clusters */
	float threshold,  /* % objects change membership */
	int *membership,  /* out: [numObjs] */
	float **clusters, /* out: [numClusters][numCoords] */
	FILE *trace_file,
	FILE *_vertices_file,
	FILE *_edges_file,
	int iterations)

{
	int i, j, index, loop = 0;
	float delta;
	int *clusterSize;
	int *newClusterSize; /* [numClusters]: no. objects assigned in each
	                                new cluster */
	float **newClusters; /* [numClusters][numCoords] */
	unsigned long long int **cluster_vertex_id;
	

	//vertex_id++;

	/* initialize membership[] */
	for (i = 0; i < numObjs; i++) {
		membership[i] = -1;
	}		

	/* need to initialize newClusterSize and newClusters[0] to all 0 */
	clusterSize = (int *)calloc(numClusters, sizeof(int));
	assert(clusterSize != NULL);
	newClusterSize = (int *)calloc(numClusters, sizeof(int));
	assert(newClusterSize != NULL);
	newClusters = (float **)malloc(numClusters * sizeof(float *));
	assert(newClusters != NULL);
	newClusters[0] = (float *)calloc(numClusters * numCoords, sizeof(float));
	assert(newClusters[0] != NULL);
	// allocate vertex id's for cluster centers
	cluster_vertex_id = (unsigned long long int **)
		malloc(numClusters * sizeof(unsigned long long int *));
	assert(cluster_vertex_id != NULL);
	cluster_vertex_id[0] = (unsigned long long int *)
		calloc(numClusters * numCoords, sizeof(unsigned long long int));
	assert(cluster_vertex_id[0] != NULL);
	for (i = 1; i < numClusters; i++) {
		newClusters[i] = newClusters[i - 1] + numCoords;
		cluster_vertex_id[i] = cluster_vertex_id[i-1] + numCoords;
	}
	
	clusters = (float **)malloc(numClusters * sizeof(float *));
	for (i = 0; i < numClusters; i++) {
		clusters[i] = (float *)calloc(numClusters * numCoords, sizeof(float));
		for (j = 0; j < numCoords; j++) {
			clusters[i][j] = objects[i][j];			
		}
	}

	for (i = 0; i < numClusters; i++) {
		for (j = 0; j < numCoords; j++) {
			cluster_vertex_id[i][j] = vertex_id++;
			fprintf(_vertices_file, "%3.2f ,= %3.2f ,- %3.2f\t%llu\n", clusters[i][j],
					clusters[i][j], 0.0, cluster_vertex_id[i][j]);
			fprintf(_edges_file, "%d->%llu\n", bootstrap, cluster_vertex_id[i][j]);
		}
	}

	do {
		delta = 0.0;
		for (int oIndex = 0; oIndex < numObjs; oIndex++) {
			float dist = 0.0, min_dist = 0.0, result = 0.0;

			/* find the cluster id that has min distance to object */
			index = 0;
			min_dist = FLT_MAX;
			fprintf(trace_file, "#Object #%i: ", oIndex + 1);
			for (int i = 0; i < numCoords; i++) {
				fprintf(trace_file, "%3.2f, ", objects[oIndex][i]);
			}				
			fprintf(trace_file, "\n");
			for (int cluster_index = 0; cluster_index < numClusters; 
				cluster_index++) {
				result = 0.0;
				dist = 0.0;
				long long unsigned int vertex_1 = 0, vertex_2 = 0, vertex_3 = 0;
				long long unsigned int vertex_4 = 0;
				fprintf(trace_file, "#Cluster %i \n", cluster_index);
				for (int feature = 0; feature < numCoords; feature++) {
					float term = objects[oIndex][feature] - 
									clusters[cluster_index][feature];
					
					fprintf(trace_file, "%3.2f = %3.2f - %3.2f\n", term, 
					objects[oIndex][feature], clusters[cluster_index][feature]);
					fprintf(_vertices_file, "%3.2f ,= %3.2f ,- %3.2f\t%llu\n", term, 
					objects[oIndex][feature], clusters[cluster_index][feature], 
						vertex_1 = vertex_id++);
					float squared_term = term * term;
					fprintf(trace_file, "%3.2f = %3.2f * %3.2f\n", squared_term
					, term, term);
					fprintf(_vertices_file, "%3.2f ,= %3.2f ,* %3.2f\t%llu\n", squared_term
					, term, term, vertex_2 = vertex_id++);
					//Create edges
					fprintf(_edges_file, "%llu->%llu\n",
						cluster_vertex_id[cluster_index][feature], vertex_1);
					fprintf(_edges_file, "%llu->%llu\n",vertex_1, vertex_2);
					float old_result = result;
					result = old_result + squared_term;
					fprintf(trace_file, "%3.2f = %3.2f + %3.2f\n", result, 
					old_result, squared_term);
					fprintf(_vertices_file, "%3.2f ,= %3.2f ,+ %3.2f\t%llu\n", result, 
					old_result, squared_term, vertex_3 = vertex_id++);
					fprintf(_edges_file, "%llu->%llu\n",vertex_2, vertex_3);
					if (vertex_4 != 0) {
						fprintf(_edges_file, "%llu->%llu\n",vertex_4, vertex_3);
					}
					// store previous vertex_3 id
					vertex_4 = vertex_3;
				}
				fprintf(trace_file, "\n");
				dist = result;
				/* no need square root */
				if (dist < min_dist) { /* find the min and its array index */
					min_dist = dist;
					index = cluster_index;
				}
			}

			/* if membership changes, increase delta by 1 */
			if (membership[oIndex] != index) {
				delta += 1.0;
			}
			/* assign the membership to object i */
			membership[oIndex] = index;
			/* update new cluster center : sum of objects located within */
			newClusterSize[index]++;
			for (int feature = 0; feature < numCoords; feature++) {
				newClusters[index][feature] += objects[oIndex][feature];
			}				
		}

		/* average the sum and replace old cluster center with newClusters */
		for (int cluster_ind = 0; cluster_ind < numClusters; cluster_ind++) {
			for (int feature = 0; feature < numCoords; feature++) {
				if (newClusterSize[cluster_ind] > 0) {
					clusters[cluster_ind][feature] = newClusters[cluster_ind]
					[feature] / newClusterSize[cluster_ind];
				}
				newClusters[cluster_ind][feature] = 0.0; /* set back to 0 */
				cluster_vertex_id[cluster_ind][feature] = vertex_id++;
				fprintf(_vertices_file, "%3.2f ,= %3.2f ,- %3.2f\t%llu\n", 
				clusters[cluster_ind][feature], clusters[cluster_ind][feature],
				 0.0, cluster_vertex_id[cluster_ind][feature]);
			}			
			clusterSize[cluster_ind] = newClusterSize[cluster_ind];
			newClusterSize[cluster_ind] = 0;
		}

		delta /= numObjs;
	} while (loop++ < iterations); //(delta > threshold && loop++ < 500);

	printf("Membership=\n");
	for (int i = 0; i < numObjs; i++)
		printf("%i\n", membership[i]);
	printf("newClusterSize=\n");
	for (int i = 0; i < numClusters; i++)
		printf("%i\n", clusterSize[i]);
	printf("newClusterCenters=\n");
	for (int index = 0; index < numClusters; index++)
	{
		for (int feature = 0; feature < numCoords; feature++)
			printf("%f ", clusters[index][feature]);
		printf("\n");
	}

	free(newClusters[0]);
	free(newClusters);
	free(newClusterSize);

	return 1;
}

int 
main (int argc, char **argv)

{
	int bootstrap_size = 0;
	int num_bootstrap = 0;
	int numObjects = 0;
	int numCoords = 0;
	int numClusters = 0;
	float threshold = 2;
	FILE *desc_file = NULL, *data_file = NULL;
	char buffer[1024];

	if(argc != 3) {
		printf("\nUsage:");
		printf("\nkmeans <object description filename> <object data filename>\n");
		exit(0);
	}
	desc_file = fopen(argv[1], "r");
	data_file = fopen(argv[2], "r");
	if(desc_file == NULL) {
		printf("Can't open description file (desc.txt).\n");
		exit(0);
	}
	if(data_file == NULL) {
		printf("Can't open data file (data.csv).\n");
		exit(0);
	}
	fscanf(desc_file, "%d %d %d %d %d", &numObjects, &numCoords, &numClusters, &bootstrap_size, &num_bootstrap);
	fclose(desc_file);
	printf("\n%d %d %d %d %d", numObjects, numCoords, numClusters, num_bootstrap, bootstrap_size);
	
	int *membership = (int *)calloc(bootstrap_size, sizeof(int));
	assert(membership != NULL);
	float **objects = (float **)calloc(bootstrap_size, sizeof(float *));
	assert(objects != NULL);
	
	int iterations = 500;
	float **clusters;
	FILE *trace_file = fopen("boot_strap3_trace.txt", "w+");
	if (trace_file == NULL) {
		printf("\nCould not create/open trace file.");
		exit(EXIT_FAILURE);
	}
	FILE *_vertices_file = fopen(VERTICES_FILE, "w+");
	if (_vertices_file == NULL) {
		printf("\nCould not create/open vertices file.");
		exit(EXIT_FAILURE);
	}
	FILE *_edges_file = fopen(EDGES_FILE, "w+");
	if (_edges_file == NULL) {
		printf("\nCould not create/open edges file.");
		exit(EXIT_FAILURE);
	}

	float *data = (float *)calloc(numObjects*numCoords, sizeof(float));
	int count = 0;
	while(fgets(buffer, sizeof(buffer), data_file)) {
		//printf("\n\n%s",buffer);
        char *str = strtok(buffer, ",");		
		while(str != NULL) {
			data[count] = strtol (str, NULL,10);
			//printf("%f ", data[count] );
			str = strtok(NULL, ",");
			count++;
		}
        //printf("\n");
	}
	fclose(data_file);
	// Allocate objects to run kmeans
	for (int i = 0; i < bootstrap_size; i++) {
		objects[i] = (float *)calloc(numCoords, sizeof(float));	
	}
	// Increment vertex_id to 1, 0 is reserved for starting node in DAG
	fprintf(_vertices_file, "%3.2f ,= %3.2f ,- %3.2f\t%d\n", 0.0,
					0.0, 0.0, 0);
	for(int b=1; b<= num_bootstrap; b++){
		fprintf(_vertices_file, "%3.2f ,= %3.2f ,- %3.2f\t%d\n", 0.0,
			0.0, 0.0, b);
		fprintf(_edges_file, "%d->%d\n",0, b);
		// create bootstrap
		for (int i = 0; i < bootstrap_size; i++) {
			int d_obj = (int) (rand() / (double) (RAND_MAX) * (numObjects));	
			// pick object from data at random		
			printf("[%d] Object # %i: \n", d_obj, i);
			for (int j = 0; j < numCoords; j++) {
				objects[i][j] = data[2 * d_obj + j];
				printf(" %6.3f, ", objects[i][j]);
			}
			printf("\n");
		}

		seq_kmeans(b, objects,	numCoords, bootstrap_size, numClusters, threshold,
		membership, clusters, trace_file, _vertices_file, _edges_file, iterations);
	}
	fclose(trace_file);
	fclose(_vertices_file);
	fclose(_edges_file);

	return EXIT_SUCCESS;
}
