# FF-OOE-Statistics Scanner
The Scanner application is a service which regularly fetches the fire department operations of the last 48 hours from the [ooelfv-api](https://cf-einsaetze.ooelfv.at/webext2/rss/json_2tage.txt) in a customizible interval. It saves the operations to a (configurable) mongoDB Atlas Cluster and uses the _id index to prevent duplicate operations from being saved to the database.

## Configuration
 - The Connection String for the MongoDB Cluster can either be configured using environment variables (for container deployment) or in a file called "mdbLogin\.py" which must be created individualy (see code comments for instructions).
 - The interval in which the scanner fetches data from the endpoint can be configured using environment variables, or it will default to one hour.

## Further information
 - Refrain from setting the scanning interval too low because this will cause the ooelfv to block requests.
 - By default the scanner will ignore operations with the operation-type "SELBST" since these operations are automatically and nearly exclusively triggered when a fire truck leaves the fire department for non-operation purposes like cleaning or training and are by thus uninteresting for statistical purposes.
 - Due to the current implementation of the duplication-prevention system through the _id index, it is not possible to update a operation in the current version of the scanner. Due to this, the scanner only saves operations which have been completed, since the completion time is relevant for statistical purposes. Otherwise an operation would always be saved to the database with status "offen" and no end-time protocolled. This might be improved in the future.
