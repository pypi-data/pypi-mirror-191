import nibabel as nb
from medimages4tests.mri.neuro.t1w import get_image


def test_openneuro_retrieve():

    nifti_fpath = get_image()

    nifti = nb.load(nifti_fpath)

    assert nifti.shape == (204, 256, 256)
