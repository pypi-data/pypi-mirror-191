from datetime import datetime
import time


class BatchLogger:
    def __init__(self, cloudwatch_client, batch_client, sf_client):
        self._cloudwatch_client = cloudwatch_client
        self._batch_client = batch_client
        self._sf_client = sf_client
        self._log_group_name = '/aws/batch/job'

    def print_step_func_status(self, execution_arn):
        spin = ['.', '..', '...']
        spinner = 0

        while True:
            time.sleep(5)
            sf_response = self._sf_client.describe_execution(executionArn=execution_arn)
            status = sf_response['status']
            #print(status)
            if status == 'SUCCEEDED':
                print(f"{'=' * 80}")
                print(f'End of the execution: {status}')
                break
            elif status in ['FAILED', 'TIMED_OUT', 'ABORTED']:
                print(f"{'=' * 80}")
                print(f'End of the execution: {status}')
                break
            elif status == 'RUNNING':
                print(f'Execution RUNNING {spin[spinner]}')
                spinner = (spinner + 1) % len(spin)
            else:
                print(f'Unexpected status of the execution: {status}')
                break

        return status

    def print_status(self, job_name, job_id):
        spin = ['.', '..', '...']
        spinner = 0
        start_time = 0
        running = False

        while True:
            time.sleep(5)
            describe_jobs_response = self._batch_client.describe_jobs(jobs=[job_id])
            status = describe_jobs_response['jobs'][0]['status']
            print(status)
            if status == 'SUCCEEDED':
                print(f"{'=' * 80}")
                print(f'Job [{job_id}] {status}')
                break
            elif status == 'FAILED':
                print(f"{'=' * 80}")
                print(f'Job [{job_id}] {status}')
                break
            elif status == 'RUNNING':
                log_stream_name = self._get_log_stream(self._log_group_name, job_name, job_id)
                if not running and log_stream_name:
                    running = True
                    print(f'\rJob [{job_name} - {job_id}] is RUNNING.')
                    print(f"Output [{log_stream_name}]:\n {'=' * 80}")
                if log_stream_name:
                    start_time = self.print_logs(self._log_group_name, log_stream_name, start_time) + 1
            else:
                print(f'\rJob [{job_name} - {job_id}] is {status}  {spin[spinner]}')
                spinner = (spinner + 1) % len(spin)

        return status

    def print_logs(self, log_group_name, log_stream_name, start_time):
        kwargs = {'logGroupName': log_group_name,
                  'logStreamName': log_stream_name,
                  'startTime': start_time,
                  'startFromHead': True}

        last_timestamp = 0
        while True:
            log_events = self._cloudwatch_client.get_log_events(**kwargs)

            for event in log_events['events']:
                last_timestamp = event['timestamp']
                timestamp = datetime.utcfromtimestamp(last_timestamp / 1000.0).isoformat()
                print('[%s] %s' % ((timestamp + ".000")[:23] + 'Z', event['message']))

            next_token = log_events['nextForwardToken']
            if next_token and kwargs.get('nextToken') != next_token:
                kwargs['nextToken'] = next_token
            else:
                break
        return last_timestamp

    def _get_log_stream(self, log_group_name, job_name, job_id):
        response = self._cloudwatch_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=job_name + '/' + job_id
        )
        log_streams = response['logStreams']
        if not log_streams:
            return ''
        else:
            return log_streams[0]['logStreamName']
