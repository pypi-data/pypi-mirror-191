import json
import os
import pathlib
import re
import uuid
from typing import Optional, Dict, List, Any, Tuple

import click
from click import style
from imagination import container

from dnastack.alpha.client.ewes.client import EWesClient
from dnastack.alpha.client.ewes.models import ExtendedRunListOptions, ExtendedRunRequest, BatchRunRequest
from dnastack.alpha.client.ewes.models import LogType, Log
from dnastack.alpha.client.workflow.client import WorkflowClient
from dnastack.cli.config.context import ContextCommandHandler
from dnastack.cli.helpers.client_factory import ConfigurationBasedClientFactory
from dnastack.cli.helpers.command.decorator import command
from dnastack.cli.helpers.command.spec import ArgumentSpec
from dnastack.cli.helpers.exporter import to_json, normalize
from dnastack.cli.helpers.iterator_printer import show_iterator, OutputFormat
from dnastack.http.session import ClientError

WORKBENCH_HOSTNAME = "workbench.dnastack.com"


def _populate_workbench_endpoint():
    handler: ContextCommandHandler = container.get(ContextCommandHandler)
    handler.use(WORKBENCH_HOSTNAME, context_name="workbench", no_auth=False)


def _get_ewes_client(context_name: Optional[str] = None,
                     endpoint_id: Optional[str] = None,
                     namespace: Optional[str] = None) -> EWesClient:
    factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
    try:
        return factory.get(EWesClient, endpoint_id=endpoint_id, context_name=context_name, namespace=namespace)
    except AssertionError:
        _populate_workbench_endpoint()
        return factory.get(EWesClient, endpoint_id=endpoint_id, context_name=context_name, namespace=namespace)


def _get_workflow_client(context_name: Optional[str] = None,
                         endpoint_id: Optional[str] = None,
                         namespace: Optional[str] = None) -> WorkflowClient:
    factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
    try:
        return factory.get(WorkflowClient, endpoint_id=endpoint_id, context_name=context_name, namespace=namespace)
    except AssertionError:
        _populate_workbench_endpoint()
        return factory.get(WorkflowClient, endpoint_id=endpoint_id, context_name=context_name, namespace=namespace)


@click.group('workbench')
def alpha_workbench_command_group():
    """ Interact with Workbench """


@click.group('runs')
def runs_command_group():
    """ EWES Runs API """


@command(runs_command_group,
         'list',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='max_results',
                 arg_names=['--max-results'],
                 help='An optional flag to limit the total number of results.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page',
                 arg_names=['--page'],
                 help='An optional flag to set the offset page number. '
                      'This allows for jumping into an arbitrary page of results.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page_size',
                 arg_names=['--page-size'],
                 help='An optional flag to set the page size returned by the server.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='order',
                 arg_names=['--order'],
                 help='An optional flag to define the ordering of the results. '
                      'The value should return to the attribute name to order the results by. '
                      'By default, results are returned in descending order. '
                      'To change the direction of ordering include the "ASC" or "DESC" string after the column. '
                      'e.g.: --O "end_time", --O "end_time ASC"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='states',
                 arg_names=['--state'],
                 help='An optional flag to filter the results by their state. '
                      'This flag can be defined multiple times, with the result being any of the states.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_since',
                 arg_names=['--submitted-since'],
                 help='An optional flag to filter the results with their start_time '
                      'greater or equal to the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -f "2022-11-23", -f "2022-11-23T00:00:00.000Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_until',
                 arg_names=['--submitted-until'],
                 help='An optional flag to filter the results with their start_time '
                      'strictly less than the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -t "2022-11-23", -t "2022-11-23T23:59:59.999Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='engine',
                 arg_names=['--engine'],
                 help='An optional flag to filter the results to runs with the given engine ID',
                 as_option=True
             ),
             ArgumentSpec(
                 name='search',
                 arg_names=['--search'],
                 help='An optional flag to perform a full text search across various fields using the search value',
                 as_option=True
             ),
         ])
def list_runs(context: Optional[str],
              endpoint_id: Optional[str],
              namespace: Optional[str],
              max_results: Optional[int],
              page: Optional[int],
              page_size: Optional[int],
              order: Optional[str],
              submitted_since: Optional[str],
              submitted_until: Optional[str],
              engine: Optional[str],
              search: Optional[str],
              states: List[str] = None):
    """ List workflow runs """

    def parse_to_datetime_iso_format(date: str, start_of_day: bool = False, end_of_day: bool = False) -> str:
        if (date is not None) and ("T" not in date):
            if start_of_day:
                return f'{date}T00:00:00.000Z'
            if end_of_day:
                return f'{date}T23:59:59.999Z'
        return date

    order_direction = None
    if order:
        order_and_direction = order.split()
        if len(order_and_direction) > 1:
            order = order_and_direction[0]
            order_direction = order_and_direction[1]

    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    list_options: ExtendedRunListOptions = ExtendedRunListOptions(
        page=page,
        page_size=page_size,
        order=order,
        direction=order_direction,
        state=states,
        since=parse_to_datetime_iso_format(date=submitted_since, start_of_day=True),
        until=parse_to_datetime_iso_format(date=submitted_until, end_of_day=True),
        engineId=engine,
        search=search,
    )
    show_iterator(output_format=OutputFormat.JSON, iterator=client.list_runs(list_options, max_results))


