import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n-seg.pt')

# Open the video file
# video_path = "C:/Users/denjo/Desktop/HackU/data/walk1.mp4"
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results_gen = model(frame, 
                            classes=0,
                            conf=0.5,
                            stream = True)
        
        for result in results_gen:  # Iterate over generator results
            # Visualize the result on the frame
            annotated_frame = result.plot()
            
            if len(result.boxes.xyxy) >= 1:
                x1 = int(result.boxes.xyxy[0][0])   #左上
                y1 = int(result.boxes.xyxy[0][1])   #左上
                x2 = int(result.boxes.xyxy[0][2])   #右下
                y2 = int(result.boxes.xyxy[0][3])   #右下
            
                # 名前を記述できるかを試す。
                cv2.putText(annotated_frame,
                            text='yamashita',
                            org=(x2-100, y1),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.0,
                            color=(123, 0,122),
                            thickness=2,
                            lineType=cv2.LINE_4)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
