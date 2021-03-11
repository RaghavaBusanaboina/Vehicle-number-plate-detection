import cv2
import pytesseract
import re

# state names
states = {"AN": "AndamanandNicobar,", "AP": "AndhraPradesh,", "AR": "ArunachalPradesh,", "AS": "Assam,", "BR": "Bihar,",
          "CG": "Chhattisgarh,", "CH": "Chandigarh,", "DD": "DadraandNagarHaveliandDamanandDiu,", "DL": "Delhi,",
          "GA": "Goa,", "GJ": "Gujarat,", "HP": "HimachalPradesh,", "HR": "Haryana,", "JH": "Jharkhand,",
          "JK": "JammuandKashmir,", "KA": "Karnataka,", "KL": "Kerala,", "LA": "Ladakh,", "LD": "Lakshadweep,",
          "MH": "Maharashtra,", "ML": "Meghalaya,", "MN": "Manipur,", "MP": "MadhyaPradesh,", "MZ": "Mizoram,",
          "NL": "Nagaland,", "OD": "Odisha,", "PB": "Punjab,", "PY": "Puducherry,", "RJ": "Rajasthan,", "SK": "Sikkim,",
          "TN": "TamilNadu,", "TR": "Tripura,", "TS": "Telangana,", "UK": "Uttarakhand,", "UP": "UttarPradesh,",
          "WB": "WestBengal,"}
## Read the image
img = cv2.imread('/home/thunder/Desktop/Number_Plate_Detection/Images/car2.jpeg')
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
## Grayscale
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
## Canny edge detection
canny_img = cv2.Canny(img_gray,150,200)

## find contours
conts, new = cv2.findContours(canny_img.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
image1 = img.copy()
##Draw contours
cv2.drawContours(image1,conts,-1,(0,255,0),3)
## Sort contours and take highest 30
conts_sorted = sorted(conts, key=cv2.contourArea,reverse=True)[:30]

image2 = img.copy()
cv2.drawContours(image2,conts_sorted,-1,(0,255,0),3)
count = 0
number = 1
pts = None
x,y,h,w = 0.0,0.0,0.0,0.0
for i in conts_sorted:
    perimeter = cv2.arcLength(curve=i,closed=True)
    approx = cv2.approxPolyDP(curve=i,epsilon=0.01*perimeter,closed=True)
    if (len(approx) == 4):# 4 because for rectangle
        pts = approx
        x,y,w,h = cv2.boundingRect(i)
        cropped_img = img[y:y+h,x+20:x+w]
        cv2.imwrite('output/'+str(number) + '.png',cropped_img)
        # #Draw License Plate and write the Text
        cv2.rectangle(img=img,pt1= (x,y),pt2= (x+w,y+h),color= (0,0,255),thickness= 3)

        number += 1
image3 = img.copy()
cv2.drawContours(image3,[pts],-1,(0,255,0),3)
cropped_img = cv2.imread('output/1.png')
try:
    license_plate = cv2.bilateralFilter(src=cropped_img,d= 5,sigmaColor= 100,sigmaSpace= 90)
    (thresh, license_plate) = cv2.threshold(src=license_plate,thresh= 120,maxval= 255,type= cv2.THRESH_BINARY)
except Exception as e:
    license_plate = cv2.bilateralFilter(src=cropped_img,d= 20,sigmaColor= 90,sigmaSpace= 90)
    (thresh, license_plate) = cv2.threshold(src=license_plate,thresh= 100,maxval= 255,type= cv2.THRESH_BINARY)

#Text Recognition
text = pytesseract.image_to_string(license_plate)
t1 = ''.join(i for i in text if not i.isspace())
t2 = re.sub(pattern='[^A-Z 0-9]*',repl='',string=t1)
# print(text)
print(f'Number plate :{t2}')

cv2.putText(img=img,text= t2,org= (x-10,y-5),fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color= (0,255,0),thickness= 3)
print(f'This vehicle is belongs to {states[t2[0:2]][:-1]} state')
print()
cv2.imshow('image3',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
