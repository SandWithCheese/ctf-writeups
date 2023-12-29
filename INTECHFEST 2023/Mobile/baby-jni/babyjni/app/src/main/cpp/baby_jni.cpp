#include <iostream>
#include <string>
#include <jni.h>
#include <unistd.h>

extern "C"
JNIEXPORT jstring JNICALL
Java_intechfest_cc_baby_1jni_MainActivity_getFlagJNIObject(JNIEnv *env, jclass clazz) {
    const char *flag = "flag{fake_flag_dont_submit}";

    jstring result = env->NewStringUTF((char *)flag);

    char fmt[64];
    sprintf(fmt, "JNIEnv: %p | Flag JNI Object: %p", env, result);
    return env->NewStringUTF(fmt);
}

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM *vm, void *reserved) {
    return JNI_VERSION_1_6;
}