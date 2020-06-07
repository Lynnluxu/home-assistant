# Home Assistant on RPI4B

## Cheatsheet

```bash
# Connect to the raspberrypi, with an SSH tunnel (for Rhasspy)
ssh pi@raspberrypi.local -L 12101:localhost:12101
```

## Install and run

### Step 1: Install Raspbian Buster Lite (headless setup)

**On another computer:**

1. [Download and write Raspbian Buster Lite to an SD card](https://www.raspberrypi.org/documentation/installation/installing-images/) as a [headless setup](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).

**On the RaspberryPi 3B+** (`ssh pi@raspberrypi.local`, default password: `raspberry`):

1. Change the default password:

   ```bash
   passwd pi
   ```

2. Add my public ssh key:

   ```bash
   mkdir -p ~/.ssh && echo $(curl https://cdn.bminusl.xyz/keys/ssh) >> ~/.ssh/authorized_keys
   ```

3. Install my dotfiles:

   ```bash
   git clone https://gitlab.com/bminusl/dotfiles.git
   cd dotfiles
   ./install-dotfiles.sh
   ```

4. [Do some tweaking to use Bluetooth.](https://sigmdel.ca/michel/ha/rpi/bluetooth_n_buster_01_en.html)

5. [Install Docker](https://docs.docker.com/install/linux/docker-ce/debian/#install-using-the-convenience-script):

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker pi
   ```

6. Install `docker-compose`:

   ```bash
   sudo apt install python3-pip
   sudo pip3 install docker-compose
   ```

### Step 2: Run Home Assistant and other services

```
docker-compose up -d
supervisord
```

### Step 3: Security

1. Install a firewall:

   ```bash
   sudo apt install ufw
   sudo ufw allow ssh
   sudo ufw allow 8123
   sudo ufw allow 15000
   sudo ufw enable
   ```

[Additional information](https://www.raspberrypi.org/documentation/configuration/security.md), if necessary.
