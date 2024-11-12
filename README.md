# QueryMatrix
GraphQL based Django Project with PostgreSQL database



### Request Body
```
query AllDesignations {
	allDesignations(ordering: "name") {
		totalCount
		pageInfo {
			hasNextPage
			hasPreviousPage
			startCursor
			endCursor
		}
		edges {
			cursor
			node {
				id
				name
				createdAt
				updatedAt
			}
		}
	}
}
```

### Response Body
```{
	"data": {
		"allDesignations": {
			"totalCount": 3,
			"pageInfo": {
				"hasNextPage": false,
				"hasPreviousPage": false,
				"startCursor": "QURNSU4=",
				"endCursor": "U0NN"
			},
			"edges": [
				{
					"cursor": "QURNSU4=",
					"node": {
						"id": "3",
						"name": "ADMIN",
						"createdAt": "2024-11-12T09:13:22.569903+00:00",
						"updatedAt": "2024-11-12T09:13:22.569919+00:00"
					}
				},
				{
					"cursor": "SUNU",
					"node": {
						"id": "1",
						"name": "ICT",
						"createdAt": "2024-11-12T09:12:59.881843+00:00",
						"updatedAt": "2024-11-12T09:12:59.881855+00:00"
					}
				},
				{
					"cursor": "U0NN",
					"node": {
						"id": "2",
						"name": "SCM",
						"createdAt": "2024-11-12T09:13:05.448335+00:00",
						"updatedAt": "2024-11-12T09:13:05.448346+00:00"
					}
				}
			]
		}
	}
}
```