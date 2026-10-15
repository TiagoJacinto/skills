---
name: ubuntu-machine-configuration
description: Inspect Ubuntu automatic login and configure the Ubuntu portion of Wake-on-LAN, with verified limits and safety gates.
disable-model-invocation: true
---

# Ubuntu machine configuration

Handle these host settings separately from Computer Use setup. Do only the requested branch; needing desktop control is not authorization to configure automatic login or remote power access.

**Failure pattern:** existing automatic-login configuration and saved wake settings do not prove next-boot behavior or end-to-end remote wake capability.

**Historical verification:** GDM automatic login was already configured, not newly enabled. NetworkManager saved magic-packet wake and the live Ethernet adapter reported `Wake-on: g` while the connection remained active. BIOS, sender installation, and real waking were not verified.

## Procedure

1. Confirm the requested outcome, target user/machine, remote-access method, and permitted changes. Explain the physical-access risk before changing automatic login. Obtain action-specific authorization before security changes or disruptive power operations.
2. Read [references/machine-settings.md](references/machine-settings.md) for the requested branch: automatic-login inspection, or the Ubuntu portion of Wake-on-LAN. Skip the other branch.
3. Inspect actual settings and prerequisites. Do not copy historical session IDs, account names, interfaces, or NetworkManager connection names without verifying them.
4. Make only authorized changes. Preserve unrelated settings and active remote access. Never restart GDM, reconnect networking, suspend, reboot, or shut down merely to test a saved setting.
5. Read back the changed values. Report saved configuration separately from observed behavior. Existing automatic-login settings do not establish a successful next boot.
6. Stop when the requested configuration is verified, or record the blocker. A real wake test requires a confirmed sender, BIOS state, explicit power-operation approval, and a local recovery plan. Respect the user's prior deferral unless they ask to resume.

For Computer Use installation, graphical-session access, screen-lock configuration needed for desktop availability, accessibility, window control, screenshot permissions, and input readiness, call the Skill tool with "ubuntu-desktop-computer-use" instead.

## What did not work / limits to preserve

- Treating GDM automatic login as a bypass for disk encryption or keyring prompts: neither was established or configured by this workflow.
- Treating `magic` / `Wake-on: g` as a successful wake: these verify only Ubuntu configuration, not firmware, delivery of a wake packet, or recovery from power-off.

## Source evidence

A local session record documented these historical checks; it is not included in this package.

- Lines 208–224: inspected GDM and discovered existing automatic login. Next-boot behavior was not tested. The accompanying screen-lock work is recorded under `ubuntu-desktop-computer-use`.
- Lines 596–615: inspected an Ethernet adapter; configured saved `magic` and live `Wake-on: g`; verified network remained connected.
- Lines 621–627: BIOS, sender setup, and wake tests remained pending; the user explicitly deferred further Wake-on-LAN setup.

These are historical checks, not a claim that current machine settings or end-to-end wake behavior have just been tested.
