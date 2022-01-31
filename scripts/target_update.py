from helpers import Point, euDistance
from math import sqrt


def targetUpdate(target_update_rate, target_state, target, path_index):
    if path_index == 0:
        # from (1, 1) to (5, 1)
        if target_state == 0:
            if target == Point(5, 1):
                target_state = 1
            else:   
                target.x += target_update_rate
        # from (5, 1) to (5, 5)
        elif target_state == 1:
            if target == Point(5, 5):
                target_state = 2
            else:
                target.y += target_update_rate
        # from (5, 5) to (-5, 5)
        elif target_state == 2:
            if target == Point(-5, 5):
                target_state = 3
            else:
                target.x -= target_update_rate
        # from (-5, 5) to (-5, -5)
        elif target_state == 3:
            if target == Point(-5, -5):
                target_state = 4
            else:
                target.y -= target_update_rate
        # from (-5, -5) to (1, 1), initial position
        elif target_state == 4:
            if target == Point(1, 1):
                return None, None
            target.x += target_update_rate
            target.y += target_update_rate
        else:
            print("You mixed something in target states!")
            exit(42)

    # start point is (1, 1)
    # a hard half-circle test
    elif path_index == 1:
        start_point = Point(1, 1)
        circle_center = Point(1, 6)
        dist = euDistance(start_point, target)
        if target_state == 0:
            # if we moved away enough
            if dist > 0.3:
                target_state = 1

        elif target_state == 2:
            # if we are close enough
            if dist < 0.01:
                return None, None
        
        a = circle_center.x
        b = circle_center.y
        r = 5
        # lets assume we are adjusting y and finding corresponding x
        if target_state == 0 or target_state == 1:
            target.y += target_update_rate
        elif target_state == 2:
            target.y -= target_update_rate
        
        # temp equals to (x-a)^2
        temp = r**2 - (target.y - b)**2
        # temp equals to x-a
        try:
            temp = sqrt(temp)
        except:
            target_state = 2
        target.x = temp + a

    # start point is (1, 1)
    elif path_index == 2:
        start_point = Point(1, 1)
        circle_center = Point(1, 6)
        dist = euDistance(start_point, target)
        if target_state == 0:
            # if we moved away enough
            if dist > 0.3:
                target_state = 1

        elif target_state == 2:
            # if we are close enough
            if dist < 0.01:
                return None, None
        
        a = circle_center.x
        b = circle_center.y
        r = 5
        # lets assume we are adjusting y and finding corresponding x
        if target_state == 0 or target_state == 1:
            target.y += target_update_rate
        elif target_state == 2:
            target.y -= target_update_rate
        
        # temp equals to (x-a)^2
        temp = r**2 - (target.y - b)**2
        # temp equals to x-a
        try:
            temp = sqrt(temp)
        except:
            target_state = 2
        if target_state == 2:
            temp *= -1

        target.x = temp + a

    else:
        print("Wrong path index, %d, while the max index is %d" % (path_index, 2))
        exit(42)

    return target, target_state