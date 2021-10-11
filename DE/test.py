
def load_to_hdfs(cls,file_local_path,file_hdfs_path,logger):
        # move file to hdfs.
        load_to_hadoop_script = "hdfs dfs -moveFromLocal {0} {1}".format('/home/ubuntu/DE/coronaStage_'+nowtime, '/data/corona')
        logger.info("SPOT.Utils: Loading file to hdfs: {0}".format(load_to_hadoop_script))
        subprocess.call(load_to_hadoop_script,shell=True)




''''
# HDFS와 연결
def run_cmd(args_list):
    """
    run linux commands
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err

def move_cmd():
    # HDFS에 적재
    (ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/coronaStage_' + nowtime, '/data/corona'])
'''


####################
# Dag Task Setting
####################
coronaStage = PythonOperator(
	task_id = 'coronaStage',
	#python_callable param points to the function you want to run 
	python_callable = stage_call,
	#dag param points to the DAG that this task is a part of
	dag = dag
    )

coronaStage_move = PythonOperator(
	task_id = 'coronaStage_move',
	python_callable = load_to_hdfs,
	dag = dag
    )

#Assign the order of the tasks in our DAG
coronaStage >> coronaStage_move

##############
#DAG Setting
##############
from airflow import DAG
from airflow.operators import PythonOperator
import json
from textwrap import dedent
from datetime import datetime, timedelta

# from airflow.operators.bash import BashOperator
# from airflow.operators.dummy import DummyOperator
# from airflow.operators.python import PythonOperator

# [START instantiate_dag]
# @dag(schedule_interval=None, start_date=datetime(2021, 1, 1), catchup=False, tags=['example'])
dag = DAG(
        dag_id = "coronaStage_test2",
        start_date = datetime(2021,10,2),
        schedule_interval = '@once'
    )


