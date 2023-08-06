from tempfile import mkdtemp
import shutil
from pathlib import Path
import openneuro
import attrs


@attrs.define
class OpenneuroSpec:

    dataset: str
    tag: str
    path: Path


def retrieve_from_openneuro(
    sample, cache_path, suffixes=(".nii.gz", ".json"), force_download=False
):
    if not cache_path.parent.exists():
        cache_path.parent.mkdir(parents=True)
    out_path = cache_path.with_suffix(suffixes[0])
    if not out_path.exists() or force_download:
        tmpdir = Path(mkdtemp())
        openneuro.download(
            dataset=sample.dataset,
            tag=sample.tag,
            target_dir=tmpdir,
            include=[sample.path],
        )
        for ext in suffixes:
            shutil.copyfile(
                (tmpdir / sample.path).with_suffix(ext), cache_path.with_suffix(ext)
            )
    return out_path
