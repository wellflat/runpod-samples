#!/usr/bin/env python

import runpod

def process_input(input):
    name = input['name']
    greeting = f'hello, {name}'

    return { 'greeting': greeting }

### RunPod Handler
def handler(event):
    print(event)
    return process_input(event['input'])

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
