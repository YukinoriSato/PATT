/**
 * This code is from Fig. 1 of the following paper.
Automatic Parameter Tuning of Three-Dimensional Tiled FDTD Kernel.
Takeshi Minami,Motoharu Hibino,Tasuku Hiraishi,Takeshi Iwashita,Hiroshi Nakashima High Performance Computing for Computational Science - VECPAR 2014 - 11th International Conference, Eugene, OR, USA, June 30 - July 3, 2014, Revised Selected Papers 284-297 2014
 */
/* fdtd-3d.c: this file is part of PolyBench/C */

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

/* Include polybench common header. */
#include <polybench.h>

/* Include benchmark-specific header. */
#include "fdtd-3d.h"

//int idn=NX;
//int idn=NX*NY*NZ;
//int idn=2;
int idn=10;



/* Array initialization. */
static
void init_array (int tmax,
		    int nx,
		    int ny,
		    int nz,  
		    DATA_TYPE POLYBENCH_3D(Ex,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Ey,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Ez,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hx,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hy,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hz,NX,NY,NZ,nx,ny,nz),
		    int POLYBENCH_3D(id,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_1D(Cex,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cey,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cez,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cexry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cexrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Ceyrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Ceyrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cezrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cezry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chxry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chxrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chyrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chyrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chzrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chzry,IND,idn))
{
  int i, j, k;

  for (i = 0; i < nx; i++)
    for (j = 0; j < ny; j++)
      for (k = 0; k < nz; k++)
      {
	Ex[i][j][k] = ((DATA_TYPE) i*(j+1)-k) / nx;
	Ey[i][j][k] = ((DATA_TYPE) i*(j+2)-k) / ny;
	Ez[i][j][k] = ((DATA_TYPE) i*(j+3)-k) / nx;
	Hx[i][j][k] = ((DATA_TYPE) i*(j-1)+k) / nx;
	Hy[i][j][k] = ((DATA_TYPE) i*(j-2)+k) / ny;
	Hz[i][j][k] = ((DATA_TYPE) i*(j-3)+k) / nx;
	
	if(i>1 && j>1 && k>1 && i<nx-2 && j<ny-2 && k<nz-2)
	  id[i][j][k] = abs((i-20)*(j+13)/(k+1))%idn;
	//id[i][j][k] = 0;
	else
	  id[i][j][k] = 0;

      }

  for (i = 0; i < idn; i++){
    Cex[i]=((i-2)*(j+3)+k)/2.6;
    Cey[i]=((i-2)*(j+3)+k)/2.2;
    Cez[i]=((i-2)*(j+3)+k)/1.6;
    Cezrx[i]=((float)(i-2)*(j+3)+k)/nx;
    Cezry[i]=((float)(i-2)*(j+3)+k)/ny;
    Ceyrz[i]=((float)(i-2)*(j+3)+k)/nz;
    Ceyrx[i]=((float)(i-2)*(j+3)+k)/nx;
    Cexry[i]=((float)(i-2)*(j+3)+k)/ny;
    Cexrz[i]=((float)(i-2)*(j+3)+k)/nz;
    Chzrx[i]=((float)(i-2)/(j+3)*k)/nx;
    Chzry[i]=((float)(i-2)/(j+3)*k)/ny;
    Chyrz[i]=((float)(i-2)/(j+3)*k)/nz;
    Chyrx[i]=((float)(i-2)/(j+3)*k)/nx;
    Chxry[i]=((float)(i-2)/(j+3)*k)/ny;
    Chxrz[i]=((float)(i-2)/(j+3)*k)/nz;
  }

}


/* Main computational kernel. The whole function will be timed,
   including the call and return. */
static
void kernel_fdtd_3d(int tmax,
		    int nx,
		    int ny,
		    int nz,  
		    DATA_TYPE POLYBENCH_3D(Ex,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Ey,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Ez,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hx,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hy,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_3D(Hz,NX,NY,NZ,nx,ny,nz),
		    int POLYBENCH_3D(id,NX,NY,NZ,nx,ny,nz),
		    DATA_TYPE POLYBENCH_1D(Cex,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cey,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cez,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cexry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cexrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Ceyrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Ceyrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cezrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Cezry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chxry,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chxrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chyrz,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chyrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chzrx,IND,idn),
		    DATA_TYPE POLYBENCH_1D(Chzry,IND,idn))
{

  int t, i, j, k,m;

  //for (t=0;t<tmax;t++){
    //fprintf(stderr,"E %d\n",t);
    for(i=1;i<nx-1;i++){
      for(j=1;j<ny-1;j++){
	for(k=1;k<nz-1;k++){
	  m=id[i][j][k];
	  //fprintf(stderr,"m %d\n",m);
	  Ex[i][j][k]=Cex[m]+Ex[i][j][k]
	    +Cexry[m]*(Hz[i][j][k]-Hz[i][j-1][k])
	    +Cexrz[m]*(Hy[i][j][k]-Hy[i][j][k-1]);
	  Ey[i][j][k]=Cey[m]+Ey[i][j][k]
	    +Ceyrz[m]*(Hx[i][j][k]-Hx[i][j][k-1])
	    +Ceyrx[m]*(Hz[i][j][k]-Hz[i-1][j][k]);
	  Ez[i][j][k]=Cez[m]+Ez[i][j][k]
	    +Cezrx[m]*(Hy[i][j][k]-Hy[i-1][j][k])
	    +Cezry[m]*(Hx[i][j][k]-Hx[i][j-1][k]);
	}
      }
    }
    //fprintf(stderr,"H %d\n",t);
    for(i=1;i<nx-1;i++){
      for(j=1;j<ny-1;j++){
	for(k=1;k<nz-1;k++){
	  m=id[i][j][k];
	  Hx[i][j][k]=Hx[i][j][k]
	    +Chxry[m]*(Ez[i][j+1][k]-Ez[i][j][k])
	    +Chxrz[m]*(Ey[i][j][k+1]-Ey[i][j][k]);
	  Hy[i][j][k]=Hy[i][j][k]
	    +Chyrz[m]*(Ex[i][j][k+1]-Ex[i][j][k])
	    +Chyrx[m]*(Ez[i+1][j][k]-Ez[i][j][k]);
	  Hz[i][j][k]=Hz[i][j][k]
	    +Chzrx[m]*(Ey[i+1][j][k]-Ey[i][j][k])
	    +Chzry[m]*(Ex[i][j+1][k]-Ex[i][j][k]);
	}
      }
    }
    //fprintf(stderr,"OK %d\n",t);
  //}

  // original 
  //for(i=1;i<=nx;i++){
  //  for(j=1;j<=ny;j++){
  //	for(k=1;k<=nz;k++){

}


int main(int argc, char** argv)
{
  /* Retrieve problem size. */
  int tmax = TMAX;
  int nx = NX;
  int ny = NY;
  int nz = NZ;


  /* Variable declaration/allocation. */
  POLYBENCH_3D_ARRAY_DECL(Ex,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(Ey,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(Ez,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(Hx,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(Hy,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(Hz,DATA_TYPE,NX,NY,NZ,nx,ny,nz);
  POLYBENCH_3D_ARRAY_DECL(id,int,NX,NY,NZ,nx,ny,nz);
#if 1
  POLYBENCH_1D_ARRAY_DECL(Cex,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cey,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cez,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cezrx,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cezry,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Ceyrz,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Ceyrx,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cexry,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Cexrz,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chzrx,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chzry,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chyrz,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chyrx,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chxry,DATA_TYPE,IND,idn);
  POLYBENCH_1D_ARRAY_DECL(Chxrz,DATA_TYPE,IND,idn);
#else

  double cex[idn],cey[idn],cez[idn],cexry[idn],cexrz[idn],ceyrz[idn],ceyrx[idn],cezrx[idn],cezry[idn];
  double chxry[idn],chxrz[idn],chyrz[idn],chyrx[idn],chzrx[idn],chzry[idn];

  double *Cex=cex, *Cey=cey, *Cez=cez;
  double *Cexry=cexry, *Cexrz=cexrz, *Ceyrz=ceyrz, *Ceyrx=ceyrx, *Cezrx=cezrx, *Cezry=cezry;
  double *Chxry=chxry, *Chxrz=chxrz, *Chyrz=chyrz, *Chyrx=chyrx, *Chzrx=chzrx, *Chzry=chzry;
#endif

  /* Initialize array(s). */
  init_array (tmax, nx, ny, nz,
	      POLYBENCH_ARRAY(Ex),
	      POLYBENCH_ARRAY(Ey),
	      POLYBENCH_ARRAY(Ez),
	      POLYBENCH_ARRAY(Hx),
	      POLYBENCH_ARRAY(Hy),
	      POLYBENCH_ARRAY(Hz),
	      POLYBENCH_ARRAY(id),
	      POLYBENCH_ARRAY(Cex),
	      POLYBENCH_ARRAY(Cey),
	      POLYBENCH_ARRAY(Cez),
	      POLYBENCH_ARRAY(Cexrz),
	      POLYBENCH_ARRAY(Cexry),
	      POLYBENCH_ARRAY(Ceyrz),
	      POLYBENCH_ARRAY(Ceyrx),
	      POLYBENCH_ARRAY(Cezrx),
	      POLYBENCH_ARRAY(Cezry),
	      POLYBENCH_ARRAY(Chxry),
	      POLYBENCH_ARRAY(Chxrz),
	      POLYBENCH_ARRAY(Chyrz),
	      POLYBENCH_ARRAY(Chyrx),
	      POLYBENCH_ARRAY(Chzrx),
	      POLYBENCH_ARRAY(Chzry)
	      );

  /* Start timer. */
  polybench_start_instruments;

  /* Run kernel. */
	int t;
  for (t=0;t<tmax;t++){
  kernel_fdtd_3d (tmax, nx, ny, nz,
		  POLYBENCH_ARRAY(Ex),
		  POLYBENCH_ARRAY(Ey),
		  POLYBENCH_ARRAY(Ez),
		  POLYBENCH_ARRAY(Hx),
		  POLYBENCH_ARRAY(Hy),
		  POLYBENCH_ARRAY(Hz),
		  POLYBENCH_ARRAY(id),
		  POLYBENCH_ARRAY(Cex),
		  POLYBENCH_ARRAY(Cey),
		  POLYBENCH_ARRAY(Cez),
		  POLYBENCH_ARRAY(Cexrz),
		  POLYBENCH_ARRAY(Cexry),
		  POLYBENCH_ARRAY(Ceyrz),
		  POLYBENCH_ARRAY(Ceyrx),
		  POLYBENCH_ARRAY(Cezrx),
		  POLYBENCH_ARRAY(Cezry),
		  POLYBENCH_ARRAY(Chxry),
		  POLYBENCH_ARRAY(Chxrz),
		  POLYBENCH_ARRAY(Chyrz),
		  POLYBENCH_ARRAY(Chyrx),
		  POLYBENCH_ARRAY(Chzrx),
		  POLYBENCH_ARRAY(Chzry)
		  );
	}

  //printf("ok\n");

  /* Stop and print timer. */
  polybench_stop_instruments;
  polybench_print_instruments;


  return 0;
}
