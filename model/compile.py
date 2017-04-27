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
        double t;
        ...;
    } qrstate_t;

    void qr_init(qrstate_t *qrstate, double z_at_gnd);
    void qr_nextstate(qrstate_t *qrstate, double DT);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
