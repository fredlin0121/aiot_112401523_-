SmartSeat: 離線式隱私優先智慧點名系統 📸
基於 Raspberry Pi 5 與 YOLOv8 的邊緣運算點名解決方案。

📖 專案簡介 (Introduction)
SmartSeat 是一套專為教室與會議室設計的自動化點名系統。不同於傳統人臉辨識系統容易引發隱私爭議，SmartSeat 採用 物件偵測 (Object Detection - YOLOv8) 結合 感興趣區域映射 (ROI Mapping) 技術。

系統會偵測預先定義的座位區域內是否有「人形 (Person)」，而非辨識「是誰」。本系統完全在 Raspberry Pi 5 上離線運行，所有的影像處理皆在本地端完成，並自動將出缺席紀錄儲存為 CSV 檔案。

核心功能 (Key Features)
🔒 隱私優先 (Privacy-First): 不進行人臉辨識，不儲存生物特徵，僅判斷「座位上是否有人」。

🚀 邊緣運算 (Edge Computing): 基於 Raspberry Pi 5 本地端運行，具備極高的推論速度。

⚡ Picamera2 整合: 使用樹莓派原生相機函式庫，實現低延遲影像擷取。

🖱️ 視覺化校正 (Visual Calibration): 提供圖形化介面 (GUI)，用滑鼠即可輕鬆框選座位區域。

📊 自動紀錄 (Auto Logging): 自動輸出包含時間戳記的點名表 (attendance_log.csv)。

📡 完全離線 (Offline Capable): 無需網路連線即可運作，資料絕對安全。

🛠️ 硬體需求 (Hardware Requirements)
Raspberry Pi 5 (建議 4GB 或 8GB 版本)

Raspberry Pi Camera Module 3 (建議使用廣角版 Wide Lens 以覆蓋更大範圍)

主動式散熱器 (Active Cooler) (執行 AI 運算時必須安裝)

MicroSD 卡 (32GB 以上，安裝 Raspberry Pi OS Bookworm 64-bit)

⚙️ 安裝教學 (Installation)
1. 系統環境準備
請確保您的 Raspberry Pi 運行的是最新的 64-bit 作業系統。

Bash
sudo apt update && sudo apt upgrade -y
2. 下載專案程式碼
Bash
git clone https://github.com/your-username/SmartSeat.git
cd SmartSeat
3. 建立虛擬環境 (強烈建議)
在 Raspberry Pi OS (Bookworm) 版本中，建議使用虛擬環境來管理 Python 套件。

Bash
python3 -m venv venv
source venv/bin/activate
4. 安裝相依套件
安裝必要的 Python 函式庫：

Bash
pip install ultralytics opencv-python
注意：picamera2 通常已內建於 Raspberry Pi OS 中。若遺失可透過 apt 安裝：sudo apt install python3-libcamera。

🚀 使用指南 (Usage)
第一階段：座位校正 (Calibration)
在初次使用或移動鏡頭位置後，需執行此步驟來定義座位位置。

執行校正工具：

Bash
python calib_seats.py
調整鏡頭： 系統會開啟預覽視窗，請調整鏡頭角度以覆蓋所有座位。

凍結畫面： 按下鍵盤 空白鍵 (SPACE) 凍結當前畫面。

框選座位：

使用 滑鼠左鍵拖曳 畫出座位的方框。

系統會自動依序編號 (Seat 1, Seat 2...)。

存檔： 按下 s 將設定儲存至 seats.json。

離開： 按下 q 關閉程式。

第二階段：日常點名 (Attendance Check)
執行主程式開始進行監控與點名。

啟動監控程式：

Bash
python main.py
即時監控： 螢幕將顯示即時影像。

執行點名： 按下鍵盤 空白鍵 (SPACE)。

系統將擷取影像並執行 YOLO 偵測。

判斷人體中心點是否落在座位框內。

綠框： 出席 / 紅框： 缺席。

資料將自動寫入 attendance_log.csv。

確認結果： 螢幕顯示標記後的結果圖，按任意鍵返回監控模式。

離開： 按下 q 關閉程式。

📂 專案結構 (Project Structure)
Plaintext
SmartSeat/
├── calib_seats.py      # 座位校正工具 (畫框框用)
├── main.py             # 點名主程式 (核心邏輯)
├── seats.json          # 座位座標設定檔 (由 calib_seats.py 生成)
├── attendance_log.csv  # 點名紀錄檔 (Excel 可開)
├── yolov8n.pt          # YOLO 模型權重 (首次執行會自動下載)
└── README.md           # 專案說明文件
📊 資料輸出 (Data Output)
系統會在專案根目錄下生成 attendance_log.csv 檔案。您可以使用 Excel、Numbers 或 Google Sheets 開啟。

格式範例： | Date (日期) | Time (時間) | Total Seats (總座位) | Present Count (出席數) | Absent List (缺席名單) | |------------|----------|-------------|---------------|------------------| | 2024-12-16 | 09:00:05 | 40 | 38 | Seat 5, Seat 12 | | 2024-12-16 | 10:15:00 | 40 | 40 | None |
