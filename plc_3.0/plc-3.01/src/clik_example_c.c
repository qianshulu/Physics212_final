#include "clik.h"

int main(int argc, char **argv) {
  error *_err,**err;
  clik_object* clikid;
  int i,cli;
  int has_cl[6],lmax[6];
  parname clnames[6];
  parname *names;
  int nextra;
  int ndim;
  double *cl_and_pars;
  double log_clikid;
  int isl;

  _err = initError();
  err = &_err;

  //testErrorExitVA(argc<3,-1,"Bad number of command line args!\nusage : %s clikidfile clfile [clfile ...]",*err,__LINE__,argv[0]);
  
  isl  = clik_try_lensing(argv[1],err);
  quitOnError(*err,__LINE__,stderr);
  if (isl==1) {
    fprintf(stdout,"this is lensed\n");
  }

  clikid = clik_init(argv[1],err);
  quitOnError(*err,__LINE__,stderr);
  
  // retrieve has_cl and lmax
  clik_get_has_cl(clikid,has_cl,err);
  quitOnError(*err,__LINE__,stderr);
  clik_get_lmax(clikid,lmax,err);
  quitOnError(*err,__LINE__,stderr);
  
  nextra = clik_get_extra_parameter_names(clikid,&names,err);
  quitOnError(*err,__LINE__,stderr);
  free(names);
  
  // compute size of the parameter vector
  
  ndim = nextra;
  for(cli=0;cli<6;cli++) {
    ndim += lmax[cli] + 1;
  }
  
  for(i=2;i<argc;i++) {
    // read cl as ascii file
    cl_and_pars = read_double_vector(argv[i],ndim,err);
    quitOnError(*err,__LINE__,stderr);

    fprintf(stdout, "cl is %f\n", cl_and_pars[20]);
        
    log_clikid = clik_compute(clikid,cl_and_pars,err);
    quitOnError(*err,__LINE__,stderr);
    
    fprintf(stdout,"Log likelihood for file %s : %g\n",argv[i],log_clikid);
    
    free(cl_and_pars);
  }
  
  clik_cleanup(&clikid);
}