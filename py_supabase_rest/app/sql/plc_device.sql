CREATE TABLE plc_device (
    id SERIAL PRIMARY KEY,          -- 自動增長主鍵
    device_id TEXT NOT NULL,        -- device_id
    voltage DOUBLE PRECISION,       -- voltage 浮點數
    current DOUBLE PRECISION,       -- current 浮點數
    timestamp TEXT NOT NULL,        -- timestamp 字串
    date TEXT NOT NULL,             -- date YYYY-MM-DD
    hh TEXT NOT NULL,               -- 小時
    mm TEXT NOT NULL,               -- 分鐘
    ss TEXT NOT NULL                -- 秒數
);

-- 複合索引 (device_id, date, hh, mm)
CREATE INDEX idx_device_date_hh_mm
ON plc_device (device_id, date, hh, mm);
