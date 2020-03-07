# Volume Control

## API usage

**`GET` `/api/volume`** Get current master volume

**Response**

* `200 OK` on success

  ```json
  {
    "message": "Success",
    "data": {
      "volume": 53
    }
  }
  ```

---

**`POST` `/api/volume`** Modify current master volume

**Parameters**

| Name                        | Type      | Description                                  | Values                        |
| --------------------------- | --------- | -------------------------------------------- | ----------------------------- |
| `action`<sup>optional</sup> | `string`  | Action to perfom<br />*Default value*: `set` | `set`, `increase`, `decrease` |
| `value`                     | `integer` | Value used by the action                     |                               |

**Response**

- `201 Created` on success

  ```json
  {
    "message": "Success",
    "data": {
      "volume": 73
    }
  }
  ```

---

*__TODO:__ this should be `POST`*

**`GET` `/api/play-beep`** Play a "beep" sound

**Response**

- `200 OK` on success

  ```json
  {
    "message": "Success",
    "data": {}
  }
  ```
