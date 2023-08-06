import json

from typing import List, Union
from beam.base import AbstractDataLoader
from beam.configs.outputs import OutputManager
from beam.configs.trigger import TriggerManager
from beam.configs.mount import MountManager
from beam.serializer import AppSpecConfiguration
from beam.types import PythonVersion, GpuType
from beam.utils.parse import compose_cpu, compose_memory, load_requirements_file


class App(AbstractDataLoader):
    def __init__(
        self,
        *,
        name: str,
        cpu: Union[str, int],
        memory: str,
        gpu: str = GpuType.NoGPU,
        python_version: PythonVersion = PythonVersion.Python38,
        python_packages: Union[str, List[str]] = [],
        workspace: str = "./"
    ) -> None:
        """
        Keyword Arguments:
            name: the unique identifier for your app
            cpu: total number of cpu cores available to your app
            memory: total amount of memory available to your app
                - in the format [Number][Mi|Gi], for example 12Gi or 250Mi
            (Optional) gpu: type of gpu device available to your app (e.g. any, T4, A10G). Defaults to "", which means no GPU will be available
            (Optional) python_version: version of python to run your app code
            (Optional) python_packages: list of python packages you want to install, or the path to a requirements.txt file
                - e.g. "torch" or "torch==1.12.0"
            (Optional) workspace: directory to continously sync to your remote container during development
        """

        if isinstance(python_packages, str):
            python_packages = load_requirements_file(python_packages)

        self.Spec = AppSpecConfiguration(
            name=name,
            cpu=compose_cpu(cpu),
            gpu=gpu,
            memory=compose_memory(memory),
            python_version=python_version,
            python_packages=python_packages,
            workspace=workspace,
        )

        self.Trigger = TriggerManager()
        self.Output = OutputManager()
        self.Mount = MountManager()

    def dumps(self):
        return json.dumps(
            {
                "app": self.Spec.validate_and_dump(),
                "triggers": self.Trigger.dumps(),
                "outputs": self.Output.dumps(),
                "mounts": self.Mount.dumps(),
                "autoscaling": self.Trigger.AutoScaling.dumps(),
            }
        )

    @staticmethod
    def from_config(config: Union[dict, str]) -> "App":
        if isinstance(config, str):
            config = json.loads(config)

        app_config = config.get("app")
        triggers = config.get("triggers")
        outputs = config.get("outputs")
        mounts = config.get("mounts")
        autoscaling = config.get("autoscaling")

        app = App(**app_config)
        app.Trigger.from_config(triggers)
        app.Output.from_config(outputs)
        app.Mount.from_config(mounts)
        app.Trigger.AutoScaling.from_config(autoscaling)

        return app
