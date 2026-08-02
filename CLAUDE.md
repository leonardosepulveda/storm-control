# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a fork of the [Zhuang Lab / Babcock Lab `storm-control`](https://github.com/ZhuangLab/storm-control) repository: Python3 + PyQt5 software for acquiring STORM/super-resolution and MERFISH-style multiplexed imaging on custom microscopes. It is four independently-launchable GUI applications sharing a common library, plus a couple of standalone utilities.

Fork remote: `https://github.com/leonardosepulveda/storm-control` (origin), kept in sync with `ZhuangLab/storm-control`'s `master` via merge (see `git log`).

## The four main programs

| Program | Entry point | Role |
|---|---|---|
| **Hal** ("hal4000") | `storm_control/hal4000/hal4000.py` | The only program that talks directly to hardware (camera/stage/laser/DAQ) via `sc_hardware/` drivers. Runs as `python hal4000.py <config.xml>`. Acts as a **TCP server** on port 9000 for remote control. |
| **Steve** | `storm_control/steve/steve.py` | Stage-position mosaic viewer/planner. Used offline to build a low-mag mosaic and mark imaging positions. Acts as a **TCP client** to Hal (its own separate connection, on-demand — see IPC below). Run as `python steve.py`. |
| **Dave** | `storm_control/dave/dave.py` | Experiment/movie-sequence automation: walks a scripted list of actions (move stage, take movie, check focus, run a fluidics protocol, …) that drive Hal and Kilroy. Acts as a **TCP client** to both Hal (port 9000) and Kilroy (port 9500). Run as `python dave.py`. |
| **Kilroy** | `storm_control/fluidics/kilroy.py` | Fluidics protocol runner (pump + valve sequencing for buffer/probe exchange between imaging rounds). Lives under `fluidics/`, not a folder named `kilroy`. Acts as a **TCP server** on port 9500. Run as `python kilroy.py <config.xml>`. |

Typical workflow: Steve plans stage positions → Dave (loaded with/generating an XML sequence) drives Hal to take movies at each position and drives Kilroy to exchange fluidics between rounds → Hal is the only one touching real hardware.

Two standalone utilities also live in this repo, unrelated to the imaging-round workflow above:
- **Hazelnut** (`storm_control/hazelnut/hazelnut.py`) — watches a local data folder and pushes newly written files to a remote destination over SFTP, to offload acquired data off the microscope PC.
- **ZeeCalibrator** (`storm_control/zee_calibrator/main.py`) — one-off GUI for calibrating the z/focus-lock stage response.

None of the four have `setup.py` `console_scripts` entry points — they are all run as plain scripts (`.bat` launchers wrap this on Windows: `hal4000.bat`, `steve.bat`, `dave.bat`, `kilroy.bat`).

## Programming paradigm

**Event-driven / Qt signal-slot throughout.** Hal formalizes this into an internal pub/sub message bus on top of Qt signals: every module is a `HalModule(QtCore.QObject)` (`hal4000/halLib/halModule.py`) with a `newMessage = QtCore.pyqtSignal(object)` signal; `HalCore` (`hal4000/hal4000.py`) connects every loaded module's `newMessage` to its own dispatcher and pumps `HalMessage` objects (`halLib/halMessage.py`) to all modules every event-loop tick via a zero-interval `QTimer`. This drives Hal's module configuration chain (`configure1` → `configure2` → `configure3` → `new parameters file` → `start`).

**Hardware is a plugin system driven by XML config, not static imports.** `HalCore.__init__` reads the `<modules>` section of the launch config XML and, per entry, does `importlib.import_module(module_name)` + `getattr(module, class_name)` + instantiate. So both Hal's own GUI modules and every `sc_hardware/*` driver are wired purely by `module_name`/`class_name` strings in XML — there is no central module registry to edit when adding a new one, only a new XML block.

