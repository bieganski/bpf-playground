#include "vmlinux.h"

#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <bpf/bpf_core_read.h>

char _license[] SEC("license") = "GPL";

SEC("kprobe/do_sysinfo")
int BPF_PROG(do_sysinfo, struct sysinfo *sysinfo)
{
    const char str[] = "called do_sysinfo\n";
    bpf_trace_printk(str, sizeof(str));
    return 0;
}
