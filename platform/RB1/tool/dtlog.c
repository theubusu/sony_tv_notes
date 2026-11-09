#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

int main(void)
{
    int fd = open("/dev/dtlog", O_RDWR);
    uint32_t arg[2] = {0, 0};
    int total = ioctl(fd, 0x4008a600, arg);
    if (fd < 0 || total <= 0) { perror("attach"); return 1; }

    volatile uint32_t *h = mmap(NULL, total, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    if (h == MAP_FAILED) { perror("mmap"); return 1; }
    uint8_t *data = (uint8_t *)h + 0x24;
    uint32_t cap = h[2];

    uint32_t off = h[3];            /* skip the old backlog */
    h[4] = off;                     /* tail = head: ring is now empty */

    for (;;) {
        volatile uint32_t *r = (volatile uint32_t *)(data + off);
        uint32_t state = r[2], next = r[1];
        if (state == 2) {
            printf("[%u.%06u] %s", r[3], r[4], (char *)r + r[6]);
            fflush(stdout);
            off = next;
            h[4] = off;
        } else if (state == 0 && next == 0 && off != 0) {   /* wrap marker */
            off = 0;
            h[4] = 0;
        } else {
            usleep(20000);          /* empty, or record still being filled */
        }
    }
}