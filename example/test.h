typedef struct _A {
    int foo;
    double bar[15];
} A;

typedef struct _B {
    A a;
    float foo;
    struct {
        short foo;
        signed s;
        unsigned long l;
    } bars[5];
} B;