@command(runs_command_group,
         'describe',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='status',
                 arg_names=['--status'],
                 help='Output a minimal response, only showing the status id, current state, start and stop times.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='inputs',
                 arg_names=['--inputs'],
                 help='Display only the run\'s inputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='outputs',
                 arg_names=['--outputs'],
                 help='Display only the run\'s outputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='include_tasks',
                 arg_names=['--include-tasks'],
                 help='Include the tasks in the output.',
                 as_option=True,
                 default=False
             ),
         ])
def describe_runs(context: Optional[str],
                  endpoint_id: Optional[str],
                  namespace: Optional[str],
                  runs: List[str],
                  status: Optional[bool],
                  inputs: Optional[bool],
                  outputs: Optional[bool],
                  include_tasks: Optional[bool]):
    """ Describe workflow run """
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    if status:
        described_runs = [client.get_status(run_id=run) for run in runs]
    else:
        described_runs = [client.get_run(run_id=run, include_tasks=include_tasks) for run in runs]

        if inputs:
            described_runs = [
                {
                    'run_id': described_run.run_id,
                    'inputs': described_run.request.workflow_params,
                } for described_run in described_runs
            ]
        elif outputs:
            described_runs = [
                {
                    'run_id': described_run.run_id,
                    'outputs': described_run.outputs
                } for described_run in described_runs
            ]
    click.echo(to_json(normalize(described_runs)))


@command(runs_command_group,
         'cancel',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
         ])
def cancel_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                runs: List[str] = None):
    """Cancel one or more workflow runs"""
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    result = client.cancel_runs(runs)
    click.echo(to_json(normalize(result)))


@command(runs_command_group,
         'delete',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='force',
                 arg_names=['--force'],
                 help='Force the deletion without prompting for confirmation.',
                 as_option=True,
                 default=False
             )
         ])
def delete_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                force: Optional[bool] = False,
                runs: List[str] = None):
    """Delete one or more workflow runs"""
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    if not force and not click.confirm('Do you want to proceed?'):
        return
    result = client.delete_runs(runs)
    click.echo(to_json(normalize(result)))


@command(runs_command_group,
         'logs',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='log_type',
                 arg_names=['--log-type'],
                 help='Print only stderr or stdout to the current console.',
                 as_option=True,
                 default=LogType.stdout
             ),
             ArgumentSpec(
                 name='task_name',
                 arg_names=['--task-name'],
                 help='Retrieve logs associated with the given task in the run.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='max_bytes',
                 arg_names=['--max-bytes'],
                 help='Limit number of bytes to retrieve from the log stream.',
                 as_option=True,
             ),
             ArgumentSpec(
                 name='output',
                 arg_names=['--output'],
                 help="Save the output to the defined path, if it does not exist",
                 as_option=True
             )
         ])
def get_run_logs(context: Optional[str],
                 endpoint_id: Optional[str],
                 namespace: Optional[str],
                 run_id_or_log_url: str,
                 output: Optional[pathlib.Path],
                 log_type: Optional[LogType] = LogType.stdout,
                 task_name: Optional[str] = None,
                 max_bytes: Optional[int] = None):
    """Get logs of a single workflow run"""

    def get_writer(output_path: Optional[pathlib.Path]):
        if not output_path:
            return click.echo
        if os.path.exists(output_path):
            click.echo(style(f"{output_path} already exists, command will not overwrite", fg="red"), color=True)
            exit(0)

        output_file = open(output_path, "w")

        def write(binary_content: bytes):
            output_file.write(binary_content.decode("utf-8"))

        return write

    def is_valid_uuid(val: str):
        try:
            uuid.UUID(val, version=4)
            return True
        except ValueError:
            return False

    def print_logs_by_url(log_url: str, writer):
        for logs_chunk in client.stream_run_logs(log_url=log_url, max_bytes=max_bytes):
            if logs_chunk:
                writer(logs_chunk)

    def print_logs(log: Log, writer):
        if log:
            print_logs_by_url(log.stderr if log_type == LogType.stderr else log.stdout, writer=writer)

    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    output_writer = get_writer(output)

    if not is_valid_uuid(run_id_or_log_url):
        print_logs_by_url(log_url=run_id_or_log_url, writer=output_writer)
        return

    described_run = client.get_run(run_id=run_id_or_log_url, include_tasks=True)
    if not task_name:
        try:
            print_logs(log=described_run.run_log, writer=output_writer)
        except ClientError as e:
            if e.response.status_code == 404:
                return
    else:
        if described_run.task_logs:
            task = next(
                (run_task for run_task in described_run.task_logs if
                 run_task.name.lower() == task_name.strip().lower()),
                None
            )
            if task:
                print_logs(log=task, writer=output_writer)


