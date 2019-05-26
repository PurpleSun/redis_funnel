# API

## 登入
1. `POST /login`
2. params:
```json
{
  "username": "admin",
  "password": "admin"
}
```
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "user": {
      "login_ts": 1558838975.93385,
      "username": "admin"
    }
  },
  "msg": null
}
```

## 登出
1. `GET /logout`
2. params: **None**
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "success": true
  },
  "msg": null
}
```

## 获取分组
1. `GET /api/group`
2. params: **None**
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "group_list": [
      "1000001"
    ]
  },
  "msg": null
}
```

## 获取分组中的漏洞列表
1. `GET /api/group/<group>`
2. params: **None**
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "funnel_list": [
      {
        "capacity": 7300,
        "leaking_ts": 1558838928.828,
        "left_quota": 903.3612308502197,
        "name": "1000001:test",
        "operations": 7300,
        "seconds": 1
      }
    ],
    "total_items": 1
  },
  "msg": null
}
```

## 获取单个漏斗详情
1. `GET /api/key/<key>`
2. params: **None**
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "funnel": {
      "capacity": 7300,
      "leaking_ts": 1558838928.828,
      "left_quota": 903.3612308502197,
      "name": "1000001:test",
      "operations": 7300,
      "seconds": 1
    }
  },
  "msg": null
}
```

## 删除单个漏斗
1. `DELETE /api/key/<key>`
2. params: **None**
3. rsp:
```json
{
  "code": 20000,
  "data": {
    "status": true
  },
  "msg": null
}
```