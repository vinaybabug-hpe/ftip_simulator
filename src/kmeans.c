/*
 * kmeans.c
 *
 *  Created on: Mar 16, 2021
 *      Modified from Vinay's stripped k-means.
 *      -Hisham.
 */


#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <assert.h>

	/*----< seq_kmeans() >-------------------------------------------------------*/
	/* return an array of cluster centers of size [numClusters][numCoords]       */
	int seq_kmeans(//char dist,
				   float **objects,      /* in: [numObjs][numCoords] */
	               int     numCoords,    /* no. features */
	               int     numObjs,      /* no. objects */
	               int     numClusters,  /* no. clusters */
	               float   threshold,    /* % objects change membership */
	               int    *membership,   /* out: [numObjs] */
	               float **clusters,     /* out: [numClusters][numCoords] */
				   FILE* trace_file,
				   int iterations
	               )

	{
	    int      i, j, index, loop=0;
	    float delta;
	    int *clusterSize;
	    int     *newClusterSize; /* [numClusters]: no. objects assigned in each
	                                new cluster */

	    float  **newClusters;    /* [numClusters][numCoords] */

	    /* initialize membership[] */
	    for (i=0; i<numObjs; i++) membership[i] = -1;

	    /* need to initialize newClusterSize and newClusters[0] to all 0 */
	    clusterSize = (int*) calloc(numClusters, sizeof(int));
	    assert(clusterSize != NULL);

	    newClusterSize = (int*) calloc(numClusters, sizeof(int));
	    assert(newClusterSize != NULL);


	    newClusters    = (float**) malloc(numClusters * sizeof(float*));
	    assert(newClusters != NULL);
	    newClusters[0] = (float*)  calloc(numClusters * numCoords, sizeof(float));
	    assert(newClusters[0] != NULL);
	    for (i=1; i<numClusters; i++)
	        newClusters[i] = newClusters[i-1] + numCoords;

	    clusters = (float**) malloc(numClusters * sizeof(float*));
	    for (i=0; i<numClusters; i++) {
	    	clusters[i] = (float*)  calloc(numClusters * numCoords, sizeof(float));
	    	for (j=0; j<numCoords; j++) {
	    		clusters[i][j] = objects[i][j];
	    	}
	    }

	    do {
	        delta = 0.0;
	        for (int oIndex=0; oIndex<numObjs; oIndex++) {


					float dist=0.0, min_dist=0.0, result=0.0;


					/* find the cluster id that has min distance to object */
					index    = 0;
					min_dist=FLT_MAX;

					fprintf(trace_file,"#Object #%i: ",oIndex+1);
					for(int i=0;i<numCoords; i++)
						fprintf(trace_file,"%3.2f, ",objects[oIndex][i]);
					fprintf(trace_file,"\n");
					for (int cluster_index=0; cluster_index<numClusters; cluster_index++) {

						result=0.0;
						dist=0.0;

						fprintf(trace_file,"#Cluster %i \n",cluster_index);
						for (int feature = 0; feature < numCoords; feature++)
						{

							float term = objects[oIndex][feature] - clusters[cluster_index][feature];
							fprintf(trace_file,"%3.2f = %3.2f - %3.2f\n",term,objects[oIndex][feature],clusters[cluster_index][feature]);

							float squared_term = term*term;
							fprintf(trace_file,"%3.2f = %3.2f * %3.2f\n",squared_term,term,term);

							float old_result=result;
							result=old_result+squared_term;
							fprintf(trace_file,"%3.2f = %3.2f + %3.2f\n",result,old_result,squared_term);

						}
						fprintf(trace_file,"\n");
						dist=result;
						/* no need square root */
						if (dist < min_dist) { /* find the min and its array index */
							min_dist = dist;
							index    = cluster_index;
						}
					}



	            /* if membership changes, increase delta by 1 */
	            if (membership[oIndex] != index) delta += 1.0;

	            /* assign the membership to object i */
	            membership[oIndex] = index;

	            /* update new cluster center : sum of objects located within */
	            newClusterSize[index]++;
	            for (int feature = 0; feature < numCoords; feature++)

	                newClusters[index][feature] += objects[oIndex][feature];
	        }

	        /* average the sum and replace old cluster center with newClusters */
	        for (int cluster_ind=0; cluster_ind<numClusters; cluster_ind++) {
	            for (int feature=0; feature<numCoords; feature++) {
	                if (newClusterSize[cluster_ind] > 0)
	                	clusters[cluster_ind][feature] = newClusters[cluster_ind][feature] / newClusterSize[cluster_ind];

	                newClusters[cluster_ind][feature] = 0.0;   /* set back to 0 */
	            }
	            clusterSize[cluster_ind]=newClusterSize[cluster_ind];
	            newClusterSize[cluster_ind]=0;
	        }

	        delta /= numObjs;
	    //} while (delta > threshold && loop++ < 500);
	    } while (loop++ < iterations);

	    printf("Membership=\n");
	    for(int i=0; i<numObjs;i++) printf("%i\n",membership[i]);
	    printf("newClusterSize=\n");
	    for(int i=0; i<numClusters; i++) printf("%i\n", clusterSize[i]);
	    printf("newClusterCenters=\n");
	    for(int index=0; index<numClusters; index++){
	    	for(int feature=0; feature<numCoords; feature++)
	    		printf("%f ", clusters[index][feature]);
	    	printf("\n");
	    }

	    free(newClusters[0]);
	    free(newClusters);
	    free(newClusterSize);

	    return 1;
	}