@command(runs_command_group,
         'submit',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow_url',
                 arg_names=['--url'],
                 help='The URL to the workflow file (*.wdl). Only urls from workflow-service are '
                      'currently supported.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='engine_id',
                 arg_names=['--engine'],
                 help='Use the given engine id for execution of runs. If this value is not defined then it is assumed '
                      'that the default engine will be used.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='default_workflow_engine_parameters',
                 arg_names=['--engine-params'],
                 help='Set the global engine parameters for all runs that are to be submitted. '
                      'Engine params can be specified as a KV pair, inlined JSON, or as a json file.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='default_workflow_params',
                 arg_names=['--default-params'],
                 help='Specify the global default inputs as a json file or as inlined json to use when submitting '
                      'multiple runs. Default inputs have the lowest level of precedence and will be overridden '
                      'by any run input or override.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow_params',
                 arg_names=['--workflow-params'],
                 help='Optional flag to specify the workflow params for a given run, as key value pairs, '
                      'a json file or inlined json. Additionally, the user may specify a directory which contains a '
                      'list of params in json format. Each file will result in a separate run. '
                      'This field may be repeated, with each repetition specifying a separate run request that '
                      'will be submitted as part of a batch.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='tags',
                 arg_names=['--tags'],
                 help='Set the global tags for all runs that are to be submitted. '
                      'Tags can be specified as a key value pair, inlined json, or as a file.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='run_request',
                 arg_names=['--run-request'],
                 help='Supply a single run configuration in the form of a JSON run request. Values can be defined '
                      'through key value inputs, a json file or inlined json. This approach allows the user to have '
                      'more control over not just the inputs but the engine params and tags that are submitted as part '
                      'of a single run. A single “request” flag will result in a single run '
                      '(similar to the –inputs flag). The value may be repeated multiple times with each repetition '
                      'corresponding to a unique run.',
                 as_option=True
             )
         ])
def submit_batch(context: Optional[str],
                 endpoint_id: Optional[str],
                 namespace: Optional[str],
                 workflow_url: str,
                 engine_id: Optional[str],
                 default_workflow_engine_parameters: Optional[str],
                 default_workflow_params: Optional[str],
                 tags: Optional[str],
                 workflow_params: List[str] = None,
                 runs_request: Optional[ExtendedRunRequest] = None):
    """ Submit a workflow batch """

    def is_json_string(string: str) -> bool:
        try:
            json.loads(string)
        except ValueError:
            return False
        return True

    def parse_input_param(param: str) -> Dict[str, Any]:
        if not param:
            return {}

        if is_json_string(param):
            return json.loads(param)

        if param.endswith(".json"):
            with open(param) as param_file:
                return json.loads(param_file.read())

    def get_workflow_id_and_version_id_from_url(url: str) -> Tuple[str, str]:
        pattern = r"/.*/(?P<namespace>.*)/workflows/(?P<workflowId>.*)/versions/(?P<versionId>.*)/"
        result = re.search(pattern, url)
        return result.group("workflowId"), result.group("versionId")

    ewes_client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    workflow_client = _get_workflow_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    workflow_and_version_ids = get_workflow_id_and_version_id_from_url(workflow_url)
    described_workflow = workflow_client.get_json_schema(workflow_and_version_ids[0], workflow_and_version_ids[1])

    batch_request: BatchRunRequest = BatchRunRequest(
        workflow_url=workflow_url,
        workflow_type="WDL",
        workflow_type_version=described_workflow.wdl_version,
        engine_id=engine_id,
        default_workflow_engine_parameters=parse_input_param(default_workflow_engine_parameters),
        default_workflow_params=parse_input_param(default_workflow_params),
        default_tags=parse_input_param(tags),
        run_requests=[runs_request] if runs_request else []
    )

    for workflow_param in workflow_params:
        if is_json_string(workflow_param) or workflow_param.endswith(".json"):
            run_request = ExtendedRunRequest(
                workflow_params=parse_input_param(workflow_param)
            )
            batch_request.run_requests.append(run_request)

    minimal_batch = ewes_client.submit_batch(batch_request)

    click.echo(to_json(normalize(minimal_batch)))


alpha_workbench_command_group.add_command(runs_command_group)
