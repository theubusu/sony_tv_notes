// decmod.c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/kallsyms.h>
#include <linux/uaccess.h>

#define KEY_SIZE 16
#define IV_SIZE  16
#define MAC_SIZE 16

struct dec_req {
	__u32 src;         /* user pointer to ciphertext, cast to __u32 for compat */
	__u32 dest;        /* user pointer to output buffer */
	__u32 size;        /* src_size == dest_size for your use case */
	__u32 key_type;
	__u32 key;         /* user pointer, KEY_SIZE bytes */
	__u32 iv;          /* user pointer, IV_SIZE bytes, or 0 for none */
	__u32 mac;         /* user pointer, MAC_SIZE bytes, or 0 for none */
	__u32 compress;    /* usually 0 */
	__s32 result;      /* decrypt_data() return value, filled on return */
};

#define DEC_IOCTL_DECRYPT _IOWR('d', 1, struct dec_req)

typedef int (*decrypt_fn_t)(void *src, unsigned src_size, void *dest, unsigned dest_size,
                             unsigned key_type, void *key, void *iv, void *mac,
                             int compress, void *param_10);
static decrypt_fn_t decrypt_fn;

static long dec_ioctl(struct file *f, unsigned int cmd, unsigned long arg)
{
	struct dec_req req;
	void *kbuf = NULL, *kkey = NULL, *kiv = NULL, *kmac = NULL;
	int ret = 0;

	if (cmd != DEC_IOCTL_DECRYPT)
		return -ENOTTY;
	if (copy_from_user(&req, (void __user *)arg, sizeof(req)))
		return -EFAULT;
	if (!req.size || req.size > 16 * 1024 * 1024)
		return -EINVAL;
	if (!req.src || !req.dest || !req.key)
		return -EINVAL;

	kbuf = kmalloc(req.size, GFP_KERNEL);
	kkey = kzalloc(KEY_SIZE, GFP_KERNEL);
	kiv  = kzalloc(IV_SIZE, GFP_KERNEL);
	kmac = kzalloc(MAC_SIZE, GFP_KERNEL);
	if (!kbuf || !kkey || !kiv || !kmac) {
		ret = -ENOMEM;
		goto out;
	}

	if (copy_from_user(kbuf, (void __user *)(unsigned long)req.src, req.size)) {
		ret = -EFAULT;
		goto out;
	}
	if (copy_from_user(kkey, (void __user *)(unsigned long)req.key, KEY_SIZE)) {
		ret = -EFAULT;
		goto out;
	}
	if (req.iv && copy_from_user(kiv, (void __user *)(unsigned long)req.iv, IV_SIZE)) {
		ret = -EFAULT;
		goto out;
	}
	if (req.mac && copy_from_user(kmac, (void __user *)(unsigned long)req.mac, MAC_SIZE)) {
		ret = -EFAULT;
		goto out;
	}

	req.result = decrypt_fn(kbuf, req.size, kbuf, req.size,
	                         req.key_type, kkey,
	                         req.iv ? kiv : NULL,
	                         req.mac ? kmac : NULL,
	                         req.compress, NULL);

	if (copy_to_user((void __user *)(unsigned long)req.dest, kbuf, req.size)) {
		ret = -EFAULT;
		goto out;
	}
	/* write back req.result */
	if (copy_to_user((void __user *)arg, &req, sizeof(req)))
		ret = -EFAULT;

out:
	kfree(kbuf);
	kfree(kkey);
	kfree(kiv);
	kfree(kmac);
	return ret;
}

static const struct file_operations dec_fops = {
	.owner = THIS_MODULE,
	.unlocked_ioctl = dec_ioctl,
};

static struct miscdevice dec_dev = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "sonydec",
	.fops = &dec_fops,
};

static int __init dec_init(void)
{
	unsigned long addr = kallsyms_lookup_name("decrypt_data");

	if (!addr) {
		pr_err("sonydec: decrypt_data not found (is sonyrd loaded?)\n");
		return -ENOENT;
	}
	decrypt_fn = (decrypt_fn_t)addr;
	pr_info("sonydec: decrypt_data resolved at %lx\n", addr);
	return misc_register(&dec_dev);
}

static void __exit dec_exit(void)
{
	misc_deregister(&dec_dev);
}

module_init(dec_init);
module_exit(dec_exit);
MODULE_LICENSE("GPL");