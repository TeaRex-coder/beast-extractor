import subprocess
from pathlib import Path


def extractUiFiles(extractDir, ouputUiDir):
    sourceBase = Path(extractDir) / "Data" / "StreamingAssets" / "UI"
    if not sourceBase.is_dir():
        raise ValueError("Data/StreamingAssets/UI not in uploaded game")

    # go through EVERY protobw
    sourcePath = Path(sourceBase)
    outputBase = Path(ouputUiDir)

    for inputPath in sourcePath.rglob("*.protobw"):
        outputPath = outputBase / inputPath.relative_to(sourcePath).with_suffix(
            ".proto"
        )
        outputPath.parent.mkdir(parents=True, exist_ok=True)
        decompileProtobw(inputPath, outputPath)


def decompileProtobw(inputPath, outputPath):
    try:
        with open(inputPath, "rb") as infile:
            result = subprocess.run(
                ["protoc", "--decode_raw"],
                stdin=infile,
                capture_output=True,
                check=True,
            )

        Path(outputPath).write_text(
            result.stdout.decode("utf-8", errors="replace"), encoding="utf-8"
        )

    except subprocess.CalledProcessError as e:
        errorMsg = f"failed to decompile {inputPath}: {e.stderr.decode()}"
        raise RuntimeError(errorMsg) from e
