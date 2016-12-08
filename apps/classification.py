from __future__ import print_function

import subprocess

class Tensorflow:
    def execute(self, graph, imgOutputPath):
        cmd = ["tensorflow/label_image/label_image"
                , "--graph=tensorflow/graph/%s.pb" %(graph)
                , "--labels=tensorflow/graph/%s.txt" %(graph)
                , "--output_layer=final_result"
                , "--image=%s" %(imgOutputPath)]
        print('Tensorflow cmd: ', cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        (output, err) = proc.communicate()
        return output
