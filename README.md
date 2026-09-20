# H3 API Server

H3 라이브러리를 이용한 H3 변환 API 서버

## 1. 주요 기능

- **`POST /latLngToCell`**
  - 위도, 경도, Resolution을 H3 Cell Index로 변환
  - Java `latLngToCell()` 대응
  - 결과는 10진수 H3 Index를 String으로 반환

- **`POST /latLngToCellAddress`**
  - 위도, 경도, Resolution을 H3 Cell Address로 변환
  - Java `latLngToCellAddress()` 대응
  - 결과는 H3 hexadecimal String으로 반환

- **`POST /cellToLatLng`**
  - H3 Cell을 해당 Cell의 중심 위도, 경도로 변환
  - Java `cellToLatLng()` 대응
  - Decimal H3 Index와 H3 Address 모두 지원

- **`POST /gridDisk`**
  - 기준 H3 Cell과 `k` 값으로 주변 Cell 조회
  - Decimal H3 Index와 H3 Address 모두 지원

- **`POST /health`**
  - API 서버 상태 확인

## 2. 시스템 구성

- **Python:** 3.13
- **Framework:** FastAPI
- **H3:** h3-py
- **Application Server:** Uvicorn
- **Container:** Docker / Docker Compose
- **Service Port:** `8137`

## 3. 공통 JSON 구조

요청과 응답은 `items` 배열을 사용하며 다건 처리를 지원합니다.

```json
{
  "items": [
    {
      "reqLat": "",
      "reqLng": "",
      "reqRes": "",
      "reqOrigin": "",
      "reqK": "",
      "reqCell": "",
      "resLat": "",
      "resLng": "",
      "resCount": "",
      "resCell": ""
    }
  ]
}
```

- `reqLat` → 위도
- `reqLng` → 경도
- `reqRes` → H3 Resolution
- `reqOrigin` → gridDisk 기준 Cell
- `reqK` → gridDisk 거리
- `reqCell` → Cell 입력값
- `resLat` → 결과 위도
- `resLng` → 결과 경도
- `resCount` → 결과 개수
- `resCell` → 결과 H3 Cell

계산 결과가 없는 경우 대응 가능한 Request 값을 Response 필드에 사용

## 4. API 호출

### latLngToCell

```http
POST /latLngToCell
Content-Type: application/json
```

```json
{
  "items": [
    {
      "reqLat": "37.5665",
      "reqLng": "126.9780",
      "reqRes": "9"
    }
  ]
}
```

Response:

```json
{
  "items": [
    {
      "reqLat": "37.5665",
      "reqLng": "126.9780",
      "reqRes": "9",
      "resLat": "37.5665",
      "resLng": "126.9780",
      "resCell": "617733123456789123"
    }
  ]
}
```

### latLngToCellAddress

```http
POST /latLngToCellAddress
Content-Type: application/json
```

```json
{
  "items": [
    {
      "reqLat": "37.5665",
      "reqLng": "126.9780",
      "reqRes": "9"
    }
  ]
}
```

Response:

```json
{
  "items": [
    {
      "reqLat": "37.5665",
      "reqLng": "126.9780",
      "reqRes": "9",
      "resLat": "37.5665",
      "resLng": "126.9780",
      "resCell": "8930e1..."
    }
  ]
}
```

### cellToLatLng

```http
POST /cellToLatLng
Content-Type: application/json
```

```json
{
  "items": [
    {
      "reqCell": "8930e1..."
    }
  ]
}
```

Response:

```json
{
  "items": [
    {
      "reqCell": "8930e1...",
      "resLat": "37.566...",
      "resLng": "126.978...",
      "resCell": "8930e1..."
    }
  ]
}
```

### gridDisk

```http
POST /gridDisk
Content-Type: application/json
```

```json
{
  "items": [
    {
      "reqOrigin": "8930e1...",
      "reqK": "1"
    }
  ]
}
```

Response:

```json
{
  "items": [
    {
      "reqOrigin": "8930e1...",
      "reqK": "1",
      "resCount": "7",
      "resCell": "8930e1..."
    },
    {
      "reqOrigin": "8930e1...",
      "reqK": "1",
      "resCount": "7",
      "resCell": "8930e2..."
    }
  ]
}
```

### health

```http
POST /health
```

Request Body 없음