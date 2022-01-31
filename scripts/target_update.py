from helpers import Point

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

    return target, target_state