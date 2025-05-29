import cv2
bmp = cv2.imread('One_Piece1.bmp')   # 開啟圖片，預設使用 cv2.IMREAD_COLOR 模式

cropped_image = bmp[0:120, 0:120]
cv2.imshow('Image', cropped_image)  # 顯示圖片
cv2.waitKey(0)
cv2.destroyAllWindows()