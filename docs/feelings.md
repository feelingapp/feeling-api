# Feelings

Daily logs of the user's emotional state.

## Fetch a list of all the user's feelings

`GET /feeling`

### Example Response

```json
{
  "feelings": [
    {
      "id": "b6aff5e1-e777-4485-b932-b62a6905d062",
      "emotion": "Amazing",
      "description": "...",
      "hashtags": [],
      "created_at": "2019-01-04T00:02:51",
      "updated_at": "2019-01-04T00:02:51"
    },
    {
      "id": "5c3eeb4c-c416-4467-9d1b-a5c3cbe96c04",
      "emotion": "Unsure",
      "description": "...",
      "hashtags": [],
      "created_at": "2019-01-04T00:02:51",
      "updated_at": "2019-01-04T00:02:51"
    },
    {
      "id": "753e56d6-2308-44b7-b817-bc76053f9cc7",
      "emotion": "Great",
      "description": "...",
      "hashtags": [],
      "created_at": "2019-01-04T00:02:51",
      "updated_at": "2019-01-04T00:02:51"
    }
  ]
}
```

## Fetch a feeling by ID

`GET /feeling/:id`

### Example Response

```json
{
  "emotion": "Amazing",
  "description": "I had a great day today. I woke up quite early and I got a lot of my assignment done. George and I made a tasty meal too, it was nice spending time with him.",
  "hashtags": ["#productive", "#love"]
}
```

## Create a Feeling

`POST /feeling`

| Parameter     | Type                 | Description                                        |
| ------------- | -------------------- | -------------------------------------------------- |
| `emotion`     | `string`             | **Required.** The emotion of the user.             |
| `description` | `string`             | **Required**. A description of the user's emotion. |
| `hashtags`    | `array` of `strings` | **Required**. A list of hashtags.                  |

### Example Request

```json
{
  "emotion": "Amazing",
  "description": "I had a great day today. I woke up quite early and I got a lot of my assignment done. George and I made a tasty meal too, it was nice spending time with him.",
  "hashtags": ["#productive", "#love"]
}
```

## Update a Feeling

`PUT /feeling/:id`

| Parameter     | Type                 | Description                          |
| ------------- | -------------------- | ------------------------------------ |
| `emotion`     | `string`             | The emotion of the user.             |
| `description` | `string`             | A description of the user's emotion. |
| `hashtags`    | `array` of `strings` | A list of hashtags.                  |

### Example Request

```json
{
  "description": "I had a great day today. I woke up quite early and I got a lot of my assignment done. George and I made a tasty meal too, it was nice spending time with him."
}
```

## Delete a Feeling

`DELETE /feeling/:id`
