import NICSoutBackend
import matplotlib
import numpy as np
import readFile
import geomAnalyzer
import mathUtilities

class output_analyzer:
    #get all deriveables by reading file, this is initialization
    def __init__(self,filename):
        self.atomList, self.geomList = readFile.read_log(filename)
        self.logBqList = self.atomList[len(self.geomList) - len(self.atomList):]
        self.conMatrix, self.bndAtom = geomAnalyzer.get_connectivity(self.geomList)
        self.ringList = geomAnalyzer.find_monocycle(self.bndAtom)
        self.ringNums2 = len(self.ringList)
        self.tensor = NICSoutBackend.save_tensor(filename,len(self.logBqList), -1) #what's the -1?
        #deriveables/info
        self.ringAverageNICSzzList = []
        self.allNICSIso = self.tensor[0]
        self.allNICSzz = self.tensor[-1]
        self.allNICSPerp,self.allNICSPerpAve = self.computeNICSPerpAllRings()

    def computeNICSIso(self,):
        pass

    
    def computeNICSPerp(self,bq_number,ring_number):
        xBqCoor, yBqCoor, zBqCoor, colorBqList = geomAnalyzer.save_coor_list(self.logBqList)
        isoTen, aniTen, xxTen, yxTen, zxTen, xyTen, yyTen, zyTen, xzTen, yzTen, zzTen = self.tensor

        ringNormal = np.array(geomAnalyzer.normal_vector(self.ringList[ring_number], self.geomList))
        
        rotationMatrix = mathUtilities.align_matrix(ringNormal,np.array([0,0,1]))
    
        if not 1 - np.dot(rotationMatrix @ np.array([0,0,1]), ringNormal) < 0.001:
            raise RuntimeError('Bad change of basis')
        
        i = bq_number
        Tensor1 = np.array(
            [[xxTen[i], xyTen[i], xzTen[i]],
             [yxTen[i], yyTen[i], yzTen[i]],
             [zxTen[i], zyTen[i], zzTen[i]]]
        )

        #the change of basis formula for a matrix
        rotTensor =  np.linalg.inv(rotationMatrix) @ Tensor1 @ rotationMatrix
        #the new NICSzz with change of basis applied
        NICSzzPerp = rotTensor[2,2]
    
        return NICSzzPerp

    def computeNICSPerpAllRings(self):
        ringAverageNICSPerpList = []
        NICSPerpList = []
        for i in range(len(self.logBqList)//2):
            NICSzzPerp1 = self.computeNICSPerp(i*2,i)
            NICSzzPerp2 = self.computeNICSPerp(i*2+1,i)
            NICSPerpList.extend([NICSzzPerp1,NICSzzPerp2])
            
            ringAverage = (NICSzzPerp1 + NICSzzPerp2) / 2
            ringAverageNICSPerpList.append(ringAverage)
            
        return NICSPerpList, ringAverageNICSPerpList