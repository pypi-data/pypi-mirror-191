import gzip
import shutil
import nibabel as nb
import numpy as np
from medimages4tests.dummy.nifti import get_image


def test_nifti(work_dir):

    nifti_fpath = get_image(work_dir / "sample.nii")

    nifti = nb.load(nifti_fpath)

    assert np.array_equal(nifti.header["dim"][:4], [3, 10, 10, 10])


def test_nifti_compressed(work_dir):

    gz_fpath = get_image(work_dir / "sample.nii.gz", compressed=True)
    uncompressed_fpath = work_dir / "nifti.nii"

    with gzip.open(gz_fpath, 'rb') as f_in:
        with open(uncompressed_fpath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    nifti = nb.load(uncompressed_fpath)

    assert np.array_equal(nifti.header["dim"][:4], [3, 10, 10, 10])
