all: sysinfo.o
	@echo DONE

####################################

deps:
	sudo apt-get install libbpf-dev



vmlinux.h:
	bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
	wc -l vmlinux.h

sysinfo.bc: vmlinux.h
	clang -w -O2 -emit-llvm -c sysinfo.c -I.

sysinfo.o: sysinfo.bc
	llc -march=bpf -mcpu=probe -filetype=obj -o sysinfo.o sysinfo.bc




load:
	sudo bpftool prog load sysinfo.o /sys/fs/bpf/programik

monitor:
	sudo cat /sys/kernel/debug/tracing/trace_pipe