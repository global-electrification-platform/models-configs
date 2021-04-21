# Model import, asbuilt

┌─name────────┬─type───┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ id          │ String │              │                    │         │                  │                │
│ updatedAt   │ Date   │              │                    │         │                  │                │
│ attribution │ String │              │                    │         │                  │                │
│ levers      │ String │              │                    │         │                  │                │
│ filters     │ String │              │                    │         │                  │                │
│ map         │ String │              │                    │         │                  │                │
│ name        │ String │              │                    │         │                  │                │
│ version     │ String │              │                    │         │                  │                │
│ description │ String │              │                    │         │                  │                │
│ country     │ String │              │                    │         │                  │                │
│ type        │ String │              │                    │         │                  │                │
│ timesteps   │ String │              │                    │         │                  │                │
│ baseYear    │ Int16  │              │                    │         │                  │                │
│ sourceData  │ String │              │                    │         │                  │                │
│ disclaimer  │ String │              │                    │         │                  │                │
└─────────────┴────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

Stringlike, directly from the .yml file:
* id - like za-1
* name
* updatedAt
* version
* type
* baseYear
* country
* description
* disclaimer?

Json, directly from the .yml file
* attribution
* map
* sourceData

Json Array, with outer [] delimiters replaced by {}
* timesteps

Json Array, with outer [] delimiters replaced by {}, and inner bits as strings of json:
* Levers
* filters, with the additional caveat that the range max/min values
  are calculated from the data as `select min(key), max(key) from
  scenarios where modelId=id`;


# Model import, new version:
(requires data server change)

Stringlike, directly from the .yml file:
* id - like za-1
* name
* updatedAt
* version
* type
* baseYear
* country
* description
* disclaimer?
* External url for model.

Json, directly from the	.yml file
* attribution
* map
* sourceData
* timesteps
* Levers
* filters, with the additional caveat that the range max/min values
  are calculated from the data as `select min(key), max(key) from
  scenarios where modelId=id`;

