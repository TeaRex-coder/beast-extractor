# BEAST Extractor

This project aids macOS BEAST players extract game assets. A local copy of the user's `/Applications/BEAST.app/Contents/Resources/Data` directory is uploaded to the server and returned as a ZIP archive of organized assets. The directory does not contain any sensitive user data and is not kept by the server. _You can check the code yourself, or self-host, it's open-source :)_

The official version is hosted here: [website.extension](https://website)

## How it Works

Three primary asset types are handled:

### Protocol Buffers

The `StreamingAssets/Data` & `StreamingAssets/UI` directories each contain protobd and protobw files respectively. They are decompiled into human-readable proto files using [protoc](https://github.com/protocolbuffers/protobuf), the Protobuf Compiler.

```sh
protoc --deocde_raw < file.protobd > file.proto
protoc --deocde_raw < file.protobw > file.proto
```

### Audio

Game audio is produced using Wwise Engine and packaged in a `.bnk` SoundBank. [wwiser's](https://github.com/bnnm/wwiser) CLI is used to extract TXTP files from the SoundBank. `SoundbanksInfo.xml` must be in the same directory as the target SoundBank to automatically apply file names.

```sh
python3 wwiser.pyz -g Soundbank_BEAST.bnk
```

TXTP files are converted to WAV using [vgmstream CLI](https://github.com/vgmstream/vgmstream/blob/master/doc/USAGE.md#testexevgmstream-cli-command-line-decoder).

```sh
vgmstream-cli file.txtp -o file.wav
```

### Assets

Unity assets (font, mesh, monoBehaviour, spirte & tex2d) are found in the `Resources/Data` directory. They are extracted using [AssetStudioModCLI](https://github.com/aelurum/AssetStudio/tree/AssetStudioMod/AssetStudioCLI) into their respective file formats.

```sh
AssetStudioModCLI file -t [assetType] -o [output directory] --log-level error
```

## Server Set Up

Ansible Playbook WIP

### Protocol Buffers

- Install [protoc](https://github.com/protocolbuffers/protobuf/releases)

### Audio

- Install [wwiser](https://github.com/bnnm/wwiser)
  - Dependencies
- Install [vgmstream-cli](https://github.com/vgmstream/vgmstream?tab=readme-ov-file#getting-vgmstream)
  - Dependencies

### Assets

- Install [AssetStudioModCLI](https://github.com/aelurum/AssetStudio/releases)
  - Dependencies

## Disclaimer

This repository is a fan project and is not affiliated with or endorsed by BEAST's original creators. This project does not re-distribute game assets, simply aiding players extract game assets from the macOS Apple Arcade version through a valid Apple Arcade Subscription.

All rights to the original game content, including but not limited too Protocol Buffers, textures, fonts, meshes and audio files, are owned by Oh BiBi. This project is primarily intended for archival purposes, not to infringe on copyright.

If you are the copyright holder and believe this project violates your rights, please contact email me at [alexandre@boutoille.com](mailto:alexandre@boutoille.com).
