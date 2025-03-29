from pathlib import Path
import zipfile
from audioExtractor import extractAudioFiles
from dataExtractor import extractDataFiles
from uiExtractor import extractUiFiles
from assetExtractor import extractAssetFiles


def checkStructure(extractDir: Path):
    requiredPaths = {
        "bnk": extractDir
        / "Data"
        / "StreamingAssets"
        / "Audio"
        / "GeneratedSoundBanks"
        / "Mac"
        / "Soundbank_BEAST.bnk",
        "xml": extractDir
        / "Data"
        / "StreamingAssets"
        / "Audio"
        / "GeneratedSoundBanks"
        / "Mac"
        / "SoundbanksInfo.xml",
    }

    missing = []
    if not requiredPaths["bnk"].exists():
        missing.append("Soundbank_BEAST.bnk")
    if not requiredPaths["xml"].exists():
        missing.append("SoundbanksInfo.xml")

    return missing, requiredPaths


def processUploadedZip(uploadedFile, tempDir):
    # extract ZIP
    extractDir = Path(tempDir) / "extracted"
    extractDir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(uploadedFile.stream, "r") as zipRef:
            zipRef.extractall(extractDir)
    except zipfile.BadZipFile:
        raise ValueError("Invalid ZIP file")

    # check structure
    missingFiles, requiredPaths = checkStructure(extractDir)
    if missingFiles:
        raise ValueError(f'Missing required files: {", ".join(missingFiles)}')

    # process files
    outputDir = Path(tempDir) / "output"
    create_directory_structure(outputDir)

    extractAudioFiles(str(extractDir), str(outputDir / "Data" / "Audio"))
    extractDataFiles(str(extractDir), str(outputDir / "Data" / "Data"))
    extractUiFiles(str(extractDir), str(outputDir / "Data" / "UI"))
    extractAssetFiles(str(extractDir), str(outputDir / "Data" / "Assets"))

    # create final ZIP
    zip_path = Path(tempDir) / "output.zip"
    create_output_zip(outputDir, zip_path)

    return str(zip_path)


def create_directory_structure(outputDir: Path):
    dirs_to_create = [
        outputDir / "Data" / "Audio",
        outputDir / "Data" / "Data",
        outputDir / "Data" / "UI",
        outputDir / "Data" / "Assets",
    ]

    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)


def create_output_zip(sourceDir: Path, zipPath: Path):
    with zipfile.ZipFile(str(zipPath), "w", zipfile.ZIP_DEFLATED) as newZip:
        for file_path in sourceDir.rglob("*"):
            if file_path.is_file():
                arcname = str(file_path.relative_to(sourceDir))
                newZip.write(str(file_path), arcname)

        # for dev
        """
        emptyDirs = []
        for emptyDir in emptyDirs:
            zipInfo = zipfile.ZipInfo(emptyDir)
            zipInfo.external_attr = 0o755 << 16
            newZip.writestr(zipInfo, b"")
        """
