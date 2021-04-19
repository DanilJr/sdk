# [Singer SDK Implementation Details](/.README.md) - Stream State

The Singer SDK automatically handles state management and bookmarks.

## Important Notice Regarding State

_Note: The descriptions on this page are intended for debugging purposes only. We **do not** recommend reading or writing state directly within your tap._

The SDK was designed to automatically handle the state implementations so that developers
don't have to. If you are building a tap with the SDK and you find a need to directly read or write to the stream's state objects, please open a ticket with a description of your use case and we will use your examples to support more advanced use cases in the future.

## Standard State Format

The Singer Spec does not dictate exactly how state needs to be tracked. However, the basic
structure is documented as follows:

```json
{
  "bookmarks": {
    "orders": {
      // 'orders' state stored here
    },
    "customers": {
      // 'customers' state stored here
    }
  }
}
```

## Per-Stream STATE Properties

Within each stream definition, the following are considered the minimal effective
implementation within the SDK:

1. `replication_key` and `replication_key_value` - These two keys together should designate
the incremental replication key (if applicable) and the highest value yet seen for this
property.

## State Message Frequency

The SDK will automatically generate and emit STATE messages according to the constant
`Stream.STATE_MSG_FREQUENCY`, which designates how many RECORD messages should be processed
before an updated STATE message should be emitted.

## Backwards Compatibility

While the exact specification of STATE messages may change between versions, it is
nevertheless important that in production scenarios, any STATE bookmarks from prior versions
of the tap should still be effective for incremental updates in newer versions.

For the purposes of backwards compatibility, developers may override `Tap.load_state(state)`
in order to translate legacy STATE formats to the updated minimal implementation documented
here.

## State and Partitions

- _**Preview Feature Notice:** As of version `0.1.0`, the partitioned state feature is in preview status. Implementation details specified here should not be considered final._

The SDK implements a feature called [partitioning](../partitioning.md) which allows the same
stream to be segmented by one or more partitioning indexes. The collection of indexes
which uniquely describe a partition are referred to as the partition's 'context'.

For streams which are partitioned, the SDK will automatically store their stream state
under a `partitions` key. The `partitions` key should be a list of objects, with
each partition object containing a `context` key which contains the dictionary of
keys needed to uniquely identify the partition. Apart from the presences of a `context`
object, the contents of the partition object should be identical to any other stream state
definition.

### Partitioned State Example

In this hypothetical example, our upstream Orders API requires `Store ID` as input, and
as a result we have partitioned the `orders` stream into two partitions: one for store ID
`1` and one for store ID `2`. Splitting into two partitions allows us to automatically track
separate bookmarks for each store, ensuring that we always have proper incremental
replication key values for each one.

Note that in this example, we have a different `replication_key_value` for each partition
and each partition's state contains a unique `context` object to distinguish it from the
others.

```json
{
  "bookmarks": {
    "orders": {
      "partitions": [
        {
          "context": {
            "storeId": 1
          },
          "replication_key": "updatedAt",
          "replication_key_value": "2021-01-02T0:00:00Z"
        },
        {
          "context": {
            "storeId": 2
          },
          "replication_key": "updatedAt",
          "replication_key_value": "2021-01-01T00:00:00Z"
        }
      ]
    }
  }
}
```

## Replication Key is Singular

The SDK's implementation of `replication_key` is intentionally within the
framework of a _singular_ column comparison. Most of those use cases which previously
required multiple bookmarks can now be handled using the [partitioning](../partitioning.md)
feature.

While legacy taps have sometimes supported multiple replication key properties,
this is not yet a supported use case within the SDK. If your source requires multiple
bookmark keys, and if it does not align with the [partitioning](../partitioning.md) feature,
please open an issue with a detailed description of the intended use case.

## See Also

- [Singer SDK Partitioning](../partitioning.md)
- [Singer Spec: State Overview](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md#state)
- [Singer Spec: Config and State](https://github.com/singer-io/getting-started/blob/master/docs/CONFIG_AND_STATE.md#state-file)