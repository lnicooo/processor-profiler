
/* $Id: cnt.c,v 1.3 2005/04/04 11:34:58 csg Exp $ */



/* sumcntmatrix.c */
//Counts non-negative numbers in a matrix.

//#define DEBUG
#define MAXSIZE 10

// Typedefs

typedef int matrix [MAXSIZE][MAXSIZE];



// Forwards declarations

int main(void);

int Test(matrix);

int Initialize(matrix);

int InitSeed(void);

void Sum(matrix);

int RandomInteger(void);



// Globals

int Seed;

matrix Array;

int Postotal, Negtotal, Poscnt, Negcnt;

// The main function

//#define DEBUG
#define LOOP 30

//#include "FIM.h"

int main (void)

{

   InitSeed();
   
#ifdef DEBUG
   printf("\n   *** MATRIX SUM AND COUNT BENCHMARK TEST ***\n\n");
   printf("RESULTS OF THE TEST:\n");
#endif   

int i;

for(i=0;i<LOOP;i++)
   Test(Array);

//FIM_exit();
return 1;

}


int Test(matrix Array)

{

   long StartTime, StopTime;

   float TotalTime;



   Initialize(Array);

   Sum(Array);

#ifdef DEBUG

   printf("    - Size of array is %d\n", MAXSIZE);
   printf("    - Num pos was %d and Sum was %d\n", Poscnt, Postotal);
   printf("    - Num neg was %d and Sum was %d\n", Negcnt, Negtotal);
   printf("    - Num neg was %d\n", Negcnt);
   printf("Array\n");


   register int OuterIndex, InnerIndex;

   for (OuterIndex = 0; OuterIndex < MAXSIZE; OuterIndex++) //100 + 1

      for (InnerIndex = 0; InnerIndex < MAXSIZE; InnerIndex++) //100 + 1

         printf("%3d %3d %5d\n",InnerIndex,OuterIndex,Array[OuterIndex][InnerIndex]);      

#endif
   return 0;

}





// Intializes the given array with random integers.

int Initialize(matrix Array)

{

   register int OuterIndex, InnerIndex;



   for (OuterIndex = 0; OuterIndex < MAXSIZE; OuterIndex++) //100 + 1

      for (InnerIndex = 0; InnerIndex < MAXSIZE; InnerIndex++) //100 + 1

         Array[OuterIndex][InnerIndex] = RandomInteger();



   return 0;

}


// Initializes the seed used in the random number generator.

int InitSeed (void)

{

   Seed = 0;

   return 0;

}



void Sum(matrix Array)

{

  register int Outer, Inner;



  int Ptotal = 0; /* changed these to locals in order to drive worst case */

  int Ntotal = 0;

  int Pcnt = 0;

  int Ncnt = 0;


  for (Outer = 0; Outer < MAXSIZE; Outer++) //Maxsize = 100

    for (Inner = 0; Inner < MAXSIZE; Inner++)


      if (Array[Outer][Inner] >= 0) {


	  Ptotal += Array[Outer][Inner];

	  Pcnt++;

	}

	else {

	  Ntotal += Array[Outer][Inner];

	  Ncnt++;

	}



  Postotal = Ptotal;

  Poscnt = Pcnt;

  Negtotal = Ntotal;

  Negcnt = Ncnt;

}



// Generates random integers between 0 and 8095

int RandomInteger(void)

{

   Seed = ((Seed * 133) + 81) % 8095;

   return Seed;

}

/*
 * 
 *    *** MATRIX SUM AND COUNT BENCHMARK TEST ***

RESULTS OF THE TEST:
    - Size of array is 10
    - Num pos was 100 and Sum was 396675
    - Num neg was 0 and Sum was 0
    - Num neg was 0
Array
  0   0    81
  1   0  2759
  2   0  2753
  3   0  1955
  4   0  1056
  5   0  2914
  6   0  7178
  7   0  7640
  8   0  4326
  9   0   694
  0   1  3338
  1   1  6905
  2   1  3711
  3   1  7944
  4   1  4283
  5   1  3070
  6   1  3641
  7   1  6729
  8   1  4588
  9   1  3160
  0   2  7516
  1   2  4024
  2   2  1003
  3   2  3960
  4   2   586
  5   2  5164
  6   2  6913
  7   2  4775
  8   2  3746
  9   2  4504
  0   3    83
  1   3  3025
  2   3  5751
  3   3  4034
  4   3  2333
  5   3  2760
  6   3  2886
  7   3  3454
  8   3  6143
  9   3  7600
  0   4  7101
  1   4  5494
  2   4  2233
  3   4  5650
  4   4  6791
  5   4  4739
  6   4  7053
  7   4  7205
  8   4  3136
  9   4  4324
  0   5   428
  1   5   340
  2   5  4826
  3   5  2434
  4   5     3
  5   5   480
  6   5  7256
  7   5  1824
  8   5  7918
  9   5   825
  0   6  4571
  1   6   899
  2   6  6318
  3   6  6590
  4   6  2291
  5   6  5269
  6   6  4688
  7   6   270
  8   6  3611
  9   6  2739
  0   7    93
  1   7  4355
  2   7  4551
  3   7  6334
  4   7   623
  5   7  1990
  6   7  5711
  7   7  6809
  8   7  7133
  9   7  1655
  0   8  1631
  1   8  6534
  2   8  2938
  3   8  2275
  4   8  3141
  5   8  4989
  6   8  7923
  7   8  1490
  8   8  3971
  9   8  2049
  0   9  5463
  1   9  6205
  2   9  7751
  3   9  2899
  4   9  5183
  5   9  1345
  6   9   876
  7   9  3259
  8   9  4493
  9   9  6715

 * */








