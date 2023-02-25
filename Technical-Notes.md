
# Techniocal Notes

## Logging

logging sholud also be saved in a file

## Async method calls

## socket vs socketserver library

## Data Serilization

Using binary static bit wide data format is not recommended in modren large scale protocols due to the hardness of creating well engineered data format and implemnting the serilization methods.

Best practice for creating data format takes into consideration

* Serialization (marshalling) is a process of converting data into a byte stream that can be efficiently stored and/or transferred elsewhere.
* Deserialization (unmarshalling) is about recreating original data from byte stream,
* Backward compatibility is when a new version of the software can run code written in an old version,
* Forward compatibility is when an older version of the software can run code written in a new version,
* Schema evolution allows to update the schema to a new format while maintaining backward compatibility.

Protobuf is an example of an appropriate message format for our example

## UDP vs TCP

Pushing messages to clients may be cahnnlengin using UDP
