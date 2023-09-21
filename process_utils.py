def check_intersect(sliced_img_list,bias = 0, isText = False):
    check = True
    sliced_img_list_after = sliced_img_list.copy()
    while check:
        check = False
        for i in range(len(sliced_img_list)):
            sliced_img = sliced_img_list[i]
            minX = sliced_img[0]
            maxX = sliced_img[0] + sliced_img[1]
            minY = sliced_img[2]
            maxY = sliced_img[2] + sliced_img[3]
            area = sliced_img[1] * sliced_img[3]
            temp_list = []
            if sliced_img not in temp_list:
                temp_list.append(sliced_img)
            for j in range(len(sliced_img_list_after)):
                sliced_img_2 = sliced_img_list_after[j]
                if sliced_img != sliced_img_2:
                    if sliced_img_2 not in temp_list:
                        temp_list.append(sliced_img_2)
                    minX_2 = sliced_img_2[0]
                    maxX_2 = sliced_img_2[0] + sliced_img_2[1]
                    minY_2 = sliced_img_2[2]
                    maxY_2 = sliced_img_2[2] + sliced_img_2[3]
                    area_2 = sliced_img_2[1] * sliced_img_2[3]
                    
                    # compute the width and height of the intersection are
                    inter_width = max(0, (min(maxX, maxX_2) - max(minX, minX_2) + bias))
                    inter_height = max(0,(min(maxY, maxY_2) - max(minY, minY_2) + bias))
                    inter_area = inter_width * inter_height
                    #check if there is intersection
                    if inter_area > 0 and inter_area/area_2 <= 1 and inter_area / area <= 1:
                        temp_list.remove(sliced_img_2)
                        if sliced_img in temp_list:
                            temp_list.remove(sliced_img)
                            #x, w, y,h
                        after_segtion = [min(minX, minX_2),max(maxX, maxX_2) - min(minX, minX_2),min(minY, minY_2),max(maxY, maxY_2) - min(minY, minY_2)]
                        if after_segtion not in temp_list:
                            temp_list.append(after_segtion)
                            
                        check = True
                    else:
                        # if there is no intersection, then check if there are two blocks are too close that they need to be merged
                        if isText and check_merge(sliced_img, sliced_img_2):
                            temp_list.remove(sliced_img_2)
                            if sliced_img in temp_list:
                                temp_list.remove(sliced_img)
                                #x, w, y,h
                            after_segtion = [min(minX, minX_2),max(maxX, maxX_2) - min(minX, minX_2),min(minY, minY_2),max(maxY, maxY_2) - min(minY, minY_2)]
                            if after_segtion not in temp_list:
                                temp_list.append(after_segtion)
                            check = True
                        pass
                    
            sliced_img_list_after = temp_list.copy()
            
        sliced_img_list = sliced_img_list_after.copy() 
        
    
        
    return sliced_img_list_after

def check_merge(a, b):
    #this is to merge the closely blocks that have a distance of 2 pixel
    a_distance_b_x = (a[0]) - (b[1] + b[0])
    b_distance_a_x = (b[0]) - (a[1] + a[0])
    a_distance_b_y = (a[2]) - (b[2] + b[3])
    b_distance_a_y = (b[2]) - (a[2] + a[3])
    distance_x = max(a_distance_b_x, b_distance_a_x)
    distance_y = max(a_distance_b_y, b_distance_a_y)
    if distance_x >= 0 and distance_x <= 2:
        if abs(b[2] - a[2]) > 2:
            return False
        else:
            return True
    elif distance_y >= 0 and distance_y <= 2:
        if abs(b[0] - a[0]) > 2:
            return False
        else:
            return True