**Common hardware base classes** live in `sc_hardware/baseClasses/hardwareModule.py`: `HardwareModule`, `HardwareFunctionality`, `BufferedFunctionality` (+ `HardwareWorker(QtCore.QRunnable)` for off-thread device I/O, serialized with a `QMutex` and a 10-minute watchdog timer). More specific bases (`stageModule.StageModule`, `daqModule.DaqModule`, `amplitudeModule.AmplitudeModule`, `filterWheelModule.FilterWheelModule`, `lockModule.LockModule`, `joystickModule.JoystickModule`, `voltageZModule.VoltageZ`) sit in the same folder; real vendor drivers subclass these. `sc_hardware/none/` provides no-op simulators (used by the hardware-free demo config `hal4000/xml/none_config.xml`) so Hal is runnable without real instruments attached.

**Configuration is XML everywhere**, parsed by the shared `sc_library/parameters.py`: `parameters.config(...)` parses a Hal launch config into a `StormXMLObject` tree with `.get()`/`.getp()`/`.getAttrs()` accessors; `parameters.parameters(...)` parses a runtime imaging-parameters file. Typed parameter classes (`ParameterInt`, `ParameterFloat`, `ParameterString`, `ParameterRange`, `ParameterCustom`, …) map to a `type="..."` XML attribute. Dave and Kilroy each have their own XML dialect on top of this for sequences/protocols (see below).

**Threading**: mostly Qt's global thread pool (`QThreadPool.globalInstance()` in `halLib/halModule.py`, `runWorkerTask()`) rather than raw `QThread`, for hardware calls that shouldn't block the GUI event loop. One real `QThread` subclass exists for continuous polling: `BufferedAmplitudeModulation` in `sc_hardware/baseClasses/illuminationHardware.py`.

## Inter-process communication (Dave / Hal / Steve / Kilroy)

Generic transport lives in `sc_library/`: `tcpMessage.TCPMessage` (a message is just a plain string `message_type` + a `message_data` dict + a `response` dict, JSON-serialized — **there is no central enum/registry of message types**, just string literals compared via `message.isType("...")`), `tcpCommunications.TCPCommunicationsMixin` (raw newline-delimited-JSON socket read/write, emits a `messageReceived` Qt signal), `tcpClient.TCPClient`, `tcpServer.TCPServer` (accepts exactly one connection at a time; a second connection attempt gets a `"Busy"` reply).

