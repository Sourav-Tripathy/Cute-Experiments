## Experiment: Document Size vs Retrieval Time in MongoDB

### Experiment Overview
This experiment explores how the size of documents stored in MongoDB affects the time it takes to retrieve them. By varying document sizes and measuring retrieval times, the goal is to understand the relationship between document size and performance.

### Theoretical Background
In MongoDB, data retrieval time is influenced by several factors:
- **Latency**: The time taken for a request to travel between the client and the server, which depends on the physical distance and network conditions.
- **Serialization/Deserialization Time**: The time required to convert data to and from BSON (Binary JSON), which increases with document size.
- **Network Transfer Time**: The time taken to transfer data over the network, which is directly proportional to the document size and affected by network bandwidth.
- **Index Lookup Time**: Index lookups (e.g., on `doc_id`) are generally fast and independent of document size.
- **MongoDB Document Size Limit**: MongoDB has a 16 MB document size limit, which constrains the maximum size of a single document.

Assuming other factors (like server configuration, client machine, and network conditions) remain constant, this experiment focuses on how document size impacts retrieval time. The hypothesis is that larger document sizes will lead to increased retrieval times due to higher data transfer and deserialization overhead.