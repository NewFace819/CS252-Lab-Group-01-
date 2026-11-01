# Lab 4 — Your First Web API (Group 01)

Mục tiêu: dùng trợ lý của nhóm (`assistant.rules.reply`) qua HTTP bằng FastAPI. Đề: `CSC10014_2026_Lab04_REST_API_Backend_Tutorial.pdf`.

## Setup (mỗi người làm một lần)

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate          # Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env
pytest -q
```

Chạy server (sau khi có `assistant_api`):

```bash
uvicorn assistant_api.main:create_app --factory --reload
```

Mở http://127.0.0.1:8000/docs để thử endpoint. Chạy curl bằng Git Bash, không dùng PowerShell.

## Hợp đồng API

| Method | Path | Gửi | Nhận |
| --- | --- | --- | --- |
| GET | `/health` | không | `{"status":"ok","version":"1.0.0"}` |
| POST | `/v1/chat` | `{"message","session_id"}` | `{"answer","intent","sources","degraded","request_id"}`; message rỗng → 422 |
| POST | `/v1/feedback` | `{"request_id","rating"(-1/0/1),"comment"}` | 201 + feedback đã lưu |
| GET | `/v1/feedback` | header `X-API-Key` | danh sách feedback; sai key → 401 |
| GET | `/v1/weather` | không | thời tiết campus; site ngoài lỗi → 503 |
| GET | `/v1/offices` (H1) | không | danh sách văn phòng, sắp theo tên |

Lỗi luôn có dạng `{"error": {"code": "...", "message": "..."}}`.

## Phân công

Quy ước chung:
- Mỗi người một branch tách từ `main`, một PR, tên branch ghi bên dưới. Không sửa file của người khác; cần đổi hợp đồng thì báo Hải.
- Commit theo dạng `feat(api): ...`, `test(api): ...`; không có dòng đồng tác giả AI.
- **Cá nhân (cả 5 người):** P1–P5 trong `lab04/practice/<tên>/hello_api.py` + `test_hello_api.py` (5 passed), và H2 reflection 5 dòng trong `docs/lab04/reflection-<tên>.md`.

### Bước 0 — chặn mọi người (Thông, làm ngay)
`data/offices.csv` đang **rỗng** nên `test_office_lookup` fail trên `main`. Điền dữ liệu với cột `name,room,hours` (ít nhất: Training Office = I.101, Student Affairs, Library = B.201 07:00-20:00, IT Helpdesk = E.005 Mon-Fri 08:00-17:00) và dùng đúng nguồn trong `docs/ui-sources.md`. Branch `fix/offices-data`. Xong khi `pytest -q` xanh toàn bộ.

### Hải — khung API + T1 + tích hợp (branch `feat/api-skeleton`)
Làm **đầu tiên**, merge trong buổi để những người khác tách branch từ đó.
1. `src/assistant_api/__init__.py`, `schemas.py`: `ChatRequest` (`message` min_length=1, `session_id`), `ChatResponse` (`answer`, `intent`, `sources`, `degraded`, `request_id`), `FeedbackIn` (`request_id`, `rating` -1/0/1, `comment`), `FeedbackOut` (+`id`, `created_at`), `Weather`.
2. `main.py`: `create_app(settings, service, weather_client)` (dùng với `--factory`), `GET /health`, hàm `error(code, message)` + handler cho `HTTPException` và lỗi validate 422 → dạng `{"error":{"code","message"}}`, code 422 là `invalid_request`.
3. `service.py`: lớp bọc `handle(message, session_id)` gọi `assistant.rules.reply()` và suy ra `intent` (`greeting|help|office|unknown`), `sources=[]`, `degraded=False`.
4. **T1** `POST /v1/chat`: gọi service, thêm `request_id = uuid4().hex[:12]`.
5. Cuối buổi: review PR của mọi người, merge, tag `v0.4-api`, nộp link tag.
Xong khi: `/health` 200; `/v1/chat` trả đủ 5 trường; message rỗng 422.

### Gia Huy — T2 + T3 + config (branch `feat/api-feedback`, tách sau khi Hải merge khung)
1. `config.py`: `Settings` đọc `API_ADMIN_KEY` từ `.env` (mặc định `change-me`).
2. `feedback.py`: `feedback_store` (list), `require_admin` đọc header `X-API-Key`, sai/thiếu → 401 `{"error":{"code":"unauthorized",...}}`.
3. **T2** `POST /v1/feedback`: status 201, `id=len(store)+1`, `created_at` UTC; rating ngoài -1/0/1 → 422.
4. **T3** `GET /v1/feedback`: có `require_admin`, trả toàn bộ store.
Xong khi: POST hợp lệ 201; rating 5 → 422; GET không key → 401; có key → danh sách.

### Đức Huy — T4 + CI (branch `feat/api-weather`)
1. `weather.py`: `ExternalServiceError`; `WeatherClient` gọi Open-Meteo (Nguyen Van Cu campus), `httpx.Client(timeout=3)`, thử lại 1 lần, lỗi thì trả bản cache cuối với `stale=True`, chưa có cache thì raise `ExternalServiceError`. Cho phép truyền `transport` giả để test.
2. **T4** `GET /v1/weather`: bắt `ExternalServiceError` → `HTTPException(503, "Weather service unavailable") from None`.
3. `.github/workflows/`: chạy `pip install -r requirements.txt`, `pip install -e .`, `pytest -q` khi mở PR (nếu workflow đã có thì chỉ bổ sung).
Xong khi: test với fake site trả 200; fake site sập trả 503; CI xanh.

### Tô Hoàng Anh — test + công cụ gọi thử (branch `test/api-suite`)
Viết theo hợp đồng ngay từ đầu; test sẽ fail cho tới khi module của người khác merge, đó là bình thường.
1. `tests/conftest.py`: fixture `settings`, `service` giả, `client = TestClient(create_app(...))`, helper `weather_with(handler)` dùng `httpx.MockTransport`.
2. `tests/test_api.py`: ít nhất 1 test cho mỗi trường hợp: health, chat OK, chat rỗng 422 (`invalid_request`), feedback tạo 201, rating sai 422, list feedback không key 401, có key 200, weather OK, `test_weather_down_returns_503` (fake site 500), `test_rate_limit` (đánh dấu skip tới khi có bonus).
3. `api-tests/curl_tests.sh` (chạy được bằng Git Bash, in status code từng request theo bảng hợp đồng) và `api-tests/study-assistant.postman_collection.json`.
Xong khi: sau khi mọi PR merge, `pytest -q` xanh (chỉ 1 skip); `bash api-tests/curl_tests.sh` in đúng status mong đợi.

### Võ Bá Thông — H1 + bonus + ảnh nộp (branch `feat/api-offices`)
1. (Sau Bước 0) `rules.py`: thêm `list_offices()` trả danh sách `{name, room, hours}` sắp theo `name`. Không đổi hành vi `reply()`.
2. **H1** `GET /v1/offices` trong `main.py` (tạo router riêng `offices.py`, Hải chỉ include một dòng) + 2 test trong `tests/test_offices_api.py`: status 200 và có item tên "Library".
3. **Bonus (+1)** `ratelimit.py` có `RateLimiter.allow(client)`; thêm vào đầu `/v1/chat` trả 429; bỏ skip của `test_rate_limit`. Làm sau khi T1 merge.
4. Chụp ảnh `/docs` với một lần `/v1/chat` thành công, lưu `docs/lab04/docs-chat.png`, dán vào PR.
Xong khi: `/v1/offices` 200, sắp theo tên; 2 test xanh; vượt hạn mức → 429.

### Thứ tự và phụ thuộc
`Thông Bước 0` ∥ `Hải khung` → (Gia Huy ∥ Đức Huy ∥ Thông H1) song song, `Tô Hoàng Anh` viết test từ đầu → Hải T1 + tích hợp → ảnh `/docs`, curl, tag.
## Checklist nộp bài

- [ ] P1–P5 (`lab04/practice/hello_api.py`, `pytest test_hello_api.py` 5 passed) — mỗi người, commit `feat(practice): hello API P1-P5`
- [ ] T1–T4 xong, `pytest -q` xanh
- [ ] Ảnh chụp `/docs` với một lần gọi `/v1/chat` thành công (đính trong PR)
- [ ] Đã chạy `bash api-tests/curl_tests.sh`
- [ ] PR mở và dán link lên LMS cuối buổi (draft được)
- [ ] Nhóm chọn một PR rõ nhất để merge, các bạn khác review; Hải tag `v0.4-api`, nộp link tag trước 23:59 ngày trước Lab 5
- [ ] H1 (`/v1/offices` + 2 test) và H2 (reflection 5 dòng, mỗi người) nộp PR link trước 23:59 ngày trước Lab 5
- [ ] Bonus (+1): rate limit hoặc một API ngoài thứ hai (`worksheets/external_api_failure.md`)

## Điểm (10 + 1)

P1–P5: 2 · T1–T4: 4 · ảnh `/docs` + curl: 1 · H1: 2 · H2: 1 · Bonus: +1

## Lưu ý

- Không commit `.env` hay key thật; chỉ commit `.env.example`.
- Chưa có file starter của thầy (`lab04/starter/`). Nếu có, đối chiếu lại tên module/hàm trong bảng phân công.
- `assistant.rules.reply()` hiện chỉ trả về chuỗi; `intent`/`sources`/`degraded` của `/v1/chat` cần được suy ra hoặc bổ sung (Hải quyết định ở bước khung).

