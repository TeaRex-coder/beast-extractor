from pathlib import Path
import subprocess

# for dev
"""
requiredAssets = [
    "level1",
    "resources.assets",
    "sharedassets0.assets",
    "globalgamemanagers",
    "sharedassets2.assets",
    "level2",
    "sharedassets1.assets",
]
"""

requiredAssets = ["."]
assetTypes = ["tex2d", "sprite", "monoBehaviour", "font", "mesh"]


def extractAssetFiles(extractDir, outputAssetDir):
    extractDir = Path(extractDir)
    outputAssetDir = Path(outputAssetDir)

    sourceDir = extractDir / "Data"
    if not sourceDir.exists():
        raise ValueError("data dir in uploaded game")

    missingFiles = []
    for assetFile in requiredAssets:
        assetPath = sourceDir / assetFile
        if not assetPath.exists():
            missingFiles.append(assetFile)

    if missingFiles:
        raise ValueError(f"missing asset file: {', '.join(missingFiles)}")

    # create sub-dirs for each asset type
    for assetType in assetTypes:
        typeDir = outputAssetDir / assetType
        typeDir.mkdir(parents=True, exist_ok=True)

    for assetFile in requiredAssets:
        assetPath = sourceDir / assetFile
        for assetType in assetTypes:
            extractAssets(assetPath, assetType, outputAssetDir)


def extractAssets(assetPath: Path, assetType: str, outputBaseDir: Path):
    outputDir = outputBaseDir / assetType

    try:
        result = subprocess.run(
            [
                "AssetStudioModCLI",
                str(assetPath),
                "-t",
                assetType,
                "-o",
                str(outputDir),
                "--log-level",
                "error",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        if result.stdout:
            print(f"Processed {assetPath.name} for {assetType}: {result.stdout}")

    except subprocess.CalledProcessError as e:
        if "No files found" not in e.stderr:
            errorMsg = (
                f"Failed to extract {assetType} from {assetPath.name}: {e.stderr}"
            )
            raise RuntimeError(errorMsg)
    except FileNotFoundError:
        raise RuntimeError("AssetStudioModCLI not installed")
