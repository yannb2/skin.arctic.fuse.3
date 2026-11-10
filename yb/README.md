# Arctic Fuse 3 YB: our fork

Yann's fork of [signde/skin.arctic.fuse.3](https://github.com/signde/skin.arctic.fuse.3) (signde's
avdvplus/p3i build of jurialmunkey's Arctic Fuse 3, Kodi 21 Omega). It runs on the Ugoos AM6B+ boxes
with CoreELEC avdvplus. How the boxes are set up, and how to install this skin on them, is in
[yannb2/home-theater](https://github.com/yannb2/home-theater) (`devices/ugoos-am6b-plus/README.md`,
part 7). Everything the fork adds is marked `YB fork` in comments, so upstream merges are easy to
read.

## What's different from signde's skin

| Change | Where | Since |
| --- | --- | --- |
| Own add-on ID `skin.arctic.fuse.3.yb`, name "Arctic Fuse 3 YB". It installs **next to** signde's skin (a fallback is one switch away), and signde's updates can't overwrite it | `addon.xml`, every `skin.arctic.fuse.3` reference in `1080i/` and `shortcuts/` | 73.3.4.18.1 |
| **Start info:** for a few seconds when a video starts, the Info panel plus a row of media flags read from the player (resolution, codec, DV with FEL/MEL, HDR10/HDR10+, Atmos/DTS:X, channels), like Arctic Zephyr Reloaded's "Show detailed info when video starts" | `1080i/Custom_1154_StartInfo.xml`, `1080i/Custom_1155_StartInfoReset.xml` | 73.3.4.18.1 |
| Start info settings: Skin settings > Playback > **Start info** (on/off, 3/5/7/10 s, panel and flags or flags only) | `SkinSettings_Items_Playback` in `Includes_SkinSettings.xml`, labels in `Includes_Labels.xml` | 73.3.4.18.1 |
| Build: XML check + installable zip on every push; a `yb-v*` tag publishes a release | `yb/make_zip.py`, `.github/workflows/yb-build.yml` | 73.3.4.18.1 |

Planned: tag badges from our MKV Tags Jellyfin plugin (edition, release group, source, DV
profile) in the start info and info panels; DVD/BDRip/Hybrid source flags.

## Versions

`<signde version>.<our revision>`: 73.3.4.18.1 = signde 73.3.4.18 + our revision 1. After merging
a new signde version, reset our revision to 1 (73.3.4.19.1). Add a line to `<news>` in `addon.xml`.

## Build and release

```
python3 yb/make_zip.py              # checks every skin XML file, writes dist/skin.arctic.fuse.3.yb-<version>.zip
python3 yb/make_zip.py --check-only # just the XML check
```

Every push and PR runs the same in GitHub Actions and keeps the zip as a build artifact. To
release: bump `version` in `addon.xml`, merge, then tag `yb-v<version>` (e.g. `yb-v73.3.4.18.1`)
and push the tag; the release gets the zip attached. Upstream's `release.yml` only reacts to tags
starting with `v`, so it ignores ours.

## Install on a box (first time)

1. Copy the zip onto the box (`scp` to `/storage/`, or the Samba share).
2. Add-ons > Install from zip file > the zip. Kodi pulls the same dependencies as signde's skin
   (keep the signde repository installed for those).
3. Switch to "Arctic Fuse 3 YB". Its settings start empty because they're stored per add-on ID:
   copy `/storage/.kodi/userdata/addon_data/skin.arctic.fuse.3/settings.xml` to
   `.../addon_data/skin.arctic.fuse.3.yb/` before switching to keep signde's skin settings.
   Home widgets (Skin Variables) are set up again.

Updates: install the new zip the same way (Kodi updates the add-on in place).

## Merging upstream (monthly)

```
git remote add upstream https://github.com/signde/skin.arctic.fuse.3   # once
git fetch upstream && git merge upstream/omega
```

Conflicts are expected only where we renamed the add-on ID (version labels, `Includes_Paths.xml`,
the Skin Variables generator) and in the two settings files. Search for `YB fork` and
`skin.arctic.fuse.3.yb` afterwards, and check new `skin.arctic.fuse.3` references:
`git grep -n 'skin\.arctic\.fuse\.3[^.]' -- 1080i shortcuts`.
