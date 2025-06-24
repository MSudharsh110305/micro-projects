import cv2
from pyzbar import pyzbar

def scan_barcode_from_camera():
    cap = cv2.VideoCapture(0)
    barcode_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            # draw a rectangle around the barcode
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            break

        cv2.imshow('Barcode Scanner - Press Q to quit', frame)
        if barcode_data or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return barcode_data
