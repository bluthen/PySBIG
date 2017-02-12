/* Uncompress C code taken from ccd view ccdread_.c */

/* CCDVIEW: read (decompress) ST-x images                 */
/* Miroslav Broz, version Feb 19th 2002, freeware         */
/* miroslav.broz@email.cz, http://www.astrohk.cz/ccdview/ */

#include "Python.h"

#define BZERO 32768

static PyObject *
PySBIGuncompress_uncompress_line(PyObject *self, PyObject *args)
{
    const char *buf;
    signed short *newline;
    int width, lengthofline;
   
    unsigned short buf2; 
    int l, k;
    char *ptr;

    PyObject *res;


    if(!PyArg_ParseTuple(args, "s#i", &buf, &lengthofline, &width))
        return NULL;
    newline = malloc(width * sizeof(signed short));
    if(newline == NULL) {
        PyErr_SetString(PyExc_MemoryError,
            "Can't allocate memory to uncompress data");
        return NULL;
    }

    buf2 = (unsigned char)buf[0] + (((unsigned short)(unsigned char)buf[1]) << 8);
    newline[0] = buf2;
    l = 1;
    k = 2;
    do {
        while ((buf[k] != -128) && (k <= (lengthofline - 1))) {
            buf2 += buf[k];
            newline[l] = buf2;
            k++;
            l++;
        }
        if (k < (lengthofline - 2)) {
            buf2 = (unsigned char)buf[k+1] + (((unsigned short)(unsigned char)buf[k+2]) << 8);
            newline[l] = buf2;
            l++;
            k += 3;
        }
    } while (k <= (lengthofline - 1));

//    for (l = 0; l < width; l++) {
        //newline[l] = newline[l] - BZERO;
        //printf("%d\n", newline[l]);
//    }

    res = Py_BuildValue("s#", newline, 2*width);
    free(newline);
    return res;
}

static PyMethodDef PySBIGuncompress_methods[] = {
    {"uncompress_line", PySBIGuncompress_uncompress_line, METH_VARARGS},
    {NULL,      NULL}       /* sentinel */
};


DL_EXPORT(void)
initPySBIGuncompress(void)
{
    PyObject *m;
    m = Py_InitModule("PySBIGuncompress", PySBIGuncompress_methods);
}