- **Dave → Hal**: `dave.py`'s `CommandEngine.HALClient = tcpClient.TCPClient(port=9000, server_name="HAL")`. Actions are `DaveAction` subclasses in `daveActions.py` (`DATakeMovie`, `DAMoveStage`, `DASetParameters`, `DACheckFocus`, `DAFindSum`, …), each hardcoding a `message_type` string and an `action_type` of `"hal"`/`"kilroy"`/`"dave"`; `CommandEngine.startCommand()` routes by `action_type`. `"dave"`-type actions (`DAClearWarnings`, `DAEmail`) never go over TCP — they route internally via a Qt signal to `Dave.handleDaveAction()`.
- **Dave → Kilroy**: same pattern, `CommandEngine.kilroyClient = tcpClient.TCPClient(port=9500, server_name="Kilroy")`, action type `"kilroy"` (e.g. `DAValveProtocol`).
- **Steve → Hal**: Steve is a *second, independent* TCP client to Hal on port 9000 (`steve/comm.py`'s `Comm.tcp_client`), used on-demand (not held open) to take a picture, get mosaic settings/objective/stage position, or move the stage.
- **Dave → Steve** (branch `feature/dave-steve-fov-markers`): a second, independent channel, port 9600, added specifically to let Dave report FOV markers onto Steve's mosaic. Steve runs a `tcpServer.TCPServer` (`steve/tcpControl.py`'s `Controller`, wired up in `steve.py`'s `Window.__init__`) — the first time Steve has ever listened rather than only connected out; Dave gets a matching `CommandEngine.steveClient` (mirroring `HALClient`/`kilroyClient`). Two message types: `"Draw FOV Marker"` (stage_x/stage_y/warning; sent automatically by `Dave.sendFOVMarkerToSteve()` whenever a movie completes at a known position — not a recipe-authored action) and `"Clear FOV Markers"` (a real recipe-authored `DAClearFOVMarkers` action / `<clear_fov_boundaries/>` tag, deliberately kept independent from `DAClearWarnings`/`<clear_warnings/>` even though a recipe will typically place both at the same round boundary — Dave's own warning-count reset and Steve's mosaic markers are separate concerns). Steve also has a manual "Clear FOV Boundaries" menu action for the same clear, independent of the recipe-driven one. Unlike Hal/Kilroy, Steve connectivity is opportunistic for the automatic marker (a missing Steve never pauses an acquisition); the explicit `<clear_fov_boundaries/>` action follows the normal action-error path if Steve is genuinely unreachable when it executes. See `prompt_history/` for the design history.

Dave's warning system (`dave/daveWarnings.py`, `DaveWarning`/`DaveWarningsModel`) is keyed to *whichever `DaveAction` is currently executing*, not to a specific stage position — there is no existing per-position warning flag.

## Steve's drawing model (QGraphicsScene)

`steve/steveItems.py`: `SteveItem` is the base class for anything drawable/loadable (has a `graphics_item` + `item_id`); `SteveItemsStore` owns the single shared `QGraphicsScene` and every item, with `addItem()`, `removeItem(item_id)`, and `removeItemType(item_type)` (removes every item of a given class in one call — the mechanism `steve.py`'s `handleDeleteImages()` already uses, and the natural way to "clear all markers of a kind before the next round"). `steve/positions.py`'s `PositionItem` is the closest existing example of a colored, addable/removable `QGraphicsRectItem` (transparent fill, blue/red outline pen depending on selection state). Coordinate conversion between microns and pixels goes through `steve/coord.py` (`coord.Point`, `coord.umToPix()`/`pixToUm()`). `steve/fovMarker.py`'s `FOVMarkerItem` follows the same `PositionItem` pattern for the Dave→Steve FOV markers described above — yellow normally, a warning color if a warning fired for that FOV, cleared in bulk via `removeItemType(FOVMarkerItem)`. `fov_marker_size_um` in `settings_default.xml` is a fixed, per-microscope placeholder rather than a live-queried camera FOV size (Steve has no reliable way to know the current objective's real frame size in microns until an image has already been loaded).

## Repository layout

```
storm_control/
  hal4000/        # Hal: main acquisition GUI + hardware message bus (halLib/) + feature
                   #   subpackages (camera/, display/, feeds/, film/, focusLock/, illumination/,
                   #   mosaic/, progressions/, settings/, spotCounter/, stage/, tcpControl/, timing/)
                   #   + xml/ (launch configs, e.g. none_config.xml runs hardware-free)
  steve/           # Mosaic/position viewer: mosaic.py/mosaicView.py, steveItems.py/imageItem.py/
                   #   positions.py/sections.py, comm.py (TCP client to Hal), coord.py/objectives.py
  dave/            # Sequence automation: daveActions.py (action vocabulary), xml_generators/
                   #   (v1Generator.py/v2Generator.py — build the sequence XML dialect),
                   #   sequenceViewer.py, daveWarnings.py, notifications.py
  fluidics/        # Kilroy (kilroy.py) + pumps/ + valves/ + kilroyProtocols.py — fluidics protocol runner
  sc_library/      # Shared utilities: parameters.py (XML config parser), tcpMessage/tcpClient/
                   #   tcpServer/tcpCommunications.py (IPC primitives), halExceptions.py, hdebug.py,
                   #   hgit.py
  sc_hardware/     # Vendor driver tree, one subfolder per manufacturer/device category
                   #   (andor/, hamamatsu/, thorlabs/, nationalInstruments/, physikInstrumente/, …);
                   #   sc_hardware/baseClasses/ has the shared HardwareModule/HardwareFunctionality
                   #   base classes; sc_hardware/none/ has no-op simulators; README.md has a full
                   #   supported-device table
  hazelnut/        # standalone SFTP data-offload watcher utility
  zee_calibrator/  # standalone focus-lock/z-stage calibration GUI
  test/            # pytest suite for the whole repo (test_hal_*.py, test_dave_*.py, test_steve*.py, …),
                   #   run via `xvfb-run py.test --forked` (see .travis.yml)
  c_libraries/     # output of the C extensions built by the repo-root SConstruct
                   #   (c_image_manipulation, focus_quality, LMMoment, corr_2d_gauss, af_lock)
```

Repo-root files: `SConstruct` (SCons build for the C extensions above), `setup.py` (packaging only, no CLI entry points), `.travis.yml` (legacy CI: builds C libs, runs the pytest suite under Xvfb), `README.md`.

## Running the software

See `storm_control/hal4000/INSTALL.txt` for dependency/setup details. Quick smoke test with no real hardware attached:
```bash
cd storm_control/hal4000
python hal4000.py xml/none_config.xml
```

## Version control

Commit and push as you go — do not leave finished work uncommitted.

- After completing each individual modification, create its own focused git commit
  (one logical change per commit) with a clear message, then `git push` to `origin`
  (`github.com/leonardosepulveda/storm-control`).
- Do not batch many unrelated changes into a single commit, and do not let edits
  pile up locally — the remote should reflect progress as it happens.
- This is standing authorization to commit and push without asking each time.
- New feature work happens on its own branch (not directly on `master`), pushed to
  `origin` with upstream tracking so it's visible on GitHub as it progresses.
- An `upstream` remote (`github.com/ZhuangLab/storm-control`) is configured
  alongside `origin` (the fork). Periodically sync `master` with
  `upstream/master` (fetch + merge) and push the result to `origin/master`, since
  this fork does not auto-track upstream.

## History records (three tiers)

This project keeps three complementary, local-only histories. All live *inside*
the project, and all three are gitignored.

1. **`verbatim_history/`** — *uncompressed*. The exact text Claude writes each turn,
   appended automatically by a `Stop` hook (`.claude/hooks/save_verbatim.ps1`). No
   action needed from Claude — the harness captures it. One file per day,
   `{YYYY-MM-DD}_verbatim.md`.
2. **`prompt_history/`** — *compressed summary*. One file per request (format below).
   The append-only source of truth: records the verbatim prompt, plan, what was
   done, and the dead-ends. **Never edit past entries** — their value is provenance.
3. **`FINDINGS.md`** — *current state*. Curated, deduplicated head: what is true now,
   what was wrong, and the open next step. Read this first when resuming.

**Maintenance habit:** for **every user question/request**, write a tier-2
`prompt_history` entry (format below). When that entry changes a conclusion or
project state, also update the relevant `FINDINGS.md` section. Keep
`prompt_history` append-only.

### `prompt_history/` entry format

- One Markdown file per request, named `{YYYY_MM_DD_HH_MM}_{short_description}.md`
  (e.g. `2026_06_04_1432_add_prompt_history_convention.md`).
- **Get the actual date/time from the system** (`date "+%Y-%m-%d %H:%M:%S"` on
  bash, `Get-Date` on PowerShell) for both the filename and the `date:` field.
  The environment context provides only the date, never the time of day — never
  fabricate the `HH_MM` (see the "No fabrication" rule above).
- **`elapsed`** (just before `status`): wall-clock from prompt submission to task
  completion. Start = the `epoch N` injected by the `UserPromptSubmit` date/time
  hook for the message that began this request (for a request that spans several
  turns, the FIRST turn's epoch); end = `date +%s` (bash) /
  `[DateTimeOffset]::Now.ToUnixTimeSeconds()` (PowerShell) run at finish. Write a
  human-readable duration (e.g. `12m 30s`). Omit the field if no submit epoch is
  available — do not guess.
- YAML frontmatter for queryable metadata, then prose sections. Template:

```markdown
---
date: YYYY-MM-DD HH:MM
title: <short description>
files_modified:
  - path/relative/to/repo
elapsed: <e.g. 12m 30s — submit→completion wall-clock>
status: completed | in-progress | abandoned
---

## Prompt
<verbatim copy of the user's request>

## Plan
<Claude's plan of action before executing>

## Summary
<what was actually done, including any deviations from the plan>
```

Format rationale: Markdown + YAML frontmatter is Claude-native, human-readable,
and lets all entries be scanned/grepped by metadata without reading every body.