def tutorial_taskflow_api_etl():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    # [END instantiate_dag]

    # [START extract]
    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
       
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict
        """
        display = Display(visible=0, size=(1024, 768)) 
        display.start()
        
        path = '/home/ubuntu/chromedriver' 
        driver = webdriver.Chrome(path)

        nowtime = datetime.today().strftime("%Y-%m-%d")
        driver.get('http://ncov.mohw.go.kr/regSocdisBoardView.do')
        info_df = pd.DataFrame(columns=("Area","Stage","Description"))
        idx = 0



    # [END extract]

    # [START transform]
   # @task(multiple_outputs=True)
    def transform():
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}
        """

        for i in range(1,18):
            location = driver.find_element_by_xpath(f'//*[@id="main_maplayout"]/button[{i}]')
            location.click()

            area = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h3').text
            stage =  driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h4').text
            description = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/p').text

            # 확인용
            area_info = [area,stage,description]
            info_df.loc[idx] = area_info
            idx += 1

            driver.implicitly_wait(3)

        return info_df.to_parquet('coronaStage_'+ nowtime)
    
    if __name__=='__main__':
        stage_call()


    # [END transform]


    def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err   


    # [START load]
    #def load(total_order_value: float):
    def movce_cmd(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        

        print(f"Total order value is: {total_order_value:.2f}")
        """
        (ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/coronaAPI_' + nowtime, '/data/corona'])




    # [END load]
    '''
    # [START main_flow]
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])
    # [END main_flow]
    '''


####################
# Dag Task Setting
####################

coronaStage = PythonOperator(
        task_id = 'coronaStage_',
        python_callable = stage_call,       
        #provide_context=True,
        dag = dag
        )


coronaStage_move = PythonOperator(
	task_id = 'coronaStage_move',
	python_callable = cmd_move,
	dag = dag
    )

airflow clear -t coronaStage --downstream coronaStage_test

#Assign the order of the tasks in our DAG
coronaStage >> coronaStage_move 
# [START dag_invocation]
tutorial_etl_dag = tutorial_taskflow_api_etl()
# [END dag_invocation]

# [END tutorial]



'''
def run_this_func(dag_run):
    """
    Print the payload "message" passed to the DagRun conf attribute.
    :param dag_run: The DagRun object
    :type dag_run: DagRun
    """
    print(f"Remotely received value of {dag_run.conf['message']} for key=message")
'''

def stage_call():
    driver.get('http://ncov.mohw.go.kr/regSocdisBoardView.do')
    info_df = pd.DataFrame(columns=("Area","Stage","Description"))
    idx = 0

    for i in range(1,18):
        location = driver.find_element_by_xpath(f'//*[@id="main_maplayout"]/button[{i}]')
        location.click()

        area = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h3').text
        stage =  driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h4').text
        description = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/p').text

        # 확인용
        area_info = [area,stage,description]
        info_df.loc[idx] = area_info
        idx += 1

        driver.implicitly_wait(3)

    info_df.to_parquet('coronaStage_'+ nowtime)

if __name__=='__main__':
    stage_call()



def run_cmd(args_list):
    """
    run linux commands
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err
    print(f"Remotely received value of {args_list.conf['message']} for key=message")

def move_cmd():
    (ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/coronaStage_' + nowtime, '/data/corona'])

    
with DAG(
    dag_id="coronaStage_test2",
    start_date=datetime(2021, 10, 3),
    catchup=False,
    schedule_interval='@once',
    tags=['example'],
) as dag:
    coronaStage_ = PythonOperator(
        task_id="coronaStage_", 
        python_callable=stage_call)

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "Here is the message: $Interacting with Hadoop HDFS using Python codes"',
        env={'message': '{{ move_cmd.conf["message"] if move_cmd else "move_cmd" }}'},
    )


    coronaStage_ >> bash_task






'''
dag = DAG(
        dag_id = "coronaStage_test",
        start_date = datetime(2021,10,2),
        schedule_interval = #'@once'
    )

#############
#Python code
#############


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd 
import numpy as np
import json

import subprocess

display = Display(visible=0, size=(1024, 768)) 
display.start()
 
path = '/home/ubuntu/chromedriver' 
driver = webdriver.Chrome(path)

nowtime = datetime.today().strftime("%Y-%m-%d")

def stage_call():
    driver.get('http://ncov.mohw.go.kr/regSocdisBoardView.do')
    info_df = pd.DataFrame(columns=("Area","Stage","Description"))
    idx = 0

    for i in range(1,18):
        location = driver.find_element_by_xpath(f'//*[@id="main_maplayout"]/button[{i}]')
        location.click()

        area = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h3').text
        stage =  driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h4').text
        description = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/p').text

        # 확인용
        area_info = [area,stage,description]
        info_df.loc[idx] = area_info
        idx += 1

        driver.implicitly_wait(3)

    info_df.to_parquet('coronaStage_'+ nowtime)

# if __name__=='__main__':
#     stage_call()


# HDFS와 연결
def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err

def cmd_move():
    (ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/coronaAPI_' + nowtime, '/data/corona'])

####################
# Dag Task Setting
####################

coronaStage = PythonOperator(
        task_id = 'coronaStage_',
        python_callable = stage_call,       
        #provide_context=True,
        dag = dag
        )


coronaStage_move = PythonOperator(
	task_id = 'coronaStage_move',
	python_callable = cmd_move,
	dag = dag
    )



#Assign the order of the tasks in our DAG
coronaStage >> coronaStage_move 
'''
'''

"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='coronaStage_test',
    schedule_interval=#'@once',
    start_date=datetime(2021, 10, 2),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:
    run_this_last = DummyOperator(
        task_id='run_this_last',
    )

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id='run_after_loop',
        bash_command='echo 1',
    )
    # [END howto_operator_bash]

    run_this >> run_this_last

# if __name__ == "__main__":
#     dag.cli()


import json
from datetime import datetime

from airflow.decorators import dag, task

# [END import_module]


# [START instantiate_dag]
@dag(schedule_interval=None, start_date=datetime(2021, 1, 1), catchup=False, tags=['example'])

def tutorial_taskflow_api_etl():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    # [END instantiate_dag]

    # [START extract]
    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
       
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict
        """
        display = Display(visible=0, size=(1024, 768)) 
        display.start()
        
        path = '/home/ubuntu/chromedriver' 
        driver = webdriver.Chrome(path)

        nowtime = datetime.today().strftime("%Y-%m-%d")



    # [END extract]

    # [START transform]
    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}
        """

        for i in range(1,18):
            location = driver.find_element_by_xpath(f'//*[@id="main_maplayout"]/button[{i}]')
            location.click()

            area = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h3').text
            stage =  driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h4').text
            description = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/p').text

            # 확인용
            area_info = [area,stage,description]
            info_df.loc[idx] = area_info
            idx += 1

            driver.implicitly_wait(3)

        return info_df.to_parquet('coronaStage_'+ nowtime)


    # [END transform]


    def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err   


    # [START load]
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        

        print(f"Total order value is: {total_order_value:.2f}")
        """
        (ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/coronaAPI_' + nowtime, '/data/corona'])




    # [END load]

    # [START main_flow]
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])
    # [END main_flow]


# [START dag_invocation]
tutorial_etl_dag = tutorial_taskflow_api_etl()
# [END dag_invocation]

# [END tutorial]



# [START tutorial]
# [START import_module]
import json
from datetime import datetime
from textwrap import dedent



# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'tutorial_etl_dag',
    default_args=default_args,
    description='ETL DAG tutorial',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs['ti']
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        ti.xcom_push('order_data', data_string)

    # [END extract_function]

    # [START transform_function]
    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value', total_value_json_string)

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
        total_order_value = json.loads(total_value_string)

        print(total_order_value)

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> transform_task >> load_task

"""
Example usage of the TriggerDagRunOperator. This example holds 2 DAGs:
1. 1st DAG (example_trigger_controller_dag) holds a TriggerDagRunOperator, which will trigger the 2nd DAG
2. 2nd DAG (example_trigger_target_dag) which will be triggered by the TriggerDagRunOperator in the 1st DAG
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def run_this_func(dag_run):
    """
    Print the payload "message" passed to the DagRun conf attribute.
    :param dag_run: The DagRun object
    :type dag_run: DagRun
    """
    print(f"Remotely received value of {dag_run.conf['message']} for key=message")


with DAG(
    dag_id="example_trigger_target_dag",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval=None,
    tags=['example'],
) as dag:
    run_this = PythonOperator(task_id="run_this", python_callable=run_this_func)

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "Here is the message: $message"',
        env={'message': '{{ dag_run.conf["message"] if dag_run else "" }}'},
    )


"""Example DAG demonstrating the usage of the PythonOperator."""
import time
from datetime import datetime
from pprint import pprint

from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator

with DAG(
    dag_id='example_python_operator',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    # [START howto_operator_python]
    def print_context(ds, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = PythonOperator(
        task_id='print_the_context',
        python_callable=print_context,
    )
    # [END howto_operator_python]

    # [START howto_operator_python_kwargs]
    def my_sleeping_function(random_base):
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

    # Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively
    for i in range(5):
        task = PythonOperator(
            task_id='sleep_for_' + str(i),
            python_callable=my_sleeping_function,
            op_kwargs={'random_base': float(i) / 10},
        )

        run_this >> task
    # [END howto_operator_python_kwargs]

    # [START howto_operator_python_venv]
    def callable_virtualenv():
        """
        Example function that will be performed in a virtual environment.
        Importing at the module level ensures that it will not attempt to import the
        library before it is installed.
        """
        from time import sleep

        from colorama import Back, Fore, Style

        print(Fore.RED + 'some red text')
        print(Back.GREEN + 'and with a green background')
        print(Style.DIM + 'and in dim text')
        print(Style.RESET_ALL)
        for _ in range(10):
            print(Style.DIM + 'Please wait...', flush=True)
            sleep(10)
        print('Finished')

    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_python",
        python_callable=callable_virtualenv,
        requirements=["colorama==0.4.0"],
        system_site_packages=False,
    )
    # [END howto_operator_python_venv]



    for i in range(3):
        task = BashOperator(
            task_id='runme_' + str(i),
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        )
        task >> run_this

    # [START howto_operator_bash_template]
    also_run_this = BashOperator(
        task_id='also_run_this',
        bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    )
    # [END howto_operator_bash_template]
    also_run_this >> run_this_last

# [START howto_operator_bash_skip]
this_will_skip = BashOperator(
    task_id='this_will_skip',
    bash_command='echo "hello world"; exit 99;',
    dag=dag,
)
# [END howto_operator_bash_skip]
this_will_skip >> run_this_last

if __name__ == "__main__":
    dag.cli()

    '''