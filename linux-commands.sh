# Lathe's reference for setting up the test environment

# Starts kvm VM with correct config given that you have mininet-vm-x86_64.vmdk in the current directory a
sudo qemu-system-x86_64 -machine accel=kvm -m 2048 mininet-vm-x86_64.vmdk -net nic,model=virtio -net user,net=192.168.101.0/24,hostfwd=tcp::8022-:22 &

# ssh into mininet-vm over local KVM port
ssh -Y -p 8022 mininet@localhost