#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

struct dec_req {
	uint32_t src, dest, size, key_type, key, iv, mac, compress;
	int32_t result;
};
#define DEC_IOCTL_DECRYPT _IOWR('d', 1, struct dec_req)

#define PORT 5151
#define MAX_SIZE (16 * 1024 * 1024)

static int read_full(int fd, void *buf, size_t n)
{
	size_t got = 0;
	while (got < n) {
		ssize_t r = read(fd, (char *)buf + got, n - got);
		if (r <= 0) return -1;
		got += r;
	}
	return 0;
}

static int write_full(int fd, const void *buf, size_t n)
{
	size_t sent = 0;
	while (sent < n) {
		ssize_t w = write(fd, (const char *)buf + sent, n - sent);
		if (w <= 0) return -1;
		sent += w;
	}
	return 0;
}

static void handle_client(int cfd, int devfd)
{
	uint32_t key_type, compress, size;
	uint8_t key[16], iv[16], mac[16];
	uint8_t have_iv, have_mac;
	uint8_t *data = NULL;

	if (read_full(cfd, &key_type, 4)) goto done;
	if (read_full(cfd, key, 16)) goto done;
	if (read_full(cfd, &have_iv, 1)) goto done;
	if (read_full(cfd, iv, 16)) goto done;
	if (read_full(cfd, &have_mac, 1)) goto done;
	if (read_full(cfd, mac, 16)) goto done;
	if (read_full(cfd, &compress, 4)) goto done;
	if (read_full(cfd, &size, 4)) goto done;

	if (size == 0 || size > MAX_SIZE) goto done;

	data = malloc(size);
	if (!data) goto done;
	if (read_full(cfd, data, size)) goto done;

	struct dec_req req = {0};
	req.src = (uint32_t)(unsigned long)data;
	req.dest = (uint32_t)(unsigned long)data;
	req.size = size;
	req.key_type = key_type;
	req.key = (uint32_t)(unsigned long)key;
	req.iv = have_iv ? (uint32_t)(unsigned long)iv : 0;
	req.mac = have_mac ? (uint32_t)(unsigned long)mac : 0;
	req.compress = compress;

	if (ioctl(devfd, DEC_IOCTL_DECRYPT, &req) < 0) {
		req.result = -1;
	}

	write_full(cfd, &req.result, 4);
	write_full(cfd, &size, 4);
	write_full(cfd, data, size);

done:
	free(data);
	close(cfd);
}

int main(void)
{
	int devfd = open("/dev/sonydec", O_RDWR);
	if (devfd < 0) {
		perror("open /dev/sonydec");
		return 1;
	}

	int sfd = socket(AF_INET, SOCK_STREAM, 0);
	int one = 1;
	setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));

	struct sockaddr_in addr = {0};
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = INADDR_ANY;
	addr.sin_port = htons(PORT);

	if (bind(sfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("bind");
		return 1;
	}
	listen(sfd, 4);
	fprintf(stderr, "decsrv listening on :%d\n", PORT);

	for (;;) {
		struct sockaddr_in cli;
		socklen_t clilen = sizeof(cli);
		int cfd = accept(sfd, (struct sockaddr *)&cli, &clilen);
		if (cfd < 0) continue;
		handle_client(cfd, devfd);
	}
	return 0;
}