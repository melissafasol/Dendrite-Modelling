#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _cad_reg(void);
extern void _nmda_reg(void);
extern void _sca_reg(void);
extern void _vecstim_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"cad.mod\"");
    fprintf(stderr, " \"nmda.mod\"");
    fprintf(stderr, " \"sca.mod\"");
    fprintf(stderr, " \"vecstim.mod\"");
    fprintf(stderr, "\n");
  }
  _cad_reg();
  _nmda_reg();
  _sca_reg();
  _vecstim_reg();
}

#if defined(__cplusplus)
}
#endif
