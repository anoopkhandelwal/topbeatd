This project is built on top of topbeat which is a system monitor.
Topbeat collects the system metrics and send it to elasticsearch.
After then you can fetch the metrics from the elasticsearch based on the
requirements like past 7 days,past 1 month and so on.
This is a version-1 of the project where only you can fetch the data from the time since you successfully start sending data to 
elasticsearch.Currently it supports the default mapping type of the topbeat index.
In version-2 I am planning to implement in a more useful way by implementing with a time-range.

