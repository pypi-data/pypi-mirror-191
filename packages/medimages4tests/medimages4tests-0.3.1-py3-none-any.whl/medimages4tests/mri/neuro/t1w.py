from medimages4tests import base_cache_dir
from medimages4tests.utils import retrieve_from_openneuro, OpenneuroSpec


cache_dir = base_cache_dir / "mri" / "neuro" / "t1w"


SAMPLES = {
    "ds004130-ON01016": OpenneuroSpec(
        dataset="ds004130",
        tag="1.0.0",
        path="sub-ON01016/anat/sub-ON01016_acq-fspgr_run-01_T1w",
    )
}


def get_image(sample="ds004130-ON01016"):
    return retrieve_from_openneuro(SAMPLES[sample], cache_dir / sample)
