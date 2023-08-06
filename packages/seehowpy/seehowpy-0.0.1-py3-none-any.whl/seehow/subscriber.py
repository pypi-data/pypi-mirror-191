import rospy
import cv2 as cv
import ros_numpy

class ImgCon:
    def __init__(self, obj = None, label = None, data = None, flag = 0, msg = None, topic = None):
        
        if obj and label != None:
            rospy.init_node(label, anonymous=True)
            self.hand           = obj.msg()
            self.label          = label
            
        else:
            rospy.init_node('image', anonymous=True)
            self.hand           = None
            self.label          = None
            
        # Topic to read the image msg data
        self.image_sub          = rospy.Subscriber(topic, msg, self.image_callback)
        self.img                = None
        self.data               = data
        self.flag               = flag

    def image_callback(self, msg):
        
        self.img = ros_numpy.numpify(msg)
        
        if self.label == 'left_hand':
            self.hand.Left(self.img)
        elif self.label == 'right_hand':
            self.hand.Right(self.img)
        
        
        if self.flag == 1:
            self.showImage()
   
    
    def showImage(self):
        
        if self.img is None:
            print("Could not read the image.")
        else:
            cv.imshow("Image Window", self.img)      
            cv.waitKey(3)
        
        
class SubHand:
    def __init__(self, msg = None, topic = None):
        rospy.Subscriber(topic, msg, self.callback)
        self.data               = None
        
    def callback(self, data):
        self.data               = data
    
    def getData(self):
        return self.data
