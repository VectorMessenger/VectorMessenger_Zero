# **Vector Messenger** - Changelog
> This changelog begins from `2020.07.01`. Any change before this date is not stated here.


# Unreleased

**2020-08-17**
- Basic implementation of web-gui with `pywebview` and `flask`
- Renamed all modules from CamelCase to under_score, also renamed some of them
- Fixed VM package detection for `poetry` with self configured `setup.py`
- Changed built-in `json` module to `ujson`
- Short arg `-L` for running server on localhost

---

## Build [**B202008020120**](https://github.com/maximilionus/VectorMessenger/releases/tag/B202008020120)

**2020-08-02**
- Downgrade to python `3.7`
- Allow only python `>=3.7` `<3.8`
- Changed `cx-Freeze` build module to `PyInstaller`
- Rewritten `build.py` script to fully support `PyInstaller`
- Added ags handling to `build.py` with `argparse` module
- Updated `.lock` file
- Fixed paths handling for PyInstaller builds
- `RedirectSTD` enhanced to be more easy to use

**2020-07-22**
- Run `update checker` thread as daemon
- CamelCase to under_score

**2020-07-21**
- Removed `--log-messages` command from server-side

**2020-07-14**
- Removed `VMClient.png` from source again

**2020-07-11**
- Separated helpers to 'global' and 'client'
- Removed build icons for platforms except win32
- Optimized build script
- Added command 'eval' to client debug console

**2020-07-02:01-26**
- Added changelog
- Cross-platform icons implemented
- Switch to `poetry run` system
- Fixed run dirs for built and source code versions
- Fixed `build.py` script deps
- Remove `.png` icon from source. `ico` works perfectly.
- Rename `compile.py` script to `build.py`
