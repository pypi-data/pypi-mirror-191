# NOTE: Later all of these can be under a `models` or some other module
# I am not entirely sure about the structure of `lib` module yet
# This can go through another round of refactoring
from servicefoundry.v2.lib.deployable_patched_models import (
    Application,
    Job,
    ModelDeployment,
    Service,
)
from servicefoundry.v2.lib.patched_models import (
    GPU,
    Autoscaling,
    BasicAuthCreds,
    Build,
    CPUUtilizationMetric,
    CUDAVersion,
    DockerFileBuild,
    FileMount,
    GitSource,
    GPUType,
    HealthProbe,
    HttpProbe,
    HuggingfaceModelHub,
    Image,
    LocalSource,
    Manual,
    Param,
    Port,
    PythonBuild,
    RemoteSource,
    Resources,
    RPSMetric,
    Schedule,
    TruefoundryModelRegistry,
)
