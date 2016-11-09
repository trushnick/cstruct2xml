/*
    Struct A description
*/
typedef struct _A {
    // field 'foo' of A struct
    int foo;
    double bar[15];
} A;

typedef struct _B {
    A a;
    float foo;
    // some inner structure
    struct {
        short foo;
        signed s;
        unsigned long l;
    } bars[5];
} B;