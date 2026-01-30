# Prompts

## Prompt for this project creation

I have a gramlin JanusGraph database, which have the following vertices:

- book, 
- quotation

Book has these properties:
- type - is always "book",
- caption - string, 
- name - string.

Quotation has these properties:
- type - is always "quotation",
- caption - string, 
- text - string, 
- book - string, 
- position - string,
- importIndex - integer,
- status - string.


A book can be connected to a quotation with the `contains` edge.

Make a full-fledged python project with the name `theo-server` for importing quotations from an e-Book, that starts as a server and provides an HTTP REST API with the following functions:

- Get the highest index of imported quotations.
- Import a quotation. If the quotation with the same importIndex already exists, then do not replace the existing quotation and return the 4xx error. If the book with the caption provided in the `book` property exists, then connect the book to the imiported quotation with the `contains` edge. If the book does not exist, then first create the book with this caption and empty name.

The API must work only if API-key is provided in an HTTP header. The valid API key should be kept in an environment variable on the server side. No complicated ACL management and user management systems are needed. Just check the incoming key with the give key in the environment variable.

The project must have a professional internal structure, and should have a docker-compose file for starting the server in a docker.

Please, pack the whole project in the zip file.