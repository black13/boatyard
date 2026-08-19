#include <stdio.h>
#include <unistd.h>

/* The reference daemon pattern:
   - plain C/C++, small binary, one failure domain
   - supervised by systemd (restart + crash-loop -> reboot)
   - writes only to its StateDirectory, runs as its own user
   - eng builds behave differently (no reboot storm, verbose logs) */

int main(void)
{
#ifdef ENG
    fprintf(stderr, "hello: engineering build\n");
#endif
    while (1) {
        printf("hello from slot boot\n");
        fflush(stdout);
        sleep(5);
    }
    return 0;
}
