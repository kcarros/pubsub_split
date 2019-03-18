import logging
import json
import warnings


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from google.cloud import pubsub_v1 as pubsub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def handle_data(name, items, project_id, dataset=None):
    if not items:
        logger.info("No items for %s publish, aborting", name)
        return
    publisher = pubsub.PublisherClient()
    topic_name = name.upper() + "_TOPIC"  # TODO make this more generic
    topic_path = publisher.topic_path(project_id, topic_name)
    table_name = name.upper() + "_TABLE"  # TODO
    send_split_pubsub(publisher, name, topic_path, items, table_name)
    logger.info(name + " topic publishing complete")


def send_split_pubsub(
    publisher,
    name,
    topic_path,
    items,
    table_name,
    dataset,
    batch_max_items=10000,
    batch_max_size=10 * 1024 * 1024,
    ingest_type="stream",
):
    if len(items) == 0:
        logger.warning("No items to send")
        return

    if len(items) > batch_max_items:
        total = len(items) // batch_max_items
        logger.info(f"Too many {name} items to publish, splitting into {total} batches")
        for begin_index in range(0, len(items), batch_max_items):
            batch = items[begin_index : begin_index + batch_max_items]
            send_split_pubsub(publisher, name, topic_path, batch, table_name)

    data = json.dumps(items).encode("utf-8")
    if len(data) > batch_max_size:
        items_left_half, items_right_half = split_list(items)
        if len(items) == 1:
            logger.warning("Item is too big to be sent via pubsub")
        else:
            logger.info(f"{name} size {len(data)} too large, splitting in half")
            send_split_pubsub(publisher, name, topic_path, items_left_half, table_name)
            send_split_pubsub(publisher, name, topic_path, items_right_half, table_name)
        return

    publisher.publish(topic_path, data, dataset, table_name, ingest_type)


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]