int main(void) {

//		int numObjects=8;
//		int numCoords=2;
//		int numClusters =2;
//		float threshold =0.001;
//		int iterations=500;
//		int    *membership = (int*) malloc(numObjects * sizeof(int));
//		float **objects = (float**) malloc(numObjects * sizeof(float*));
//
//		float **clusters;
//		float data[]={18,23,5,22,8,9,10,3,14,16,1,6,2,14,2,23};
//
//
//
//		//initialize objects
//		for(int i=0; i<numObjects;i++){
//			objects[i]=(float*)  calloc(numCoords, sizeof(float));
//			printf("Object # %i: ",i);
//			for(int j=0; j<numCoords; j++){
//
//				objects[i][j]=data[2*i+j];
//				printf(" %6.3f, ",objects[i][j]);
//			}
//			printf("\n");
//
//		}
//		FILE* trace_file=fopen("boot_strap1_trace.txt","w+");
//
//		seq_kmeans(//char dist,
//				   objects,      /* in: [numObjs][numCoords] */
//			       numCoords,    /* no. features */
//			       numObjects,      /* no. objects */
//			       numClusters,  /* no. clusters */
//			       threshold,    /* % objects change membership */
//			       membership,   /* out: [numObjs] */
//			       clusters,     /* out: [numClusters][numCoords] */
//				   trace_file,
//				   iterations
//			       );
//		fclose(trace_file);


			int numObjects=8;
			int numCoords=3;
			int numClusters =3;
			float threshold =2;
			int    *membership = (int*) malloc(numObjects * sizeof(int));
			float **objects = (float**) malloc(numObjects * sizeof(float*));
			int iterations=500;
			float **clusters;
			FILE* trace_file=fopen("boot_strap3_trace.txt","w+");


			float data[]={18,23,5,22,8,9,10,3,14,16,1,6,2,14,2,23,11,23,22,9,25,23,2,14};
			for(int i=0; i<numObjects;i++){
				objects[i]=(float*)  calloc(numCoords, sizeof(float));
				printf("Object # %i: ",i);
				for(int j=0; j<numCoords; j++){

					objects[i][j]=data[2*i+j];
					printf(" %6.3f, ",objects[i][j]);
				}
				printf("\n");

			}
			seq_kmeans(//char dist,
					   objects,      /* in: [numObjs][numCoords] */
				       numCoords,    /* no. features */
				       numObjects,      /* no. objects */
				       numClusters,  /* no. clusters */
				       threshold,    /* % objects change membership */
				       membership,   /* out: [numObjs] */
				       clusters,     /* out: [numClusters][numCoords] */
					   trace_file,
					   iterations
				       );
			fclose(trace_file);

	return EXIT_SUCCESS;
}
