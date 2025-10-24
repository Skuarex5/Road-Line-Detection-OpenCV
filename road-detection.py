import cv2
import numpy as np

def detectar_linea_derecha(frame):
    h, w = frame.shape[:2]

    roi = frame[int(h*0.6):h, int(w*0.5):w]

    hls = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)

    lower_white = np.array([0, 200, 0])
    upper_white = np.array([255, 255, 255])
    lower_yellow = np.array([10, 0, 90])
    upper_yellow = np.array([40, 255, 255])

    mask_white = cv2.inRange(hls, lower_white, upper_white)
    mask_yellow = cv2.inRange(hls, lower_yellow, upper_yellow)
    mask = cv2.bitwise_or(mask_white, mask_yellow)

    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50,
                            minLineLength=40, maxLineGap=20)

    salida = roi.copy()
    if lines is not None:
        lineas_ordenadas = sorted(lines, key=lambda l: max(l[0][1], l[0][3]), reverse=True)
        x1, y1, x2, y2 = lineas_ordenadas[0][0]
        cv2.line(salida, (x1, y1), (x2, y2), (0, 255, 0), 3)

    frame[int(h*0.6):h, int(w*0.5):w] = salida
    return frame, mask, edges

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    procesado, mask, edges = detectar_linea_derecha(frame)

    cv2.imshow("Detection", procesado)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
