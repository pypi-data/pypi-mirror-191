# function for sending data to Kinesis at the absolute maximum throughput
import json
import os

import boto3

region = os.environ['region']
FIREHOSE = boto3.client('firehose', region_name=region)


def send_to_kns_delivery_stream(kinesis_stream_name, data, kinesis_shard_count=1):
    kinesis_records = []  # empty list to store data
    current_bytes = 0  # counter for bytes
    row_count = 0  # as we start with the first
    total_row_count = len(data)  # using our rows variable we got earlier
    send_to_kinesis = False  # flag to update when it's time to send data
    shard_count = 1  # shard counter

    # loop over each of the data rows received
    for row in data:
        values = json.dumps(row)
        encoded_values = bytes(values + '\n', 'utf-8')  # encode the string to bytes

        kinesis_records.append({'Data': encoded_values})  # add the object to the list
        string_bytes = len(values.encode('utf-8'))  # get the number of bytes from the string
        current_bytes = current_bytes + string_bytes  # keep a running total

        # check conditional whether ready to send
        # if we have 500 records packed up, then proceed
        # if the byte size is over 50000, proceed
        # if we've reached the last record in the results
        if len(kinesis_records) == 500 or current_bytes > 50000 or (
            row_count == total_row_count - 1
        ):
            send_to_kinesis = True  # set the flag

        # if the flag is set
        if send_to_kinesis:
            # "PartitionKey": str(shard_count)
            # put the records to kinesis
            response = FIREHOSE.put_record_batch(
                Records=kinesis_records,
                DeliveryStreamName=kinesis_stream_name
            )
            print(response)
            # resetting values ready for next loop
            kinesis_records = []  # empty array
            send_to_kinesis = False  # reset flag
            current_bytes = 0  # reset byte count

            # increment shard count after each put
            shard_count = shard_count + 1

            # if it's hit the max, reset
            if shard_count > kinesis_shard_count:
                shard_count = 1

        # regardless, make sure to increment the counter for rows.
        row_count = row_count + 1

    # log out how many records were pushed
    print('Total Records sent to Kinesis: {0}'.format(total_row_count))
