import os
import shlex
from pathlib import Path
from typing import List

import yaml

from . import exceptions, file_contents, helpers, steps
from .configs import Config


class Runtime:
    def __init__(self, config: Config, operation_id: str, **kwargs):
        self.config = config
        self.operation_id = operation_id
        self.memory = kwargs.get('memory')
        self.cpu = kwargs.get('cpu')

    @property
    def command_build(self) -> str:
        return f"gcloud builds submit --pack image=gcr.io/{self.config.gcp_project}/{self.operation_id} --project={self.config.gcp_project}"

    @property
    def command_create(self) -> str:
        name = self.operation_id.replace('_', '-')
        return " ".join([
            f"gcloud beta run jobs create {name}"
            f" --image='gcr.io/{self.config.gcp_project}/{self.operation_id}' --tasks 1 --set-env-vars ENV='production'"
            f" --max-retries 3 --region={self.config.gcp_region} --project={self.config.gcp_project}",
            "" if self.memory is None else f"--memory={self.memory}",
            "" if self.cpu is None else f"--cpu={self.cpu}",
        ])

    @property
    def command_delete(self) -> str:
        name = self.operation_id.replace('_', '-')
        return f"gcloud beta run jobs delete {name} --region='{self.config.gcp_region}' --project='{self.config.gcp_project}'"

    @property
    def command_run(self) -> str:
        name = self.operation_id.replace('_', '-')
        return f"gcloud beta run jobs execute {name} --region='{self.config.gcp_region}' --project='{self.config.gcp_project}'"


class Job:
    def __init__(self, operation_id: str, **kwargs):
        self.operation_id = operation_id

    def runtime(self, config: Config) -> Runtime:
        path = f'{config.base_dir}/jobs/config.yaml'

        if Path(path).exists():
            with open(path) as f:
                runtime_config = yaml.safe_load(f.read())
        else:
            runtime_config = {}

        return Runtime(config, self.operation_id, **runtime_config)


def job_list(config: Config) -> List[Job]:
    jobs_path = f'{config.base_dir}/jobs'
    if not Path(jobs_path).exists():
        Path(jobs_path).mkdir(parents=True, exist_ok=True)
    return [
        Job(x) for x in os.listdir(f'{config.base_dir}/jobs')
    ]


def job_name_clean(value: str) -> str:
    return value.replace(' ', '_').lower()


def cli_main(args, config: Config):
    try:
        config.load()
    except exceptions.ConfigInvalidVersion:
        print(
            helpers.bcolors.FAIL
            + 'Config file is not compatible with this version. Please run `init` again.'
            + helpers.bcolors.ENDC
        )
        return 1
    if args.action == 'init':
        manager = steps.Manager(config, [
            steps.StepCommand(
                shlex.split(
                    f'gcloud services enable run.googleapis.com --project="{config.gcp_project}"'
                )
            ),
            steps.StepCommand(
                shlex.split(
                    f'gcloud services enable cloudscheduler.googleapis.com --project="{config.gcp_project}"'
                )
            ),
        ], simulate=args.simulate)
        rc = manager.run()
        if rc != 0:
            return rc
        print(helpers.bcolors.OKGREEN + 'Init API-Gateway success' + helpers.bcolors.ENDC)
        return 0
    if args.action == 'list':
        jobs = list(job_list(config))
        for job in jobs:
            print(job.operation_id)
        return 0
    elif args.action == 'create':
        job_name = job_name_clean(args.name)
        jobs = [x for x in job_list(config) if x.operation_id == job_name]
        if len(jobs) > 0:
            print(
                helpers.bcolors.FAIL
                + f'Job {args.endpoint} already exists'
                + helpers.bcolors.ENDC
            )
            return 1

        commands = [
            steps.StepCreatDir(f'{config.base_dir}/jobs/{job_name}'),
            steps.StepCreateFile(
                f'{config.base_dir}/jobs/{job_name}/main.py',
                file_contents.job_main(),
            ),
            steps.StepCreateFile(
                f'{config.base_dir}/jobs/{job_name}/Procfile',
                file_contents.job_procfile(),
            ),
            steps.StepCreateFile(
                f'{config.base_dir}/jobs/{job_name}/requirements.txt',
                "",
            ),
        ]
        manager = steps.Manager(config, commands, simulate=args.simulate)
        rc = manager.run()
        if rc != 0:
            return rc
        return 0
    elif args.action == 'describe':
        job_name = job_name_clean(args.name)
        jobs = [x for x in job_list(config) if x.operation_id == job_name]
        if len(jobs) == 0:
            print(
                helpers.bcolors.FAIL
                + f'Job {job_name} not found'
                + helpers.bcolors.ENDC
            )
            return 1
        print('Operation ID:', jobs[0].operation_id)
        return 0
    elif args.action == 'deploy':
        job_name = job_name_clean(args.name)
        jobs = [x for x in job_list(config) if x.operation_id == job_name]
        if len(jobs) == 0:
            print(
                helpers.bcolors.FAIL
                + f'Job {job_name} not found'
                + helpers.bcolors.ENDC
            )
            return 1

        print('# Deploy')
        job = jobs[0]
        runtime = job.runtime(config)
        commands = [
            # delete job if exists?
            steps.StepCommand(
                shlex.split(runtime.command_build),
                work_dir=f'{config.base_dir}/jobs/{job_name}',
            ),
            steps.StepCommand(
                shlex.split(runtime.command_delete),
                work_dir=f'{config.base_dir}/jobs/{job_name}',
                can_fail=True,
            ),
            steps.StepCommand(
                shlex.split(runtime.command_create),
                work_dir=f'{config.base_dir}/jobs/{job_name}',
            ),
        ]
        manager = steps.Manager(config, commands, simulate=args.simulate)
        rc = manager.run()
        if rc != 0:
            return rc

        return 0
    elif args.action == 'run':
        job_name = job_name_clean(args.name)
        jobs = [x for x in job_list(config) if x.operation_id == job_name]
        if len(jobs) == 0:
            print(
                helpers.bcolors.FAIL
                + f'Job {job_name} not found'
                + helpers.bcolors.ENDC
            )
            return 1

        print('# Deploy')
        job = jobs[0]
        runtime = job.runtime(config)
        commands = [
            steps.StepCommand(
                shlex.split(runtime.command_run),
                work_dir=f'{config.base_dir}/jobs/{job_name}',
            ),
        ]
        manager = steps.Manager(config, commands, simulate=args.simulate)
        rc = manager.run()
        if rc != 0:
            return rc

        return 0
