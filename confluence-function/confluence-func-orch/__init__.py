# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df



def orchestrator_function(context: df.DurableOrchestrationContext):
    input = context.get_input()
    page_id = input['page_id']
    unit= input['OARID']
    group= input['group']
    # result1 = yield context.call_activity('confluence-func-get-snow', "Tokyo")
    result2 = yield context.call_activity('confluence-func-get-graph', group)
    print(str(result2))
    result3 = yield context.call_activity('confluence-func-get-content', page_id)
    
    input4 = [result3, unit]
    result4 = yield context.call_activity('confluence-func-store-table', input4)
    
    # result5 = yield context.call_activity('confluence-func-compare-states', result4)

    # result6 = yield context.call_activity('confluence-func-publish-result', result5)
    
    return [result4]

main = df.Orchestrator.create(orchestrator_function)