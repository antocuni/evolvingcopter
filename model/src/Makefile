CFLAGS = -W -Wall -O2 
LDLIBS = -lm

qrmod.so:
		gcc -o qrmod.so -shared -fPIC $(CFLAGS) qrmod.c $(LDLIBS)

qrmod.o: 	qrsim.h qrmod.c
		gcc -c $(CFLAGS) qrmod.c
