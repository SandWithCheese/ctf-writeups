#include <linux/module.h>
#include <linux/fs.h>
#include <linux/mman.h>
#include "char.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("hyffs");
MODULE_DESCRIPTION("Auth as a Service - User - Kernel");

static struct chrdev_info cinfo = {};

static int auth_open(struct inode *inode, struct file *filp){
    if(!(filp->private_data = (aes_ctx_t*)kzalloc(sizeof(aes_ctx_t), GFP_KERNEL))) return -1;
    return 0;
}

static int auth_close(struct inode *inode, struct file *filp){
    aes_ctx_t *ctx;

    if((ctx = filp->private_data)){
        if(ctx->round_key) {
            kfree(ctx->round_key);
            ctx->round_key = NULL;
        }
        if(ctx->key) {
            kfree(ctx->key);
            ctx->key = NULL;
        }
        if(ctx->iv) {
            kfree(ctx->iv);
            ctx->iv = NULL;
        }
        kfree(filp->private_data);
        filp->private_data = NULL;
    }
    return 0;
}

static long auth_ioctl(struct file *filp, unsigned int cmd, unsigned long arg){
    aes_ctx_t *ctx = filp->private_data;

    switch (cmd) {
        case SET_KEY: {
            if(!arg) return -EINVAL;
            if(!ctx->key)
                if(!(ctx->key = (u8*)kzalloc(AES_BLOCK_SIZE, GFP_KERNEL))) return -ENOMEM;
            if(copy_from_user(ctx->key, (void*)arg, AES_BLOCK_SIZE)) return -EINVAL;
            break;
        }
        case SET_IV: {
            if(!arg) return -EINVAL;
            if(!ctx->iv)
                if(!(ctx->iv = (u8*)kzalloc(AES_BLOCK_SIZE, GFP_KERNEL))) return -ENOMEM;
            if(copy_from_user(ctx->iv, (void*)arg, AES_BLOCK_SIZE)) return -EINVAL;
            break;
        }
        default: return -EINVAL;
    }

    return 0;
}

static ssize_t auth_read(struct file *filp, char __user *buf, size_t count, loff_t *fpos){
    aes_ctx_t *ctx = filp->private_data;
    u8 *ciphertext = NULL;

    if(!ctx->key || !ctx->iv) return 0;
    if(count % AES_BLOCK_SIZE != 0) return -EINVAL;

    if(!ciphertext)
        if(!(ciphertext = kzalloc(count, GFP_KERNEL))) return -ENOMEM;

    if(copy_from_user(ciphertext, (u8*)buf, count)) return -EINVAL;

    if(!ctx->round_key)
        if(!(ctx->round_key = (u8*)kzalloc(EXP_KEYLEN, GFP_KERNEL))) return -ENOMEM;

    mode_CBC_decrypt(ctx, ciphertext, count, *fpos);

    if(copy_to_user((u8*)buf, ciphertext, count)) return -EINVAL;
    
    kfree(ciphertext);
    return 0;
}

static ssize_t auth_write(struct file *filp, const char __user *buf, size_t count, loff_t *fpos){
    aes_ctx_t *ctx = filp->private_data;
    u8 *plaintext = NULL;
    size_t size;

    if(!ctx->key || !ctx->iv) return 0;
    size = count + AES_BLOCK_SIZE - (count % AES_BLOCK_SIZE);

    if(!plaintext)
        if(!(plaintext = kzalloc(size, GFP_KERNEL))) return -ENOMEM;

    if(copy_from_user(plaintext, (u8*)buf, count)) return -EINVAL;

    if(!ctx->round_key) 
        if(!(ctx->round_key = (u8*)kzalloc(EXP_KEYLEN, GFP_KERNEL))) return -ENOMEM;    

    mode_CBC_encrypt(ctx, plaintext, pad(plaintext, count), *fpos);

    kfree(plaintext);
    return 0;
}

static vm_fault_t vma_fault_mmap(struct vm_fault *vmf){
    struct page *page = NULL;
    unsigned long offset = ((vmf->vma->vm_pgoff << PAGE_SHIFT) + (vmf->address - vmf->vma->vm_start));

    if(offset > (PAGE_SIZE << 6))
        goto page_err;
    
    page = virt_to_page(vmf->vma->vm_private_data + offset);
    vmf->page = page;
    get_page(page);

page_err:
    return 0;
}

static struct vm_operations_struct kauth_mmap_vm_ops = {
    .fault = vma_fault_mmap
};

static int auth_mmap(struct file *filp, struct vm_area_struct *vma){
    if((vma->vm_pgoff << PAGE_SHIFT) + vma->vm_end - vma->vm_start > MAX_SIZE) return -ENOMEM;

    vma->vm_private_data = filp->private_data;
    vma->vm_ops = &kauth_mmap_vm_ops;

    return 0;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = auth_open,
    .release = auth_close,
    .unlocked_ioctl = auth_ioctl,
    .read = auth_read,
    .write = auth_write,
    .mmap = auth_mmap
};

int reg_chrdev(void){
    dev_t dev;
    if(alloc_chrdev_region(&dev, 0, 1, DEVICE_NAME)) return -EBUSY;
    
    cinfo.major = MAJOR(dev);
    cdev_init(&cinfo.cdev, &fops);

    if(cdev_add(&cinfo.cdev, dev, 1)){
        unregister_chrdev_region(dev, 1);
        return -EBUSY;
    }
    cinfo.class = class_create(DEVICE_NAME);
    if(IS_ERR(cinfo.class)) cdev_del(&cinfo.cdev);

    device_create(cinfo.class, NULL, MKDEV(cinfo.major,0), NULL, DEVICE_NAME);
    return 0;
}

void unreg_chrdev(void){
    device_destroy(cinfo.class, MKDEV(cinfo.major,0));
    class_destroy(cinfo.class);
    cdev_del(&cinfo.cdev);
    unregister_chrdev_region(MKDEV(cinfo.major, 0), 1);
}

static int __init module_initialize(void){
    int ret;
    if((ret = reg_chrdev()) < 0) goto err;
err:
    return ret;
}

static void __exit module_finalize(void){
    unreg_chrdev();
}

module_init(module_initialize);
module_exit(module_finalize);