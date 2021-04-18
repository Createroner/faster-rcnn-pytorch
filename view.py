import numpy
import os
import cv2


"""
用于读取txt文档
"""
def file_lines_to_list(path):
    # open txt file lines to a list
    with open(path) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

'''
用于对真实框与预测框进行可视化，其中漏检的框用红色的表示，预测
的框用绿色表示
'''
def draw_box(gt_box , dr_box, img):

    #gt_box 代表的是真实的box内容，是list类型
    #dr_box包含的是预测的box内容，是list类型
    #img 是用cv2读取的图像
    # 最终返回画好的img

    # 画预测的box，分为两个步骤，其中一个是话正确的预测框，另外一个是画虚警
    for line in dr_box :
        
        # iou用来判断是虚警还是正确预测的，如果iou大于0.1则认为是正确预测的，如果iou<0.1则认为是虚警
        iou = 0.1 

        class_name,confidence, left, top, right, bottom = line.split()

        left, top, right, bottom = int(left), int(top), int(right),int(bottom)

      

        for line in gt_box :

            gt_class_name, gt_left, gt_top, gt_right, gt_bottom = line.split()

            gt_left, gt_top, gt_right, gt_bottom = int(gt_left), int(gt_top), int(gt_right),int(gt_bottom)

            iou_calcute = comput_iou((left, top, right, bottom), (gt_left, gt_top, gt_right, gt_bottom))

            if iou_calcute > iou :

                iou = iou_calcute

            # 首先判断正确预测
        if iou > 0.1 :

            img = cv2.rectangle(img,(left,top),(right, bottom),color=(0,255,0),thickness=3)
                # cv2.rectangle(img, (left, top), (left + 40, top - 20), (0,255,0), -1)
            cv2.putText(img, '{} : {:.2f}'.format(class_name, float(confidence)), (left,top-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        else : 

            img = cv2.rectangle(img,(left,top),(right, bottom),color=(0,255,255),thickness=3)
            # cv2.imshow('1',img)
            # cv2.waitKey(0)
            cv2.putText(img, '{} : {:.2f}'.format(class_name, float(confidence)), (left,top-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)



                




    # 画真实的box, 在此时需要注意的是需要和原来的画得预测的进行iou计算，如果
    # iou > 0.1， 那么认为已经预测出来了船舶， 如果<0.1的认为没有预测出来的
    #框，此时则需要对其进行可视化
    for line in gt_box:

        class_name, left, top, right, bottom = line.split()

        left, top, right, bottom = int(left), int(top), int(right),int(bottom)

        # 接下来将真实的框和每个预测框进行对比 

        iou = 0.1

        for line in dr_box :

            dr_class_name,dr_confidence, dr_left, dr_top, dr_right, dr_bottom = line.split()

            dr_left, dr_top, dr_right, dr_bottom = int(dr_left), int(dr_top), int(dr_right),int(dr_bottom)

            iou_calcute = comput_iou((left, top, right, bottom), (dr_left, dr_top, dr_right, dr_bottom))
            if iou_calcute > iou :

                iou = iou_calcute

        if (iou <= 0.1):

            img = cv2.rectangle(img,(left,top),(right, bottom),color=(0,0,255),thickness=3)




    # # 接下来画预测的box
    # for line in dr_box :

    #     class_name,confidence, left, top, right, bottom = line.split()

    #     left, top, right, bottom = int(left), int(top), int(right),int(bottom)
    #     img = cv2.rectangle(img,(left,top),(right, bottom),color=(0,255,0),thickness=3)

    # cv2.imshow('test',img)
    # cv2.waitKey(0)
    return img


''' 
计算两个框iou
'''
def comput_iou(box1, box2):
    """
    box1 : 代表的是第一个框的坐标(left, top, right, bottom)
    box2 : 代表的是第二个框的坐标(left, top, right, bottom)
    最后返回iou值
    """

    # 首先计算第一个框和第二框的面积
    box1_area = (box1[2] - box1[0]) * (box1[1] - box1[3])
    box2_area = (box2[2] - box2[0]) * (box2[1] - box2[3])

    # 接下来计算并的面积
    uion_area = box1_area + box2_area

    # 接下来需要计算交集
    left_line = max(box1[0], box2[0])
    right_line = min(box1[2], box2[2])
    top_line = min(box1[1], box2[1])
    bottom_line = max(box1[3], box2[3])

    # 接下来需要判断是否有交集与没有交集的情况，如果没有交集的情况下
    #则返回0， 如果两个有交集的话，则进一步计算交并比

    if left_line > right_line or top_line > bottom_line:

        return 0
    
    else :
        
        # 有交集的情况下，先计算交集, 然后计算iou
        intersection = (top_line - bottom_line)*(right_line - left_line)

        return (intersection / uion_area)*1.0
    



# 得到真实框，预测框，真实图片的路径
#GT_PATH代表真实框路径
#DR_PATH代表预测框路径
#IMG_PATH代表图像路径

GT_PATH = os.path.join(os.getcwd(),'input','ground-truth')
DR_PATH = os.path.join(os.getcwd(),'input','detection-results')
IMG_PATH = os.path.join(os.getcwd(),'input','images-optional')


#out_path 用来存放最终可视化的图片
out_path = r'input/outputs'
os.makedirs(out_path, exist_ok=True)

# 接下来得到图像文件夹下所有图片的名称，默认的是真实框、预测框、图片所对应
#的索引是相同


#gt_files_list代表所有真实框的txt文件的绝对路径
#dr_files_list代表所有预测框的txt文件的绝对路径
#img_files_list代表所有图片的文件的绝对路径
gt_files_list = [GT_PATH + '/' + x for x in os.listdir(GT_PATH)] 
dr_files_list = [DR_PATH + '/' + x for x in os.listdir(DR_PATH)]
img_files_list = [IMG_PATH + '/' + x for x in os.listdir(IMG_PATH)]

# 接下来对每个文件进行遍历
for i in range(len(img_files_list)):

    # 首先读取出文件当中的txt内容
    gt_lines = file_lines_to_list(gt_files_list[i])
    dr_lines = file_lines_to_list(dr_files_list[i])
    img = cv2.imread(img_files_list[i])
    # cv2.imshow(img_files_list[i], img)
    # cv2.waitKey(0)


    # break

    # 接下来要做的是将得到的真实框，与预测出来的框放到图片上进行可视化
    img = draw_box(gt_lines, dr_lines, img)

    # 接下来保存画好的图片

    cv2.imwrite(os.path.join(out_path,os.listdir(IMG_PATH)[i]), img )





