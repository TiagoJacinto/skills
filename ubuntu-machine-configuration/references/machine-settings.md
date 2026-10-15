# Optional host configuration

These branches record work beyond desktop-tool installation. None is an automatic prerequisite. Confirm the user's requested scope and obtain action-specific authorization for security changes or power operations. Historical settings are not proof of current state.

## Automatic login

Automatic login exposes logged-in accounts to anyone with physical access. Obtain explicit approval before changing it. Screen-lock configuration needed for Computer Use belongs to `ubuntu-desktop-computer-use`, not this branch.

Inspect the actual display manager and account. In the source session `/etc/gdm3/custom.conf` already contained:

```ini
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=tiago
```

The agent did not establish next-boot success or need to change that file. Do not blindly write it on another machine, restart GDM, or bypass boot encryption/keyring prompts. If automatic login needs changing, confirm the intended user and inspect the current GDM configuration first.

## Power control and Wake-on-LAN — partial workflow

**Verified:** the Ubuntu portion on Dell Precision 5810: NetworkManager saved `magic`, the Ethernet adapter reported `Wake-on: g`, and the connection remained active.

**Not verified:** BIOS changes, Raspberry Pi sender setup, waking from suspend/shutdown, or power-on from outside the LAN. The user deferred those steps. This is not a complete, proven Wake-on-LAN recipe.

An agent running on a powered-off machine cannot wake itself. Reboot/suspend/shutdown can only be requested while it runs and remain subject to system permissions. Do not test them remotely without explicit authorization and a recovery plan.

### Inspect and configure only Ubuntu's portion

Discover the active wired interface and NetworkManager connection rather than assuming historical names:

```bash
nmcli device status
nmcli -g GENERAL.CONNECTION device show INTERFACE
sudo ethtool INTERFACE
```

Check support for magic-packet wake and confirm this is the connection carrying remote access. Substitute the observed interface and connection in the following commands, with configuration authorization:

```bash
sudo nmcli connection modify "CONNECTION_NAME" \
  802-3-ethernet.wake-on-lan magic
sudo ethtool -s INTERFACE wol g
nmcli -g 802-3-ethernet.wake-on-lan connection show "CONNECTION_NAME"
sudo ethtool INTERFACE
nmcli -g GENERAL.STATE device show INTERFACE
```

Require saved `magic` (or the equivalent documented value), live `Wake-on: g`, and an active link/connection. Do not reconnect the interface merely to apply the setting; that could sever SSH. Missing support or privilege is a blocker, not permission to change drivers or disconnect networking.

### Deferred continuation, not historical success

The prior session recommended Dell BIOS **Wake on LAN → LAN Only** and **Deep Sleep Control → Disabled**, with AC power and Ethernet connected. These were recommendations, not observed changes. Verify the current model's manual and actual BIOS state before applying them; do not choose PXE boot unless requested.

The user selected a Raspberry Pi as a potential LAN wake sender but did not provide its SSH target. Before continuing, ask for the authorized target and confirm it is on the same LAN. A future sender could use `wakeonlan`, with broadcast address derived from the actual network and MAC read from the target adapter—not copied from the transcript.

For remote waking over Tailscale, an always-on LAN sender is needed; Tailscale alone does not deliver a LAN broadcast to a powered-off Dell. A local test only needs a powered-on sender on that LAN. Do not expose a public wake port.

Report Ubuntu setting verification separately from a real wake test. Arrange local recovery before any future suspend/shutdown test.
