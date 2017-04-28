from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source(
    "_qrmod",
    '#include "src/qrmod.h"',
    sources=['src/qrmod.c'],
    include_dirs=['.'],
)

ffibuilder.cdef("""
    typedef struct {
        double t;       /* simulation time */
        double phi;     /* roll angle (Euler angle x) */
        double theta;   /* pitch angle (Euler angle y) */
        double psi;     /* yaw angle (Euler angle z) */
        double x;       /* position coordinate (earth axis x) */
        double y;       /* position coordinate (earth axis y) */
        double z;       /* position coordinate (earth axis z) */

        double a1;      /* rotor 1 control */
        double a2;      /* rotor 2 control */
        double a3;      /* rotor 3 control */
        double a4;      /* rotor 4 control */

        ...;
    } qrstate_t;

    void qr_init(qrstate_t *qrstate, double z_at_gnd);
    void qr_nextstate(qrstate_t *qrstate, double DT);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
