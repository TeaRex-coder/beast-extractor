import pathlib
import shutil
import subprocess
import tempfile


def extractAudioFiles(extractDir, outputAudioDir):
    extractDir = pathlib.Path(extractDir)
    outputAudioDir = pathlib.Path(outputAudioDir)

    with tempfile.TemporaryDirectory() as tempDir:
        processDir = pathlib.Path(tempDir)

        # setup wwiser
        wwiserSource = pathlib.Path(__file__).resolve().parent / "wwiser.pyz"
        if not wwiserSource.exists():
            raise RuntimeError("wwiser.pyz not found")

        shutil.copy(wwiserSource, processDir)

        bnkPath = (
            extractDir
            / "Data"
            / "StreamingAssets"
            / "Audio"
            / "GeneratedSoundBanks"
            / "Mac"
            / "Soundbank_BEAST.bnk"
        )
        shutil.copy(bnkPath, processDir)

        # retrieve wav files
        txtpGenerator(processDir)
        txtpToWav(processDir, outputAudioDir)


def txtpGenerator(processDir: pathlib.Path):
    cmd = ["python", "wwiser.pyz", "-g", "Soundbank_BEAST.bnk"]
    result = subprocess.run(
        cmd,
        cwd=processDir,
        check=True,
        capture_output=True,
        text=True,
    )

    txtpDir = processDir / "txtp"
    if not txtpDir.exists():
        raise RuntimeError("TXTPs not generated")

    return txtpDir


def txtpToWav(processDir: pathlib.Path, outputDir: pathlib.Path):
    txtpDir = processDir / "txtp"
    txtpFiles = [f for f in txtpDir.iterdir() if f.suffix.lower() == ".txtp"]

    if not txtpFiles:
        raise RuntimeError("TXTPs not found")

    outputDir.mkdir(parents=True, exist_ok=True)

    for txtpFile in txtpFiles:
        wavFilename = f"{txtpFile.stem}.wav"
        wavPath = outputDir / wavFilename

        cmd = [
            "vgmstream-cli",
            "-o",
            str(wavPath),
            str(txtpFile),
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
