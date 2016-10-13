/* some description
*/
// some more description
typedef struct {
    struct {
        int a;
        int b;
    } c;
    int foo;
    double bar;
} StructName1;
====================
// comment to second description
typedef struct {
    long foo_bar;
    float bar;
    struct {
        struct {
            char g[80];
        } d;
        int a;
    } b;
    struct {
        signed short j;
    } h;
} StructName2;