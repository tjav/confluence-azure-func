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
    result1 = yield context.call_activity('confluence-func-get-snow', "Tokyo")

    result2 = yield context.call_activity('confluence-func-get-content', result1)
    result3 = yield context.call_activity('confluence-func-get-graph', result1)

    result4 = yield context.call_activity('confluence-func-get-store-table', result2, result3)

    result5 = yield context.call_activity('confluence-func-compare-states', result4)

    result6 = yield context.call_activity('confluence-func-publish-result', result5)
    
    return [result6]

main = df.Orchestrator.create(orchestrator_function)