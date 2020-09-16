# rotation
    # On considère la droite passant par les deux coins droits et on cherche son intersection avec l'horizontale passant par le coin en bas à gauche
    if rotation:
        # Right Lower Edge Angle
        i_A = leftLowerEdge[0]
        i_C = rightTopEdge[0]
        i_D = rightLowerEdge[0]
        j_A = leftLowerEdge[1]
        j_C = rightTopEdge[1]
        j_D = rightLowerEdge[1]
        is_C = -i_C + i_A
        is_D = -i_D + i_A
        jp_C = j_C - j_A
        jp_D = j_D - j_A

        a = (is_C-is_D)/(jp_C-jp_D)
        b = is_D-jp_D*a

        right_intersection = [i_A, j_A-b/a]
        rightLowEdge_dist = ((right_intersection[0]-rightLowerEdge[0])**2 + (
            right_intersection[1]-rightLowerEdge[1])**2)**(1/2)

        angleRLE = np.arctan(rightLowEdge_dist/lower_length)*180/np.pi
        if i_A < i_D:  # negative angle
            angleRLE *= -1

        #print('Lower angle: ' + str(angleRLE))

        # Left Top Edge Angle

        i_A = rightTopEdge[0]

        i_C = leftLowerEdge[0]
        i_D = leftTopEdge[0]
        j_A = rightTopEdge[1]
        j_C = leftLowerEdge[1]
        j_D = leftTopEdge[1]
        ip_C = i_C - i_A
        ip_D = i_D - i_A
        jp_C = -j_C + j_A
        jp_D = -j_D + j_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        left_intersection = [i_A, j_A+b/a]
        # print(left_intersection)
        leftTopEdge_dist = ((left_intersection[0]-leftTopEdge[0])**2 + (
            left_intersection[1]-leftTopEdge[1])**2)**(1/2)

        angleLTE = np.arctan(leftTopEdge_dist/upper_length)*180/np.pi
        if i_A > i_D:  # negative angle
            angleLTE *= -1

        #print('upper angle: '+str(angleLTE))

        # Left Lower Edge Angle
        i_A = leftTopEdge[0]
        i_C = rightLowerEdge[0]
        i_D = leftLowerEdge[0]
        j_A = leftTopEdge[1]
        j_C = rightLowerEdge[1]
        j_D = leftLowerEdge[1]
        ip_C = j_C - j_A
        ip_D = j_D - j_A
        jp_C = i_C - i_A
        jp_D = i_D - i_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        left_intersection = [i_A-b/a, j_A]
        # print(left_intersection)
        leftTopEdge_dist = ((left_intersection[0]-leftLowerEdge[0])**2 + (
            left_intersection[1]-leftLowerEdge[1])**2)**(1/2)
        angleLLE = np.arctan(leftTopEdge_dist/left_length)*180/np.pi
        if j_A > j_D:  # negative angle
            angleLLE *= -1

        #print('left angle: '+str(angleLLE))

        # Right Lower Edge Angle
        i_A = rightLowerEdge[0]
        i_C = leftTopEdge[0]
        i_D = rightTopEdge[0]
        j_A = rightLowerEdge[1]
        j_C = leftTopEdge[1]
        j_D = rightTopEdge[1]
        ip_C = -j_C + j_A
        ip_D = -j_D + j_A
        jp_C = -i_C + i_A
        jp_D = -i_D + i_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        right_intersection = [i_A+b/a, j_A]
        # print(right_intersection)
        rightLowerEdge_dist = ((right_intersection[0]-rightTopEdge[0])**2 + (
            right_intersection[1]-rightTopEdge[1])**2)**(1/2)
        angleRTE = np.arctan(rightLowerEdge_dist/right_length)*180/np.pi
        if j_A < j_D:  # negative angle
            angleRTE *= -1

        #print('right angle: '+str(angleRTE))

    else:
        angleRLE = 0
        angleLTE = 0
        angleLLE = 0
        angleRTE = 0

    # Looking for absurd values

    angles = [angleLLE, angleLTE, angleRLE, angleRTE]

    if verbose:
        print('angles: '+str(angles))

    rotation_angle = 0
    meanLLE = angleLTE/3 + angleRLE/3 + angleRTE/3
    meanLTE = angleLLE/3 + angleRLE/3 + angleRTE/3
    meanRLE = angleLLE/3 + angleLTE/3 + angleRTE/3
    meanRTE = angleLLE/3 + angleLTE/3 + angleRLE/3

    if (abs(abs(angleLLE)) > 2*abs(meanLLE)) or (abs(angleLLE) < 1/2*abs(meanLLE)):
        angles.pop(0)
    if (abs(abs(angleLTE)) > 2*abs(meanLTE)) or (abs(angleLTE) < 1/2*abs(meanLTE)):
        angles.pop(1)
    if (abs(abs(angleRLE)) > 2*abs(meanRLE)) or (abs(angleRLE) < 1/2*abs(meanRLE)):
        angles.pop(-2)
    if (abs(abs(angleRTE)) > 2*abs(meanRTE)) or (abs(angleRTE) < 1/2*abs(meanRTE)):
        angles.pop(-1)

    if (angleLLE > 0 and angleLTE > 0 and angleRLE > 0 and angleRTE > 0) or (angleLLE < 0 and angleLTE < 0 and angleRLE < 0 and angleRTE < 0):
        rotation_angle = - sum(angles)/len(angles)

    if verbose:
        print('Rotation de '+str(rotation_angle)+' degrés.')