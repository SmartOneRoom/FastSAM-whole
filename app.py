from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import torch
from fastsam import FastSAM, FastSAMPrompt

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# FastSAM 모델 로드
model = FastSAM('FastSAM-x.pt')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_segmentation():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # FastSAM 모델로 세그멘테이션 수행
            with torch.no_grad():
                everything_results = model(frame, device=device, retina_masks=True, imgsz=1024, conf=0.4, iou=0.9)
            
            # 프롬프트 생성 및 마스크 추출
            prompt_process = FastSAMPrompt(frame, everything_results, device=device)
            ann = prompt_process.everything_prompt()
            
            # 마스크 시각화
            for mask in ann:
                mask = mask.cpu().numpy()  # 텐서를 NumPy 배열로 변환
                colored_mask = np.random.randint(0, 255, (1, 3), dtype=np.uint8)
                frame[mask.astype(bool)] = frame[mask.astype(bool)] * 0.5 + colored_mask * 0.5
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/segmentation_feed')
def segmentation_feed():
    return Response(generate_segmentation(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/search', methods=['POST'])
def search_object():
    data = request.json
    search_text = data.get('text', '')
    return jsonify({'result': f'Searching for: {search_text}'})

if __name__ == '__main__':
    app.run(debug=True)