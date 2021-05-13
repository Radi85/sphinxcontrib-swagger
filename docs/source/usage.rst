Config Variables
================

spec_path
----------

**Required** ``True``

The path to openapi yaml/json file and it should be relative to `config.py` file.

title
------

**Required** ``False``

**Default** ``OpenAPI Documentation``

The title in swagger page. (HTML title tag)

page_name
----------

**Required** ``False``

**Default** ``swagger``

The name of rendered standalone openapi page. This will be reachable on ``$DOCUMENT_BASE_URL/swagger.html``. See `<swagger.html>`_

The value of this variable will be prepended with ``_`` i.e ``_swagger.html`` if it's similar to ``swagger_embedded_in``.

swagger_embedded_in
-------------------

**Required** ``False``

Name of existing document that swagger should be embedded in. The document must have `{{openapi}}` value inside. See `Example For Embedded Swagger Page <example.html>`_

If this value is not provided, the standalone page will be created and won't be embedded in any document.

template
--------

**Required** ``False``

**Default** ``assets/openapi.html``

Path to openapi html template that should be used to render swagger document and it should be relative to `config.py` file.
