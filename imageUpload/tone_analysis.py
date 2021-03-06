import math
import operator

class ToneAnalysis:
    def dist(self, x, c, a):
        '''
        x와 c 사이의 거리를 구함.
        x : 인체 질의 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        c : 기준 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        a : 인체 부위별 가중치(list : [skin, hair, eye])
        '''
        distance = 0
        for body in range(3): #body = 0: skin, 1: hair, 2: eye
            diff = list(map(operator.sub, x[body], c[body]))
            distance += a[body] * sum(i*i for i in diff)
        return math.sqrt(distance)

    def minDist(self, x, Ct, a):
        '''
        x와 계절 t에 대한 c집합 Ct 중 가장 짧은 거리를 구함.
        x : 인체 질의 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        c : 기준 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        C : 전체 계절에 대한 c들의 집합 list
        Ct : 계절 t에 대한 c들의 집합 list
        a : 인체 부위별 가중치(list : [skin, hair, eye])
        '''
        distance = []
        for c in Ct:
            distance.append(self.dist(x, c, a))
        return min(distance)

    def probability(self, x, t, C, a):

        '''
        x의 특정 계절유형 t에 대한 소속도를 구함.
        x : 인체 질의 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        t : 특정 계절(int : 0: spring, 1: summer, 2: fall, 3: winter)
        c : 기준 색상(list : [skin[R,G,B], hair[R,G,B], eye[R,G,B]])
        C : 전체 계절에 대한 c들의 집합 list
        a : 인체 부위별 가중치(list : [skin, hair, eye])
        '''
        #분모
        denominator = sum((1/self.minDist(x, C[i], a)) for i in range(4))
        #분자
        numerator = 1/(self.minDist(x, C[t], a))
        return (numerator/denominator)*100

    def is_warm(self, lab_b, a):
        '''
        파라미터 lab_b = [skin_b, hair_b, eye_b]
        a = 가중치 [skin, hair, eye]
        질의색상 lab_b값에서 warm의 lab_b, cool의 lab_b값 간의 거리를
        각각 계산하여 warm이 가까우면 1, 반대 경우 0 리턴
        '''
        # skin, hair, eye
        warm_b_std = [12.16, 16.315, 7.94]
        cool_b_std = [2.312, 3.278, 2.675]

        warm_dist = 0
        cool_dist = 0

        body_part = ['skin', 'eyebrow', 'eye']
        for i in range(3):
            warm_dist += abs(lab_b[i] - warm_b_std[i]) * a[i]
            # print(body_part[i],"의 warm 기준값과의 거리")
            # print(abs(lab_b[i] - warm_b_std[i]))
            cool_dist += abs(lab_b[i] - cool_b_std[i]) * a[i]
            # print(body_part[i],"의 cool 기준값과의 거리")
            # print(abs(lab_b[i] - cool_b_std[i]))

        if (warm_dist <= cool_dist):
            return 1  # warm
        else:
            return 0  # cool

    def is_spr(self, hsv_s, a):
        '''
        파라미터 hsv_s = [skin_s, hair_s, eye_s]
        a = 가중치 [skin, hair, eye]
        질의색상 hsv_s값에서 spring의 hsv_s, fall의 hsv_s값 간의 거리를
        각각 계산하여 spring이 가까우면 1, 반대 경우 0 리턴
        '''
        # skin, hair, eye
        spr_s_std = [17.21, 42.47, 49.02]
        fal_s_std = [32.24, 38.59, 29.73]

        spr_dist = 0
        fal_dist = 0

        body_part = ['skin', 'eyebrow', 'eye']
        for i in range(3):
            spr_dist += abs(hsv_s[i] - spr_s_std[i]) * a[i]
            # print(body_part[i],"의 spring 기준값과의 거리")
            # print(abs(hsv_s[i] - spr_s_std[i]))
            fal_dist += abs(hsv_s[i] - fal_s_std[i]) * a[i]
            # print(body_part[i],"의 fall 기준값과의 거리")
            # print(abs(hsv_s[i] - fal_s_std[i]))

        if (spr_dist <= fal_dist):
            return 1  # spring
        else:
            return 0  # fall

    def is_smr(self, hsv_s, a):
        '''
        파라미터 hsv_s = [skin_s, hair_s, eye_s]
        a = 가중치 [skin, hair, eye]
        질의색상 hsv_s값에서 summer의 hsv_s, winter의 hsv_s값 간의 거리를
        각각 계산하여 summer가 가까우면 1, 반대 경우 0 리턴
        '''
        # skin, hair, eye
        smr_s_std = [9.5, 15.54, 24.39]
        wnt_s_std = [14.06, 27.43, 38.02]

        smr_dist = 0
        wnt_dist = 0

        body_part = ['skin', 'eyebrow', 'eye']
        for i in range(3):
            smr_dist += abs(hsv_s[i] - smr_s_std[i]) * a[i]
            # print(body_part[i],"의 summer 기준값과의 거리")
            # print(abs(hsv_s[i] - smr_s_std[i]))
            wnt_dist += abs(hsv_s[i] - wnt_s_std[i]) * a[i]
            # print(body_part[i],"의 winter 기준값과의 거리")
            # print(abs(hsv_s[i] - wnt_s_std[i]))

        if (smr_dist <= wnt_dist):
            return 1  # summer
        else:
            return 0  # winter