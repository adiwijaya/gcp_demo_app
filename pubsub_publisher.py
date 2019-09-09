"""Publishes multiple messages to a Pub/Sub topic with an error handler."""


def pubsub_publisher(topic, message):
    import time

    from google.cloud import pubsub_v1

    # TODO
    project_id = "demoendtoend"
    # TODO
    topic_name = topic

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    futures = dict()

    def get_callback(f, data):
        def callback(f):
            try:
                print(f.result())
                futures.pop(data)
            except:  # noqa
                print('Please handle {} for {}.'.format(f.exception(), data))

        return callback


    data = message
    futures.update({data: None})
    # When you publish a message, the client returns a future.
    future = publisher.publish(
        topic_path, data=data.encode('utf-8')  # data must be a bytestring.
    )
    futures[data] = future
    # Publish failures shall be handled in the callback function.
    future.add_done_callback(get_callback(future, data))

    # Wait for all the publish futures to resolve before exiting.
    while futures:
        time.sleep(5)

    print('Published message with error handler.')
