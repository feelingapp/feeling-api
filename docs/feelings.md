# Feelings

Daily logs of the user's emotional state.

## Fetch a list of all the user's feelings

`GET /feeling`

### Example Response

```json
{
  "feelings": [
    {
      "emotion": "Amazing",
      "description": "...",
      "hashtags": []
    },
    {
      "emotion": "Unsure",
      "description": "...",
      "hashtags": []
    },
    {
      "emotion": "Great",
      "description": "...",
      "hashtags": []
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

`PUT /feeling`

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

`DELETE /feeling`
