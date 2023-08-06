import onnxruntime as ort
import cv2
import numpy as np



class classifier():
    def __init__(self,model,classes) :
        self.sess = ort.InferenceSession(model,providers=['CUDAExecutionProvider']) # 'CPUExecutionProvider'
        self.input_name = self.sess.get_inputs()[0].name
        self.output_name = [output.name for output in self.sess.get_outputs()]
        self.classes=classes

    def run(self,image):
        data=self.preprocess(image)
        outputs = self.sess.run(self.output_name, {self.input_name:data})
        return (np.argmax(outputs),self.softmax(outputs).tolist())

    def softmax(self,x):
        row_max = np.max(x)
        x = x - row_max
        x_exp = np.exp(x)
        x_sum = np.sum(x_exp)
        s = x_exp / x_sum
        return s[0][0]

    def preprocess(self,image_path):
        def resize_by_short(im, resize_size):
            short_size = min(im.shape[0], im.shape[1])
            scale = 224 / short_size
            new_w = int(round(im.shape[1] * scale))
            new_h = int(round(im.shape[0] * scale))
            return cv2.resize(im, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        def center_crop(im, crop_size):
            h, w, c = im.shape
            w_start = (w - crop_size) // 2
            h_start = (h - crop_size) // 2
            w_end = w_start + crop_size
            h_end = h_start + crop_size
            return im[h_start:h_end, w_start:w_end, :]

        def normalize(im, mean, std):
            im = im.astype("float32") / 255.0
            # to rgb
            im = im[:, :, ::-1]
            mean = np.array(mean).reshape((1, 1, 3)).astype("float32")
            std = np.array(std).reshape((1, 1, 3)).astype("float32")
            return (im - mean) / std

        # resize the short edge to `resize_size`
        im = image_path
        resized_im = resize_by_short(im, 224)
        center_im= center_crop(resized_im, 224)
        #print(center_im.shape)
        # normalize
        normalized_im = normalize(center_im, [0.485, 0.456, 0.406],
                                [0.229, 0.224, 0.225])
        # transpose to NCHW
        data = np.expand_dims(normalized_im, axis=0)
        data = np.transpose(data, (0, 3, 1, 2))
        return data





  