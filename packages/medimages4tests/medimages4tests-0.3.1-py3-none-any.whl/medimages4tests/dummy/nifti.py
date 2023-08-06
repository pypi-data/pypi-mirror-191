import os
import tempfile
from pathlib import Path
import gzip
import shutil
import numpy as np
import nibabel as nb


def get_image(
    out_file: Path = None,
    data: np.ndarray = None,
    vox_sizes=(1.0, 1.0, 1.0),
    qform=(1, 2, 3, 1),
    compressed=None,
) -> Path:
    """Create a random Nifti file to satisfy BIDS parsers

    Parameters
    ----------
    out_file : Path


    """
    if out_file is None:
        out_file = Path(tempfile.mkdtemp()) / "sample.nii"
    out_file = Path(out_file)

    suffix = "".join(out_file.suffixes) if out_file.suffixes else ""
    out_stem = out_file.parent / out_file.name[:-len(suffix)]
    if not suffix:
        if compressed is None:
            raise RuntimeError(
                f"Must either specify the suffix of the 'out_file' ('{out_file}') or the "
                "compression type ('compressed' option)"
            )
        elif compressed:
            suffix = ".nii.gz"
        else:
            suffix = ".nii"
    elif compressed is None:
        compressed = suffix == ".nii.gz"
    elif suffix == ".nii":
        if compressed:
            raise RuntimeError(
                f"Suffix '{suffix}' doesn't match the compressed being True"
            )
    elif suffix == ".nii.gz":
        if not compressed:
            raise RuntimeError(
                f"Suffix '{suffix}' doesn't match the compressed being True"
            )
    else:
        raise RuntimeError(
            f"Unrecognised suffix for nifti file, '{suffix}'"
        )

    if data is None:
        data = np.random.randint(0, 1, size=[10, 10, 10])

    uncompressed = out_stem.with_suffix('.nii')

    hdr = nb.Nifti1Header()
    hdr.set_data_shape(data.shape)
    hdr.set_zooms(vox_sizes)  # set voxel size
    hdr.set_xyzt_units(2)  # millimeters
    hdr.set_qform(np.diag(qform))
    nb.save(
        nb.Nifti1Image(
            data,
            hdr.get_best_affine(),
            header=hdr,
        ),
        uncompressed,
    )

    if compressed:
        out_path = out_stem.with_suffix('.nii.gz')
        with open(uncompressed, 'rb') as f_in:
            with gzip.open(out_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.unlink(uncompressed)
    else:
        out_path = uncompressed

    return out_path
